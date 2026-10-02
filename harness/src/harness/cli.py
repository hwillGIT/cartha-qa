"""harness CLI — the executable face of the CI/CD pipeline.

Thin YAML workflows call these commands; all behavior lives here.
"""
from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import subprocess
import sys
import tempfile
from threading import Thread
import time
from urllib.parse import urlparse

import yaml

from . import determinism as det
from . import quarantine as quar
from . import smoke


def _run(cmd: list[str], env: dict, cwd: str, timeout: int) -> dict:
    """Run one test command. Failures are recorded, never swallowed."""
    start = time.time()
    try:
        proc = subprocess.run(
            cmd, env=env, cwd=cwd, capture_output=True, text=True, timeout=timeout
        )
        status = "passed" if proc.returncode == 0 else "failed"
        return {
            "command": " ".join(cmd),
            "status": status,
            "returncode": proc.returncode,
            "duration_s": round(time.time() - start, 1),
            "tail": (proc.stdout + proc.stderr)[-2000:],
        }
    except FileNotFoundError as e:
        return {
            "command": " ".join(cmd),
            "status": "error",
            "returncode": -1,
            "duration_s": round(time.time() - start, 1),
            "tail": f"tool not installed: {e}",
        }
    except subprocess.TimeoutExpired:
        return {
            "command": " ".join(cmd),
            "status": "timeout",
            "returncode": -1,
            "duration_s": timeout,
            "tail": f"exceeded {timeout}s — no silent retries",
        }


def _base_env(master_seed: str, clock: str | None) -> dict:
    env = dict(os.environ)
    env.update(det.seed_env(master_seed))
    env.update(det.clock_env(clock))
    # Condition-based waits, never fixed sleeps, are enforced by the flows.
    return env


def _maestro_command(ref: str, env: dict, harness_dir: str = ".") -> list[str]:
    device = env.get("SIMULATOR_UDID")
    # QA-owned flows live with the harness; upstream flows remain relative to
    # the mobile checkout. An absolute path works from either working dir.
    qa_flow = os.path.join(os.path.abspath(harness_dir), ref)
    flow = qa_flow if os.path.isfile(qa_flow) else ref
    return ["maestro", "test", *(["--device", device] if device else []), flow]


def _qa_setup(test: dict, env: dict, mobile_dir: str) -> dict | None:
    """Reuse the mobile repo's existing simulator QA handoff, loop 1 only."""
    stage = test.get("qa_stage")
    seed_group = test.get("qa_seed_meet_group", False)
    if not stage and not seed_group:
        return None
    udid = env.get("SIMULATOR_UDID")
    if not udid:
        return {"command": "QA simulator setup", "status": "error",
                "returncode": -1, "duration_s": 0,
                "tail": "QA staging requires SIMULATOR_UDID"}
    scripts = os.path.join(os.path.abspath(mobile_dir), "cartha_ai_mobile", "scripts")
    if seed_group:
        cmd = ["bash", os.path.join(scripts, "qa_seed_meet_group.sh"),
               "--udid", udid,
               "--user-email", "testuser1@yopmail.com",
               "--user-email", "testuser2@yopmail.com",
               "--user-email", "carthaomegle1@yopmail.com"]
        timeout = 90
    else:
        cmd = [sys.executable, os.path.join(scripts, "qa_debug_api.py"),
               "stage-qa-screen", "--udid", udid, "--screen", stage["screen"]]
        if stage.get("data"):
            cmd += ["--data-json", json.dumps(stage["data"], separators=(",", ":"))]
        if stage.get("launch_app", True):
            cmd.append("--launch-app")
        timeout = 60
    return _run(cmd, env, mobile_dir, timeout)


def _without_qa_open_link(flow: str, destination: str,
                          dismiss: list[str] | None = None) -> str:
    """Use the already-staged QA screen, keeping upstream UI assertions intact.

    The iOS simulator's custom-scheme openLink is unreliable: it can show an OS
    confirmation or leave the app on its previous screen. The mobile repo's
    stage-qa-screen helper is the established prompt-free path for this lane.
    """
    with open(flow) as source:
        docs = list(yaml.safe_load_all(source))
    if len(docs) != 2 or not isinstance(docs[1], list):
        raise ValueError(f"expected a two-document Maestro flow: {flow}")
    commands = [command for command in docs[1]
                if not (isinstance(command, dict) and "openLink" in command)]
    if len(docs[1]) - len(commands) != 1:
        raise ValueError(f"expected exactly one QA openLink in {flow}")
    for label in reversed(dismiss or []):
        commands.insert(0, {"runFlow": {"when": {"visible": label},
                                        "commands": [{"tapOn": label}]}})
    with open(destination, "w") as prepared:
        yaml.safe_dump(docs[0], prepared, sort_keys=False)
        prepared.write("---\n")
        yaml.safe_dump(commands, prepared, sort_keys=False)
    return destination


def _run_maestro(test: dict, ref: str, env: dict,
                 mobile_dir: str, harness_dir: str) -> dict:
    if test.get("qa_use_staged_screen") and not test.get("qa_stage"):
        return {"command": "QA simulator setup", "status": "error",
                "returncode": -1, "duration_s": 0,
                "tail": "qa_use_staged_screen requires qa_stage"}
    setup = _qa_setup(test, env, mobile_dir)
    if setup is not None and setup.get("status") != "passed":
        return {**setup, "status": "error",
                "tail": f"QA setup failed: {setup.get('tail', '')}"}
    try:
        cmd = _maestro_command(ref, env, harness_dir)
        result_dir = os.path.abspath(os.path.join(
            "maestro-results", env.get("GITHUB_RUN_ID", "local"),
            os.path.splitext(os.path.basename(ref))[0]))
        os.makedirs(result_dir, exist_ok=True)
        cmd[-1:-1] = ["--test-output-dir", result_dir]
        with tempfile.TemporaryDirectory(prefix="cartha-maestro-") as temp_dir:
            if test.get("qa_use_staged_screen") and env.get("SIMULATOR_UDID"):
                flow = cmd[-1]
                source = flow if os.path.isabs(flow) else os.path.join(mobile_dir, flow)
                cmd[-1] = _without_qa_open_link(
                    source, os.path.join(temp_dir, os.path.basename(flow)),
                    test.get("qa_dismiss"))
            return _run(cmd, env, mobile_dir, test.get("timeout_s", 600))
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return {"command": f"prepare Maestro flow {ref}", "status": "error",
                "returncode": -1, "duration_s": 0,
                "tail": f"QA flow preparation failed: {exc}"}


class _QuietStaticHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass


def _run_browser(ref: str, env: dict, web_dir: str, timeout: int) -> dict:
    """Run the website's node:test browser suite against an explicit URL.

    Loop 1 serves the checked-out static promo locally. Loop 2 must be given
    an HTTPS production URL; it must never silently skip the browser test.
    """
    browser_env = env.copy()
    if env.get("HARNESS_PROD") == "1":
        url = env.get("DOWNLOAD_PROMO_URL", "")
        if urlparse(url).scheme != "https":
            return {"command": f"node --test {ref}", "status": "error",
                    "returncode": -1, "duration_s": 0,
                    "tail": "DOWNLOAD_PROMO_URL must be an HTTPS production URL"}
        return _run(["node", "--test", ref], browser_env, web_dir, timeout)

    static_dir = os.path.join(os.path.abspath(web_dir), "redirects")
    if not os.path.isfile(os.path.join(static_dir, "index.html")):
        return {"command": f"node --test {ref}", "status": "error",
                "returncode": -1, "duration_s": 0,
                "tail": f"static promo missing: {static_dir}/index.html"}
    handler = partial(_QuietStaticHandler, directory=static_dir)
    with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
        port = server.server_address[1]
        browser_env["DOWNLOAD_PROMO_URL"] = f"http://127.0.0.1:{port}"
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            return _run(["node", "--test", ref], browser_env, web_dir, timeout)
        finally:
            server.shutdown()
            thread.join()


def cmd_run_smoke(args: argparse.Namespace) -> int:
    manifest = smoke.load_manifest(args.manifest)
    tests = smoke.select_tests(
        manifest, "loop1", args.shard_index, args.shard_total
    )
    if args.kinds:
        kinds = set(args.kinds.split(","))
        unknown = kinds - {"maestro", "playwright", "node", "flutter", "go"}
        if unknown:
            raise ValueError(f"unknown test kinds: {sorted(unknown)}")
        tests = [t for t in tests if t["id"].split(":", 1)[0] in kinds]
    if not tests:
        print("no tests selected; refusing to report a passing smoke run", file=sys.stderr)
        return 2
    quarantined = quar.load_quarantine(args.quarantine)
    runnable, skipped = quar.partition(tests, quarantined)

    run_manifest = det.emit_manifest(
        loop="loop1",
        master_seed=args.seed,
        clock_value=args.clock,
        test_selection=smoke.test_ids(runnable),
        repo_shas={
            "mobile": det.git_sha(args.mobile_dir),
            "web": det.git_sha(args.web_dir),
            "backend": det.git_sha(args.backend_dir),
            "harness": det.git_sha(args.backend_dir),
        },
    )
    det.write_manifest(run_manifest, args.out_manifest)
    print(f"manifest -> {args.out_manifest}  seed={args.seed}")

    env = _base_env(args.seed, args.clock)
    results = []
    for t in runnable:
        kind, ref = t["id"].split(":", 1)
        if kind == "maestro":
            cmd = None
            cwd = args.mobile_dir
        elif kind == "playwright":
            cmd = None
            cwd = args.web_dir
        elif kind == "node":
            cmd = ["npm", "run", ref]
            cwd = args.web_dir
        elif kind == "flutter":
            cmd = ["flutter", "test", ref, "--test-randomize-ordering-seed",
                   str(det.derive_seed(args.seed, "dart"))]
            cwd = args.mobile_dir
        elif kind == "go":
            cmd = ["go", "test", ref]
            cwd = args.backend_dir
        else:
            results.append({"id": t["id"], "status": "error",
                            "tail": f"unknown test kind: {kind}"})
            continue
        print(f"run {t['id']} ...", flush=True)
        if kind == "maestro":
            r = _run_maestro(t, ref, env, cwd, args.backend_dir)
        elif kind == "playwright":
            r = _run_browser(ref, env, cwd, t.get("timeout_s", 600))
        else:
            r = _run(cmd, env, cwd, t.get("timeout_s", 600))
        r["id"] = t["id"]
        results.append(r)
        print(f"  {r['status']} ({r['duration_s']}s)")

    report = {
        "manifest": run_manifest,
        "results": results,
        "quarantined_skipped": [
            {"id": s["id"], "reason": s["quarantine"].get("reason"),
             "owner": s["quarantine"].get("owner")} for s in skipped
        ],
    }
    with open(args.out_report, "w") as f:
        json.dump(report, f, indent=2)
    failed = [r for r in results if r["status"] != "passed"]
    print(f"report -> {args.out_report}: "
          f"{len(results) - len(failed)}/{len(results)} passed, "
          f"{len(skipped)} quarantined-skipped")
    return 1 if failed else 0


def cmd_verify_prod(args: argparse.Namespace) -> int:
    manifest = smoke.load_manifest(args.manifest)
    tests = smoke.select_tests(manifest, "loop2")
    run_manifest = det.emit_manifest(
        loop="loop2",
        master_seed=args.seed,
        clock_value=None,  # production is live; the clock is not frozen
        test_selection=smoke.test_ids(tests),
        repo_shas={"harness": det.git_sha(os.getcwd())},
        app_version=args.version,
        environment=f"production ({args.platform})",
    )
    det.write_manifest(run_manifest, args.out_manifest)
    print(f"verifying production build {args.version} on {args.platform}")
    env = _base_env(args.seed, None)
    env["HARNESS_PROD"] = "1"  # flows must refuse destructive steps when set
    results = []
    for t in tests:
        kind, ref = t["id"].split(":", 1)
        cwd = args.mobile_dir if kind in ("maestro", "flutter") else args.web_dir
        cmd = {"maestro": _maestro_command(ref, env, args.harness_dir),
               "playwright": ["node", "--test", ref],
               "node": ["npm", "run", ref]}[kind]
        print(f"run {t['id']} ...", flush=True)
        if kind == "playwright":
            r = _run_browser(ref, env, cwd, t.get("timeout_s", 300))
        else:
            r = _run(cmd, env, cwd, t.get("timeout_s", 300))
        r["id"] = t["id"]
        results.append(r)
        print(f"  {r['status']} ({r['duration_s']}s)")
    failed = [r for r in results if r["status"] != "passed"]
    print(f"{len(results) - len(failed)}/{len(results)} passed on {args.version}")
    if failed:
        print("ALERT: production smoke failures on", args.version)
        for r in failed:
            print(f"  FAIL {r['id']}: {r['tail'][-300:]}")
    return 1 if failed else 0


def cmd_emit_manifest(args: argparse.Namespace) -> int:
    m = det.emit_manifest(
        loop=args.loop,
        master_seed=args.seed,
        clock_value=args.clock,
        test_selection=[],
        repo_shas={},
    )
    det.write_manifest(m, args.out)
    print(f"manifest -> {args.out}")
    return 0


def cmd_explore(args: argparse.Namespace) -> int:
    print("Loop 3 exploratory missions land in Phase 3. "
          f"Requested mission: {args.mission}")
    print("See harness/STRATEGY.md and the Phase 0 assessment for mission order.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="harness",
                                description="Cartha deterministic test harness")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("run-smoke", help="Loop 1: deterministic smoke tier")
    s.add_argument("--seed", required=True)
    s.add_argument("--clock", default="2026-10-02T12:00:00Z")
    s.add_argument("--manifest", default=None)
    s.add_argument("--quarantine", default=None)
    s.add_argument("--mobile-dir", default=".")
    s.add_argument("--web-dir", default=".")
    s.add_argument("--backend-dir", default=".")
    s.add_argument("--shard-index", type=int, default=0)
    s.add_argument("--shard-total", type=int, default=1)
    s.add_argument("--kinds", default="", help="Comma-separated test kinds to run")
    s.add_argument("--out-manifest", default="run-manifest.json")
    s.add_argument("--out-report", default="smoke-report.json")
    s.set_defaults(func=cmd_run_smoke)

    v = sub.add_parser("verify-prod", help="Loop 2: production verification")
    v.add_argument("--seed", required=True)
    v.add_argument("--version", required=True)
    v.add_argument("--platform", default="production")
    v.add_argument("--manifest", default=None)
    v.add_argument("--mobile-dir", default=".")
    v.add_argument("--web-dir", default=".")
    v.add_argument("--harness-dir", default=".")
    v.add_argument("--out-manifest", default="prod-manifest.json")
    v.set_defaults(func=cmd_verify_prod)

    e = sub.add_parser("emit-manifest", help="Write a run manifest only")
    e.add_argument("--seed", required=True)
    e.add_argument("--loop", default="loop1")
    e.add_argument("--clock", default=None)
    e.add_argument("--out", default="run-manifest.json")
    e.set_defaults(func=cmd_emit_manifest)

    x = sub.add_parser("explore", help="Loop 3: exploratory mission (Phase 3)")
    x.add_argument("--mission", required=True)
    x.set_defaults(func=cmd_explore)
    return p


def main() -> None:
    args = build_parser().parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
