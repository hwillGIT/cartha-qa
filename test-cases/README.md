# Test Cases — Widget Tests & Maestro Flows

This directory contains new exception-flow tests authored to close zero-coverage gaps identified in `docs/EXCEPTION_FLOW_GAP_MATRIX.md`.

## Structure

```
.
├── widget/
│   └── payment_result_cancel_test.dart     # Widget tests for payment cancel/decline
└── maestro/
    └── 201_party_join_invalid_code_dead_end.yaml   # E2E flow for deep-link 404
```

## Contributing

See `../CONTRIBUTION.md` for guidelines on:
- Writing new widget tests
- Adding Maestro E2E flows
- Running tests locally
- Commit message conventions

## Running Tests

### Widget Tests

Copy the `.dart` file to the upstream repo's `test/` directory and run:

```bash
cd ~/dev/projects-cartha/cartha.ai.mobile
flutter test test/payment_result_cancel_test.dart
```

### Maestro Flows

Copy the `.yaml` file to the upstream repo's `.maestro/flows/` directory:

```bash
cp 201_party_join_invalid_code_dead_end.yaml \
   ~/dev/projects-cartha/cartha.ai.mobile/.maestro/flows/

# Validate
maestro validate ~/dev/projects-cartha/cartha.ai.mobile/.maestro/flows/201_party_join_invalid_code_dead_end.yaml

# Run on emulator (requires active emulator + token)
maestro test ~/dev/projects-cartha/cartha.ai.mobile/.maestro/flows/201_party_join_invalid_code_dead_end.yaml
```

## Status

| Test | Gap | Status | Notes |
|------|-----|--------|-------|
| `payment_result_cancel_test.dart` | Payment cancel/decline (zero coverage) | ✅ Written, tested green | 3 widget tests |
| `201_party_join_invalid_code_dead_end.yaml` | Deep-link 404 (zero coverage) | ✅ Written, pending Maestro validation | Requires signed-in state + bad code |

## Next Priority Gaps

Per `docs/EXCEPTION_FLOW_GAP_MATRIX.md`:

1. ✅ Payment fail / cancel — **DONE**
2. ✅ Deep-link 404 / invalid route — **DONE**
3. 🔲 Session expired mid-action (currently only static notice)
4. 🔲 Mid-call network loss on LiveKit
5. 🔲 Mic/camera permission denial at room entry

