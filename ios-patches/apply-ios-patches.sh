#!/bin/bash
# Applies test-only iOS patches for the Cartha QA harness.
# These work around iOS 27 SDK requirements so the app can launch on the simulator.
# DO NOT commit these to zackseyun/cartha.ai.mobile — they are test-only.
#
# Usage: ./apply-ios-patches.sh /path/to/cartha.ai.mobile/cartha_ai_mobile
#
# Patches applied:
# 1. ios/Podfile: Raise pod deployment targets below 15.0 (Xcode 27 rejects them)
# 2. ios/Runner/Info.plist: Add UIScene manifest, remove UIMainStoryboardFile
# 3. ios/Runner/SceneDelegate.swift: Add manual scene delegate (new file)
# 4. ios/Runner.xcodeproj/project.pbxproj: Register SceneDelegate.swift in target
# 5. ios/Runner/AppDelegate.swift: Move plugin registration to SceneDelegate
#
# After building, strip PlugIns (app extensions) before installing on simulator:
#   rm -rf /path/to/Runner.app/PlugIns
# The extensions cause "Invalid placeholder attributes" on simulator install.

set -e

MOBILE_DIR="${1:?Usage: $0 /path/to/cartha.ai.mobile/cartha_ai_mobile}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Applying iOS test patches to $MOBILE_DIR..."

# 1. Podfile: iOS 15 floor for pods
echo "  [1/5] Patching Podfile..."
if ! grep -q "QA harness: Xcode 27" "$MOBILE_DIR/ios/Podfile" 2>/dev/null; then
  python3 - "$MOBILE_DIR" <<'PYEOF'
import sys
p = sys.argv[1] + "/ios/Podfile"
try:
    s = open(p).read()
except FileNotFoundError:
    print(f"    WARNING: Podfile not found at {p}, skipping")
    sys.exit(0)
old = "      config.build_settings['ENABLE_BITCODE'] = 'NO'\n"
new = """      config.build_settings['ENABLE_BITCODE'] = 'NO'

      # QA harness: Xcode 27 rejects pod deployment targets below 15.0.
      # Raise only the ones below the floor; leave higher ones untouched.
      current_target = config.build_settings['IPHONEOS_DEPLOYMENT_TARGET']
      if current_target && Gem::Version.new(current_target) < Gem::Version.new('15.0')
        config.build_settings['IPHONEOS_DEPLOYMENT_TARGET'] = '15.0'
      end
"""
if old not in s:
    print("    WARNING: Podfile pattern not found, skipping (may already be patched or different version)")
    sys.exit(0)
s = s.replace(old, new, 1)
open(p, "w").write(s)
print("    Podfile patched")
PYEOF
else
  echo "    Podfile already patched"
fi

# 2. Info.plist: scene manifest + remove UIMainStoryboardFile
echo "  [2/5] Patching Info.plist..."
python3 - "$MOBILE_DIR" <<'PYEOF'
import sys, plistlib
p = sys.argv[1] + "/ios/Runner/Info.plist"
with open(p, "rb") as f:
    d = plistlib.load(f)
changed = False
# Remove app-level storyboard (conflicts with scene manifest)
if "UIMainStoryboardFile" in d:
    del d["UIMainStoryboardFile"]
    changed = True
    print("    Removed UIMainStoryboardFile")
# Add scene manifest if missing
if "UIApplicationSceneManifest" not in d:
    d["UIApplicationSceneManifest"] = {
        "UIApplicationSupportsMultipleScenes": False,
        "UISceneConfigurations": {
            "UIWindowSceneSessionRoleApplication": [
                {
                    "UISceneClassName": "UIWindowScene",
                    "UISceneConfigurationName": "flutter",
                    "UISceneDelegateClassName": "$(PRODUCT_MODULE_NAME).SceneDelegate",
                }
            ]
        },
    }
    changed = True
    print("    Added UIApplicationSceneManifest")
with open(p, "wb") as f:
    plistlib.dump(d, f)
if not changed:
    print("    Info.plist already patched")
PYEOF

# 3. SceneDelegate.swift: copy new file
echo "  [3/5] Installing SceneDelegate.swift..."
cp "$SCRIPT_DIR/SceneDelegate.swift" "$MOBILE_DIR/ios/Runner/SceneDelegate.swift"
echo "    SceneDelegate.swift installed"

# 4. project.pbxproj: register SceneDelegate.swift
echo "  [4/5] Patching project.pbxproj..."
python3 - "$MOBILE_DIR" <<'PYEOF'
import sys
p = sys.argv[1] + "/ios/Runner.xcodeproj/project.pbxproj"
try:
    s = open(p).read()
except FileNotFoundError:
    print(f"    WARNING: project.pbxproj not found at {p}, skipping")
    sys.exit(0)
if "SceneDelegate.swift in Sources" in s:
    print("    project.pbxproj already patched")
    sys.exit(0)
# Note: UUIDs below are specific to the verified ref. If they don't match,
# the patch is skipped with a warning (build will fail without SceneDelegate).
patterns = [
    ("\t\t74858FAF1ED2DC5600515810 /* AppDelegate.swift in Sources */ = {isa = PBXBuildFile; fileRef = 74858FAE1ED2DC5600515810 /* AppDelegate.swift */; };\n",
     "\t\t74858FB01ED2DC5600515811 /* SceneDelegate.swift in Sources */ = {isa = PBXBuildFile; fileRef = 74858FB11ED2DC5600515811 /* SceneDelegate.swift */; };\n",
     "PBXBuildFile"),
    ("\t\t74858FAE1ED2DC5600515810 /* AppDelegate.swift */ = {isa = PBXFileReference; fileEncoding = 4; lastKnownFileType = sourcecode.swift; path = AppDelegate.swift; sourceTree = \"<group>\"; };\n",
     "\t\t74858FB11ED2DC5600515811 /* SceneDelegate.swift */ = {isa = PBXFileReference; fileEncoding = 4; lastKnownFileType = sourcecode.swift; path = SceneDelegate.swift; sourceTree = \"<group>\"; };\n",
     "PBXFileReference"),
    ("\t\t\t\t74858FAE1ED2DC5600515810 /* AppDelegate.swift */,\n",
     "\t\t\t\t74858FB11ED2DC5600515811 /* SceneDelegate.swift */,\n",
     "Group"),
    ("\t\t\t\t74858FAF1ED2DC5600515810 /* AppDelegate.swift in Sources */,\n",
     "\t\t\t\t74858FB01ED2DC5600515811 /* SceneDelegate.swift in Sources */,\n",
     "Sources"),
]
for old, new_suffix, name in patterns:
    if old not in s:
        print(f"    WARNING: {name} pattern not found, skipping pbxproj patch (UUIDs may differ)")
        sys.exit(0)
    s = s.replace(old, old + new_suffix, 1)
open(p, "w").write(s)
print("    project.pbxproj patched")
PYEOF

# 5. AppDelegate.swift: move plugin registration to SceneDelegate
echo "  [5/5] Patching AppDelegate.swift..."
python3 - "$MOBILE_DIR" <<'PYEOF'
import sys
p = sys.argv[1] + "/ios/Runner/AppDelegate.swift"
lines = open(p).read().split("\n")
for i, l in enumerate(lines):
    if "GeneratedPluginRegistrant.register(with: self)" in l:
        lines[i] = "    // QA harness: plugin registration moved to SceneDelegate"
        print(f"    AppDelegate.swift patched (line {i+1})")
        break
else:
    print("    AppDelegate.swift already patched (or pattern not found)")
    sys.exit(0)
open(p, "w").write("\n".join(lines))
PYEOF

echo "All iOS patches applied."
echo ""
echo "Remember to strip app extensions before simulator install:"
echo "  rm -rf build/ios/iphonesimulator/Runner.app/PlugIns"
