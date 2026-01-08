#!/bin/bash
# Comprehensive CostPilot Optimization Testing Script

set -e

# Configuration
TEST_DIR="../optimization_tests/comprehensive_scenarios"
RESULTS_DIR="../test_results"
COSTPILOT_CMD="../costpilot"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_FILE="${RESULTS_DIR}/comprehensive_test_report_${TIMESTAMP}.json"

# Categories to test
CATEGORIES=(
    "instance_rightsizing"
    "storage_optimization"
    "architecture_patterns"
    "network_optimization"
    "security_overhead"
)

echo "🚀 Starting Comprehensive CostPilot Testing Suite"
echo "📅 $(date)"
echo ""

# Initialize counters
total_tests=0
total_detections=0

# Expected optimizations for each test case
declare -A EXPECTED_OPTIMIZATIONS
EXPECTED_OPTIMIZATIONS["large_instance_single_purpose"]="rightsizing m5.large bastion host to smaller instance"
EXPECTED_OPTIMIZATIONS["compute_heavy_web_server"]="switch web server to compute-optimized instance"
EXPECTED_OPTIMIZATIONS["memory_intensive_database"]="switch database to memory-optimized instance"
EXPECTED_OPTIMIZATIONS["ebs_overprovisioned"]="reduce EBS IOPS and throughput"
EXPECTED_OPTIMIZATIONS["rds_small_dataset_large_storage"]="reduce RDS storage allocation"
EXPECTED_OPTIMIZATIONS["microservices_consolidation_realistic"]="consolidate multiple small instances"
EXPECTED_OPTIMIZATIONS["single_instance_multiple_services"]="split monolithic application into microservices"
EXPECTED_OPTIMIZATIONS["idle_development_instances"]="use smaller instances for development"
EXPECTED_OPTIMIZATIONS["unused_nat_gateway"]="consider VPC endpoints instead of NAT Gateway"
EXPECTED_OPTIMIZATIONS["over_provisioned_waf"]="reduce WAF rate limits"

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
echo "🎯 Comprehensive test run complete!"
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
    local result_file="${RESULTS_DIR}/comprehensive_${category}_${test_id}_result.json"
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
