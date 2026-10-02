"""Quarantine: flaky tests are visible, owned, and skipped — never silent."""
from __future__ import annotations

import os

import yaml


def load_quarantine(path: str | None = None) -> dict[str, dict]:
    """Returns {test_id: {reason, owner, since}}."""
    if path is None:
        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(
            os.path.dirname(os.path.dirname(here)), "quarantine.yml"
        )
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        data = yaml.safe_load(f) or {}
    return {q["id"]: q for q in data.get("quarantined", [])}


def partition(
    tests: list[dict], quarantined: dict[str, dict]
) -> tuple[list[dict], list[dict]]:
    """Split tests into (runnable, quarantined). Both lists are returned so
    the report always shows what was skipped and why."""
    runnable, skipped = [], []
    for t in tests:
        if t["id"] in quarantined:
            skipped.append({**t, "quarantine": quarantined[t["id"]]})
        else:
            runnable.append(t)
    return runnable, skipped
