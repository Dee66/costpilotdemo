#!/bin/bash
# test_framework/scripts/test_runners/run_full_test_suite.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"

echo "🚀 CostPilot Comprehensive Test Framework"
echo "=========================================="

# Run all test suites
echo "📊 Running Realistic Test Suite..."
"$SCRIPT_DIR/run_realistic_tests.sh"

echo "🧪 Running Massive Test Suite..."
"$SCRIPT_DIR/run_massive_test_suite.sh"

echo "🔬 Running Stress Tests..."
"$SCRIPT_DIR/run_stress_tests.sh"

echo "📈 Generating Analysis Report..."
"$SCRIPT_DIR/../analyzers/generate_test_report.sh"

echo "✅ All tests completed successfully!"