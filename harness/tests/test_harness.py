import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from harness import determinism as det
from harness import smoke, quarantine, cli


def test_derive_seed_stable():
    assert det.derive_seed("abc", "maestro") == det.derive_seed("abc", "maestro")


def test_derive_seed_differs_by_component():
    assert det.derive_seed("abc", "maestro") != det.derive_seed("abc", "playwright")


def test_derive_seed_differs_by_master():
    assert det.derive_seed("abc", "maestro") != det.derive_seed("abd", "maestro")


def test_seed_in_31_bits():
    s = det.derive_seed("x", "y")
    assert 0 <= s <= 0x7FFFFFFF


def test_manifest_roundtrip(tmp_path):
    m = det.emit_manifest(loop="loop1", master_seed="s1", clock_value="2026-10-02T12:00:00Z",
                          test_selection=["a", "b"], repo_shas={"mobile": "abc123"})
    p = str(tmp_path / "m.json")
    det.write_manifest(m, p)
    import json
    back = json.load(open(p))
    assert back["master_seed"] == "s1"
    assert back["derived_seeds"]["maestro"] == det.derive_seed("s1", "maestro")
    assert back["loop"] == "loop1"


def test_smoke_manifest_loads():
    here = os.path.dirname(os.path.abspath(__file__))
    mp = os.path.join(here, "..", "smoke-manifest.yml")
    manifest = smoke.load_manifest(mp)
    l1 = smoke.select_tests(manifest, "loop1")
    l2 = smoke.select_tests(manifest, "loop2")
    assert len(l1) == 19  # 16 maestro + 3 web
    assert len(l2) == 15  # 12 maestro + 3 web
    assert "maestro:harness/maestro/launch-fellowship.yaml" in smoke.test_ids(l1)
    assert not any("00_launch_and_screenshot.yaml" in t["id"] for t in l1)
    # the 4 production-unsafe flows are absent from loop2
    ids2 = " ".join(smoke.test_ids(l2))
    for bad in ("30_hangouts_smoke", "62_profile_audio_call_smoke",
                "63_public_profile_add_friend_smoke", "64_profile_video_call_smoke"):
        assert bad not in ids2


def test_sharding_stable_and_complete():
    here = os.path.dirname(os.path.abspath(__file__))
    mp = os.path.join(here, "..", "smoke-manifest.yml")
    manifest = smoke.load_manifest(mp)
    shards = [smoke.select_tests(manifest, "loop1", i, 3) for i in range(3)]
    all_ids = sorted(sum([smoke.test_ids(s) for s in shards], []))
    full_ids = sorted(smoke.test_ids(smoke.select_tests(manifest, "loop1")))
    assert all_ids == full_ids  # every test on exactly one shard
    # stable: same test, same shard, every time
    again = smoke.select_tests(manifest, "loop1", 0, 3)
    assert smoke.test_ids(again) == smoke.test_ids(shards[0])


def test_quarantine_partition():
    tests = [{"id": "a"}, {"id": "b"}]
    q = {"b": {"reason": "flaky", "owner": "jess", "since": "2026-10-02"}}
    runnable, skipped = quarantine.partition(tests, q)
    assert [t["id"] for t in runnable] == ["a"]
    assert skipped[0]["id"] == "b"
    assert skipped[0]["quarantine"]["reason"] == "flaky"


def test_maestro_uses_prepared_simulator():
    assert cli._maestro_command("flow.yaml", {"SIMULATOR_UDID": "device-123"}) == [
        "maestro", "test", "--device", "device-123", "flow.yaml"
    ]


def test_qa_owned_maestro_flow_resolves_from_harness(tmp_path):
    flow = tmp_path / "harness" / "maestro" / "launch.yaml"
    flow.parent.mkdir(parents=True)
    flow.write_text("appId: com.cartha.app\n---\n")
    assert cli._maestro_command("harness/maestro/launch.yaml", {}, str(tmp_path))[-1] == str(flow)


def test_qa_stage_reuses_mobile_helper(tmp_path, monkeypatch):
    seen = {}

    def fake_run(cmd, env, cwd, timeout):
        seen.update(cmd=cmd, cwd=cwd, timeout=timeout)
        return {"status": "passed"}

    monkeypatch.setattr(cli, "_run", fake_run)
    result = cli._qa_setup(
        {"qa_stage": {"screen": "public_profile", "data": {"user_id": "fixture"},
                      "launch_app": False}},
        {"SIMULATOR_UDID": "device-123"}, str(tmp_path))
    assert result["status"] == "passed"
    assert seen["cmd"][1].endswith("cartha_ai_mobile/scripts/qa_debug_api.py")
    assert seen["cmd"][-2:] == ["--data-json", '{"user_id":"fixture"}']
    assert "--launch-app" not in seen["cmd"]


def test_staged_screen_keeps_original_assertions(tmp_path):
    import yaml

    source = tmp_path / "source.yaml"
    source.write_text("appId: com.cartha.app\n---\n- openLink: cartha://qa-screen?screen=messages_home\n- assertVisible:\n    id: messages_thread_search_button\n")
    prepared = tmp_path / "prepared.yaml"
    cli._without_qa_open_link(str(source), str(prepared), ["Got it"])
    config, commands = list(yaml.safe_load_all(prepared.read_text()))
    assert config["appId"] == "com.cartha.app"
    assert commands == [
        {"runFlow": {"when": {"visible": "Got it"},
                     "commands": [{"tapOn": "Got it"}]}},
        {"assertVisible": {"id": "messages_thread_search_button"}},
    ]


def test_qa_setup_failure_does_not_run_maestro(tmp_path, monkeypatch):
    monkeypatch.setattr(cli, "_qa_setup", lambda *args: {
        "status": "failed", "tail": "staging failed", "duration_s": 1})
    monkeypatch.setattr(cli, "_run", lambda *args: (_ for _ in ()).throw(
        AssertionError("Maestro must not run without its fixture")))
    result = cli._run_maestro({"qa_stage": {"screen": "clips_home"}}, "x.yaml",
                              {"SIMULATOR_UDID": "device-123"},
                              str(tmp_path), str(tmp_path))
    assert result["status"] == "error"
    assert "QA setup failed" in result["tail"]


def test_browser_smoke_serves_checked_out_promo(tmp_path, monkeypatch):
    import urllib.request
    promo = tmp_path / "redirects"
    promo.mkdir()
    (promo / "index.html").write_text("<h1>checked-out promo</h1>")
    seen = {}

    def fake_run(cmd, env, cwd, timeout):
        seen["cmd"] = cmd
        seen["url"] = env["DOWNLOAD_PROMO_URL"]
        with urllib.request.urlopen(seen["url"]) as response:
            assert b"checked-out promo" in response.read()
        return {"status": "passed"}

    monkeypatch.setattr(cli, "_run", fake_run)
    result = cli._run_browser("test/download-promo.browser.mjs", {}, str(tmp_path), 30)
    assert result["status"] == "passed"
    assert seen["cmd"] == ["node", "--test", "test/download-promo.browser.mjs"]
    assert seen["url"].startswith("http://127.0.0.1:")


def test_production_browser_requires_explicit_https_url(tmp_path):
    result = cli._run_browser("test/download-promo.browser.mjs",
                              {"HARNESS_PROD": "1"}, str(tmp_path), 30)
    assert result["status"] == "error"
    assert "DOWNLOAD_PROMO_URL" in result["tail"]
