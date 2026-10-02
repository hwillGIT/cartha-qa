#!/bin/bash
#
# Helper script: run widget tests from the cartha-qa repo
#
# Usage:
#   ./scripts/run_widget_tests.sh                    # Run all widget tests
#   ./scripts/run_widget_tests.sh payment_result     # Run specific test file

set -e

UPSTREAM_REPO="${UPSTREAM_REPO:-$HOME/dev/projects-cartha/cartha.ai.mobile}"
TEST_PATTERN="${1:-}"

if [ ! -d "$UPSTREAM_REPO" ]; then
    echo "Error: upstream repo not found at $UPSTREAM_REPO"
    echo "Set UPSTREAM_REPO env var or clone to default location:"
    echo "  git clone https://github.com/zackseyun/cartha.ai.mobile.git $UPSTREAM_REPO"
    exit 1
fi

cd "$UPSTREAM_REPO"

echo "=== Flutter Doctor ==="
flutter doctor -v | head -15

echo
echo "=== Running Widget Tests ==="
if [ -z "$TEST_PATTERN" ]; then
    echo "Running all tests in test/ ..."
    flutter test test/ --timeout=60s
else
    echo "Running tests matching: $TEST_PATTERN"
    flutter test test/ -k "$TEST_PATTERN" --timeout=60s
fi

echo
echo "=== Test run complete ==="
