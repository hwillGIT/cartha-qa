# How to Use COMPLETE_FLOW_SPECIFICATIONS.md to Write Tests

**For:** Test Authors, QA Engineers, Developers writing test cases  
**Purpose:** Bridge specs → tests (every test validates a specific requirement)  
**Approach:** Spec-driven test writing (requirements first)

---

## The Workflow

```
1. Read COMPLETE_FLOW_SPECIFICATIONS.md
   ↓
2. Find the flow you're testing
   ↓
3. Extract requirements from the flow
   ↓
4. Write test that validates each requirement
   ↓
5. For bugs: test should catch the bug (assertion fails on current broken code)
   ↓
6. For features: test should pass when feature is complete
```

---

## Example 1: Testing Groups Join (Invalid Code Error)

### Step 1: Read the Spec

**From COMPLETE_FLOW_SPECIFICATIONS.md → GF-3: Join Group (by Code)**

```
2. Screen layout:
   - Header: "Join a Group"
   - Text: "Ask your group leader for the group code."
   - Group code input field (placeholder: "Enter code")
   - "Join" button (disabled until valid code entered)
   - "Discover Groups" button

3. User enters group code
   → Validation: code format (alphanumeric, case-insensitive)
   → Real-time validation: code length check
   → If invalid format: "Invalid code format"

4. User taps "Join"
   → Loading: "Joining group..." spinner
   → API call: POST /groups/join with {code}
   
   **Failure (404):**
   → Error: "Group code not found"
   → Sub-message: "Check the code and try again"
   → Retry button
```

### Step 2: Extract Requirements

```
REQ-1: Join Group screen displays with correct fields
  - Email/text input labeled "Enter code"
  - "Join" button (disabled initially)
  - Placeholder text "Enter code"

REQ-2: Real-time validation
  - Code must be alphanumeric
  - If invalid format: error message below field
  - "Join" button disabled until valid format

REQ-3: Submit with valid code
  - User taps "Join"
  - Loading spinner shows "Joining group..."
  - API call sent

REQ-4: Handle 404 (CRITICAL BUG TO TEST)
  - API returns 404
  - Error modal appears (NOT silent fallback)
  - Error message: "Group code not found"
  - Sub-message: "Check the code and try again"
  - User can retry or dismiss

REQ-5: Deep-linking
  - URL: /groups/join?code=GROUPCODE works
  - If already member: show "Already a member" message
```

### Step 3: Write Test

```dart
// test/groups/invalid_code_error_test.dart
// BUG-001: Groups Invalid Code Silent Fallback

void main() {
  group('GF-3: Join Group (Invalid Code) - BUG-001', () {
    
    testWidgets('REQ-4: 404 Error Shows Modal (Not Silent Fallback)', 
      (WidgetTester tester) async {
      
      // Setup: Mock API to return 404
      final mockClient = MockHttpClient();
      when(mockClient.post(
        Uri.parse('https://api.cartha.com/groups/join'),
        body: jsonEncode({'code': 'INVALIDCODE'})
      )).thenAnswer((_) async => http.Response('{"error": "not found"}', 404));
      
      // REQ-1: Render Join Group screen
      await tester.pumpWidget(
        createApp(httpClient: mockClient)
      );
      
      // Navigate to /groups/join
      await tester.tap(find.byText('Join a Group'));
      await tester.pumpAndSettle();
      
      // Verify screen shows input field
      expect(find.byType(TextField), findsOneWidget);
      expect(find.byText('Enter code'), findsOneWidget);
      
      // REQ-2: Enter invalid code, button disabled
      await tester.enterText(find.byType(TextField), 'INVALID@CODE');
      await tester.pumpAndSettle();
      expect(find.byType(ElevatedButton), findsOne);
      
      // Button should be disabled (invalid format)
      final button = find.byType(ElevatedButton);
      expect(tester.widget<ElevatedButton>(button).onPressed, isNull);
      
      // REQ-3: Enter valid code, button enabled
      await tester.enterText(find.byType(TextField), 'VALIDCODE123');
      await tester.pumpAndSettle();
      expect(tester.widget<ElevatedButton>(button).onPressed, isNotNull);
      
      // REQ-4: Tap join, handle 404 error
      await tester.tap(button);
      
      // REQ-3: Loading spinner should show
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
      expect(find.byText('Joining group...'), findsOneWidget);
      
      // API call fails with 404
      await tester.pumpAndSettle();
      
      // BUG-001 FIX: Error modal appears (not silent fallback)
      expect(
        find.byType(AlertDialog),
        findsOneWidget,
        reason: 'Error modal should appear for 404 (not silent fallback)'
      );
      
      // REQ-4: Error message correct
      expect(find.byText('Group code not found'), findsOneWidget);
      expect(
        find.byText('Check the code and try again'),
        findsOneWidget
      );
      
      // Buttons to retry/dismiss
      expect(find.byText('Try Again'), findsOneWidget);
      expect(find.byText('Dismiss'), findsOneWidget);
      
      // REQ-5 (bonus): User can retry
      await tester.tap(find.byText('Try Again'));
      await tester.pumpAndSettle();
      expect(find.byType(TextField), findsOneWidget);
    });
  });
}
```

### Step 4: What This Test Validates

✅ **REQ-1** — Join screen displays correctly  
✅ **REQ-2** — Real-time validation (invalid format disables button)  
✅ **REQ-3** — User can submit and API is called  
✅ **REQ-4** — **404 ERROR SHOWS MODAL (catches BUG-001)**  
✅ **REQ-5** — Error can be dismissed and user can retry  

**On Current Broken Code:** Test FAILS (no modal, silent fallback instead)  
**After Fix:** Test PASSES (modal shows correctly)

---

## Example 2: Testing Invalid Routes (404)

### Step 1: Read the Spec

**From COMPLETE_FLOW_SPECIFICATIONS.md → NF-3: Error Handling**

```
**Invalid Routes:**
  User navigates to /invalid-route
  → Show in-app 404 page:
    - Title: "Page not found"
    - Description: "We couldn't find that page."
    - Image/icon: 404 illustration
    - Button: "Go Home"
  → NOT redirect to domain
```

### Step 2: Extract Requirements

```
REQ-1: Invalid route displays 404 IN-APP (not redirect to domain)
REQ-2: 404 page shows:
  - Title: "Page not found"
  - Description: "We couldn't find that page."
  - Illustration/icon
  - "Go Home" button
REQ-3: "Go Home" button navigates to home screen
REQ-4: Valid routes still work (regression)
```

### Step 3: Write Integration Test

```dart
// integration_test/routing/invalid_route_404_test.dart
// BUG-002: Invalid Routes Redirect to Domain

void main() {
  group('NF-3: Invalid Routes Show 404 - BUG-002', () {
    
    testWidgets('REQ-1: Invalid route /invalid-page shows 404 in-app',
      (WidgetTester tester) async {
      
      final appTest = AppTest();
      await appTest.pumpApp(tester);
      
      // Navigate to invalid route
      await tester.tap(find.byIcon(Icons.search));
      await tester.enterText(find.byType(TextField), '/invalid-page');
      await tester.sendKeyEvent(LogicalKeyboardKey.enter);
      await tester.pumpAndSettle();
      
      // BUG-002 FIX: 404 page shows IN-APP (not domain redirect)
      expect(
        find.byType(Uri(path: '/invalid-page')),
        findsNothing,
        reason: 'Should not navigate to actual /invalid-page'
      );
      
      // REQ-1 & REQ-2: 404 page displays with correct content
      expect(find.byType(NotFoundPage), findsOneWidget);
      expect(find.byText('Page not found'), findsOneWidget);
      expect(find.byText("We couldn't find that page."), findsOneWidget);
      expect(find.byIcon(Icons.error_outline), findsOneWidget);
      
      // REQ-3: Go Home button
      expect(find.byText('Go Home'), findsOneWidget);
      
      // REQ-3: Button navigates home
      await tester.tap(find.byText('Go Home'));
      await tester.pumpAndSettle();
      
      expect(find.byType(HomePage), findsOneWidget);
    });
    
    testWidgets('REQ-4: Valid routes still work (regression)',
      (WidgetTester tester) async {
      
      final appTest = AppTest();
      await appTest.pumpApp(tester);
      
      // Test several valid routes
      final validRoutes = [
        '/watch',
        '/bible/genesis',
        '/groups',
        '/meet',
        '/moments',
        '/messages',
      ];
      
      for (final route in validRoutes) {
        // Navigate to valid route
        await appTest.navigateTo(tester, route);
        
        // Should NOT show 404
        expect(
          find.byType(NotFoundPage),
          findsNothing,
          reason: 'Valid route $route should not show 404'
        );
        
        // Should show expected feature page
        expect(find.byType(FeaturePage), findsWidgets);
      }
    });
  });
}
```

---

## Example 3: Testing Gated Routes (Auth)

### Step 1: Read the Spec

**From COMPLETE_FLOW_SPECIFICATIONS.md → NF-2: Deep-Linking**

```
**Deep-Link Behavior:**

IF user not logged in:
  → Show sign-in screen
  → On successful sign-in: navigate to deep-link destination

IF deep-link is gated (e.g., /plan, /meet/create):
  → If not logged in: show sign-in modal
  → If logged in: check permissions
  → If allowed: navigate to content
  → If not allowed: show error
```

### Step 2: Extract Requirements

```
REQ-1: /plan route is gated (requires authentication)
REQ-2: When logged out, /plan shows signin modal (not redirect)
REQ-3: Modal has email/password fields
REQ-4: User can dismiss modal
REQ-5: After signin, user redirected to /plan
REQ-6: When logged in, /plan shows content (not signin modal)
```

### Step 3: Write Integration Test

```dart
// integration_test/auth/plan_route_gated_test.dart
// BUG-003: Plan Route Gated Auth Redirect (Not Modal)

void main() {
  group('AF-1+NF-2: Gated Route /plan Shows Signin Modal - BUG-003', () {
    
    testWidgets('REQ-2,3,4: Logged out user sees signin modal',
      (WidgetTester tester) async {
      
      final app = AppTest(isLoggedIn: false);
      await app.pumpApp(tester);
      
      // REQ-1: /plan is gated
      // Navigate to /plan while logged out
      await tester.press.navigateToDeepLink('/plan');
      await tester.pumpAndSettle();
      
      // BUG-003 FIX: Signin modal appears (not redirect to landing)
      expect(
        find.byType(SigninModal),
        findsOneWidget,
        reason: 'Gated route /plan should show signin modal when logged out'
      );
      
      // REQ-3: Modal has auth fields
      expect(find.byType(EmailField), findsOneWidget);
      expect(find.byType(PasswordField), findsOneWidget);
      
      // REQ-4: User can dismiss
      await tester.tap(find.byIcon(Icons.close));
      await tester.pumpAndSettle();
      
      // Should dismiss modal
      expect(find.byType(SigninModal), findsNothing);
      
      // REQ-4: User can cancel and go back
      expect(find.byType(LandingPage), findsOneWidget);
    });
    
    testWidgets('REQ-5: After signin, user redirected to /plan',
      (WidgetTester tester) async {
      
      final app = AppTest(isLoggedIn: false);
      await app.pumpApp(tester);
      
      // Navigate to /plan
      await tester.press.navigateToDeepLink('/plan');
      await tester.pumpAndSettle();
      
      // Signin modal shown
      expect(find.byType(SigninModal), findsOneWidget);
      
      // Enter email
      await tester.enterText(
        find.byType(EmailField),
        'user@example.com'
      );
      
      // Enter password
      await tester.enterText(
        find.byType(PasswordField),
        'password123'
      );
      
      // Submit
      await tester.tap(find.byText('Sign In'));
      
      // Loading spinner
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
      
      // Wait for API response
      await tester.pumpAndSettle();
      
      // REQ-5: After signin, user is on /plan (not back at landing)
      expect(find.byType(PlanPage), findsOneWidget);
      expect(find.byType(SigninModal), findsNothing);
    });
    
    testWidgets('REQ-6: Logged in user sees /plan content',
      (WidgetTester tester) async {
      
      final app = AppTest(isLoggedIn: true);
      await app.pumpApp(tester);
      
      // Navigate to /plan while logged in
      await tester.press.navigateToDeepLink('/plan');
      await tester.pumpAndSettle();
      
      // REQ-6: Should show content (not signin modal)
      expect(find.byType(PlanPage), findsOneWidget);
      expect(find.byType(SigninModal), findsNothing);
    });
  });
}
```

---

## How to Map Specs to Tests

### For Feature Flows (Happy Path)

| Spec Section | Test Type | What to Validate |
|--------------|-----------|-----------------|
| Entry Point | Integration | Can navigate to this screen |
| Screen Layout | Widget | All required fields present |
| User Actions (Steps) | Widget | Each action updates state correctly |
| Validation Rules | Widget | Real-time feedback shown |
| API Calls (Success) | Integration | API called with correct params, response handled |
| Edge Cases | Widget | Empty states, disabled buttons, etc. |

### For Bug Fixes

| From DEFECTS_AND_REQUIREMENTS.md | Test Type | What to Validate |
|----------------------------------|-----------|-----------------|
| OBSERVED (buggy behavior) | Integration | Show that current code exhibits bug |
| EXPECTED (correct behavior) | Widget + Integration | Assert correct behavior after fix |
| REPRODUCTION STEPS | Test setup | These become test steps 1-N |
| ROOT CAUSE | Test comment | Document WHY the bug existed |
| TEST CASES | Test name | Reference BUG-001, BUG-002, etc. |

---

## Test Naming Convention

```
test_{feature}_{flow}_{requirement}.dart

Examples:
  test_groups_join_invalid_code_shows_error.dart
  test_plan_route_gated_shows_signin_modal.dart
  test_invalid_route_shows_404_in_app.dart
  test_moment_detail_invalid_id_shows_error.dart
  test_bible_invalid_book_shows_error.dart
```

---

## Checklist: Before Writing a Test

- [ ] Read the relevant section in COMPLETE_FLOW_SPECIFICATIONS.md
- [ ] Extract all requirements (REQ-1, REQ-2, etc.)
- [ ] If testing a bug: Read DEFECTS_AND_REQUIREMENTS.md BUG-XXX section
- [ ] Know the test file path (from TEST_WRITING_ROADMAP.md)
- [ ] Know the test type: Widget / Integration / Maestro
- [ ] Write test name following convention (test_{feature}_{flow}_{req}.dart)
- [ ] Each assertion should validate one requirement
- [ ] Each bug test should FAIL on broken code, PASS when fixed
- [ ] Include comments linking to COMPLETE_FLOW_SPECIFICATIONS.md
- [ ] Include comments linking to DEFECTS_AND_REQUIREMENTS.md (if bug fix)

---

## Quick Reference: Spec → Test

**You have:**
```
COMPLETE_FLOW_SPECIFICATIONS.md (specs for what should happen)
DEFECTS_AND_REQUIREMENTS.md (what's broken + what the fix should do)
TEST_STRATEGY.md (which tests to write, in what order)
TEST_WRITING_ROADMAP.md (where test files go)
```

**You do:**
```
1. Read spec for the feature/bug
2. Extract requirements (REQ-1, REQ-2, etc.)
3. Write test that validates each requirement
4. For bugs: test catches the bug (fails on broken code)
5. Reference specs in test comments (documentation)
6. Save in correct directory (from TEST_WRITING_ROADMAP.md)
7. Run: flutter test <path/to/test.dart>
```

**You get:**
```
✅ Test that validates spec
✅ Bug fix that makes test pass
✅ Regression protection (test stays in repo forever)
✅ Evidence (test code shows what was broken, how it's fixed)
```

---

**Document Version:** 1.0  
**Last Updated:** 2026-06-30  
**Audience:** Test Authors, QA Engineers, Developers
