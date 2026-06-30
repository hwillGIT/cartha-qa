# Phase 2 Tests — Parameter Validation + Deep-Link Robustness

**Status:** Phase 1 in progress, Phase 2 ready to assign  
**Tests:** 6 tests (3 Widget + 2 Integration + 1 Maestro)  
**Timeline:** Weeks 4-5  
**Effort:** 1-2 weeks

---

## Phase 2.1: Parameter Validation (3 Widget Tests)

### Test 1: Invalid Bible Book Name

**BUG #4 from TEST_STRATEGY.md:** `/bible/invalidbook/1` silently loads default Bible view

**File:** `test/bible/invalid_book_name_test.dart`

**What to test:**
- Navigate to `/bible/invalidbookname/1`
- Verify error message appears (not silent default)
- Error says "Book not found" or "Invalid book name"
- User can dismiss and navigate back
- Valid book navigation still works (regression)

**Framework:** Widget test (WidgetTester)
**Dependencies:** Provider mocks, BibleService mock
**Effort:** 1 day

---

### Test 2: Invalid Watch Category

**BUG #7 from TEST_STRATEGY.md:** `/watch/invalid-category` defaults silently

**File:** `test/watch/invalid_category_test.dart`

**What to test:**
- Navigate to `/watch/invalid-category`
- Verify validation or error handling
- If default behavior intended, verify it doesn't show broken state
- Categories filter works for valid categories (regression)

**Framework:** Widget test
**Effort:** 1 day

---

### Test 3: Invalid Community Event Parameter

**BUG #11 from TEST_STRATEGY.md:** `/community/invalid-event` ignores parameter

**File:** `test/community/invalid_event_param_test.dart`

**What to test:**
- Navigate to `/community/invalid-event`
- Verify parameter validation
- Error message or graceful fallback if invalid
- Valid event parameters work (regression)

**Framework:** Widget test
**Effort:** 1 day

---

## Phase 2.2: Deep-Link Robustness (2 Integration + 1 Maestro)

### Test 4: Valid Deep-Links While Logged Out

**BUG #3 from TEST_STRATEGY.md:** Gated routes redirect to landing page

**File:** `integration_test/deep_links/valid_logged_out_test.dart`

**What to test:**
- User is logged out
- Access valid deep-links: `/bible/genesis/1`, `/watch/clips/xyz`, `/moments/closefriendsgroup`
- Each deep-link shows appropriate error or sign-in prompt (not domain redirect)
- User can sign in and view content
- After auth, deep-link resolves correctly

**Framework:** Integration test + API mocks
**Effort:** 2 days

---

### Test 5: Deep-Link After Session Expiry

**New flow:** User has valid token, deep-links while token expires mid-navigation

**File:** `integration_test/deep_links/stale_token_test.dart`

**What to test:**
- User is logged in
- API token set to expire mid-request
- Access deep-link (e.g., `/meet/room/xyz`)
- Verify app detects expired token
- Shows "Session expired" error or re-auth prompt (not crash)
- User can sign back in
- Deep-link resolves after re-auth

**Framework:** Integration test + API mock that returns 401/403
**Effort:** 2 days

---

### Test 6: Deep-Link Robustness (Maestro E2E)

**File:** `test-cases/maestro/301_deep_link_robustness.yaml`

**What to test (Maestro flow):**
1. User logged out → access valid deep-link → see sign-in
2. User logs in → deep-link resolves → content loads
3. Token expires mid-action → see "Session expired"
4. User re-authenticates → deep-link re-resolves
5. Back button from deep-linked page works
6. Multiple deep-links in sequence work correctly

**Framework:** Maestro YAML
**Effort:** 1-2 days

---

## File Organization (Phase 2)

```
test/
├── bible/
│   └── invalid_book_name_test.dart (NEW)
├── watch/
│   └── invalid_category_test.dart (NEW)
└── community/
    └── invalid_event_param_test.dart (NEW)

integration_test/
└── deep_links/
    ├── valid_logged_out_test.dart (NEW)
    └── stale_token_test.dart (NEW)

test-cases/maestro/
└── 301_deep_link_robustness.yaml (NEW)
```

---

## Success Criteria for Phase 2

- [ ] 3 parameter validation tests written + passing
- [ ] 2 deep-link integration tests written + passing
- [ ] 1 Maestro deep-link robustness flow written
- [ ] All 6 tests passing locally
- [ ] GitHub Actions shows green ✅
- [ ] Ready to copy to upstream

---

## Next Assignment

When Phase 1 completes, assign Phase 2 tests:

```bash
delegate_task(
  tasks=[
    {goal: "Write test_invalid_bible_book_name (Widget)"},
    {goal: "Write test_invalid_watch_category (Widget)"},
    {goal: "Write test_invalid_community_event_param (Widget)"},
    {goal: "Write test_valid_deep_links_logged_out (Integration)"},
    {goal: "Write test_deep_link_stale_token (Integration)"},
    {goal: "Write 301_deep_link_robustness.yaml (Maestro)"},
  ]
)
```

---

**Status:** Ready to assign after Phase 1 completes
**Total Phase 2 effort:** 1-2 weeks
