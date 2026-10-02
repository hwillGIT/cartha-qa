"""Smoke manifest loading, test selection, and deterministic sharding."""
from __future__ import annotations

import hashlib
import os

import yaml

REQUIRED_TOP_KEYS = ("version", "loop1", "loop2")


def default_manifest_path() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    # <repo>/harness/src/harness -> <repo>/harness/smoke-manifest.yml
    return os.path.join(os.path.dirname(os.path.dirname(here)), "smoke-manifest.yml")


def load_manifest(path: str | None = None) -> dict:
    path = path or default_manifest_path()
    with open(path) as f:
        data = yaml.safe_load(f)
    missing = [k for k in REQUIRED_TOP_KEYS if k not in data]
    if missing:
        raise ValueError(f"smoke manifest {path} missing keys: {missing}")
    return data


def _stable_index(test_id: str, shards: int) -> int:
    digest = hashlib.sha256(test_id.encode()).digest()
    return int.from_bytes(digest[:4], "big") % shards


def select_tests(
    manifest: dict,
    loop: str,
    shard_index: int = 0,
    shard_total: int = 1,
) -> list[dict]:
    """Pick the tests for this run. Sharding is by stable hash of the test id,
    so the same test always lands on the same shard — no flapping between runs.
    """
    if loop not in ("loop1", "loop2"):
        raise ValueError(f"unknown loop: {loop}")
    tests = manifest[loop].get("tests", [])
    if shard_total < 1:
        raise ValueError("shard_total must be >= 1")
    if not 0 <= shard_index < shard_total:
        raise ValueError("shard_index out of range")
    if shard_total == 1:
        return tests
    return [t for t in tests if _stable_index(t["id"], shard_total) == shard_index]


def test_ids(tests: list[dict]) -> list[str]:
    return [t["id"] for t in tests]
