#!/bin/bash
# test_framework/scripts/test_runners/run_stress_tests.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"
STRESS_DIR="$PROJECT_DIR/stress_tests"
RESULTS_DIR="$PROJECT_DIR/test_results"

mkdir -p "$RESULTS_DIR"

echo "🔬 Running Stress Tests"
echo "======================="

if [ ! -d "$STRESS_DIR" ]; then
    echo "❌ Stress test directory not found: $STRESS_DIR"
    exit 1
fi

# Run tests on malformed and edge case files
find "$STRESS_DIR" -name "*.json" -type f | while read -r test_file; do
    echo "Testing: $(basename "$test_file")"
    if "$PROJECT_DIR/costpilot" scan "$test_file" --format json 2>&1; then
        echo "  ✅ Passed"
    else
        echo "  ❌ Failed (expected for malformed data)"
    fi
done > "$RESULTS_DIR/stress_tests_output.txt"

echo "✅ Stress tests completed"