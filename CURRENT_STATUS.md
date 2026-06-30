# Cartha QA — Current Status & Roadmap

**Last Updated:** 2026-06-30
**Status:** Analysis phase → Opus deep-dive in progress

---

## 📊 What We Know (Confirmed Broken Flows)

### Broken Flows Identified So Far

| Issue | Severity | Status | Test | Root Cause |
|-------|----------|--------|------|-----------|
| Groups 404 fallback | 🟡 Medium | Open | ✅ Written | No route validation |
| Messages onboarding | 🟡 Medium | Open | ⏳ Needed | Shared groups component |
| Invalid routes redirect | 🟢 Low | Open | ⏳ Optional | No catch-all 404 |

### Zero-Coverage Exception Flows (Gap Matrix)

| Flow | Coverage | Priority | Impact | Test Type |
|------|----------|----------|--------|-----------|
| **Payment failure** | 0% | 🔴 CRITICAL | Revenue loss | Maestro + Widget |
| **Deep-link invalid** | 0% | 🔴 HIGH | Dead-ends | Maestro flows (3) |
| **Session expiry** | 1% | 🔴 HIGH | Data loss | Maestro + Widget |
| **Network drop** | 1% | 🔴 HIGH | Service | Integration test |
| **Permission denial** | 4% | 🟡 MEDIUM | Accessibility | Maestro + Widget |
| **Double-submit** | 2% | 🟡 MEDIUM | Race conditions | Widget test |
| **Error UI/retry** | 2% | 🟡 MEDIUM | Recovery | Maestro + Widget |

---

## 📚 Documentation Created

| Document | Purpose | Status |
|----------|---------|--------|
| **QA_FINDINGS.md** | 7 live-site findings (0 blockers) | ✅ Complete |
| **EXCEPTION_FLOW_GAP_MATRIX.md** | Coverage analysis (316 flows + 393 tests) | ✅ Complete |
| **BROKEN_FLOWS_SUMMARY.md** | Consolidated broken flows overview | ✅ Complete |
| **TEST_AUTHORING_GUIDELINES.md** | How to write tests for Cartha patterns | ✅ Complete |
| **TEST_STRATEGY.md** | Comprehensive broken-flows + roadmap | ⏳ Opus delegated |

---

## 🧪 Tests Written

| Test | Type | Status | Location |
|------|------|--------|----------|
| Payment cancel (3 tests) | Widget | ✅ GREEN | `test-cases/widget/payment_result_cancel_test.dart` |
| Deep-link invalid code | Maestro | ✅ Written | `test-cases/maestro/201_party_join_invalid_code_dead_end.yaml` |

---

## ⏳ What's Happening Now

**Delegated to Opus (background):**

```
TASK: Comprehensive exploratory QA on cartha.com
SCOPE: Test ALL user flows for broken interactions
OUTPUT: Complete TEST_STRATEGY.md with:
  - All identified broken flows (matrix)
  - Prioritized test roadmap (Phase 1/2/3)
  - Test authoring examples
  - Effort estimates

STATUS: Running (~/browser tools)
ETA: 10-15 minutes
```

---

## 🎯 High-Level Roadmap

### Phase 0: Documentation & Analysis ✅ (In Progress)

- [x] Gap analysis complete (EXCEPTION_FLOW_GAP_MATRIX.md)
- [x] Live-site findings documented (QA_FINDINGS.md)
- [x] Test authoring guidelines created (TEST_AUTHORING_GUIDELINES.md)
- [x] 2 tests written (payment cancel, deep-link invalid)
- ⏳ Comprehensive test strategy (awaiting Opus)

**Deliverables:**
- ✅ 8 documentation files
- ✅ 7 findings (0 blockers)
- ✅ 2 exception-flow tests
- ✅ GitHub repo public and documented

---

### Phase 1: Critical Tests (2-3 weeks)

**High-priority gaps that block release:**

| Flow | Test Type | Effort | Impact |
|------|-----------|--------|--------|
| Payment cancel/decline/IAP | Maestro + Widget | High | Revenue risk |
| Deep-link invalid code (3 scenarios) | Maestro flows | Medium | User dead-ends |
| Session expiry mid-action | Maestro + Widget | High | Data loss |

**Success Criteria:**
- All 3 critical flows have tests
- Tests are passing (green)
- Documented in upstream cartha.ai.mobile
- Ready for PR review

---

### Phase 2: High-Priority Tests (1-2 weeks)

**Reliability & accessibility gaps:**

| Flow | Test Type | Effort | Impact |
|------|-----------|--------|--------|
| Mid-call network drop | Integration | High | LiveKit reliability |
| Mic/camera permission denial | Maestro + Widget | Medium | Room entry |
| Double-submit prevention | Widget | Low | Race conditions |
| Error UI & retry paths | Maestro + Widget | Medium | Error recovery |

**Success Criteria:**
- All 4 flows have tests
- Network resilience verified
- Permission flows tested
- Added to upstream repo

---

### Phase 3: Nice-to-Have Tests (1 week)

**Edge cases & completeness:**

| Flow | Test Type | Effort | Impact |
|------|-----------|--------|--------|
| 404 page UX | Maestro | Low | Analytics |
| Banned user flows | Maestro | Low | Safety |
| Empty states (all sections) | Maestro | Medium | UX polish |

---

## 🚀 What's Next (When Opus Finishes)

### Immediate Actions:

1. **Review TEST_STRATEGY.md**
   - Examine all identified flows
   - Agree on priorities
   - Estimate total effort

2. **Triage with Zack**
   - Confirm: Groups 404 is a bug (not intended fallback)
   - Confirm: Messages onboarding needs messaging-specific copy
   - Review: Phase 1 test priorities

3. **Create Phase 1 Sprint**
   - Assign test authoring (to subagents)
   - Set timeline (2-3 weeks)
   - Track progress in GitHub issues

---

## 📍 Repository Status

**Location:** `~/dev/cartha-qa`
**GitHub:** https://github.com/hwillGIT/cartha-qa (Public)

**Content:**
- 8 documentation files
- 2 exception-flow tests written
- Comprehensive gap analysis
- Test authoring guidelines
- 8 commits, fully pushed

**Structure:**
```
cartha-qa/
├── README.md                          # Overview
├── CONTRIBUTION.md                    # Test authoring guide
├── INDEX.md                           # Quick reference
├── docs/
│   ├── QA_FINDINGS.md                # Live-site findings
│   ├── EXCEPTION_FLOW_GAP_MATRIX.md  # Coverage analysis
│   ├── BROKEN_FLOWS_SUMMARY.md       # Consolidated issues
│   ├── TEST_AUTHORING_GUIDELINES.md  # How to write tests
│   ├── TEST_STRATEGY.md (⏳ incoming) # Full roadmap
│   └── SETUP.md                       # Environment setup
├── test-cases/
│   ├── widget/payment_result_cancel_test.dart (✅)
│   └── maestro/201_party_join_invalid_code_dead_end.yaml (✅)
└── scripts/
    └── run_widget_tests.sh            # Test runner
```

---

## 💡 Key Insights

### What's Working Well

✅ Watch section (Scripture clips)
✅ Bible section (People's Open Bible)
✅ Moments section (groups discovery)
✅ Community page (groups discovery)
✅ Existing QA infrastructure (316 Maestro flows)

### What's Broken

🔴 **Critical:** Payment failure paths (0% coverage)
🔴 **Critical:** Deep-link invalid handling (0% coverage)
🔴 **Critical:** Session expiry mid-action (1% coverage)
🟡 **High:** Network resilience (1% coverage)
🟡 **Medium:** UX inconsistencies (Groups 404, Messages copy)

### Why It Matters

1. **Payment failure = revenue loss** — untested cancel paths
2. **Deep-link invalid = user confusion** — no error states
3. **Session expiry = data loss** — no mid-action recovery
4. **Network drop = feature broken** — LiveKit calls fail
5. **UX inconsistency = user friction** — Groups 404 fallback

---

## 📋 Next: Await Opus

When the background delegation completes, we'll have:

- ✅ Comprehensive TEST_STRATEGY.md
- ✅ All identified broken flows documented
- ✅ Prioritized test roadmap (Phase 1/2/3)
- ✅ Effort estimates per test
- ✅ Test authoring examples
- ✅ Ready to delegate test authoring

**Then:**
1. Review with Zack
2. Create sprint plan
3. Assign test authoring to Sonnet (coding model)
4. Track implementation in GitHub

---

**Status:** Phase 0 (documentation) → Phase 0.5 (Opus analysis) → Phase 1 (test implementation)

**Questions?** See `docs/INDEX.md` or `docs/CONTRIBUTION.md`
