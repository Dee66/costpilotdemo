#!/bin/bash
# test_framework/scripts/analyzers/generate_test_report.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"
RESULTS_DIR="$PROJECT_DIR/test_results"

echo "📈 Generating Comprehensive Test Report"
echo "======================================="

# Run the Python analyzer
python3 "$SCRIPT_DIR/analyze_detection_rates.py"

# Generate additional metrics
echo "Generating performance metrics..."

# Count total test files
total_files=$(find "$PROJECT_DIR/test_framework/optimization_tests" "$PROJECT_DIR/optimization_tests" -name "*.json" -type f 2>/dev/null | wc -l)
echo "Total test files: $total_files"

# Check license status
if [ -f "$PROJECT_DIR/license.yml" ]; then
    echo "License: ✅ Configured"
else
    echo "License: ❌ Missing"
fi

echo "✅ Report generation completed: $RESULTS_DIR/comprehensive_analysis.md"