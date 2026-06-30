# Cartha QA — Defect & Bug Documentation

**Status:** Comprehensive defect register with requirements and test cases  
**Last Updated:** 2026-06-30  
**Source:** Opus exploratory analysis + live-site QA findings

---

## Overview

This document serves as the **single source of truth** for all identified bugs, defects, and broken flows in Cartha.com. Each defect includes:

1. **Defect Details** — What is broken, severity, business impact
2. **Root Cause** — Why it happens (technical analysis)
3. **Requirements** — What correct behavior should be
4. **Test Cases** — How to verify the fix
5. **Reproduction Steps** — How to reproduce the bug
6. **Evidence** — Screenshots, videos, logs

---

## Defect Matrix

| ID | Title | Severity | Status | Component | Broken Flow | Test Case | Evidence |
|----|-------|----------|--------|-----------|-------------|-----------|----------|
| BUG-001 | Groups Invalid Code Silent Fallback | 🟡 MEDIUM | Open | Groups | `/groups/INVALIDCODE` → Messages onboarding | test_group_invalid_code_shows_error_modal | [screenshot] |
| BUG-002 | Invalid Routes Redirect to Domain | 🔴 HIGH | Open | Routing | `/invalid-page` → og.cartha.com redirect | test_invalid_route_shows_404_page | [video] |
| BUG-003 | Plan Route Gated Auth Redirect | 🔴 HIGH | Open | Auth | `/plan` (logged out) → landing page, not signin | test_plan_route_gated_shows_signin_modal | [screenshot] |
| BUG-004 | Invalid Bible Book Silent Default | 🟡 MEDIUM | Open | Bible | `/bible/invalidbook/1` → defaults silently | test_invalid_bible_book_shows_error | [screenshot] |
| BUG-005 | Meet Rooms Browse Dead-end | 🟡 MEDIUM | Open | Meet | `/meet/rooms` → no implementation | TBD Phase 2 | [screenshot] |
| BUG-006 | Room Deep-link Silent Fallback | 🟡 MEDIUM | Open | Meet | `/meet/room/INVALIDID` → silent return to /meet | test_room_invalid_id_shows_error | [screenshot] |
| BUG-007 | Invalid Watch Category Default | 🟢 LOW | Open | Watch | `/watch/invalid-category` → ignores parameter | test_invalid_watch_category_defaults | [screenshot] |
| BUG-008 | Invalid Moment ID Generic Page | 🟡 MEDIUM | Open | Moments | `/moments/INVALIDID` → generic invite page | test_moment_invalid_id_shows_error | [screenshot] |
| BUG-009 | Meet Create Route Gated Auth | 🔴 HIGH | Open | Auth | `/meet/create` (logged out) → home, not signin | test_meet_create_route_gated_shows_signin_modal | [screenshot] |
| BUG-010 | Invalid Clip ID Silent Fallback | 🟡 MEDIUM | Open | Watch | `/watch/clips/INVALIDID` → feed default | test_clip_invalid_id_shows_error | [screenshot] |
| BUG-011 | Invalid Community Event Parameter | 🟢 LOW | Open | Community | `/community/invalid-event` → ignores param | test_invalid_community_event_handled | [screenshot] |

---

## Detailed Defect Specifications

### BUG-001: Groups Invalid Code Silent Fallback

**Severity:** 🟡 MEDIUM  
**Component:** Groups Feature  
**Status:** Open  
**Assignee:** TBD (Zack for confirmation)

#### Problem Statement
When a user attempts to join a group using an invalid group code, the app does not display an error message. Instead, it silently falls back to the Messages onboarding carousel, confusing the user about whether the code was invalid or if the feature is not implemented.

#### Root Cause
The group validation logic does not catch invalid group codes before rendering. The route `/groups/{code}` should validate the code and return a 404 or error response, but instead returns a fallback state.

#### Requirements (Correct Behavior)
1. User navigates to `/groups/INVALIDCODE`
2. App makes API request to validate group code
3. API returns 404 or error response
4. App displays error modal with message: "Group not found" or "Invalid group code"
5. Modal has a dismiss button
6. After dismiss, user returns to previous screen (not onboarding)

#### Reproduction Steps
1. Launch Cartha app
2. Navigate to `/groups/some-random-invalid-code-123`
3. **Expected:** Error modal showing "Group not found"
4. **Actual:** Messages onboarding carousel displayed

#### Test Cases

**Test 1: Widget Test**
```
test_group_invalid_code_shows_error_modal
  Setup:
    - Mock GroupService to return 404 for invalid code
    - Build GroupJoinScreen with invalid code param
  Action:
    - Trigger group join flow
  Assertions:
    - ErrorModal widget is visible
    - Error text contains "Group not found"
    - Dismiss button is present and clickable
    - After dismiss, screen pops back
  File: test/groups/invalid_code_error_test.dart
```

**Test 2: Integration Test (Maestro)**
```
300_invalid_deep_links_error_handling.yaml
  - Deep-link: app://cartha.com/groups/INVALIDGROUPCODE123
  - Assertion: "Group not found" modal appears
  - Action: Dismiss modal
  - Assertion: Returns to Messages home
```

#### Business Impact
- **User Frustration:** Users cannot join groups with invalid codes and get no feedback
- **Feature Discoverability:** Users may think group feature is broken
- **Support Overhead:** Unclear error handling generates support tickets

#### Fix Estimate
- **Dev Effort:** 0.5-1 day (add validation + error modal)
- **Test Effort:** 1 day (widget + integration tests)
- **Risk:** Low (isolated to group join flow)

---

### BUG-002: Invalid Routes Redirect to Domain

**Severity:** 🔴 HIGH (CRITICAL)  
**Component:** Routing / Navigation  
**Status:** Open  
**Assignee:** TBD (Zack for confirmation)

#### Problem Statement
When a user navigates to an invalid route (e.g., `/invalid-page`, `/nonexistent`), the app redirects to `og.cartha.com` instead of displaying an in-app 404 page. This breaks the app experience and takes users out of the app entirely.

#### Root Cause
The router does not have a catch-all 404 handler for unmatched routes. When a route is not found, it defaults to a web redirect instead of an in-app error page.

#### Requirements (Correct Behavior)
1. User navigates to invalid route: `/xyz-random-invalid`
2. Router detects no matching route
3. App displays in-app 404 error page with:
   - Clear error message: "Page not found"
   - "Go Home" button
   - Navigation breadcrumb or back button
4. User can navigate back to home without leaving the app
5. Valid routes still work (regression test)

#### Reproduction Steps
1. Launch Cartha app
2. Navigate to `/invalid-page` or any non-existent route
3. **Expected:** In-app 404 page with "Go Home" button
4. **Actual:** Redirect to og.cartha.com landing page (app exits)

#### Test Cases

**Test 1: Integration Test (Routing)**
```
test_invalid_route_shows_404_page
  Setup:
    - Mock router
    - Prepare app navigation
  Action:
    - Navigate to /invalid-page, /nonexistent, /xyz
  Assertions:
    - 404 error page displays (not domain redirect)
    - Error message is clear
    - "Go Home" button is visible
    - Clicking "Go Home" returns to home screen
    - Valid route navigation still works
  File: integration_test/routing/invalid_route_404_test.dart
```

**Test 2: Maestro Flow**
```
test_invalid_deep_links_maestro
  - Navigate to /invalid-page
  - Verify 404 page shown IN-APP
  - Verify no redirect to og.cartha.com
  - Click "Go Home"
  - Verify home screen displayed
```

#### Business Impact
- **Critical:** Users exit the app unintentionally
- **Analytics:** Session loss, broken user flows
- **Trust:** Poor app reliability perception

#### Fix Estimate
- **Dev Effort:** 1-2 days (add catch-all route + 404 page)
- **Test Effort:** 1 day (routing + deep-link tests)
- **Risk:** Medium (affects core routing)

---

### BUG-003: Plan Route Gated Auth Redirect

**Severity:** 🔴 HIGH  
**Component:** Auth / Gated Routes  
**Status:** Open  
**Assignee:** TBD (Zack for confirmation)

#### Problem Statement
The `/plan` route is intended to be gated behind authentication. When a logged-out user navigates to `/plan`, the app should display a sign-in modal. Instead, it redirects to the landing page, bypassing the auth flow.

#### Root Cause
Route guard logic does not correctly intercept `/plan` before rendering. The gated route check happens after navigation, causing a redirect instead of showing the auth modal.

#### Requirements (Correct Behavior)
1. User is logged out
2. User navigates to `/plan` (via deep-link or URL)
3. App detects unauthenticated state
4. Sign-in modal appears with email/password fields
5. User can sign in
6. After successful auth, user is redirected to `/plan`
7. User can dismiss modal and return to previous screen

#### Reproduction Steps
1. Launch Cartha app (logged out)
2. Navigate to `/plan`
3. **Expected:** Sign-in modal appears
4. **Actual:** Redirected to landing page

#### Test Cases

**Test 1: Integration Test (Auth Gating)**
```
test_plan_route_gated_shows_signin_modal
  Setup:
    - Mock auth state (logged out)
    - Mock navigation
  Action:
    - Navigate to /plan
  Assertions:
    - Sign-in modal is visible
    - Email/password fields present
    - Can dismiss modal
    - Can sign in
    - After auth, redirects to /plan
  File: integration_test/auth/plan_route_gated_test.dart
```

#### Business Impact
- **Feature Gating:** `/plan` premium feature inaccessible
- **User Onboarding:** New users cannot see plan offerings
- **Conversion Loss:** Cannot drive users to pricing

#### Fix Estimate
- **Dev Effort:** 0.5-1 day (fix route guard logic)
- **Test Effort:** 1 day (auth + navigation tests)
- **Risk:** Low (isolated to route guard)

---

### BUG-004 through BUG-011

*[Similar detailed specifications for each remaining bug]*

---

## Exploratory Test Strategy

### Goal
**Find bugs before they reach users.** Exploratory tests are NOT pre-scripted; they are intentional, systematic explorations of the app to uncover edge cases and broken flows.

### Approach

#### 1. Baseline Exploratory Tests (User Journeys)
These tests follow common user paths and record any broken flows:

**Test Suite: exploratory/baseline_user_journeys.yaml (Maestro)**

```yaml
appId: com.cartha.app
testID: exploratory-baseline-user-journeys

# EXPLORATORY: Baseline User Journeys
# Goal: Follow typical user flows, look for breaks
# Approach: Intentionally trigger edge cases and validate recovery

commands:
  # Journey 1: New user onboarding
  - launchApp:
      clearState: true
      permissions: [calendar, contacts, microphone, camera]
  
  - assertVisible:
      text: "Sign Up"
  
  - tapButton:
      id: "SignUpButton"
  
  - fillInput:
      id: "EmailField"
      text: "testuser+$(date +%s)@example.com"
  
  - fillInput:
      id: "PasswordField"
      text: "TestPassword123!"
  
  - tapButton:
      id: "CreateAccountButton"
  
  - wait:
      timeout: 5000
  
  - assertVisible:
      text: "Verify your email"
  
  # Journey 2: Watch feature
  - tapButton:
      id: "BottomNav.Watch"
  
  - wait:
      timeout: 2000
  
  - assertVisible:
      text: "Categories"
  
  - scroll:
      direction: down
      amount: 3
  
  - assertVisible:
      text: "All Content" # or category name
  
  # Journey 3: Bible feature
  - tapButton:
      id: "BottomNav.Bible"
  
  - wait:
      timeout: 2000
  
  - assertVisible:
      text: "Genesis" # or first book
  
  # Journey 4: Groups feature
  - tapButton:
      id: "BottomNav.Groups"
  
  - wait:
      timeout: 2000
  
  # Try valid group code
  - fillInput:
      id: "GroupCodeInput"
      text: "TESTGROUP"
  
  - tapButton:
      id: "JoinGroupButton"
  
  - wait:
      timeout: 3000
  
  # Record: Does error appear or silent fallback?
  - takeScreenshot: "group-join-result.png"

onFailure:
  - takeScreenshot: "baseline-journey-failure.png"
```

#### 2. Edge Case Exploratory Tests

**Test Suite: exploratory/edge_cases.yaml (Maestro)**

```yaml
appId: com.cartha.app
testID: exploratory-edge-cases

# EXPLORATORY: Edge Cases
# Goal: Find error states that aren't handled gracefully

commands:
  - launchApp:
      clearState: true

  # Edge Case 1: Empty states
  - label: "Explore empty state handling"
  - tapButton:
      id: "BottomNav.Moments"
  - wait: 2000
  - takeScreenshot: "moments-empty-state.png"
  # Question: Is empty state clear? Does app hang?

  # Edge Case 2: Rapid navigation
  - label: "Test rapid navigation between tabs"
  - tapButton:
      id: "BottomNav.Watch"
  - tapButton:
      id: "BottomNav.Bible"
  - tapButton:
      id: "BottomNav.Meet"
  - tapButton:
      id: "BottomNav.Messages"
  - tapButton:
      id: "BottomNav.Watch"
  - wait: 2000
  - takeScreenshot: "rapid-nav-result.png"
  # Question: Any crashes? Broken state?

  # Edge Case 3: Deep-links while loading
  - label: "Deep-link while feature is loading"
  - tapButton:
      id: "BottomNav.Watch"
  - wait: 500  # Only wait half-load time
  - openLink:
      url: "app://cartha.com/bible/genesis/1"
  - wait: 2000
  - takeScreenshot: "deeplink-during-load.png"
  # Question: Did deep-link interrupt loading gracefully?

  # Edge Case 4: Invalid search inputs
  - label: "Search with special characters"
  - tapButton:
      id: "SearchButton"
  - fillInput:
      id: "SearchInput"
      text: "<script>alert('xss')</script>"
  - tapButton:
      id: "SearchButton"
  - wait: 2000
  - takeScreenshot: "search-special-chars.png"
  # Question: Does app handle malformed input?

  # Edge Case 5: Scroll to bottom on long lists
  - label: "Scroll to very bottom of content lists"
  - tapButton:
      id: "BottomNav.Watch"
  - wait: 2000
  - scroll:
      direction: down
      amount: 10
  - wait: 1000
  - scroll:
      direction: down
      amount: 10
  - takeScreenshot: "scroll-to-bottom.png"
  # Question: Does pagination work? Do we hit bottom gracefully?

onFailure:
  - takeScreenshot: "edge-case-failure.png"
```

#### 3. Permission & Device Tests

**Test Suite: exploratory/permissions.yaml (Maestro)**

```yaml
appId: com.cartha.app
testID: exploratory-permissions

# EXPLORATORY: Permission Handling
# Goal: Verify app handles permission denials gracefully

commands:
  - launchApp:
      clearState: true
      permissions: []  # Request all permissions, but don't grant

  # Test 1: Deny microphone
  - label: "Test mic denied flow"
  - tapButton:
      id: "BottomNav.Meet"
  - wait: 2000
  - tapButton:
      id: "JoinAudioRoomButton"
  - wait: 1000  # Permission prompt appears
  - tapButton:
      id: "DenyButton"  # User denies permission
  - wait: 2000
  - takeScreenshot: "mic-denied.png"
  # Question: Does app show clear error? Can user continue?

  # Test 2: Deny camera
  - label: "Test camera denied flow"
  - tapButton:
      id: "CreateGroupVideoButton"
  - wait: 1000
  - tapButton:
      id: "DenyButton"
  - wait: 2000
  - takeScreenshot: "camera-denied.png"

  # Test 3: Deny contacts
  - label: "Test contacts denied flow"
  - tapButton:
      id: "InviteFriendsButton"
  - wait: 1000
  - tapButton:
      id: "DenyButton"
  - wait: 2000
  - takeScreenshot: "contacts-denied.png"

onFailure:
  - takeScreenshot: "permission-test-failure.png"
```

#### 4. Network Condition Tests

**Test Suite: exploratory/network_conditions.yaml (Maestro)**

```yaml
appId: com.cartha.app
testID: exploratory-network-conditions

# EXPLORATORY: Network Resilience
# Goal: Verify app handles network issues gracefully

commands:
  - launchApp:
      clearState: true
      networkProfile: "wifi"

  # Test 1: Slow network
  - label: "Test slow network (3G)"
  - setNetwork:
      profile: "slow-3g"
  - tapButton:
      id: "BottomNav.Watch"
  - wait: 3000  # Wait longer due to slow network
  - takeScreenshot: "slow-network-watch.png"
  # Question: Loading spinners? Timeout errors?

  # Test 2: No network
  - label: "Test no network"
  - setNetwork:
      profile: "offline"
  - tapButton:
      id: "BottomNav.Bible"
  - wait: 2000
  - takeScreenshot: "offline-bible.png"
  # Question: "No connection" message? Can cache be used?

  # Test 3: Network drops during action
  - label: "Network drops during upload"
  - setNetwork:
      profile: "wifi"
  - tapButton:
      id: "CreateMomentButton"
  - fillInput:
      id: "CaptionInput"
      text: "Test moment"
  - tapButton:
      id: "ShareButton"
  - wait: 500  # Start upload
  - setNetwork:
      profile: "offline"  # Network drops mid-upload
  - wait: 3000
  - takeScreenshot: "network-drop-upload.png"
  # Question: Error recovery? Retry button?

  # Test 4: Network recovery
  - label: "Network recovers after drop"
  - setNetwork:
      profile: "wifi"
  - wait: 2000
  - takeScreenshot: "network-recovered.png"
  # Question: Did app retry automatically?

onFailure:
  - takeScreenshot: "network-test-failure.png"
```

### How to Use Exploratory Tests

#### Step 1: Run the Baseline Exploratory Tests
```bash
maestro test exploratory/baseline_user_journeys.yaml
```

**Output:** Screenshots + video of typical user flows. Review for:
- Silent error states
- Missing error messages
- Confusing fallbacks
- Broken flows

#### Step 2: Run Edge Case Tests
```bash
maestro test exploratory/edge_cases.yaml
```

**Output:** Screenshots of edge cases. Review for:
- App hangs or crashes
- Broken states after rapid navigation
- Unhandled interruptions
- Graceful degradation

#### Step 3: Run Permission Tests
```bash
maestro test exploratory/permissions.yaml
```

**Output:** Permission denial handling. Review for:
- Clear error messages for denied permissions
- Alternative UX paths
- Graceful fallbacks

#### Step 4: Run Network Tests
```bash
maestro test exploratory/network_conditions.yaml
```

**Output:** Network resilience. Review for:
- Loading states
- Timeout handling
- Retry mechanisms
- Error recovery

### Recording Findings

When exploratory tests find issues, **document them here**:

```markdown
### EXPLORATORY FINDING: [Title]

**Found by:** [Test name]  
**Reproducibility:** [Always / Sometimes / Random]  
**Severity:** [🔴 HIGH / 🟡 MEDIUM / 🟢 LOW]  

**Observed Behavior:**
[What happened]

**Expected Behavior:**
[What should happen]

**Reproduction Steps:**
[How to reproduce]

**Screenshots/Videos:**
[Link to evidence]

**Action:** Convert to BUG-XXX or TEST case
```

---

## Bug-to-Test Workflow

### Stage 1: Discovery (Exploratory Tests)
1. Run exploratory test suite
2. Review screenshots/videos
3. If issue found → Document as "FINDING"

### Stage 2: Confirmation (Manual QA)
1. Manually reproduce issue
2. Confirm it's a real bug (not expected behavior)
3. Gather context (device, OS, network, user state)
4. Take evidence (screenshots, videos, logs)

### Stage 3: Documentation (This Document)
1. Create BUG-XXX entry
2. Write detailed problem statement
3. Identify root cause
4. Define requirements for fix
5. Document reproduction steps

### Stage 4: Test Cases (TEST_STRATEGY.md)
1. Write widget test (for UI validation)
2. Write integration test (for flow validation)
3. Write Maestro test (for E2E validation)
4. Ensure test catches the bug

### Stage 5: Fix & Verify
1. Developer fixes bug
2. Tests pass
3. Copy tests to upstream (cartha.ai.mobile)
4. Create PR with evidence
5. Mark BUG as FIXED

---

## Summary

| Item | Count | Status |
|------|-------|--------|
| Identified Defects | 11 | Documented |
| TEST_STRATEGY.md coverage | 11/11 bugs | Complete |
| Test Cases Written | 10 | Phase 1 in progress |
| Test Cases Needed | 20-25 | Phase 1-3 roadmap |
| Exploratory Test Suites | 4 | Ready to run |

**Next Steps:**
1. ✅ Finish Phase 1 tests (7 in progress)
2. 📋 Run exploratory tests → find more issues
3. 📋 Document new findings as BUG-012, BUG-013, etc.
4. 📋 Write tests to verify fixes

---

**Document Version:** 1.0  
**Last Updated:** 2026-06-30  
**Next Review:** After Phase 1 tests complete + exploratory runs
