#!/bin/bash
# test_framework/scripts/test_runners/run_realistic_tests.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"
REALISTIC_DIR="$PROJECT_DIR/optimization_tests/realistic_plans"
RESULTS_DIR="$PROJECT_DIR/test_results"

mkdir -p "$RESULTS_DIR"

echo "📊 Running Realistic Test Suite"
echo "==============================="

if [ ! -d "$REALISTIC_DIR" ]; then
    echo "❌ Realistic test directory not found: $REALISTIC_DIR"
    exit 1
fi

# Find all JSON files in realistic test directory
find "$REALISTIC_DIR" -name "*.json" -type f | while read -r test_file; do
    echo "Running: $(basename "$test_file")"
    "$PROJECT_DIR/costpilot" scan "$test_file" --format json
done > "$RESULTS_DIR/realistic_tests_output.json"

echo "✅ Realistic tests completed"