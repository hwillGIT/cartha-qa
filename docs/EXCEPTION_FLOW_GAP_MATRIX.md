# Cartha — Exception-Flow QA Gap Matrix

**Generated:** 2026-06-30
**Method:** Cross-referenced all Maestro flows (`.maestro/flows`, `.maestro/subflows`) and
widget/unit tests (`test/**/*_test.dart`) against an exception/dead-end taxonomy.
**Corpus:** 316 Maestro flows + 393 widget tests vs. 547 screens (`lib/screens`).

> Goal: surface **dead-ends and missing exception flows** — the negative space the
> existing (happy-path-heavy) suite does not cover. This is a gap analysis, **not** a
> rebuild. Cartha already has a mature QA system (Maestro + Gemini video sweep +
> agentic QA scripts). Per `CLAUDE.md`, do NOT run `./scripts/qa_sweep.sh` by default.

## Coverage by exception state (worst first)

| Exception state | Maestro flows | Widget tests | Verdict |
|---|---|---|---|
| Payment fail / cancel | 0 | 0 | 🔴 Zero coverage (`PaymentResultScreen` `/payment-cancel`, paywall, IAP restore) |
| Deep-link 404 / invalid route | 0 | 0 | 🔴 Zero coverage (`/join/:code`, party/clip deep links, `onGenerateRoute`) |
| Session expired (mid-action) | 1 | 1 | 🔴 Only `41_session_expired_notice` — static notice, no mid-action expiry |
| Double-submit / rapid-tap | 4 | 0 | 🟠 Incidental only, no debounce assertions |
| Offline / network drop | 5 | 0 | 🟠 Critical for LiveKit calls; no mid-call disconnect test |
| Error / failure UI | 8 | 1 | 🟠 Thin vs 547 screens; no generic API-500 / retry assertions |
| Banned / safety | 10 | 3 | 🟡 Temp-vs-permanent ban paths unverified |
| Permission denied | 11 | 3 | 🟡 Notification covered; mic/camera denial on room entry not clearly tested |
| Empty states | 20 | 2 | 🟡 Decent breadth, shallow depth |
| Auth gate / guest | 65 | 7 | 🟢 Well covered |
| Cancel mid-flow | 84 | 0 | 🟢 Heavily covered in flows |

## Top priority gaps (recommended new tests)

1. **Payments negative paths** — Stripe `/payment-cancel`, declined card, IAP restore
   failure, paywall dismiss. Screens: `PaymentResultScreen`, `SubscriptionPaywallScreen`,
   `CreditsWalletScreen`. *Highest business risk.*
2. **Deep-link dead-ends** — invalid/expired `/join/:code`, malformed clip/party links,
   unknown routes. Screens: `PartyJoinByCodeScreen`, `onGenerateRoute` in `main.dart`.
3. **Session expiry mid-action** — token dies while sending a message / joining a call;
   verify re-auth routing, not just the static notice.
4. **Mid-call network loss** — LiveKit disconnect/reconnect on `VideoRoomScreenV2` /
   `AudioRoomScreen`; verify recovery UI vs. a frozen dead-end.
5. **Mic / camera permission denial at room entry** — denied hardware perms entering a
   video/audio room; verify graceful fallback (`115_video_camera_recovery_controls`
   exists but entry-denial path is unverified).

## Notes / caveats

- `session_expired` initially scored 317 (false positive: the keyword "timeout" matches
  Maestro's built-in per-flow retry config). Strict re-scan → **1** real flow.
- "Cancel mid-flow" = 84 is mostly happy-path teardown (dismiss sheets), not true
  abort-and-recover assertions — depth is shallower than the count implies.
- Coverage is keyword-based (file + body scan); treat counts as signal, not proof. Each
  prioritized gap should be confirmed by reading the candidate flow before authoring.
