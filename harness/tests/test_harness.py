import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from harness import determinism as det
from harness import smoke, quarantine


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
