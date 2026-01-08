#!/bin/bash
# test_framework/scripts/test_runners/run_massive_test_suite.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"
MASSIVE_DIR="$PROJECT_DIR/test_framework/optimization_tests/massive_suite"
RESULTS_DIR="$PROJECT_DIR/test_results"

mkdir -p "$RESULTS_DIR"

echo "🧪 Running Massive Test Suite"
echo "============================="

# Generate test files if they don't exist
if [ ! -d "$MASSIVE_DIR/containers" ] || [ -z "$(ls -A "$MASSIVE_DIR/containers")" ]; then
    echo "Generating massive test suite..."
    python3 "$SCRIPT_DIR/../generators/generate_massive_tests.py"
fi

# Run tests for each category
categories=("containers" "instance_rightsizing" "storage_optimization" "serverless" "network_optimization" "database_optimization" "cost_anomaly_detection")

total_tests=0
total_detections=0
declare -A category_results

for category in "${categories[@]}"; do
    category_dir="$MASSIVE_DIR/$category"
    if [ -d "$category_dir" ]; then
        echo "Running $category tests..."
        test_files=("$category_dir"/*.json)
        category_tests=${#test_files[@]}
        category_detections=0

        for test_file in "${test_files[@]}"; do
            if [ -f "$test_file" ]; then
                # Run CostPilot scan
                if "$PROJECT_DIR/costpilot" scan "$test_file" --format json > /dev/null 2>&1; then
                    ((category_detections++))
                fi
            fi
        done

        category_results["$category"]="$category_tests:$category_detections"
        ((total_tests += category_tests))
        ((total_detections += category_detections))

        echo "  $category: $category_detections/$category_tests detections"
    fi
done

# Save results
results_file="$RESULTS_DIR/massive_suite_results.json"
cat > "$results_file" << EOF
{
  "suite": "massive_suite",
  "total_tests": $total_tests,
  "total_detections": $total_detections,
  "detection_rate": $(echo "scale=4; $total_detections / $total_tests" | bc -l 2>/dev/null || echo "0"),
  "by_category": {
EOF

first=true
for category in "${!category_results[@]}"; do
    if [ "$first" = true ]; then
        first=false
    else
        echo "," >> "$results_file"
    fi
    IFS=':' read -r tests detections <<< "${category_results[$category]}"
    cat >> "$results_file" << EOF
    "$category": {
      "tests": $tests,
      "detections": $detections,
      "rate": $(echo "scale=4; $detections / $tests" | bc -l 2>/dev/null || echo "0")
    }
EOF
done

cat >> "$results_file" << EOF
  }
}
EOF

echo "✅ Massive test suite completed: $total_detections/$total_tests detections ($(echo "scale=2; $total_detections * 100 / $total_tests" | bc -l 2>/dev/null || echo "0")%)"