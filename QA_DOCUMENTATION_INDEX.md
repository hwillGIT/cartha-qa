# Cartha QA — Complete Documentation Index

**Last Updated:** 2026-06-30  
**Status:** Comprehensive QA framework in progress  
**Purpose:** Single source of truth for all QA-related documentation

---

## 📚 Documentation Structure

### Phase 0: Foundation Documents (Define WHAT Should Happen)

#### 1. **COMPLETE_FLOW_SPECIFICATIONS.md** ⭐
**Purpose:** Business analyst specs for ALL features  
**Contains:** 50+ detailed UI flows with step-by-step instructions

| Feature | Flows | Routes |
|---------|-------|--------|
| Authentication | 6 | /auth/signup, /signin, /forgot-password, /verify, /reset |
| Watch | 3 | /watch, /watch/video/{id}, /watch/search, /watch/clips/{id} |
| Bible | 4 | /bible, /bible/{book}, /bible/{book}/{chapter}, /bookmarks |
| Groups | 4 | /groups, /groups/{id}, /groups/join, /groups/create |
| Meet | 4 | /meet, /meet/create, /meet/rooms, /meet/room/{id} |
| Moments | 3 | /moments, /moments/create, /moments/{id} |
| Messages | 3 | /messages, /messages/{user_id}, /messages/compose |
| Navigation | 3 | BottomNav, Deep-linking, Error handling |

**Key Sections:**
- Entry points (how users get to each flow)
- Screen layouts (what components are visible)
- User actions (step-by-step walkthrough)
- Validation rules (real-time feedback)
- API calls (success/failure scenarios)
- Error handling (what errors users see)
- Edge cases (empty states, permissions, offline)

**How to Use:**
1. Developer: Reference before building feature
2. QA: Write test cases from these specs
3. Product: Validate app matches intended design

---

### Phase 1: Issue Documentation (Define What's BROKEN)

#### 2. **DEFECTS_AND_REQUIREMENTS.md** 🐛
**Purpose:** Register of all identified bugs with detailed specs  
**Contains:** 11 confirmed broken flows + exploratory test suites

**Defect Matrix:**
| ID | Title | Severity | Component | Test Case |
|----|-------|----------|-----------|-----------|
| BUG-001 | Groups Invalid Code Silent Fallback | 🟡 MEDIUM | Groups | test_group_invalid_code_shows_error_modal |
| BUG-002 | Invalid Routes Redirect to Domain | 🔴 HIGH | Routing | test_invalid_route_shows_404_page |
| BUG-003 | Plan Route Gated Auth Redirect | 🔴 HIGH | Auth | test_plan_route_gated_shows_signin_modal |
| BUG-004 | Invalid Bible Book Silent Default | 🟡 MEDIUM | Bible | test_invalid_bible_book_shows_error |
| BUG-005 | Meet Rooms Browse Dead-end | 🟡 MEDIUM | Meet | Phase 2 test |
| BUG-006 | Room Deep-link Silent Fallback | 🟡 MEDIUM | Meet | test_room_invalid_id_shows_error |
| BUG-007 | Invalid Watch Category Default | 🟢 LOW | Watch | test_invalid_watch_category |
| BUG-008 | Invalid Moment ID Generic Page | 🟡 MEDIUM | Moments | test_moment_invalid_id_shows_error |
| BUG-009 | Meet Create Route Gated Auth | 🔴 HIGH | Auth | test_meet_create_route_gated_shows_signin_modal |
| BUG-010 | Invalid Clip ID Silent Fallback | 🟡 MEDIUM | Watch | test_clip_invalid_id_shows_error |
| BUG-011 | Invalid Community Event Parameter | 🟢 LOW | Community | test_invalid_community_event |

**Each BUG Entry Includes:**
- Problem statement
- Root cause analysis
- Requirements (correct behavior)
- Reproduction steps
- Test cases (unit/integration/E2E)
- Business impact
- Fix effort estimate

**Exploratory Test Suites:**
- `exploratory/01_baseline_user_journeys.yaml` — Follow typical user paths
- `exploratory/02_edge_cases.yaml` — Push app to limits
- `exploratory/03_permissions.yaml` — Permission denial handling
- `exploratory/04_network_conditions.yaml` — Network resilience

**How to Use:**
1. QA: Run exploratory tests to confirm bugs
2. Developer: Use as spec for fixing issues
3. Product: Track bug status and priorities

---

### Phase 2: Test Strategy & Planning (Define How to VERIFY)

#### 3. **TEST_STRATEGY.md** 📋
**Purpose:** Comprehensive test plan for verifying all identified bugs  
**Contains:** 11 broken flows × 9 attributes + implementation roadmap

**Broken Flows Matrix:**
- **BUG #** | **Flow** | **Severity** | **Reproduction Steps** | **Expected Behavior** | **Actual Behavior** | **Root Cause** | **Test Type** | **Effort**

**Test Implementation Roadmap:**

```
PHASE 1 (Weeks 1-3): Critical Blockers
  Week 1: Auth gating tests (signin modals)
  Week 2: Invalid route 404 + Resource validation (groups, rooms)
  Week 3: Maestro E2E + review

  Tests: 8 total (2 existing + 1 Maestro + 5 new)

PHASE 2 (Weeks 4-5): High-Severity Gaps
  - Parameter validation (Bible, categories, events)
  - Deep-link robustness (logged out, stale tokens)
  - Meet rooms browse implementation
  
  Tests: +6 new

PHASE 3 (Week 6+): Medium/Low Priority
  - Empty states
  - Edge cases (double-submit, rapid nav)
  - Permission denial handling
  - Back-button behavior
  
  Tests: +8-10 new
```

**Success Criteria Per Phase:**
- Phase 1: 8 tests written + passing, all HIGH-severity covered
- Phase 2: All MEDIUM-severity covered, deep-link robustness verified
- Phase 3: Edge cases tested, 20-25 total tests complete

**How to Use:**
1. QA: Create test cases from this roadmap
2. Developers: Know which areas need coverage
3. Project manager: Track test progress

---

#### 4. **TEST_WRITING_ROADMAP.md** 🗺️
**Purpose:** Detailed execution plan for writing test cases  
**Contains:** Weekly breakdown, file organization, assignment options

**Timeline Breakdown:**

```
WEEK 1:
  Mon-Tue: Auth gating (2 tests)
  Wed: Invalid routes 404 (1 test)
  Thu-Fri: Review & fixes

WEEK 2:
  Mon-Tue: Groups + Room validation (2 tests)
  Wed: Moments + Clips validation (2 tests)
  Thu-Fri: Maestro E2E flow

WEEK 3:
  Mon-Tue: All tests passing locally
  Wed-Thu: Copy to upstream
  Fri: Phase 1 complete 🎉
```

**File Organization:**
```
test/                          # Widget tests
  ├── groups/invalid_code_error_test.dart (NEW)
  ├── watch/invalid_category_test.dart (Phase 2)
  └── bible/invalid_book_test.dart (Phase 2)

integration_test/              # Integration tests
  ├── auth/plan_route_gated_test.dart (NEW)
  ├── meet/invalid_room_test.dart (NEW)
  ├── moments/invalid_moment_test.dart (NEW)
  ├── watch/invalid_clip_test.dart (NEW)
  └── routing/invalid_route_404_test.dart (NEW)

test-cases/maestro/            # Maestro E2E flows
  ├── 300_invalid_deep_links_error_handling.yaml (NEW)
  ├── 301_deep_link_robustness.yaml (Phase 2)
  └── 302_auth_gating_flows.yaml (Phase 2)
```

**Assignment Options:**
1. **Delegate to Sonnet (Coding Model)** — batch parallel writing
2. **Manual Writing** — copy templates and implement
3. **Batch Parallel** — assign multiple tests to subagents

**How to Use:**
1. QA: Follow weekly breakdown to plan sprints
2. Developers: Know which tests are coming
3. Team lead: Track test writing progress

---

### Phase 3: Live App Analysis (Find What's ACTUALLY BROKEN)

#### 5. **OPUS_EXPLORATORY_FINDINGS.md** 🔍 (In Progress)
**Purpose:** Real-world app exploration results  
**Status:** Opus is currently analyzing the live app systematically

**Expected Contents:**
- ✅ Confirmed bugs (with evidence)
- ✅ Working flows (regression validation)
- ✅ Additional issues found (not in original 11)
- ✅ Edge cases discovered
- ✅ Screenshots/evidence of each finding

**How to Use:**
1. QA: Compare expected specs vs. actual app behavior
2. Product: Prioritize bug fixes
3. Developers: Use as comprehensive specification

---

## 🎯 Complete Workflow

### Step 1: Understand Intended Behavior
```
Read: COMPLETE_FLOW_SPECIFICATIONS.md
Output: Know what SHOULD happen for each feature/flow
```

### Step 2: Identify Issues
```
Read: DEFECTS_AND_REQUIREMENTS.md
Run: Exploratory test suites (Maestro)
Review: OPUS_EXPLORATORY_FINDINGS.md (when complete)
Output: Catalog of ALL bugs + evidence
```

### Step 3: Plan Tests
```
Read: TEST_STRATEGY.md
Read: TEST_WRITING_ROADMAP.md
Output: Know which tests to write + timeline
```

### Step 4: Write Tests
```
Reference: TEST_WRITING_ROADMAP.md (file organization, templates)
Delegate: To Sonnet or write manually
Implement: Widget / Integration / Maestro tests
Output: Test cases that catch bugs
```

### Step 5: Verify App
```
Run: flutter test (all tests)
Run: maestro test (E2E flows)
Check: GitHub Actions CI/CD
Output: Confirmation of working/broken flows
```

### Step 6: Document Results
```
Mark: Bugs as CONFIRMED or WORKING
Create: GitHub issues for fixes
Copy: Tests to upstream (cartha.ai.mobile)
Output: PR with evidence + test cases
```

---

## 📊 Current Status

### Documentation Complete ✅
- [x] COMPLETE_FLOW_SPECIFICATIONS.md — 50+ flows defined
- [x] DEFECTS_AND_REQUIREMENTS.md — 11 bugs documented + exploratory strategy
- [x] TEST_STRATEGY.md — Test roadmap + broken flows matrix
- [x] TEST_WRITING_ROADMAP.md — Weekly timeline + file organization
- [ ] OPUS_EXPLORATORY_FINDINGS.md — Live app analysis (in progress)

### Tests Written ✅
- [x] 2 existing tests (payment_cancel, party_join_invalid)
- [x] 1 Maestro test (300_invalid_deep_links_error_handling.yaml)
- [ ] 7 Phase 1 tests (in progress from Sonnet delegation — interrupted)

### CI/CD Setup ✅
- [x] GitHub Actions (LIVE, tests auto-run on push/PR)
- [x] GitLab CI (READY, awaiting repo mirror)
- [x] Test coverage reports

### Ready for Next Phase
- [ ] Opus exploratory findings (waiting for completion)
- [ ] Confirm bugs with Zack (real vs. intended behavior)
- [ ] Re-assign test writing to Sonnet (with Opus findings)
- [ ] Implement Phase 1 tests + Phase 2 specs

---

## 🚀 Next Immediate Actions

### 1. WAIT FOR OPUS ANALYSIS (Currently Running)
Opus is exploring cartha.com systematically. When complete:
- ✅ Real bugs confirmed with evidence
- ✅ Additional issues discovered
- ✅ Comprehensive finding report

### 2. REVIEW OPUS FINDINGS WITH ZACK
Share OPUS_EXPLORATORY_FINDINGS.md:
- Confirm which bugs are real (vs. intended design)
- Prioritize fixes
- Clarify ambiguous behaviors

### 3. RE-ASSIGN TEST WRITING (After Opus + Zack Confirmation)
- Create corrected task list based on Opus findings
- Delegate to Sonnet in parallel batches
- Reference COMPLETE_FLOW_SPECIFICATIONS.md for expected behavior

### 4. TRACK PROGRESS
- GitHub issues for each test
- Kanban board (to-do, in-progress, done)
- Daily standup on blocked tests

### 5. VALIDATE & COPY TO UPSTREAM
- All tests passing locally (flutter test)
- GitHub Actions shows green
- Copy tests to cartha.ai.mobile/
- Create PR with evidence

---

## 📁 Repository Structure

```
~/dev/cartha-qa/
│
├── docs/
│   ├── COMPLETE_FLOW_SPECIFICATIONS.md      ⭐ Business specs (50+ flows)
│   ├── DEFECTS_AND_REQUIREMENTS.md          🐛 Bug register + exploratory tests
│   ├── TEST_STRATEGY.md                     📋 Test roadmap + broken flows matrix
│   ├── TEST_AUTHORING_GUIDELINES.md         📖 Pattern templates
│   ├── QA_FINDINGS.md                       📸 Live-site findings (7 items)
│   ├── BROKEN_FLOWS_SUMMARY.md              📝 Overview of confirmed issues
│   ├── EXCEPTION_FLOW_GAP_MATRIX.md         🗂️ Coverage analysis (11 flows)
│   └── OPUS_EXPLORATORY_FINDINGS.md         🔍 (In progress)
│
├── test/                                   # Widget tests
│   ├── groups/
│   │   └── invalid_code_error_test.dart    (⏳ Phase 1)
│   ├── watch/
│   │   └── invalid_category_test.dart      (⏳ Phase 2)
│   └── bible/
│       └── invalid_book_test.dart          (⏳ Phase 2)
│
├── integration_test/                       # Integration tests
│   ├── auth/
│   │   ├── plan_route_gated_test.dart      (⏳ Phase 1)
│   │   └── meet_create_gated_test.dart     (⏳ Phase 1)
│   ├── routing/
│   │   └── invalid_route_404_test.dart     (⏳ Phase 1)
│   ├── meet/
│   │   └── invalid_room_test.dart          (⏳ Phase 1)
│   ├── moments/
│   │   └── invalid_moment_test.dart        (⏳ Phase 1)
│   └── watch/
│       └── invalid_clip_test.dart          (⏳ Phase 1)
│
├── test-cases/maestro/                     # Maestro E2E flows
│   ├── 201_party_join_invalid_code_dead_end.yaml (✅ Done)
│   ├── 300_invalid_deep_links_error_handling.yaml (✅ Done)
│   ├── 301_deep_link_robustness.yaml       (⏳ Phase 2)
│   └── 02_edge_cases.yaml                  (⏳ Exploratory)
│
├── test-cases/exploratory/                 # Exploratory tests
│   ├── 01_baseline_user_journeys.yaml      (✅ Ready)
│   ├── 02_edge_cases.yaml                  (✅ Ready)
│   ├── 03_permissions.yaml                 (⏳ Ready to write)
│   └── 04_network_conditions.yaml          (⏳ Ready to write)
│
├── .github/workflows/
│   └── test.yml                            (✅ GitHub Actions LIVE)
│
├── .gitlab-ci.yml                          (🟡 Ready, awaiting mirror)
│
├── CI_CD_DUAL_SETUP.md                     (📖 Setup guide)
├── GITHUB_GITLAB_CI_SETUP_COMPLETE.md      (✅ Status summary)
├── PHASE_2_TESTS_READY.md                  (📋 Phase 2 specs)
├── TEST_WRITING_ROADMAP.md                 (🗺️ Timeline)
│
├── README.md                               (📖 Project overview)
├── CONTRIBUTION.md                         (📖 Contributing guide)
├── SETUP.md                                (⚙️ Environment setup)
└── QA_DOCUMENTATION_INDEX.md               (📚 This file)
```

---

## 📞 Quick Reference

### "What should this flow do?"
→ Read **COMPLETE_FLOW_SPECIFICATIONS.md**

### "What's broken in the app?"
→ Read **DEFECTS_AND_REQUIREMENTS.md** or wait for **OPUS_EXPLORATORY_FINDINGS.md**

### "How do I write tests?"
→ Read **TEST_STRATEGY.md** + **TEST_WRITING_ROADMAP.md** + **TEST_AUTHORING_GUIDELINES.md**

### "What tests need to be written?"
→ Check **TEST_WRITING_ROADMAP.md** (file organization + weekly breakdown)

### "How is CI/CD set up?"
→ Read **CI_CD_DUAL_SETUP.md** or **GITHUB_GITLAB_CI_SETUP_COMPLETE.md**

### "What's the current project status?"
→ Check **Current Status** section above

---

## 🎓 Key Principles

1. **Specs First** — Define WHAT should happen before testing IF it does
2. **Real Exploration** — Use Opus to actually navigate the app (not guesses)
3. **Evidence-Based** — Document bugs with screenshots/videos
4. **Comprehensive** — Cover all flows (happy path + errors + edge cases)
5. **Automated** — GitHub Actions runs tests automatically
6. **Iterative** — Phase 1 → Phase 2 → Phase 3 (blockers first)

---

## 📈 Progress Tracking

| Item | Status | Completion |
|------|--------|-----------|
| Flow Specifications (COMPLETE_FLOW_SPECIFICATIONS.md) | ✅ Complete | 100% |
| Bug Documentation (DEFECTS_AND_REQUIREMENTS.md) | ✅ Complete | 100% |
| Test Strategy (TEST_STRATEGY.md) | ✅ Complete | 100% |
| Test Roadmap (TEST_WRITING_ROADMAP.md) | ✅ Complete | 100% |
| Opus Live App Analysis (OPUS_EXPLORATORY_FINDINGS.md) | ⏳ In Progress | 0% |
| Test Cases Written | 🟡 Partial | 10% (2/20 done) |
| Phase 1 Tests | ⏳ Pending | 0% (7 tasks interrupted) |
| Phase 2 Tests | 📋 Specs Ready | 0% |
| Phase 3 Tests | 📋 Specs Ready | 0% |
| GitHub Actions CI | ✅ Live | 100% |
| GitLab CI Setup | 🟡 Ready | 100% (awaiting mirror) |

---

**Version:** 1.0  
**Last Updated:** 2026-06-30 02:30 EDT  
**Audience:** QA Team, Developers, Product Management  
**Next Review:** After Opus exploratory findings complete
