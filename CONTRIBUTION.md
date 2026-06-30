# Contributing to Cartha QA

This guide covers how to add tests, run the harness, and submit findings.

## Before You Start

1. **Read the gap matrix** — `docs/EXCEPTION_FLOW_GAP_MATRIX.md` shows which areas have zero/thin coverage
2. **Understand the upstream repo** — clone [zackseyun/cartha.ai.mobile](https://github.com/zackseyun/cartha.ai.mobile) (separate from this repo)
3. **Set up Flutter 3.41.6** — see `docs/SETUP.md`
4. **Run codegen** — Flutter projects with `@freezed` / `build_runner` need this before tests compile

## Writing Widget Tests

### Pattern

Widget tests in the upstream repo follow this structure:

```dart
import 'package:carthaai/screens/some_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('SomeScreen', () {
    testWidgets('description of what is tested', (WidgetTester tester) async {
      // Setup
      await tester.pumpWidget(
        MaterialApp(
          home: SomeScreen(...),
          onGenerateRoute: (settings) => MaterialPageRoute(
            builder: (_) => const Scaffold(body: Text('STUB')),
            settings: settings,
          ),
        ),
      );
      await tester.pump();

      // Act
      await tester.tap(find.byType(ElevatedButton));
      await tester.pump();

      // Assert
      expect(find.byType(SuccessWidget), findsOneWidget);
    });
  });
}
```

### Guidelines

- **Test exception flows first** — unhappy paths are where gaps hide
- **Use actual widget strings** — read the source screen to assert against real text, not guesses
- **Mock network/services only when needed** — prefer pure UI state tests
- **Name tests by behavior** — `"payment cancel shows no-charge message"`, not `"test 1"`
- **Document gap source** — why is this test needed? Link to `EXCEPTION_FLOW_GAP_MATRIX.md`

### Checklist

- [ ] Test compiles (`flutter test test/your_test.dart`)
- [ ] Test passes green
- [ ] Asserts against real widget strings from source
- [ ] Gap documented in commit message and test comments
- [ ] Follows existing test conventions (no new patterns)

## Writing Maestro E2E Flows

### Pattern

Maestro flows are YAML with a config header + command list, separated by `---`:

```yaml
appId: com.cartha.app
tags:
  - your-feature
  - qa
  - regression
  - exception-flow
---
# Exception-flow coverage for [what is tested].
#
# Gap: [link to EXCEPTION_FLOW_GAP_MATRIX.md]
# Precondition: [what state the app must be in]

- launchApp:
    stopApp: true

- waitForAnimationToEnd:
    timeout: 15000

- assertVisible: "Expected Text"
- assertNotVisible: "Should Not Be There"

- tapOn: "Button Label"
- waitForAnimationToEnd:
    timeout: 6000

- takeScreenshot: "flow_name_state_description"
```

### Guidelines

- **Naming** — `NNN_description.yaml` (e.g., `201_party_join_invalid_code_dead_end.yaml`)
- **Numbering** — use the next available number from `.maestro/flows/` in upstream repo
- **Tags** — include `qa`, `exception-flow`, `regression`, and feature tag
- **Documentation** — every flow needs a comment explaining the gap it covers
- **Preconditions** — explicitly document what state is needed (signed in? guest? with a token?)
- **Screenshots** — use `takeScreenshot` at key decision points for evidence

### Checklist

- [ ] Flow number is next available (grep highest in `.maestro/flows/`)
- [ ] YAML is valid (no multi-doc `---` errors when run through `maestro validate`)
- [ ] Gap is documented in comments + commit message
- [ ] Follows naming/tagging conventions
- [ ] Uses `waitForAnimationToEnd` for async operations
- [ ] Takes screenshots for evidence

### Note on qa_sweep

The upstream repo has an **automated qa_sweep** script, but **Zack has opted out** (see `CLAUDE.md`). Do **not** run `./scripts/qa_sweep.sh` unless explicitly requested. Instead:

- Validate flows locally with `maestro validate <flow.yaml>`
- Test on an emulator/device manually before committing
- Or submit as a PR and let upstream CI validate

## Submitting Findings

### Live-Site QA Reports

When you explore cartha.com and find bugs/dead-ends:

1. **Screenshot everything** — save to `findings/screenshots/`
2. **Document steps** — how to reproduce (URL, actions, state)
3. **Capture error text** — console logs, API errors, UI error messages
4. **Categorize** — is this groups? auth? negative space? (see gap matrix categories)
5. **Add to findings/report.md** — structure:

```markdown
## [Category] — [Title]

**Severity:** High / Medium / Low

**URL/Flow:** 
- Start at: [URL or screen]
- Actions: [steps to reproduce]

**Evidence:**
- Screenshot: `screenshots/[name].png`
- Error: [error text]
- Network: [API response, if relevant]

**Root Cause Hypothesis:**
[What you think is broken]

**Recommendation:**
[How to fix]
```

6. **Commit with evidence** — `git add findings/` + commit with detailed message
7. **PR or notify** — link findings in a PR or message

## Running Tests Locally

### Widget Tests

```bash
cd ~/dev/projects-cartha/cartha.ai.mobile

# Single test file
flutter test test/payment_result_cancel_test.dart

# All widget tests
flutter test

# With verbose output
flutter test -v

# Coverage report
flutter test --coverage
```

### Maestro Flows

```bash
# Validate flow YAML
maestro validate .maestro/flows/201_party_join_invalid_code_dead_end.yaml

# Run on emulator (requires active emulator + flow setup)
maestro test .maestro/flows/201_party_join_invalid_code_dead_end.yaml

# See maestro docs for device/auth setup
```

### Static Analysis

```bash
cd ~/dev/projects-cartha/cartha.ai.mobile

# Lint check
flutter analyze

# Format check
flutter format --line-length 80 test/your_test.dart
```

## Codegen Setup (Critical)

The upstream repo uses `build_runner` for `@freezed` code generation. If tests fail with "method 'map' isn't defined", codegen is missing:

```bash
cd ~/dev/projects-cartha/cartha.ai.mobile

# Codegen in packages/core
cd packages/core
dart run build_runner build --delete-conflicting-outputs

# Codegen in features/chat
cd ../..
cd features/chat
dart run build_runner build --delete-conflicting-outputs
```

## Commit Message Format

```
type(scope): subject

body

Refs: [gap or issue]
```

Examples:

```
test(payment): add cancel-flow widget tests

Add 3 widget tests for PaymentResultScreen cancel path to cover
the zero-coverage gap identified in EXCEPTION_FLOW_GAP_MATRIX.md:
- cancel shows "Payment Cancelled" message
- continue button escapes to root
- tier purchase never falsely claims "activated" on cancel

Refs: EXCEPTION_FLOW_GAP_MATRIX.md#payment-fail--cancel
```

```
test(deep-link): add invalid party code Maestro flow

Add 201_party_join_invalid_code_dead_end.yaml to test the
signed-in dead-end when a user joins an expired/missing party code.
Gap: EXCEPTION_FLOW_GAP_MATRIX.md#deep-link-404--invalid-route

Preconditions:
- User signed in (QA token)
- App cold-started onto /join/QA-MISSING-PARTY

Refs: EXCEPTION_FLOW_GAP_MATRIX.md
```

## Questions?

See `docs/SETUP.md` for environment help, or check the gap matrix for what to test next.
