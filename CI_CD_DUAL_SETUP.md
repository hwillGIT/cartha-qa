# Dual CI/CD Setup — GitHub Actions + GitLab

**Status:** GitHub Actions is LIVE, GitLab is READY (awaiting repo mirror)

---

## ✅ GitHub Actions (ACTIVE NOW)

### What's Running

**File:** `.github/workflows/test.yml`

**Jobs:**
1. **Widget Tests** — Flutter unit/widget tests with coverage
2. **Maestro E2E Tests** — End-to-end tests (builds web + runs Maestro)
3. **Integration Tests** — Flutter integration tests

**Triggers:**
- 🔵 Push to `main` or `develop`
- 🟡 Pull request to `main` or `develop`
- 📅 Daily schedule (2 AM UTC)

**Results Visible In:**
- ✅ GitHub PR checks (red/green status)
- ✅ GitHub Actions UI (`github.com/hwillGIT/cartha-qa/actions`)
- ✅ Codecov badge (coverage reports)

**Status Page:** https://github.com/hwillGIT/cartha-qa/actions

---

## ⏳ GitLab CI (READY, PENDING MIRROR)

### What's Configured

**File:** `.gitlab-ci.yml`

**Jobs:** Same as GitHub (widget, maestro, integration)

**Triggers:**
- 🔵 Push to any branch
- 🟡 Merge request
- 📅 Schedule

**Results Visible In:**
- ✅ GitLab pipeline UI
- ✅ GitLab MR checks
- ✅ Coverage reports

---

## 🔄 How to Activate GitLab CI

### Step 1: Create GitLab Account (if needed)

```bash
# Option A: Create at https://gitlab.com/
# Option B: Use existing gitlab.com account
# Option C: Use self-hosted GitLab (provide URL + token)
```

### Step 2: Mirror Repository

**Option A: Mirror to gitlab.com (easiest)**

```bash
# Create new project on gitlab.com (e.g., gitlab.com/yourusername/cartha-qa)
# Then mirror from GitHub:

cd ~/dev/cartha-qa

# Add GitLab as a second remote
git remote add gitlab https://gitlab.com/yourusername/cartha-qa.git

# Push to GitLab
git push gitlab main

# (Optional) Enable mirror syncing in GitLab settings for auto-sync
```

**Option B: Add Dual Push (one command updates both)**

```bash
# Edit .git/config to push to both GitHub + GitLab

cd ~/dev/cartha-qa
git remote set-url origin 'git::https://github.com/hwillGIT/cartha-qa.git|https://gitlab.com/yourusername/cartha-qa.git'

# Now `git push origin main` updates BOTH repos simultaneously
```

**Option C: Use GitHub-GitLab Sync App**

- Install: https://github.com/apps/gitlab-com
- Authorize: Select cartha-qa repo
- Result: Auto-sync to GitLab

### Step 3: Verify GitLab CI

```bash
# Check pipeline status
# Visit: https://gitlab.com/yourusername/cartha-qa/-/pipelines/

# Watch tests run on every push
```

---

## 📊 Dual CI/CD Dashboard

Once both are active, you'll have:

### GitHub Actions
- 📍 Location: https://github.com/hwillGIT/cartha-qa/actions
- 🔍 View: By workflow, branch, commit
- 📊 Reports: Coverage (Codecov), artifacts
- 🔔 Notifications: GitHub email/UI

### GitLab CI
- 📍 Location: https://gitlab.com/yourusername/cartha-qa/-/pipelines
- 🔍 View: By pipeline, branch, commit
- 📊 Reports: Coverage, test results
- 🔔 Notifications: GitLab email/UI

### Synchronized

Both systems:
- ✅ Run same tests (widget, maestro, integration)
- ✅ Test same code (dual push keeps repos in sync)
- ✅ Report same results (coverage, pass/fail)
- ✅ Trigger on same events (push, MR, schedule)

---

## 🎯 What Tests Run

### Widget Tests
```bash
flutter test test/
```
- Cartha's Flutter widget tests
- Fast (seconds)
- High coverage
- Runs on: Ubuntu latest

### Maestro E2E Tests
```bash
flutter build web --release
maestro test test-cases/maestro/
```
- End-to-end flows (payment, deep-links, session expiry, etc.)
- Full app simulation
- Slower (minutes)
- Results: Video + screenshots

### Integration Tests
```bash
flutter test integration_test/ --dart-define=CI=true
```
- Cross-feature integration
- API mocks
- Slower (minutes)

---

## 📋 Next Steps

### Now (GitHub Actions Active)
1. ✅ Push code to GitHub
2. ✅ Watch tests run automatically
3. ✅ See results in PR checks

### When You're Ready (Activate GitLab)
1. Create GitLab account (gitlab.com or self-hosted)
2. Mirror cartha-qa repo
3. Enable dual push (one command, both platforms)
4. Watch GitLab pipelines run in parallel

---

## 💡 Questions?

**GitHub Actions not running?**
- Check: https://github.com/hwillGIT/cartha-qa/actions
- Look for: Workflow syntax errors, missing Flutter version, timeout issues

**GitLab setup questions?**
- Ask: Provide your GitLab URL / username
- I'll: Mirror repo + configure dual push

**Both running but results different?**
- Sync: `git push` to update both repos
- Check: Individual job logs in each platform

---

## 📝 Configuration Files

- **GitHub Actions:** `.github/workflows/test.yml`
- **GitLab CI:** `.gitlab-ci.yml`

Both files are already in the repo and pushed. No additional setup needed for GitHub Actions (already live). Just need GitLab account + mirror for GitLab.

---

**Status:** ✅ GitHub Actions LIVE | ⏳ GitLab READY (awaiting mirror)
