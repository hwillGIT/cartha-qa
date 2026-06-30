# Cartha Test Strategy — Test Authoring Guidelines

**Status:** Foundational guidelines (awaiting Opus full strategy)

**Purpose:** Provide test authors with proven patterns for cartha.com test coverage

---

## Test Types & When to Use

### 1. Widget Tests (Dart)

**When:** Testing isolated screen logic, state transitions, user interactions

**Example:** `payment_result_cancel_test.dart` (3 tests for payment cancel screen)

**Structure:**
```dart
testWidgets('description', (WidgetTester tester) async {
  // 1. Build the widget with mocks
  await tester.pumpWidget(
    MaterialApp(home: PaymentResultScreen(...))
  );
  
  // 2. Interact
  await tester.tap(find.byIcon(Icons.close));
  await tester.pumpAndSettle();
  
  // 3. Assert
  expect(find.byType(HomeScreen), findsOneWidget);
});
```

**Advantages:**
- Fast (no device needed)
- Isolatable (mock dependencies)
- Good for state/UI logic

**Challenges:**
- Can't test device permissions
- Can't test network conditions
- Can't test LiveKit/real RTC

**Cartha Patterns:**
- Mock `Preferences()` for auth state
- Mock `GoRouter` for navigation
- Use `MockSpec` for API responses

---

### 2. Maestro Flows (YAML)

**When:** Testing end-to-end user journeys, navigation, multi-screen flows

**Example:** `201_party_join_invalid_code_dead_end.yaml` (deep-link invalid code)

**Structure:**
```yaml
appId: com.cartha.app
tags: [qa, regression, exception-flow]
---
- runFlow: flows/common/login.yaml  # Reuse login setup
- tapOn:
    text: "Browse Rooms"
- inputText: invalid-code
- tap: Join
- assertVisible:
    text: "Party not found"
- tap: "Go Back"
- assertVisible:
    text: "Community"  # Back to community screen
```

**Advantages:**
- Real app (no mocks)
- Multi-screen flows
- Device automation (taps, gestures)
- Fast execution (Maestro is efficient)

**Challenges:**
- Can't test permission denial (needs app-level mocking)
- Can't simulate network loss (no network-level control)
- Can't mock API responses directly

**Cartha Patterns:**
- Subflows for common setup (login, create group, join call)
- Tags for categorization (qa, regression, exception-flow, payment, etc.)
- Assertions for dead-end verification

---

### 3. Integration Tests (Flutter)

**When:** Testing user flows that require device interaction + state verification

**Example:** Testing mic/camera permission denial during room entry

**Structure:**
```dart
void main() {
  testWidgets('deny camera permission → room with camera off', (WidgetTester tester) async {
    // 1. Mock permission denial
    MockPermissionHandler.denyPermission(Permission.camera);
    
    // 2. Pump app
    await tester.pumpWidget(CarthaApp());
    
    // 3. Navigate to room
    await tester.tap(find.byType(RoomJoinButton));
    await tester.pumpAndSettle();
    
    // 4. Verify camera unavailable UI
    expect(find.byType(CameraOffIndicator), findsOneWidget);
    expect(find.byType(VideoPreview), findsNothing);
  });
}
```

**Advantages:**
- Real app + mocked permissions
- Device permission testing
- State persistence between screens

**Challenges:**
- Requires test devices (iOS Simulator, Android Emulator)
- Slower than widget tests
- Network mocking limited

**Cartha Patterns:**
- Mock `PermissionHandler` for camera/mic
- Mock `LiveKit` for RTC interactions
- Test permission-denied → fallback UI transitions

---

## Cartha-Specific Test Patterns

### Pattern 1: Auth State Mocking

**Problem:** Many flows require logged-in state, but testing real auth is slow

**Solution:** Mock `Preferences` and `AuthService`

```dart
testWidgets('send message in group', (WidgetTester tester) async {
  // Mock logged-in user
  final mockAuth = MockAuthService();
  when(mockAuth.currentUser).thenReturn(
    User(id: 'test-user', email: 'test@cartha.com')
  );
  
  await tester.pumpWidget(
    CarthaApp(authService: mockAuth)
  );
});
```

### Pattern 2: Navigation State

**Problem:** Testing deep-links requires route validation

**Solution:** Use `GoRouter` assertion

```dart
testWidgets('invalid deep-link → 404 or home', (WidgetTester tester) async {
  await tester.pumpWidget(CarthaApp());
  
  // Simulate deep-link
  router.go('/party/invalid-code');
  await tester.pumpAndSettle();
  
  // Verify error or fallback
  expect(
    find.byType(PartyNotFoundScreen),
    findsOneWidget
  );
});
```

### Pattern 3: API Mock (Maestro)

**Problem:** Testing payment failure without real Stripe

**Solution:** Mock API responses via Maestro assertion

```yaml
- tapOn:
    text: "Purchase"
- assertVisible:
    text: "Card declined"  # API mocked to return error
- tap: "Try again"
- assertVisible:
    text: "Enter payment details"
```

### Pattern 4: LiveKit Mock (Widget Test)

**Problem:** Testing mid-call network drop requires live RTC

**Solution:** Mock `LiveKitClient` behavior

```dart
testWidgets('live call → network drop → reconnect', (WidgetTester tester) async {
  final mockLiveKit = MockLiveKitClient();
  
  // Simulate connection
  await tester.pumpWidget(VideoRoomScreen(liveKit: mockLiveKit));
  
  // Simulate disconnect
  mockLiveKit.simulateDisconnect();
  await tester.pump();
  
  // Verify recovery UI
  expect(find.byType(ReconnectingIndicator), findsOneWidget);
  
  // Simulate reconnect
  mockLiveKit.simulateReconnect();
  await tester.pumpAndSettle();
  
  // Verify video restored
  expect(find.byType(VideoPreview), findsOneWidget);
});
```

---

## Priority Framework

### Phase 1 (Critical — Block Release)

Tests for flows that:
- Cause data loss (session expiry without save)
- Lose revenue (payment without completion)
- User-facing crashes (404 without recovery)

**Examples:**
1. Payment cancel → proper error state
2. Deep-link invalid code → error page, not fallback
3. Session expires mid-message-send → saved draft or explicit fail

**Effort:** 2-3 weeks (10-15 tests)

**Test Types:** Maestro flows + widget tests (2 per flow for redundancy)

---

### Phase 2 (High — Next Sprint)

Tests for flows that:
- Impact feature reliability (network resilience)
- Affect accessibility (permission denial)
- Create user friction (double-submit races)

**Examples:**
1. Mid-call network drop → graceful recovery or clear error
2. Deny camera permission → audio-only fallback
3. Rapid join button taps → single join attempt

**Effort:** 1-2 weeks (8-10 tests)

**Test Types:** Maestro flows + integration tests

---

### Phase 3 (Nice-to-have — Future)

Tests for edge cases:
- Empty states (all sections)
- Banned user flows
- Auth gate fallbacks
- Analytics/instrumentation

**Effort:** 1 week (5-8 tests)

**Test Types:** Maestro flows

---

## Test Authoring Checklist

Before writing a test:

- [ ] Identify the broken flow (steps, expected, actual)
- [ ] Identify the test type (widget / Maestro / integration)
- [ ] Identify dependencies to mock (auth, API, permissions, LiveKit)
- [ ] Identify assertions (what should the user see/not see?)
- [ ] Identify edge cases (rapid interaction, state changes, errors)
- [ ] Run the test locally (--verify success)
- [ ] Add to cartha-qa and document in TEST_STRATEGY.md

---

## Running Tests

### Widget Tests

```bash
cd ~/dev/projects-cartha/cartha.ai.mobile
flutter test test/payment_result_cancel_test.dart -v
```

### Maestro Flows

```bash
cd ~/dev/projects-cartha/cartha.ai.mobile
maestro test .maestro/flows/201_party_join_invalid_code_dead_end.yaml
```

### All Tests

```bash
cd ~/dev/cartha-qa
./scripts/run_widget_tests.sh
```

---

## Example: Full Test Authoring (Session Expiry)

### 1. Identify the Broken Flow

**Scenario:** User is composing a message in a group when their session token expires.

**Steps:**
1. Log in to cartha.com
2. Open a group chat
3. Start typing a message
4. Session token expires (simulated)
5. Try to send the message

**Expected:** "Session expired, please sign in" error + draft saved or explicit failure

**Actual:** ??? (untested)

### 2. Choose Test Type

→ **Maestro flow** (full app flow) + **Widget test** (auth state transition)

### 3. Write Maestro Flow

```yaml
appId: com.cartha.app
tags:
  - exception-flow
  - session-expiry
  - messaging
---
- runFlow: flows/common/login.yaml
- tapOn:
    text: "Messages"
- tapOn:
    text: "Group Name"
- tapOn:
    id: "message_input"
- inputText: "Hello from Cartha"
- evalScript: |
    // Simulate session token expiry
    localStorage.removeItem('auth_token');
- tapOn:
    text: "Send"
- assertVisible:
    text: "Session expired"
```

### 4. Write Widget Test

```dart
testWidgets('send message with expired session → error', (WidgetTester tester) async {
  final mockAuth = MockAuthService();
  mockAuth.tokenExpiry = DateTime.now().subtract(Duration(hours: 1));
  
  await tester.pumpWidget(CarthaApp(authService: mockAuth));
  
  // Compose message
  await tester.tap(find.byType(MessageInput));
  await tester.enterText(find.byType(TextField), 'test message');
  
  // Attempt send (should fail)
  await tester.tap(find.byIcon(Icons.send));
  await tester.pumpAndSettle();
  
  // Verify error
  expect(find.byType(SessionExpiredDialog), findsOneWidget);
  expect(find.byType(SignInButton), findsOneWidget);
});
```

### 5. Document in TEST_STRATEGY.md

```markdown
| Flow | Test Type | Effort | Status |
|------|-----------|--------|--------|
| Send message with expired session | Maestro + Widget | Medium | Pending |
```

---

**Next:** Await Opus results for comprehensive TEST_STRATEGY.md with all identified flows and prioritized test plan.
