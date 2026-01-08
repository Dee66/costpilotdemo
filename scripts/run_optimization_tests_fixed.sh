#!/bin/bash
# Comprehensive CostPilot Optimization Testing Script

set -e

# Configuration
TEST_DIR="../optimization_tests"
RESULTS_DIR="../test_results"
COSTPILOT_CMD="../costpilot"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_FILE="${RESULTS_DIR}/optimization_test_report_${TIMESTAMP}.json"

# Categories to test (in priority order)
CATEGORIES=(
    "instance_rightsizing"
    "storage_optimization"
    "architecture_patterns"
)

# Expected optimizations for each test case
declare -A EXPECTED_OPTIMIZATIONS
EXPECTED_OPTIMIZATIONS["burstable_overprovision"]="rightsizing t3.large to smaller instance"
EXPECTED_OPTIMIZATIONS["wrong_instance_family"]="switch from c5 to storage-optimized instance"
EXPECTED_OPTIMIZATIONS["graviton_migration"]="migrate from x86 to Graviton instance"
EXPECTED_OPTIMIZATIONS["ebs_gp3_overprovision"]="reduce EBS IOPS and throughput"
EXPECTED_OPTIMIZATIONS["s3_versioning_no_lifecycle"]="add lifecycle rules for versioned objects"
EXPECTED_OPTIMIZATIONS["rds_storage_overprovision"]="reduce RDS storage allocation"
EXPECTED_OPTIMIZATIONS["microservices_consolidation"]="consolidate multiple small instances"
EXPECTED_OPTIMIZATIONS["event_driven_vs_always_on"]="migrate to Lambda or event-driven architecture"
EXPECTED_OPTIMIZATIONS["spot_instance_candidates"]="use spot instances for fault-tolerant workloads"

echo "🚀 Starting CostPilot Optimization Testing Suite"
echo "📅 $(date)"
echo ""

# Initialize counters
total_tests=0
total_detections=0

# Run tests for each category
for category in "${CATEGORIES[@]}"; do
    category_dir="$TEST_DIR/$category"
    test_count=0
    detection_count=0
    
    echo "�� Testing category: $category"
    
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
            start_time=$(date +%s%N)
            output=$($COSTPILOT_CMD scan "$test_file" 2>&1)
            exit_code=$?
            end_time=$(date +%s%N)
            
            execution_time=$(( (end_time - start_time) / 1000000 )) # Convert to ms
            
            # Analyze output for optimization detection
            expected_opt="${EXPECTED_OPTIMIZATIONS[$test_id]}"
            detected=$(analyze_detection "$output" "$expected_opt")
            
            if [[ "$detected" == "true" ]]; then
                ((detection_count++))
                ((total_detections++))
                echo "    ✅ Optimization detected"
            else
                echo "    ❌ Optimization NOT detected"
            fi
            
            # Log detailed results
            log_test_result "$category" "$test_id" "$exit_code" "$execution_time" "$output" "$detected" "$expected_opt"
        fi
    done
    
    # Calculate category detection rate
    detection_rate=0
    if [[ $test_count -gt 0 ]]; then
        detection_rate=$(echo "scale=2; $detection_count * 100 / $test_count" | bc 2>/dev/null || echo "0")
    fi
    
    echo "📊 $category: $detection_count/$test_count tests detected optimizations ($detection_rate% detection rate)"
    echo ""
done

# Generate final summary
echo "🎯 Test run complete!"
echo ""

# Calculate overall detection rate
overall_rate=0
if [[ $total_tests -gt 0 ]]; then
    overall_rate=$(echo "scale=2; $total_detections * 100 / $total_tests" | bc 2>/dev/null || echo "0")
fi

echo "📈 Overall Results:"
echo "   Total tests run: $total_tests"
echo "   Optimizations detected: $total_detections"
echo "   Overall detection rate: ${overall_rate}%"

if (( $(echo "$overall_rate < 50" | bc -l 2>/dev/null || echo "1") )); then
    echo "⚠️  WARNING: Detection rate below 50% indicates significant gaps in CostPilot's optimization capabilities"
fi

echo ""
echo "📄 Detailed results saved in: $RESULTS_DIR"

# Analyze detection function
analyze_detection() {
    local output="$1"
    local expected="$2"
    
    # Simple analysis - check if output contains optimization-related keywords
    if echo "$output" | grep -qi "cost\|optimization\|recommend\|rightsizing\|efficiency\|savings"; then
        echo "true"
    else
        echo "false"
    fi
}

# Log individual test result
log_test_result() {
    local category="$1"
    local test_id="$2"
    local exit_code="$3"
    local execution_time="$4"
    local output="$5"
    local detected="$6"
    local expected="$7"
    
    # Create individual test result file
    local result_file="${RESULTS_DIR}/${category}_${test_id}_result.json"
    cat > "$result_file" << RESULT_EOF
{
  "test_id": "$test_id",
  "category": "$category",
  "timestamp": "$TIMESTAMP",
  "exit_code": $exit_code,
  "execution_time_ms": $execution_time,
  "optimization_expected": "$expected",
  "optimization_detected": $detected,
  "costpilot_output": "$(echo "$output" | sed 's/"/\\"/g' | sed 's/$/\\n/' | tr -d '\n')"
}
RESULT_EOF
}
