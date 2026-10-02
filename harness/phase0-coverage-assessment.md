# Phase 0 — Coverage Assessment

**Date:** 2026-10-02. **Method:** full inventory of all test files across the
three app repos, mapped against the June QA docs as oracle.
**Inventories:** `phase0/mobile-coverage.md`, `phase0/web-backend-coverage.md`,
`phase0/qa-docs-summary.md` (working files, not checked in).

## Verdict

The corpus is large and real: **546 Maestro flows, 281 web test files, 637
backend test files.** Bible reader, messaging, clips, and auth are deeply
covered. But flow count is not coverage — and five areas are thin or empty
everywhere: **payments, deep links, session expiry, network drops,
double-submit.** The June gap analysis is still open on all five. The draft
16-flow smoke tier needs surgery before it touches production: 4 flows are
production-unsafe.

## What's covered

**Mobile** (`cartha.ai.mobile`, 546 Maestro flows — staged determinism via
`cartha://qa-screen` fixtures): bible reader 106, messages/chat 72,
clips/watch 43, daily moments 41, profile/social 39, launch/login 34,
connect/matchmaking 31, church/community 29, hangouts 32.

**Web** (`cartha.website`, 281 files, `node --test`): bible reader 34, atlas
27, sermons 25, graphic novel 23, discovery 18, ask-cartha 17, nav/shell 16,
auth/session 13, payments/wallet 9.

**Backend** (`CarthaCdkService`, 637 files — 476 Go, 161 Python): dominated by
`mobile-api-service-go` (387). Auth/session is the best-covered sensitive area
on both web and backend.

## The gaps (ranked)

1. **Payments / transaction edges.** Mobile has 18 payment flows but they
   assert UI only or use local fakes — zero real purchase completions, zero
   failure/cancel/restore paths. Web wallet tests cover checkout UI; the
   donate route is untested. Highest business risk. → Exploratory mission 1.
2. **Deep links.** Mobile: 6 flows, happy-path staged only. Web: zero tests.
   The 11 documented bugs are dominated by invalid-route silent fallbacks —
   the app's known weak pattern. → Mission 2.
3. **Session expiry.** Mobile: 3 flows, all QA-button staged. No
   expiry-mid-action, no refresh races. Web/backend auth coverage is good for
   the happy path. → Mission 3.
4. **Network drops.** Mobile: ~1 flow (needs manual network disable). No
   mid-call disconnect test, no reconnect behavior. → Mission 4.
5. **Double-submit / idempotency.** Zero everywhere. No flow taps
   submit/send/purchase twice. → Mission 5.
6. **Push notifications.** Thin on all three surfaces (1 backend test, 2–3
   web, permission UI only on mobile). No delivery-path tests.
7. **Safety services.** `gemma4-safety-service`, `shieldgemma2-safety-service`,
   `safety-benchmark` — zero tests. No baseline exists; needs new tests, not
   curation.

## Structural risks

- **Smoke tier surgery required.** 4 of the 16 draft flows are
  production-unsafe (live Open Room creation, real audio/video call
  initiation, real friend request). Loop 1 keeps them QA-staged; Loop 2 gets a
  separate prod-safe manifest of ~11–12 flows.
- **Live LLM test.** `cerebras_client_live_test.go` hits a real API — it must
  be stubbed or quarantined before entering any deterministic tier.
- **Generated-flow rot.** Many Maestro flows are AI-authored and assert copy
  text; they will rot. Fixture freshness (`qa-screen` staging) needs periodic
  checks — a flow can pass against a stale fixture.
- **Playwright is ad-hoc.** 2 browser tests, no shared config. Formalize in
  Phase 1.
- **Oracle docs are 3 months old.** "50+ flows" is actually 30; bug statuses
  need re-verification; the docs contradict themselves on payment coverage.
  Treat as expected behavior to verify, not ground truth.

## What this means next

- **Phase 1** builds the smoke manifest from this assessment (not the raw
  16-flow draft), the determinism contract, and the run-manifest schema — plus
  a separate Loop 2 prod-safe manifest.
- **Phase 3** runs exploratory missions in the order above.
- Safety services and push delivery need **new** tests (Loop 3 output), not
  curation.
