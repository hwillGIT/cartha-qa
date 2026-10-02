#!/bin/bash
# Patches flutter_contacts in the pub cache for iOS 27 scene lifecycle.
# The plugin force-unwraps UIApplication.shared.delegate!.window!! which is nil
# under scenes. This replaces it with a scene-aware lazy resolution.
# Test-only; do not commit to the plugin repo.
#
# Usage: ./patch-flutter-contacts.sh
# Run after `flutter pub get`, before `flutter build`.

set -e

PLUGIN_FILE="$HOME/.pub-cache/hosted/pub.dev/flutter_contacts-1.1.9+2/ios/Classes/SwiftFlutterContactsPlugin.swift"

if [ ! -f "$PLUGIN_FILE" ]; then
  echo "flutter_contacts plugin not found at $PLUGIN_FILE"
  echo "Run 'flutter pub get' first."
  exit 1
fi

if grep -q "QA harness: the original code force-unwrapped" "$PLUGIN_FILE"; then
  echo "flutter_contacts already patched"
  exit 0
fi

echo "Patching flutter_contacts for scene lifecycle..."

python3 - <<'PYEOF'
import re, sys, os
p = os.path.expanduser("~/.pub-cache/hosted/pub.dev/flutter_contacts-1.1.9+2/ios/Classes/SwiftFlutterContactsPlugin.swift")
s = open(p).read()

# Original (pre-patch) code force-unwraps the app delegate window.
# Match the property and replace with scene-aware version.
old_pattern = r"private var rootViewController: UIViewController\? \{\s+UIApplication\.shared\.delegate!\.window!!\.rootViewController!\s+\}"
new_code = """// QA harness: the original code force-unwrapped UIApplication.shared.delegate?.window,
// which is nil under the UIScene lifecycle (iOS 27 SDK requires scenes).
    // Resolve the presenter lazily from the key window instead.
    private var rootViewController: UIViewController? {
        UIApplication.shared.connectedScenes
            .compactMap { $0 as? UIWindowScene }
            .flatMap { $0.windows }
            .first { $0.isKeyWindow }?.rootViewController
    }"""

if re.search(old_pattern, s):
    s = re.sub(old_pattern, new_code, s, count=1)
    open(p, "w").write(s)
    print("  Patched rootViewController property")
else:
    # Try a more lenient match (in case formatting differs)
    old_simple = "UIApplication.shared.delegate!.window!!.rootViewController!"
    if old_simple in s:
        # Find the enclosing property and replace
        # This is fragile; log a warning
        print("  WARNING: Found force-unwrap but pattern didn't match. Manual patch needed.")
        print(f"  File: {p}")
        sys.exit(1)
    else:
        print("  Pattern not found; may already be patched or version differs")
        sys.exit(1)
PYEOF

echo "flutter_contacts patched."
