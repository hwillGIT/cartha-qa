"""harness CLI — the executable face of the CI/CD pipeline.

Thin YAML workflows call these commands; all behavior lives here.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time

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


def cmd_run_smoke(args: argparse.Namespace) -> int:
    manifest = smoke.load_manifest(args.manifest)
    tests = smoke.select_tests(
        manifest, "loop1", args.shard_index, args.shard_total
    )
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
            "harness": det.git_sha(os.getcwd()),
        },
    )
    det.write_manifest(run_manifest, args.out_manifest)
    print(f"manifest -> {args.out_manifest}  seed={args.seed}")

    env = _base_env(args.seed, args.clock)
    results = []
    for t in runnable:
        kind, ref = t["id"].split(":", 1)
        if kind == "maestro":
            cmd = ["maestro", "test", ref]
            cwd = args.mobile_dir
        elif kind == "playwright":
            cmd = ["npx", "playwright", "test", ref]
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
        cmd = {"maestro": ["maestro", "test", ref],
               "playwright": ["npx", "playwright", "test", ref],
               "node": ["npm", "run", ref]}[kind]
        print(f"run {t['id']} ...", flush=True)
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
