# Cartha QA Repo — Setup Complete

**Repo Location:** `~/dev/cartha-qa` (local Git repo, not yet pushed to GitHub)

**Structure:**
```
cartha-qa/
├── README.md                                  # Project overview + quick-start
├── CONTRIBUTION.md                            # Test authoring guidelines
├── .gitignore                                 # Excludes screenshots, logs, build artifacts
├── .hermes-config.example.yaml                # Model routing config (qa→Opus, etc.)
├── docs/
│   ├── SETUP.md                              # Detailed environment setup (Flutter 3.41.6, codegen, troubleshooting)
│   ├── EXCEPTION_FLOW_GAP_MATRIX.md           # Coverage analysis — zero-coverage gaps ranked
│   └── QA_FINDINGS.md                        # Template for exploratory findings report
├── test-cases/
│   ├── README.md                             # Test-cases overview + status
│   ├── widget/
│   │   └── payment_result_cancel_test.dart   # 3 widget tests (payment cancel dead-end) — WRITTEN + GREEN
│   └── maestro/
│       └── 201_party_join_invalid_code_dead_end.yaml  # E2E flow (deep-link 404) — WRITTEN, pending maestro validation
└── scripts/
    └── run_widget_tests.sh                   # Helper: run widget tests locally
```

## Commits

1. **cca6d0d** — init: cartha QA project
2. **e8e2cbc** — docs: cartha QA project structure + gap matrix + widget/Maestro test templates

## What's Included

### Documentation
- **README.md** — full project overview, quick-start, directory structure, key findings summary, Zack's preferences, model routing
- **CONTRIBUTION.md** — detailed guidelines for writing widget tests, Maestro flows, submitting findings, commit message format
- **SETUP.md** — step-by-step environment setup (Flutter 3.41.6 install, codegen, verification, troubleshooting)
- **QA_FINDINGS.md** — template for the live-site exploratory report (will be populated by Opus subagent)

### Tests
- **payment_result_cancel_test.dart** — 3 widget tests for payment cancel/decline dead-end (zero-coverage gap)
  - ✅ Tests compile without errors
  - ✅ Tests run and pass green
  - ✅ Asserts against real PaymentResultScreen strings from source
  - Ready to copy into upstream repo `test/` directory
  
- **201_party_join_invalid_code_dead_end.yaml** — Maestro E2E flow for invalid party deep-link (zero-coverage gap)
  - ✅ Follows exact Maestro conventions (appId, tags, ---, comments, commands)
  - ✅ Numbered correctly (201 = next available after upstream flows)
  - ✅ Ready to copy into upstream repo `.maestro/flows/` directory

### Configuration
- **.hermes-config.example.yaml** — example config for per-job model routing (qa→Opus, coding→Sonnet, etc.)
- **.gitignore** — excludes screenshots, logs, build artifacts, IDE files

## Next Steps

### 1. Push to GitHub (when ready)
```bash
cd ~/dev/cartha-qa
git remote add origin <your-cartha-qa-github-url>
git push -u origin main
```

### 2. Copy Tests to Upstream (when ready to PR)
```bash
# Widget test
cp ~/dev/cartha-qa/test-cases/widget/payment_result_cancel_test.dart \
   ~/dev/projects-cartha/cartha.ai.mobile/cartha_ai_mobile/test/

# Maestro flow
cp ~/dev/cartha-qa/test-cases/maestro/201_party_join_invalid_code_dead_end.yaml \
   ~/dev/projects-cartha/cartha.ai.mobile/cartha_ai_mobile/.maestro/flows/
```

### 3. Await Opus Exploratory QA Results
An Opus subagent is currently running live-site QA on cartha.com (groups mode, navigation, auth flows, negative space). Results will be populated into `docs/QA_FINDINGS.md` when complete.

### 4. Write Additional Tests (Parallel)
Based on gap matrix priorities:
- [ ] Session expiry mid-action (widget test)
- [ ] Mid-call network loss (Maestro flow + widget test)
- [ ] Mic/camera permission denial at room entry (widget test)

## Key Notes

- **Upstream constraint:** zackseyun/cartha.ai.mobile is the source of truth. This repo contains QA artifacts only.
- **Zack's preferences:** No auto QA sweeps (`qa_sweep.sh` disabled). Prefer focused `flutter test` + `flutter analyze`.
- **Model routing:** Configured in `~/.hermes/config.yaml` — qa→Opus (deep reasoning), coding→Sonnet (fast), default→Haiku (cheap).
- **Codegen critical:** The upstream app uses `@freezed` + `build_runner`. Generated `.freezed.dart` and `.g.dart` files are git-ignored. Must regenerate locally before any test compiles. See `docs/SETUP.md` for details.

## Questions?

See the respective README or doc in each directory. All files are heavily commented and include examples.

