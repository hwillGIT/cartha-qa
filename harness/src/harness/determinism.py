"""Determinism primitives: seed derivation, clock control, manifests.

The contract: one master seed in, fully reproducible run out. Every component
derives its own seed from the master so runs are identical and parallel shards
never share random streams.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone

SCHEMA_VERSION = "1.0"


def derive_seed(master_seed: str, component: str) -> int:
    """Derive a stable 31-bit integer seed for one component.

    Same master seed + same component name always gives the same integer,
    on any machine. Different components never collide by construction.
    """
    digest = hashlib.sha256(f"{master_seed}:{component}".encode()).digest()
    return int.from_bytes(digest[:4], "big") & 0x7FFFFFFF


def seed_env(master_seed: str) -> dict[str, str]:
    """Environment variables that pin randomness for every tool in the run."""
    return {
        "HARNESS_MASTER_SEED": master_seed,
        "HARNESS_MAESTRO_SEED": str(derive_seed(master_seed, "maestro")),
        "HARNESS_PLAYWRIGHT_SEED": str(derive_seed(master_seed, "playwright")),
        "HARNESS_FLUTTER_SEED": str(derive_seed(master_seed, "flutter")),
        "HARNESS_BACKEND_SEED": str(derive_seed(master_seed, "backend")),
        # Dart/Flutter test randomization uses a fixed seed, never "random".
        "HARNESS_DART_SEED": str(derive_seed(master_seed, "dart")),
    }


def clock_env(clock_value: str | None) -> dict[str, str]:
    """Freeze the test clock. clock_value is ISO-8601, e.g. 2026-10-02T12:00:00Z.

    Date-dependent features (Daily Moments, reading plans) read this instead of
    the wall clock. None means "no freeze" — allowed only outside Loop 1.
    """
    if clock_value is None:
        return {}
    return {"HARNESS_TEST_CLOCK": clock_value}


def tool_versions() -> dict[str, str]:
    """Best-effort snapshot of pinned toolchain versions."""
    versions: dict[str, str] = {"python": platform.python_version()}
    for name, cmd in [
        ("flutter", ["flutter", "--version"]),
        ("maestro", ["maestro", "--version"]),
        ("node", ["node", "--version"]),
        ("go", ["go", "version"]),
    ]:
        try:
            out = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30
            ).stdout.strip().splitlines()
            versions[name] = out[0] if out else "unknown"
        except Exception:
            versions[name] = "not-installed"
    return versions


def git_sha(repo_dir: str) -> str:
    """Short SHA of the repo under test, or 'unknown'."""
    try:
        out = subprocess.run(
            ["git", "-C", repo_dir, "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=15,
        ).stdout.strip()
        return out or "unknown"
    except Exception:
        return "unknown"


def emit_manifest(
    *,
    loop: str,
    master_seed: str,
    clock_value: str | None,
    test_selection: list[str],
    repo_shas: dict[str, str],
    app_version: str | None = None,
    environment: str | None = None,
) -> dict:
    """Build the reproducibility manifest for one run.

    Everything needed to replay this exact run lives here. The manifest is
    written next to the results and uploaded as a CI artifact.
    """
    return {
        "schema_version": SCHEMA_VERSION,
        "loop": loop,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "master_seed": master_seed,
        "derived_seeds": {
            c: derive_seed(master_seed, c)
            for c in ("maestro", "playwright", "flutter", "backend", "dart")
        },
        "clock_value": clock_value,
        "test_selection": test_selection,
        "repo_shas": repo_shas,
        "app_version": app_version,
        "environment": environment or platform.platform(),
        "tool_versions": tool_versions(),
        "python": sys.version.split()[0],
    }


def write_manifest(manifest: dict, path: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
