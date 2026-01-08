#!/bin/bash
# Simple Comprehensive CostPilot Optimization Testing Script

# Configuration
TEST_DIR="../optimization_tests/comprehensive_scenarios"
RESULTS_DIR="../test_results"
COSTPILOT_CMD="../costpilot"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Categories to test
CATEGORIES=(
    "instance_rightsizing"
    "storage_optimization"
    "architecture_patterns"
    "network_optimization"
    "security_overhead"
)

echo "🚀 Starting Simple Comprehensive CostPilot Testing Suite"
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
            result_file="${RESULTS_DIR}/simple_comprehensive_${category}_${test_id}_result.json"
            cat > "$result_file" << RESULT_EOF
{
  "test_id": "$test_id",
  "category": "$category",
  "timestamp": "$TIMESTAMP",
  "exit_code": $exit_code,
  "optimization_expected": "${EXPECTED_OPTIMIZATIONS[$test_id]}",
  "optimization_detected": $detected,
  "costpilot_output": "$(echo "$output" | sed 's/"/\\"/g' | tr -d '\n')"
}
RESULT_EOF
        fi
    done
    
    echo "📊 $category: $detection_count/$test_count optimizations detected"
    echo ""
done

echo "🎯 Simple comprehensive test run complete!"
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
