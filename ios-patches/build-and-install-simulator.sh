#!/usr/bin/env bash
# Build the checked-out Flutter app and install it on an available iPhone sim.
# Shared by the standalone iOS and deterministic smoke workflows.
set -euo pipefail

app_dir="${1:?Usage: build-and-install-simulator.sh /path/to/cartha_ai_mobile}"
runner_temp="${RUNNER_TEMP:?RUNNER_TEMP must be set}"
script_dir="$(cd "$(dirname "$0")" && pwd)"

if [ ! -d "$app_dir/ios/Runner.xcworkspace" ]; then
  echo "Missing iOS workspace: $app_dir/ios/Runner.xcworkspace" >&2
  exit 1
fi

xcode_version="$(xcodebuild -version | awk '/^Xcode / { print $2 }')"
xcode_major="${xcode_version%%.*}"
echo "Building with Xcode $xcode_version"

if [ "$xcode_major" -ge 27 ]; then
  "$script_dir/apply-ios-patches.sh" "$app_dir"
fi

(
  cd "$app_dir"
  flutter pub get
)

if [ "$xcode_major" -ge 27 ]; then
  "$script_dir/patch-flutter-contacts.sh"
fi

# Clean only this Xcode workspace's products. The mini previously failed when
# a stale Runner bridging-header PCH outlived Flutter.framework.
(
  cd "$app_dir"
  xcodebuild clean -workspace ios/Runner.xcworkspace -scheme Runner \
    -configuration Debug -sdk iphonesimulator
)

stage_dir="$(mktemp -d "$runner_temp/cartha-cloud-projects.XXXXXX")"
restore_cloud_projects() {
  for project in "$stage_dir"/*Cloud.xcodeproj; do
    [ -e "$project" ] || continue
    mv "$project" "$app_dir/ios/"
  done
}
trap restore_cloud_projects EXIT
for project in "$app_dir"/ios/*Cloud.xcodeproj; do
  [ -e "$project" ] || continue
  mv "$project" "$stage_dir/"
done

(
  cd "$app_dir"
  flutter build ios --simulator --debug 2>&1 | tee "$runner_temp/cartha-ios-build.log"
)
restore_cloud_projects
trap - EXIT

if [ ! -d "$app_dir/build/ios/iphonesimulator/Runner.app" ]; then
  echo "Flutter reported success but Runner.app is missing" >&2
  exit 1
fi

if [ -z "${SIMULATOR_UDID:-}" ]; then
  SIMULATOR_UDID="$(xcrun simctl list -j devices available | python3 -c '
import json, sys
devices = [d for runtime, items in json.load(sys.stdin)["devices"].items()
           if "iOS" in runtime for d in items
           if d.get("isAvailable") and "iPhone" in d.get("name", "")]
devices.sort(key=lambda d: (d["name"] != "iPhone 17 Pro", d["state"] != "Booted", d["name"]))
if not devices:
    sys.exit("No available iPhone simulator")
print(devices[0]["udid"])
')"
fi
echo "Using iPhone simulator $SIMULATOR_UDID"

if ! xcrun simctl list devices booted | grep -Fq "$SIMULATOR_UDID"; then
  xcrun simctl boot "$SIMULATOR_UDID"
fi
xcrun simctl bootstatus "$SIMULATOR_UDID" -b

copy_dir="$(mktemp -d "$runner_temp/cartha-ios-app.XXXXXX")"
app_copy="$copy_dir/Runner.app"
ditto "$app_dir/build/ios/iphonesimulator/Runner.app" "$app_copy"
# Extensions have invalid placeholder attributes on the simulator. Strip only
# our temporary app copy; the build artifact remains intact.
if [ -d "$app_copy/PlugIns" ]; then
  rm -rf "$app_copy/PlugIns"
fi
xcrun simctl install "$SIMULATOR_UDID" "$app_copy"
xcrun simctl get_app_container "$SIMULATOR_UDID" com.cartha.app app >/dev/null

if [ -n "${GITHUB_ENV:-}" ]; then
  echo "SIMULATOR_UDID=$SIMULATOR_UDID" >> "$GITHUB_ENV"
fi
echo "Installed com.cartha.app on $SIMULATOR_UDID"
