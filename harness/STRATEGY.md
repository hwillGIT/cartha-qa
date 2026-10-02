# Cartha Test Harness — Strategy & Plan

**Status:** Draft for review. Nothing here runs until the plan is approved.
**Owner:** Hubert Williams. **Date:** 2026-10-02.

## The decision

Build a three-loop verification system for Cartha's mobile, web, and desktop
apps that runs **in parallel with releases, never blocking them**. Zack ships
when he is ready. The harness verifies what shipped, warns about defects before
users report them, and gets faster over time until it keeps pace with his
release speed.

Why this shape: most defects are minor annoyances and Zack fixes showstoppers
fast. The harness does not gate him — it gives early warning. Speed is the
primary design constraint.

## The three loops

**Loop 1 — Deterministic baseline.** The regression corpus. Seeded data, fixed
inputs, controlled clocks, stubbed external systems (LLM, push, third-party
APIs). Pinned toolchains. No fixed sleeps, no silent retries. Flaky tests go to
a visible quarantine with an owner and reason — never silently dropped. The
corpus only grows; nothing removes coverage without a recorded decision. Every
run emits a reproducibility manifest (repo SHAs, app version, seed, clock,
tool versions, environment, test selection).

**Loop 2 — Production verification.** Runs after Zack ships, asynchronously. A
small fast smoke suite against the deployed production build, recording the
exact app version under test. Dedicated test accounts. Strictly
non-destructive: no purchases, no uploads, no matchmaking, no messages to real
users. If Zack outruns the harness, reports are version-aware — they always
say which build was actually verified.

**Loop 3 — Agentic exploratory.** The discovery engine. Vision-capable agents
drive the app through the same tools as Loop 1 (Maestro on mobile, Playwright
on web) — no separate automation stack. Time-boxed missions, not scripts
("probe checkout edge cases", "check Bible-reader parity mobile vs web").
Each finding ships as a package: repro steps, screenshots, video, logs,
network evidence, tested version and SHAs. Findings are deduplicated against
known issues, then validated by a human. Validated defects become tracked
issues **and** new deterministic regression tests (agent drafts, human reviews)
that join the Loop 1 baseline. This is the only place new tests are authored,
and only from validated bugs.

How the loops feed each other: Loop 3 discovers what Loop 1 misses; validated
findings grow Loop 1; Loop 2 checks that production builds survive Loop 1's
smoke subset.

## Platform scope

- **Mobile (iOS/Android):** Maestro flows + Flutter unit/widget tests. The
  existing 546 Maestro flows are the inventory; the smoke manifest curates the
  under-10-minute subset.
- **Web:** two surfaces. The Next.js site (`node --test` suites + Playwright)
  and the Flutter web build (Playwright). Both covered.
- **Desktop (macOS):** last, offline. Separate macOS build of the Flutter app.
  Unit/widget coverage is free via `melos test`; E2E needs a new
  `integration_test` suite and runs on the self-hosted mini runner. Tracked as
  a defined gap, not silently omitted.
- **Backend:** Go and pytest suites run in CI. Full ephemeral-stack E2E is a
  later phase (decision pending: Docker Compose stack vs recorded-fixture mock).

## What exists vs. what we build

The app tests already exist (Zack's team wrote them over months). We do not
re-author them. We build:

1. The **coverage assessment** — map all existing tests against the 50+
   documented flows and the app's real surface; write the gaps down.
2. The **smoke manifest** — the curated subset, defined as code, sharded to
   the 10-minute target. Built *from* the assessment, not before it.
3. The **determinism contract** — seed propagation, frozen clock, stubs,
   pinned versions, quarantine rules.
4. The **run-manifest schema** — what every run records.
5. **CI workflows** — mobile/web loops on Linux runners; desktop on the mini.
6. **Release manifests + async triggers** — Loop 2 wiring.
7. **Mission files + finding schema + triage process** — Loop 3 wiring.

## Infrastructure (live)

- **Huberts-Mac-mini**: self-hosted GitHub Actions runner, online and idle,
  labels `self-hosted, macOS, ARM64`. Verified end-to-end 2026-10-02. Zero
  cloud Mac minutes. Target it with `runs-on: [self-hosted, macOS, ARM64]`.
- **Tailscale**: this build agent's VM and the mini are on Hubert's tailnet.
  Direct SSH to the mini works (key-authenticated) for setup and debugging.
- **MacBook Pro**: runner files staged; can become a second runner if wanted.
  Not needed now.

## Phased plan

**Phase 0 — Coverage assessment.** Inventory every Maestro flow, web test, and
backend suite; map against the documented flows and the app surface; publish
the gap list.
*Outcome: a written assessment naming what's covered, what's not, and where
the first exploratory missions should go.*

**Phase 1 — Scaffold.** Smoke manifest (from Phase 0), determinism contract,
run-manifest schema, CI workflows for Loop 1 on mobile + web.
*Outcome: `main` runs the deterministic baseline on every push, under 10
minutes for smoke, with manifests emitted.*

**Phase 2 — Production verification.** Release-version manifests, async
release triggers, the production-safe smoke subset, alert routing.
*Outcome: every Zack release is smoke-verified without blocking him, and
someone is notified of failures.*

**Phase 3 — Exploratory loop.** Mission files (payments, auth/session edges,
deep links first), finding schema, triage queue, first missions run.
*Outcome: candidate findings flowing, with at least the first validated bug
converted to a baseline regression test.*

**Phase 4 — Desktop.** `integration_test` suite mirroring the smoke tier,
mini-runner CI job, offline cadence.
*Outcome: the macOS build gets the same smoke treatment as mobile/web.*

**Phase 5 — Backend E2E.** Ephemeral full-system stack per run (pending the
Compose-vs-mock decision).
*Outcome: contract and E2E coverage between backend and clients.*

## Open decisions (need Hubert)

1. E2E backend target: ephemeral Docker Compose stack vs recorded-fixture
   mock server.
2. Alert destination for production-smoke failures.
3. Issue repo for exploratory findings (working default: cartha-qa).
4. Whether the MacBook also becomes a runner.

## Risks

- **Zack's velocity vs. harness speed.** Mitigated by version-aware reporting
  and the 10-minute smoke target; accepted, not solved, by design.
- **Flaky mobile tests.** Quarantine with owner/reason keeps the signal clean.
- **Mini availability.** The runner needs the mini awake and on the network.
  Cloud macOS runners are the fallback (paid, 10x minutes).
- **June QA docs are stale.** Treat cartha-qa's flow docs as oracles to
  verify, not ground truth.
