# Setup & Environment Guide

This guide walks through a clean environment setup for the cartha QA harness.

## Prerequisites

- macOS or Linux (Windows via WSL2)
- Git
- Homebrew (macOS) or apt (Linux)
- ~5GB free disk space (Flutter SDK + dependencies)

## Step 1: Clone This Repo

```bash
git clone <your-cartha-qa-repo> ~/dev/cartha-qa
cd ~/dev/cartha-qa
```

## Step 2: Clone Upstream Cartha Mobile App

This is **separate** from the QA repo — it's the source of truth for the app:

```bash
git clone https://github.com/zackseyun/cartha.ai.mobile.git ~/dev/projects-cartha/cartha.ai.mobile
cd ~/dev/projects-cartha/cartha.ai.mobile
```

Verify you have write access (you should be invited as @hwillGIT):

```bash
git remote -v  # should show zackseyun/cartha.ai.mobile
```

## Step 3: Install Flutter 3.41.6

CI pins Flutter 3.41.6. Clone it at a predictable location:

```bash
git clone --depth 1 --branch 3.41.6 https://github.com/flutter/flutter.git ~/flutter
export PATH="$HOME/flutter/bin:$PATH"

# Verify
flutter --version
# Expected: Flutter 3.41.6 • channel stable
```

**Persist PATH** — add to your `~/.zshrc` or `~/.bashrc`:

```bash
export PATH="$HOME/flutter/bin:$PATH"
```

## Step 4: Codegen in Upstream App

The Flutter app uses `@freezed` + `build_runner` for code generation. Generated files are `.gitignore`'d, so you must regenerate them locally before any test compiles.

```bash
cd ~/dev/projects-cartha/cartha.ai.mobile

# Install melos (monorepo tool)
flutter pub global activate melos

# Or manually: codegen in each package
cd packages/core
flutter pub get
dart run build_runner build --delete-conflicting-outputs

cd ../..
cd features/chat
flutter pub get
dart run build_runner build --delete-conflicting-outputs
cd ../..
```

Verify codegen succeeded:

```bash
find packages/core features/chat -name '*.freezed.dart' | wc -l
# Should be > 0
```

## Step 5: Run a Test to Verify Setup

```bash
cd ~/dev/projects-cartha/cartha.ai.mobile

# Run the payment cancel test
flutter test test/payment_result_cancel_test.dart

# Expected output:
# ✓ payment cancel shows "Payment Cancelled" message
# ✓ continue button escapes to root
# ✓ cancel path never shows success-only chrome for a tier purchase
# 
# 00:XX +3: All tests passed!
```

If tests fail:
- **"method 'map' isn't defined"** → codegen missing (re-run build_runner)
- **"flutter: command not found"** → PATH not set (re-source ~/.zshrc or restart terminal)
- **Gradle/Xcode errors** → run `flutter doctor` and fix issues (iOS build tools, Android SDK)

## Step 6 (Optional): Set Up an Emulator for Maestro Tests

If you want to run Maestro E2E flows:

### Android Emulator

```bash
# List available AVDs
emulator -list-avds

# Or create one via Android Studio
# Settings → Devices → Virtual Device Manager → Create Device

# Launch emulator
emulator -avd <device-name> &
```

### iOS Simulator

```bash
# List available simulators
xcrun simctl list devices

# Launch simulator
open -a Simulator
```

## Step 7: Install Maestro (Optional)

For running E2E flows locally (requires active emulator/device):

```bash
curl -Ls "https://get.maestro.mobile/install.sh" | bash

# Add to PATH
export PATH="$HOME/.maestro/bin:$PATH"

# Verify
maestro --version
```

## Verification Checklist

- [ ] Flutter 3.41.6 installed and in PATH (`flutter --version`)
- [ ] Codegen completed (`find .../*.freezed.dart | wc -l` > 0)
- [ ] Payment widget test passes (`flutter test test/payment_result_cancel_test.dart`)
- [ ] `flutter analyze` has no new errors (pre-existing ones are OK)
- [ ] Cartha QA repo cloned locally (`cd ~/dev/cartha-qa`)
- [ ] Hermes config has model routing enabled (`hermes config show | grep model_profiles`)

## Troubleshooting

### "flutter: command not found"

Add to `~/.zshrc` or `~/.bashrc` and restart terminal:

```bash
export PATH="$HOME/flutter/bin:$PATH"
```

### "build_runner: failed to run builders"

Codegen crashed. Try:

```bash
cd packages/core
rm -rf .dart_tool build
flutter pub get
dart run build_runner build --delete-conflicting-outputs
```

### "No AVD found" or emulator won't start

Use Android Studio to create a virtual device, or check `emulator -list-avds`.

### "Xcode build failed"

Run `flutter doctor -v` and follow instructions. Usually requires accepting Xcode licenses:

```bash
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
sudo xcodebuild -runFirstLaunch
```

### Test hangs or times out

Dart analyzer or build_runner can be slow on first run. Increase timeout:

```bash
flutter test --timeout=60s test/payment_result_cancel_test.dart
```

### Cannot push to upstream repo

Verify SSH key is set up and you're invited to zackseyun/cartha.ai.mobile:

```bash
git remote -v
# Should show zackseyun/cartha.ai.mobile

ssh -T git@github.com
# Should show: Hi <username>! You've successfully authenticated...
```

## Next Steps

- Run the gap analysis: `cat docs/EXCEPTION_FLOW_GAP_MATRIX.md`
- Start writing tests: see `CONTRIBUTION.md`
- Run exploratory QA on cartha.com (with Opus model routing)

## Questions?

See `../CONTRIBUTION.md` or `../README.md` for more.
