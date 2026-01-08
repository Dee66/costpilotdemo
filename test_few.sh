#!/bin/bash

# Test just a few files
TEST_FILES=(
    "optimization_tests/massive_suite/api/api_gateway/api_gw_EDGE_11.json"
    "optimization_tests/massive_suite/storage_optimization/rds_instances/large_small_storage_db_t3_large_50gb.json"
)

RESULTS_FILE="/tmp/mini_results.json"

# Initialize results
cat > "$RESULTS_FILE" << 'EOF_JSON'
{
  "run_id": "mini_test",
  "timestamp": "2026-01-06T19:15:14+02:00",
  "total_tests": 2,
  "costpilot_version": "test",
  "results": {
    "summary": {
      "tests_run": 0,
      "optimizations_detected": 0,
      "detection_rate": 0.0,
      "total_cost_savings": 0.0
    },
    "by_category": {},
    "by_subcategory": {},
    "failures": [],
    "successes": []
  }
}
EOF_JSON

for test_file in "${TEST_FILES[@]}"; do
    echo "Testing: $test_file"
    
    # Extract category and subcategory from path
    category=$(echo "$test_file" | cut -d'/' -f3)
    subcategory=$(echo "$test_file" | cut -d'/' -f4)
    test_name=$(basename "$test_file" .json)
    
    echo "Category: $category, Subcategory: $subcategory, Test: $test_name"
    
    # Run CostPilot
    costpilot_output=$(timeout 30s ./costpilot scan "$test_file" 2>/dev/null)
    exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        # Analyze output
        optimization_count=0
        cost_savings=0
        
        if echo "$costpilot_output" | grep -q "optimization\|saving\|recommendation\|rightsizing\|over-provisioned\|under-utilized\|cost reduction\|cost savings"; then
            optimization_count=1
            cost_savings=$(echo "$costpilot_output" | grep -o '$[0-9]\+\.[0-9]\+' | head -1 | sed 's/\$//' | cut -d'.' -f1 || echo "0")
            if [ "$cost_savings" = "0" ]; then
                cost_savings=$(echo "$costpilot_output" | grep -o '[0-9]\+\.[0-9]\+.*month' | head -1 | cut -d'.' -f1 || echo "50")
            fi
        fi
        
        echo "Optimization count: $optimization_count, Cost savings: $cost_savings"
        
        if [ "$optimization_count" -gt 0 ]; then
            echo "✅ DETECTED"
            
            # Update results with jq
            jq --arg category "$category" --arg subcategory "$subcategory" --arg test_name "$test_name" \
               --argjson count "$optimization_count" --argjson savings "$cost_savings" \
               '.results.summary.tests_run += 1 |
                .results.summary.optimizations_detected += $count |
                .results.summary.total_cost_savings += $savings |
                .results.by_category[$category].tests_run = (.results.by_category[$category].tests_run // 0) + 1 |
                .results.by_category[$category].optimizations_detected = (.results.by_category[$category].optimizations_detected // 0) + $count |
                .results.by_subcategory[$category + "/" + $subcategory].tests_run = (.results.by_subcategory[$category + "/" + $subcategory].tests_run // 0) + 1 |
                .results.by_subcategory[$category + "/" + $subcategory].optimizations_detected = (.results.by_subcategory[$category + "/" + $subcategory].optimizations_detected // 0) + $count |
                .results.successes += [{"category": $category, "subcategory": $subcategory, "test": $test_name, "optimizations": $count, "savings": $savings}]' \
               "$RESULTS_FILE" > "${RESULTS_FILE}.tmp" && mv "${RESULTS_FILE}.tmp" "$RESULTS_FILE" || echo "JQ FAILED"
        else
            echo "❌ NOT DETECTED"
        fi
    else
        echo "❌ COSTPILOT FAILED (exit code $exit_code)"
    fi
    
    echo "---"
done

echo "Final results:"
cat "$RESULTS_FILE" | jq '.results.summary'
