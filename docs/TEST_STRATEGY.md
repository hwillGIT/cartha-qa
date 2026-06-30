# Cartha QA Test Strategy

**Status:** Comprehensive analysis complete (Opus deep-dive)  
**Date:** 2026-06-30  
**Broken Flows Identified:** 11  
**Critical Gaps:** 3 HIGH + 5 MEDIUM + 3 LOW

---

## Executive Summary

Cartha.com (Flutter Web) has **11 identified broken user flows and exception handling gaps** across authentication, routing, resource validation, and navigation patterns. The app handles ~70% of flows well but has critical gaps in error states, invalid resource handling, and gated route redirects.

**Current Test Coverage:** 2 tests written
**Needed for Phase 1:** 5-8 critical tests
**Total Estimated:** 20-25 tests across all phases

---

## Broken Flows Matrix

| # | Flow | Severity | Steps to Reproduce | Expected | Actual | Root Cause | Test Type | Effort |
|---|------|----------|-------------------|----------|--------|-----------|-----------|--------|
| 1 | Groups 404 Fallback | 🟡 MEDIUM | Navigate `/groups/invalid-code` | "Group not found" error | Falls back to onboarding carousel | No group validation | Widget | 1 day |
| 2 | Invalid Routes Redirect | 🔴 HIGH | Access `/invalid-page` | 404 page in app | Redirects to `og.cartha.com` | Missing route catch-all | Integration | 2 days |
| 3 | Gated Routes Redirect Away | 🔴 HIGH | Access `/plan` (logged out) | Sign-in modal | Redirects to landing page | Auth check redirects | Integration | 2 days |
| 4 | Invalid Bible Book | 🟡 MEDIUM | Navigate `/bible/invalidbook/1` | "Book not found" | Loads default Bible silently | No book validation | Widget | 1 day |
| 5 | Meet Rooms Browse Dead-end | 🟡 MEDIUM | Navigate `/meet/rooms` | Show rooms list | Falls back to `/meet` home | Route not implemented | Widget | 2 days |
| 6 | Room Deep-link Silent Fallback | 🟡 MEDIUM | Access `/meet/room/test-room-id` | Load room or error | Silently returns to `/meet` | Room ID not validated | Integration | 2 days |
| 7 | Invalid Watch Category | 🟢 LOW | Access `/watch/invalid-category` | Error or redirect | Defaults silently | Invalid params ignored | Widget | 1 day |
| 8 | Invalid Moment ID | 🟡 MEDIUM | Access `/moments/invalid-moment-id` | "Moment not found" | Generic invite page | No data validation | Integration | 2 days |
| 9 | Meet Create Route Gated | 🔴 HIGH | Access `/meet/create` (logged out) | Sign-in modal | Falls back to home | Missing auth check | Integration | 2 days |
| 10 | Invalid Watch Clip ID | 🟡 MEDIUM | Access `/watch/clips/123` | Load clip or error | Defaults silently | Clip ID not validated | Integration | 2 days |
| 11 | Invalid Community Event | 🟢 LOW | Access `/community/invalid-event` | Error or filter | Ignores parameter | Event params not validated | Widget | 1 day |

---

## Working Flows (Verified ✅)

✅ **Watch page** - Categories work, content loads, swipe instructions clear  
✅ **Bible reader** - Search UI present, book navigation works, deep-links to chapters (`/bible/genesis/1`)  
✅ **Moments deep-link** - Proper landing page shown with context  
✅ **Invalid group join** - Shows "Room no longer available" with recovery path  
✅ **Messages onboarding** - Clear carousel explaining features  
✅ **Community page** - Events show, RSVP buttons visible  
✅ **Rapid navigation** - No crashes or race conditions  

---

## Phase 1: Critical Blockers (2-3 weeks)

### Priority 1.1: Auth Gating for Gated Routes
**Flows:** `/plan`, `/meet/create` (BUG #3, #9)  
**Issue:** Routes redirect to landing page instead of showing sign-in modal  
**Tests Needed:** 2 integration tests + 2 widget tests

**Test Cases:**
```
1. test_plan_route_gated_shows_signin_modal
   - Access /plan while logged out
   - Verify sign-in modal appears
   - User can authenticate
   - Redirects to /plan after auth

2. test_meet_create_route_gated_shows_signin_modal
   - Access /meet/create while logged out
   - Verify sign-in modal appears
   - User can authenticate
   - Redirects to /meet/create after auth
```

**Effort:** 2-3 days  
**Unlock:** Enables testing of gated features

---

### Priority 1.2: Invalid Route Handling (404 Page)
**Flow:** BUG #2 — `/invalid-page` redirects to domain  
**Issue:** No in-app 404 page; redirects entirely to landing page  
**Tests Needed:** 2 integration tests + 1 Maestro flow

**Test Cases:**
```
1. test_invalid_route_shows_404_page
   - Access /invalid-page, /nonexistent, /random
   - Verify 404 page shown in-app (not domain redirect)
   - "Go Home" button works
   - Breadcrumb/nav allows recovery

2. test_invalid_deep_links_show_error
   - Maestro flow: Access invalid deep-link
   - Verify error message or 404 shown
   - User can navigate back
```

**Effort:** 1-2 days  
**Unlock:** Prevents domain redirects for invalid routes

---

### Priority 1.3: Resource Validation (Groups, Rooms, Moments, Clips)
**Flows:** BUG #1, #6, #8, #10 — Invalid IDs show fallback  
**Issue:** Invalid resource IDs silently fallback to home/default  
**Tests Needed:** 4 integration tests + 2 Maestro flows

**Test Cases:**
```
1. test_group_invalid_code_shows_error_modal
   - Access /groups/INVALIDCODE
   - Verify "Group not found" modal appears (not carousel)
   - Error message clear
   - Can dismiss and return

2. test_room_invalid_id_shows_error
   - Access /meet/room/INVALIDID
   - Verify "Room not found" or error shown
   - Not silent fallback to home

3. test_moment_invalid_id_shows_error
   - Access /moments/INVALIDID
   - Verify "Moment not found" message
   - Not generic invite page

4. test_clip_invalid_id_shows_error
   - Access /watch/clips/INVALIDID
   - Verify error message or 404
   - Not silent default to feed
```

**Effort:** 3-4 days  
**Unlock:** Prevents silent fallbacks across 4 major features

---

## Phase 2: High-Severity Gaps (1-2 weeks)

### Priority 2.1: Route Parameter Validation
**Flows:** BUG #4, #7, #11 — Invalid params silently ignored  
**Issue:** Bible books, watch categories, community events not validated  
**Tests Needed:** 3 widget tests

```
1. test_invalid_bible_book_shows_error
2. test_invalid_watch_category_defaults_safely
3. test_invalid_community_event_handled_gracefully
```

**Effort:** 1-2 days

---

### Priority 2.2: Deep-Link Robustness
**Flows:** All routes with invalid IDs  
**Issue:** Deep-links fail silently when parameters are invalid  
**Tests Needed:** 3 Maestro flows + 2 integration tests

```
1. test_deep_link_valid_while_logged_out
2. test_deep_link_after_session_expiry
3. test_deep_link_invalid_code_shows_error
```

**Effort:** 2-3 days

---

### Priority 2.3: Meet Rooms Browse Implementation
**Flow:** BUG #5 — `/meet/rooms` falls back to home  
**Issue:** Route exists but not fully implemented  
**Tests Needed:** 2 widget tests + 1 Maestro flow (depends on implementation)

```
1. test_rooms_browse_page_loads
2. test_rooms_filtering_and_sorting
3. test_rooms_join_from_browse
```

**Effort:** 2-3 days (depends on code changes)

---

## Phase 3: Medium/Low-Priority (1 week)

- Empty state handling
- Edge cases (double-submit, rapid nav, token expiry)
- Back-button behavior from dead-ends
- Permission denial handling

---

## Test Implementation Roadmap

### Week 1 (Phase 1.1 + 1.2)
```
Mon: Auth gating tests (signin modals)
Tue: Invalid route 404 page tests
Wed: Resource validation tests (groups, rooms)
Thu: Test review + fixes
Fri: Merge and push to upstream
```

**Tests to Write:** 4-5 tests
**Tests to Validate:** Payment cancel + deep-link invalid (already written)

### Week 2 (Phase 1.3 + 2.1)
```
Mon: Moments + clips validation
Tue: Parameter validation (Bible, categories, events)
Wed: Integration testing
Thu-Fri: Buffer for fixes
```

**Tests to Write:** 3-4 tests

### Week 3 (Phase 2.2 + 2.3)
```
Deep-link robustness (Maestro)
Meet rooms browse (if code changes landed)
Final Phase 1 validation
```

**Tests to Write:** 3-4 tests

---

## Test Writing Patterns

### Widget Test Template (for error states)
```dart
void main() {
  group('Error Handling', () {
    testWidgets('Invalid group code shows error modal', (WidgetTester tester) async {
      // 1. Mock API to return 404 for invalid code
      // 2. Navigate to /groups/INVALID
      // 3. Verify error modal appears
      // 4. Verify error message is clear
      // 5. Verify dismiss button works
    });
  });
}
```

### Maestro Flow Template (for routing)
```yaml
appId: com.cartha.app
testID: test-invalid-deep-link

commands:
  - launchApp:
      clearState: true
      permissions:
        - calendar
        - contacts
  - openLink:
      url: "app://cartha.com/groups/INVALIDCODE"
  - assertVisible:
      text: "Group not found"
  - tapButton:
      id: "ErrorModal.dismiss"
  - assertVisible:
      text: "Messages"  # Back on home
```

### Integration Test Template
```dart
void main() {
  group('Integration: Resource Validation', () {
    testWidgets('Invalid room ID returns error', (WidgetTester tester) async {
      // 1. Mock API responses
      // 2. Navigate with invalid room ID
      // 3. Verify error handling
      // 4. Verify recovery path
    });
  });
}
```

---

## Test Authoring Guidelines

### When to Use Each Test Type

| Type | When | Speed | Isolation | Cost |
|------|------|-------|-----------|------|
| **Widget** | Error states, UI rendering, small logic | ⚡ Fast | High | Low |
| **Maestro** | Full flows, navigation, deep-links | 🐢 Slow | Medium | Medium |
| **Integration** | API mocks, cross-feature, state | 🐢 Slow | Low | Medium |

### Key Patterns for Cartha

1. **Always test both logged-in and logged-out** for gated routes
2. **Validate route parameters** before rendering
3. **Show contextual error messages**, not silent fallbacks
4. **Test deep-links** from external source, while logged out, with stale tokens
5. **Test back-button** from each route (should go to previous, not home)
6. **Test empty states** with helpful UX

---

## Success Criteria

### Phase 1 Complete ✅
- [ ] 5-8 critical tests written + passing
- [ ] All 3 HIGH-severity bugs have test coverage
- [ ] Tests documented and reviewable
- [ ] Ready to copy to upstream (cartha.ai.mobile)

### Phase 2 Complete ✅
- [ ] All MEDIUM-severity bugs have tests
- [ ] Deep-link robustness verified
- [ ] Parameter validation tested

### Phase 3 Complete ✅
- [ ] Edge cases covered
- [ ] Empty states tested
- [ ] 20-25 total tests in repo

---

## Next Steps

1. **Review this strategy** with Zack
   - Confirm bugs are real (not intended behavior)
   - Agree on Phase 1 priorities
   - Decide: implement fixes or just test them?

2. **Assign test writing**
   - Delegate to Sonnet (coding model) for implementation
   - Use Maestro/widget test patterns provided above

3. **Track progress**
   - Create GitHub issues for each test
   - Use kanban board to track sprint

4. **Copy to upstream**
   - Once passing locally, copy to cartha.ai.mobile
   - Create PR with evidence + reproduction steps

---

## Summary of Findings

**Total Broken Flows:** 11  
**Critical (Blocker):** 3 — Auth gating, invalid routes, resource validation  
**High-Severity:** 5 — Deep-links, parameter validation, rooms browse  
**Low-Severity:** 3 — Edge cases, empty states  

**Current Test Coverage:** 2 tests (payment cancel, deep-link invalid)  
**Phase 1 Goal:** 5-8 tests for blockers  
**Total Needed:** 20-25 tests across all phases  

**Zack's Preferences Met:**
- ✅ Lightweight, focused tests (not full QA sweep)
- ✅ Blockers prioritized first
- ✅ Clear effort estimates
- ✅ Actionable test patterns ready

---

**Status:** Analysis complete, roadmap clear, ready to implement.

Next: Review with Zack, assign test writing, track progress in GitHub.
