# CI/CD & Visibility — Clarification

## Current Setup

### cartha-qa (hwillGIT/cartha-qa)
- **Remote:** GitHub (public repo)
- **CI/CD:** NONE configured yet
- **Tests:** Manual run only (`./scripts/run_widget_tests.sh`)
- **Visibility:** GitHub only (no GitLab, no automated checks)

### cartha.ai.mobile (upstream, zackseyun/cartha.ai.mobile)
- **Remote:** GitHub
- **CI/CD:** GitHub Actions → AWS CodeBuild
- **Tests:** Run in CodeBuild (see `.github/workflows/deploy-*.yml`)
- **Visibility:** GitHub Actions checks on PRs, CodeBuild logs

---

## What This Means

### Q: Will cartha-qa tests show up in GitLab?

**A: NO** — cartha-qa is GitHub-only. No GitLab integration exists.

### Q: Will tests run automatically in GitHub Actions?

**A: NO (currently)** — No GitHub Actions workflows in cartha-qa yet.
- Tests must be run manually: `cd ~/dev/cartha-qa && ./scripts/run_widget_tests.sh`
- No automated CI/CD pipeline

### Q: How will upstream (cartha.ai.mobile) tests run?

**A: GitHub Actions + AWS CodeBuild** —
- When you copy tests to `cartha.ai.mobile` and create a PR
- GitHub Actions trigger (upstream has `deploy-*.yml` workflows)
- Tests run in AWS CodeBuild
- Results show in GitHub PR checks
- NOT in GitLab (upstream is GitHub-only)

---

## Options

### Option 1: Keep As-Is ✅ (Current)

**cartha-qa:**
- Manual test execution only
- Tests stay in GitHub (public, documented)
- No CI/CD overhead

**When copying to upstream:**
- Copy tests to `cartha.ai.mobile/test/` and `.maestro/flows/`
- Create PR to zackseyun/cartha.ai.mobile
- GitHub Actions trigger (CodeBuild)
- Results show in PR checks

**Pros:** Simple, no extra configuration
**Cons:** Tests don't run automatically in cartha-qa

---

### Option 2: Add GitHub Actions to cartha-qa ⭐ (Recommended)

**Setup:** Create `.github/workflows/test.yml`

```yaml
name: Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
      - run: flutter pub get
      - run: flutter test test/
      - run: maestro test .maestro/flows/
```

**Benefits:**
- ✅ Tests auto-run on push/PR
- ✅ Results show in GitHub (UI)
- ✅ Catch regressions early
- ✅ Same setup as upstream

**Cons:** Requires Flutter setup in GitHub Actions (may be slower)

---

### Option 3: Add GitLab CI (Only if needed)

**If you need GitLab visibility:**
- Mirror cartha-qa to GitLab
- Create `.gitlab-ci.yml`
- Tests run in GitLab CI
- Separate from GitHub

**Pros:** Full GitLab integration
**Cons:** Dual maintenance, complexity

---

## Recommendation

**Use Option 2** (GitHub Actions for cartha-qa):

1. **Add `.github/workflows/test.yml`** to cartha-qa
2. **Auto-run tests** on push/PR
3. **See results** in GitHub (UI badges, PR checks)
4. **Same workflow** as upstream (familiar)

This way:
- cartha-qa tests run automatically
- Upstream tests run automatically (CodeBuild)
- Everything visible in GitHub
- No GitLab needed (unless explicitly required)

---

## Next Steps

**Now:**
1. Decide: Keep manual (Option 1) or add GitHub Actions (Option 2)?
2. If Option 2: I'll create `.github/workflows/test.yml` and commit

**Later (when copying to upstream):**
- Tests will automatically run in upstream's GitHub Actions + CodeBuild
- Results visible in PR checks

---

**What would you prefer?**
- Option 1: Manual tests (current, no changes)
- Option 2: GitHub Actions auto-run (recommended)
- Option 3: GitLab CI (if required by your team)
