# Cartha QA & Testing

Dedicated QA automation, test harness, and exploratory findings for [cartha.com](https://cartha.com) — a social audio/video platform with groups, messaging, and live rooms.

## Overview

This repo contains:

- **Gap analysis** — coverage matrix for existing Flutter QA suite (316 Maestro flows, 393 widget tests)
- **Exception-flow tests** — new widget tests & Maestro flows for zero-coverage dead-ends (payments, deep-links, etc.)
- **Exploratory findings** — live-site QA reports with evidence (screenshots, error logs, reproduction steps)
- **Test infrastructure** — setup guides, contribution patterns, CI/CD integration

## Quick Start

### Prerequisites

- Flutter 3.41.6 (pinned in CI; see `.fvm/fvmrc` in upstream repo)
- Dart SDK (included with Flutter)
- Git

### Setup

```bash
# Clone this repo
git clone <your-cartha-qa-repo> ~/dev/cartha-qa
cd ~/dev/cartha-qa

# Clone the upstream cartha mobile app (separate, for reference)
git clone https://github.com/zackseyun/cartha.ai.mobile.git ~/dev/projects-cartha/cartha.ai.mobile

# Install Flutter 3.41.6
git clone --depth 1 --branch 3.41.6 https://github.com/flutter/flutter.git ~/flutter
export PATH="$HOME/flutter/bin:$PATH"

# Run codegen in upstream repo
cd ~/dev/projects-cartha/cartha.ai.mobile
cd packages/core && dart run build_runner build --delete-conflicting-outputs
cd ../.. && cd features/chat && dart run build_runner build --delete-conflicting-outputs
```

### Run Tests

```bash
cd ~/dev/projects-cartha/cartha.ai.mobile

# Widget tests only (fast, no full sweep)
flutter test test/payment_result_cancel_test.dart

# All widget tests
flutter analyze
flutter test

# Maestro E2E flows (requires active emulator/device + qa_sweep config)
# Note: do NOT run ./scripts/qa_sweep.sh unless explicitly requested
# See CONTRIBUTION.md for manual Maestro flow execution
```

## Directory Structure

```
.
├── README.md                              # This file
├── CONTRIBUTION.md                        # Guidelines for adding tests
├── docs/
│   ├── EXCEPTION_FLOW_GAP_MATRIX.md       # Coverage analysis (zero-coverage gaps)
│   ├── SETUP.md                           # Detailed environment setup
│   └── QA_FINDINGS.md                     # Live-site exploratory findings
├── test-cases/
│   ├── widget/
│   │   ├── payment_result_cancel_test.dart   # Zero-coverage gap: payment cancel/decline
│   │   └── [future widget tests]
│   └── maestro/
│       ├── 201_party_join_invalid_code_dead_end.yaml  # Zero-coverage gap: deep-link 404
│       └── [future Maestro flows]
├── findings/
│   ├── screenshots/                       # Evidence from live-site QA
│   ├── logs/                              # Error logs, network traces
│   └── report.md                          # Synthesized QA report
└── scripts/
    ├── run_widget_tests.sh                # Helper: run widget tests locally
    └── [future: CI helpers, data collection]
```

## Key Findings (Live-Site QA)

See `docs/QA_FINDINGS.md` for the full exploratory report.

**High-priority gaps:**
- 🔴 **Payment cancel/decline** — zero exception-flow coverage
- 🔴 **Deep-link 404s** — no invalid route handling tests
- 🟠 **Session expiry mid-action** — only static notice, not live expiry
- 🟠 **Mid-call network loss** — weak coverage on LiveKit disconnect scenarios
- 🟠 **Mic/camera permission denial** — untested at room entry

## Important Notes

### Upstream Repo Constraint

The upstream [zackseyun/cartha.ai.mobile](https://github.com/zackseyun/cartha.ai.mobile) is the source of truth for the Flutter app. This repo contains **QA artifacts only** — tests, findings, and documentation. Do not edit the upstream app source here.

### Zack's QA Preferences (from CLAUDE.md)

- ✅ DO: Run focused `flutter test` + `flutter analyze` on specific tests
- ✅ DO: Write widget tests matching existing patterns (PR-mergeable)
- ❌ DO NOT: Run `./scripts/qa_sweep.sh` (auto QA disabled) unless explicitly asked
- ✅ DO: Keep Bible reader in parity with Next.js web client

### Model Routing

This project uses Hermes with per-job model routing:
- QA work (exploratory, gap analysis) → Claude Opus (best for edge-case reasoning)
- Coding/test authoring → Claude Sonnet (sufficient for logic, fast)
- Default → Claude Haiku (scripting, fast)

See `.hermes-config.example.yaml` for configuration.

## Contributing

See `CONTRIBUTION.md` for guidelines on:
- Writing new widget tests
- Adding Maestro E2E flows
- Running tests locally
- Submitting findings
- PR checklist

## License

[TBD — match upstream cartha repo]

## Contact

QA Lead: Hubert Williams (@hwillGIT on GitHub)
