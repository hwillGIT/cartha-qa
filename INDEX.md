# Cartha QA — Quick Index

**Location:** `~/dev/cartha-qa` (Git repo, local only for now)

**Upstream:** [zackseyun/cartha.ai.mobile](https://github.com/zackseyun/cartha.ai.mobile) (source of truth)

---

## Start Here

1. **Quick Overview** → `README.md`
2. **Setup (first time)** → `docs/SETUP.md`
3. **Contributing Tests** → `CONTRIBUTION.md`

---

## Key Documents

| Document | Purpose |
|----------|---------|
| `README.md` | Project overview, structure, quick-start, Zack's preferences |
| `CONTRIBUTION.md` | Guidelines: write widget tests, Maestro flows, submit findings |
| `docs/SETUP.md` | Step-by-step: Flutter 3.41.6, codegen, troubleshooting |
| `docs/EXCEPTION_FLOW_GAP_MATRIX.md` | **Coverage analysis** — 316 flows + 393 tests vs 547 screens. Zero-coverage gaps ranked. |
| `docs/QA_FINDINGS.md` | Template for live-site exploratory report (will be populated by Opus subagent) |
| `SETUP_COMPLETE.md` | Summary of this setup (what was created, next steps) |

---

## Tests (Ready to Use)

| Test | Gap | Status | Location |
|------|-----|--------|----------|
| **payment_result_cancel_test.dart** | Payment cancel/decline (zero coverage) | ✅ Written, tested green | `test-cases/widget/` |
| **201_party_join_invalid_code_dead_end.yaml** | Deep-link 404 (zero coverage) | ✅ Written, pending validation | `test-cases/maestro/` |

**Next priority gaps:**
- [ ] Session expiry mid-action
- [ ] Mid-call network loss (LiveKit)
- [ ] Mic/camera permission denial at room entry

---

## Running Tests

### Widget Tests (Fast)
```bash
cd ~/dev/projects-cartha/cartha.ai.mobile
flutter test test/payment_result_cancel_test.dart
```

### Maestro Flows (E2E, requires emulator)
```bash
maestro validate ~/dev/cartha-qa/test-cases/maestro/201_party_join_invalid_code_dead_end.yaml
maestro test ~/dev/cartha-qa/test-cases/maestro/201_party_join_invalid_code_dead_end.yaml
```

### Run All Tests
```bash
~/dev/cartha-qa/scripts/run_widget_tests.sh
```

---

## Status

- ✅ **Repo structure created** — 11 files, 3 commits
- ✅ **Documentation complete** — README, CONTRIBUTION, SETUP guides
- ✅ **Gap analysis done** — exception-flow matrix populated
- ✅ **2 tests written** — payment cancel + deep-link 404 (zero-coverage gaps)
- ✅ **Payment test validated** — passing green in Flutter
- 🔄 **Opus exploratory QA running** — live-site testing cartha.com (groups, auth, negative space)
- 🔲 **Tests copied to upstream** — pending (when ready for PR)
- 🔲 **GitHub repo created** — pending (decide on ownership)

---

## Model Routing (Hermes)

```yaml
delegation.model_profiles:
  qa:      claude-opus-4-1-20250805       # deep reasoning
  coding:  claude-sonnet-4-20250514       # sufficient logic, fast
  research: claude-opus-4-1-20250805      # synthesis
  default: claude-haiku-4-5-20251001      # baseline
```

See `.hermes-config.example.yaml` for example config.

---

## Constraints (from upstream CLAUDE.md)

- ✅ DO: Focused `flutter test` + `flutter analyze`
- ✅ DO: Write PR-mergeable tests in upstream conventions
- ❌ DO NOT: Run `./scripts/qa_sweep.sh` (auto QA disabled unless asked)
- ✅ DO: Keep Bible reader in parity with Next.js web client

---

## Next Actions

1. **Push to GitHub** (when ready) — `git remote add origin <url> && git push`
2. **Copy tests to upstream** — `cp test-cases/* ~/dev/projects-cartha/cartha.ai.mobile/`
3. **Await Opus findings** — exploratory QA will populate `docs/QA_FINDINGS.md`
4. **Write additional tests** — see gap matrix priorities

---

## Questions?

- Setup issues → `docs/SETUP.md`
- Test patterns → `CONTRIBUTION.md`
- Coverage gaps → `docs/EXCEPTION_FLOW_GAP_MATRIX.md`
- Exploratory findings → `docs/QA_FINDINGS.md` (will be populated)

