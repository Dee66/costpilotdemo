#!/bin/bash
# Simplified CostPilot Optimization Testing Script

# Configuration
TEST_DIR="../optimization_tests"
RESULTS_DIR="../test_results"
COSTPILOT_CMD="../bin/costpilot"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Categories to test
CATEGORIES=(
    "instance_rightsizing"
    "storage_optimization"
    "architecture_patterns"
)

echo "🚀 Starting CostPilot Optimization Testing Suite"
echo "�� $(date)"
echo ""

# Initialize counters
total_tests=0
total_detections=0

# Run tests for each category
for category in "${CATEGORIES[@]}"; do
    category_dir="$TEST_DIR/$category"
    test_count=0
    detection_count=0
    
    echo "🧪 Testing category: $category"
    
    if [[ ! -d "$category_dir" ]]; then
        echo "⚠️  Category directory not found: $category_dir"
        continue
    fi
    
    for test_file in "$category_dir"/*.json; do
        if [[ -f "$test_file" ]]; then
            test_id=$(basename "$test_file" .json)
            ((test_count++))
            ((total_tests++))
            
            echo "  📋 Running test: $test_id"
            
            # Run CostPilot
            output=$($COSTPILOT_CMD scan "$test_file" 2>&1)
            exit_code=$?
            
            # Simple detection check
            if echo "$output" | grep -qi "optimization\|recommend\|rightsizing\|efficiency\|savings"; then
                detected="true"
                ((detection_count++))
                ((total_detections++))
                echo "    ✅ Optimization detected"
            else
                detected="false"
                echo "    ❌ Optimization NOT detected"
            fi
            
            # Log result
            result_file="${RESULTS_DIR}/${category}_${test_id}_result.json"
            cat > "$result_file" << RESULT_EOF
{
  "test_id": "$test_id",
  "category": "$category",
  "timestamp": "$TIMESTAMP",
  "exit_code": $exit_code,
  "optimization_detected": $detected,
  "costpilot_output": "$(echo "$output" | sed 's/"/\\"/g' | tr -d '\n')"
}
RESULT_EOF
        fi
    done
    
    echo "📊 $category: $detection_count/$test_count optimizations detected"
    echo ""
done

echo "🎯 Test run complete!"
echo ""
echo "📈 Overall Results:"
echo "   Total tests run: $total_tests"
echo "   Optimizations detected: $total_detections"

if [[ $total_tests -gt 0 ]]; then
    rate=$(( total_detections * 100 / total_tests ))
    echo "   Overall detection rate: ${rate}%"
    
    if [[ $rate -lt 50 ]]; then
        echo "⚠️  WARNING: Detection rate below 50% indicates significant gaps"
    fi
fi

echo ""
echo "📄 Detailed results saved in: $RESULTS_DIR"
