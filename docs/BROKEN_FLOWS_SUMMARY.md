# Cartha Broken Flows & Test Strategy — Summary

**Status:** Analysis in progress (Opus deep-dive delegated)

**Last Updated:** 2026-06-30

---

## Executive Summary

From our initial exploratory QA and gap analysis, we've identified **broken flows and missing test coverage** across cartha.com:

### Current Known Issues

| Issue | Severity | Status | Test Status |
|-------|----------|--------|------------|
| Groups 404 fallback | 🟡 Medium | Open (bug) | ✅ Test written |
| Messages onboarding copy | 🟡 Medium | Open (UX) | ⏳ Needs test |
| Invalid routes redirect | 🟢 Low | Open (minor) | ⏳ Optional test |

### Zero-Coverage Exception Flows

From gap matrix (316 Maestro + 393 widget tests vs 547 screens):

| Exception Flow | Coverage | Priority | Impact |
|---|---|---|---|
| **Payment fail/cancel** | 🔴 0% | 🔴 CRITICAL | Business risk (revenue) |
| **Deep-link 404/invalid** | 🔴 0% | 🔴 HIGH | User-facing dead-ends |
| **Session expiry mid-action** | 🔴 1% | 🔴 HIGH | Data loss risk |
| **Mid-call network drop** | 🟠 1% | 🔴 HIGH | LiveKit reliability |
| **Mic/camera permission denial** | 🟠 4% | 🟡 MEDIUM | Accessibility |
| **Double-submit/rapid-tap** | 🟠 2% | 🟡 MEDIUM | UX/race conditions |
| **Error UI / retry** | 🟠 2% | 🟡 MEDIUM | Error recovery |
| **Banned/safety flows** | 🟡 5% | 🟢 LOW | Safety features |

---

## Broken Flows (Confirmed)

### 1. Groups 404 Handling

**Broken Flow:**
- User visits invalid group ID: `/groups/invalid-code`
- **Expected:** "Group not found" error page or message
- **Actual:** Shows groups onboarding carousel (indistinguishable from logged-out discovery)
- **Root Cause:** No route validation; invalid group ID not checked before render
- **Impact:** User confusion, untested deep-link flows

**Test Status:**
- ✅ Maestro flow written: `201_party_join_invalid_code_dead_end.yaml`
- ⏳ Widget test needed: `GroupsPage` exists check

---

### 2. Messages Onboarding Copy

**Broken Flow:**
- User visits `/messages` (logged out)
- **Expected:** Messaging-specific onboarding ("Start conversations with friends")
- **Actual:** Groups onboarding carousel ("Create group chats for your people")
- **Root Cause:** Messages page shares groups onboarding component
- **Impact:** UX inconsistency, feature confusion

**Test Status:**
- ⏳ Test needed: Verify `/messages` shows messaging copy, not groups copy

---

### 3. Invalid Routes → Landing Page Redirect

**Broken Flow:**
- User visits `/this-route-does-not-exist`
- **Expected:** 404 error page
- **Actual:** Silent redirect to landing page
- **Root Cause:** Route handler has no catch-all 404; falls back to home
- **Impact:** Lost analytics, debugging opacity (low severity)

**Test Status:**
- ⏳ Optional: Test invalid route behavior

---

## Zero-Coverage Gaps (Not Yet Tested)

### Critical Gaps

#### 1. Payment Failure Flows (CRITICAL)

**Flows:**
- Stripe payment cancellation (`/payment-cancel`)
- Card declined during purchase
- IAP restore failure
- Paywall dismiss (user exits without paying)

**Why Broken:** Zero test coverage on payment exception paths

**Test Type:** Maestro flow + widget test

**Effort:** Medium (requires mock payment provider)

---

#### 2. Deep-Link Invalid/Expired Codes (HIGH)

**Flows:**
- Join group with expired code: `/join/expired-code`
- Malformed clip deep-link: `/clip/invalid-id`
- Visit party after it ends
- Deep-link to gated content while logged out

**Why Broken:** Zero validation on link parameters

**Test Type:** Maestro flow (multiple scenarios)

**Effort:** Medium

---

#### 3. Session Expiry Mid-Action (HIGH)

**Flows:**
- Token expires while sending a message
- Session dies mid-group-join
- Auth session timeout during live call
- Re-auth routing after expiry

**Why Broken:** Only 1 static "session expired" notice; no mid-action recovery tested

**Test Type:** Maestro flow + widget test (mock auth timeout)

**Effort:** High (requires timing/mocking)

---

#### 4. Mid-Call Network Loss (HIGH)

**Flows:**
- WiFi drops during video call
- Internet reconnects after 5sec disconnect
- Call recovery after network change (LTE → WiFi)
- No recovery path (stuck call screen)

**Why Broken:** LiveKit resilience untested; only 5 offline flows (no mid-call)

**Test Type:** Integration test (requires network simulation)

**Effort:** High

---

#### 5. Mic/Camera Permission Denial (MEDIUM)

**Flows:**
- User denies camera permission at app startup
- User denies mic permission when entering audio room
- Permission flip: deny → allow (app state sync)
- Entering room without permissions

**Why Broken:** Only 11 permission flows; mic/camera entry denial unverified

**Test Type:** Widget test + Maestro flow (permission mocking)

**Effort:** Medium

---

#### 6. Double-Submit/Rapid-Tap (MEDIUM)

**Flows:**
- User taps "Join Group" twice quickly
- Submits form, then taps again before response
- Creates duplicate messages on rapid send
- Multiple room entry requests queued

**Why Broken:** Only 4 incidental flows; no explicit debounce testing

**Test Type:** Widget test (rapid interaction mocking)

**Effort:** Low

---

#### 7. Error UI & Retry (MEDIUM)

**Flows:**
- API returns 500 error
- Network timeout during group message fetch
- Retry button triggers re-request
- Retry success after first failure

**Why Broken:** Only 8 error flows; generic retry path not clearly tested

**Test Type:** Widget test + Maestro flow (mock API errors)

**Effort:** Medium

---

## Test Strategy (Waiting for Opus)

We've delegated to Opus (high-reasoning model) to:

1. **Systematically test cartha.com** for additional broken flows we haven't discovered
2. **Prioritize test gaps** by impact and effort
3. **Create TEST_STRATEGY.md** with:
   - Complete broken flows matrix
   - Prioritized test roadmap (Phase 1/2/3)
   - Test authoring guidelines
   - Effort estimates per test

**Status:** ⏳ In progress (background delegation)

---

## What We Need to Do

### Immediate (when Opus finishes):

1. **Review Opus findings** — additional broken flows
2. **Merge with existing gap matrix** — create unified broken-flows matrix
3. **Create TEST_STRATEGY.md** — prioritized test roadmap
4. **Triage with Zack** — confirm bugs vs. intentional behavior

### Phase 1 (High-Priority Tests):

- [ ] Payment failure flows (1-2 Maestro flows + widget tests)
- [ ] Deep-link invalid codes (2-3 Maestro flows)
- [ ] Session expiry mid-action (1 complex Maestro flow)

### Phase 2 (Medium-Priority):

- [ ] Network resilience (LiveKit mid-call loss)
- [ ] Mic/camera permission denial
- [ ] Double-submit prevention
- [ ] Error UI & retry paths

### Phase 3 (Nice-to-have):

- [ ] 404 page UI
- [ ] Banned/safety flow edge cases
- [ ] Empty state deep coverage

---

## Next: Waiting for Opus Analysis

**Delegation Details:**
- Model: Opus (high-reasoning, exploratory QA)
- Toolset: Browser
- Scope: Comprehensive cartha.com flow testing
- Deliverable: Complete broken-flows matrix + TEST_STRATEGY.md

**ETA:** ~10-15 minutes (background process)

---

**For more:** See `docs/QA_FINDINGS.md` and `docs/EXCEPTION_FLOW_GAP_MATRIX.md`
