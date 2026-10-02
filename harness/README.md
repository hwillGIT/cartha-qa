# Cartha Test Harness

The harness verifies Cartha's mobile, web, and desktop apps **without blocking
releases**. It checks what shipped, warns about defects before users find them,
and grows smarter with every validated bug.

![CI/CD pipeline](cicd-pipeline.png)

## The three loops

**Loop 1 — Deterministic baseline.** The regression corpus. Seeded data, a
frozen clock, stubbed external services, pinned tools. Same inputs give the
same outputs on every run. The corpus only grows; nothing removes coverage
without a recorded decision.

**Loop 2 — Production verification.** Runs after each release, asynchronously.
A fast smoke suite against the live build, using test accounts and strictly
non-destructive steps. Every report names the exact build it verified — even
when releases ship faster than verification can keep up.

**Loop 3 — Agentic exploratory.** LangChain agents probe the app with
time-boxed missions (payments, auth edges, deep links). Findings ship as
packages — repro steps, video, screenshots, logs. Humans validate; validated
bugs become tracked issues **and** new regression tests that join Loop 1. This
is the only place new tests are authored.

## Design rules

- **YAML describes what; Python decides how.** Workflow files stay thin —
  checkout, set up, call the CLI. All behavior lives in the `harness/` Python
  package: seed handling, sharding, manifests, quarantine. It is tested, typed,
  and runs the same on a laptop as in CI.
- **Determinism is a contract.** One seed propagates to backend, Maestro, and
  Playwright. No fixed sleeps, no silent retries, no random ordering. Flaky
  tests go to a visible quarantine with an owner — never silently dropped.
- **LangChain stays in Loop 3.** No model touches the deterministic path.

## Run it locally

```bash
pip install ./harness
harness run-smoke --seed 42        # Loop 1 smoke tier
harness verify-prod --version 1.2.3  # Loop 2 against a release
harness explore --mission payments  # Loop 3 exploratory mission
```

Every run writes a manifest (`run-manifest.json`) recording repo SHAs, app
version, seed, clock, tool versions, and test selection — so any run can be
replayed exactly.

## CI

| Workflow | Trigger | Runner |
|---|---|---|
| `ci.yml` | push to main, nightly, manual | self-hosted macOS ARM64 |
| `verify-prod.yml` | release published, manual | self-hosted macOS ARM64 |
| `explore.yml` | Phase 3 | — |
| desktop E2E | Phase 4 | self-hosted macOS ARM64 |

The mini runner costs nothing and needs no cloud Mac minutes. Target it with
`runs-on: [self-hosted, macOS, ARM64]`.

## Layout

```
harness/
  README.md            # this file
  STRATEGY.md          # full strategy and phased plan
  cicd-pipeline.png    # architecture diagram
  cicd-pipeline.svg
  pyproject.toml       # pip-installable CLI package
  src/harness/         # CLI source: seed, sharding, manifests, quarantine
  tests/               # package tests
  smoke-manifest.yml   # curated smoke tier (from coverage assessment)
  quarantine.yml       # visible flake quarantine
  DETERMINISM.md       # the determinism contract
  run-manifest-schema.json
  missions/            # exploratory mission definitions (Phase 3)
```

## Status

Phase 0 (coverage assessment) and Phase 1 (Python CLI, determinism contract,
smoke manifests, thin CI) are done. Phase 2 (production verification wiring) is
next. See [STRATEGY.md](STRATEGY.md) for the full phased plan and
[PROGRESS.md](PROGRESS.md) for live status.
