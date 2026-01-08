#!/bin/bash
# Massive CostPilot Test Suite Runner
# Tests 100+ optimization scenarios

set -e

# Configuration
TEST_DIR="../optimization_tests/massive_suite"
RESULTS_DIR="../test_results"
COSTPILOT_CMD="../bin/costpilot"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_FILE="${RESULTS_DIR}/massive_test_report_${TIMESTAMP}.json"

echo "🚀 Starting MASSIVE CostPilot Testing Suite (100+ tests)"
echo "📅 $(date)"
echo ""

# Initialize counters
total_tests=0
total_detections=0
category_stats=()

# Function to analyze detection
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

# Function to log test result
log_test_result() {
    local category="$1"
    local subcategory="$2"
    local test_id="$3"
    local exit_code="$4"
    local execution_time="$5"
    local output="$6"
    local detected="$7"
    local expected="$8"
    
    # Create individual test result file
    local result_file="${RESULTS_DIR}/massive_${category}_${subcategory}_${test_id}_result.json"
    cat > "$result_file" << RESULT_EOF
{
  "category": "$category",
  "subcategory": "$subcategory",
  "test_id": "$test_id",
  "timestamp": "$TIMESTAMP",
  "exit_code": $exit_code,
  "execution_time_ms": $execution_time,
  "optimization_expected": "$expected",
  "optimization_detected": $detected,
  "costpilot_output": "$(echo "$output" | sed 's/"/\\"/g' | tr -d '\n')"
}
RESULT_EOF
}

# Expected optimizations mapping
declare -A EXPECTED_OPTIMIZATIONS

# Instance rightsizing expectations
EXPECTED_OPTIMIZATIONS["bastion_hosts"]="rightsizing large instances used for bastion/SSH access to smaller instances"
EXPECTED_OPTIMIZATIONS["web_servers"]="optimizing web server instance types for better performance/cost"
EXPECTED_OPTIMIZATIONS["databases"]="using appropriate instance families for database workloads"
EXPECTED_OPTIMIZATIONS["development"]="rightsizing development instances to smaller sizes"
EXPECTED_OPTIMIZATIONS["background_jobs"]="optimizing batch job instance configurations"

# Storage optimization expectations
EXPECTED_OPTIMIZATIONS["ebs_volumes"]="rightsizing EBS volumes and optimizing storage types"
EXPECTED_OPTIMIZATIONS["rds_instances"]="optimizing RDS storage allocations and instance types"
EXPECTED_OPTIMIZATIONS["s3_buckets"]="optimizing S3 storage configurations"
EXPECTED_OPTIMIZATIONS["efs"]="optimizing EFS storage configurations"

# Architecture pattern expectations
EXPECTED_OPTIMIZATIONS["microservices"]="consolidating multiple small microservice instances"
EXPECTED_OPTIMIZATIONS["monolithic"]="breaking down monolithic applications"
EXPECTED_OPTIMIZATIONS["development_envs"]="optimizing development environment instances"
EXPECTED_OPTIMIZATIONS["staging_envs"]="rightsizing staging environment instances"

# Network optimization expectations
EXPECTED_OPTIMIZATIONS["nat_gateways"]="replacing NAT gateways with VPC endpoints where possible"
EXPECTED_OPTIMIZATIONS["vpc_endpoints"]="optimizing VPC endpoint configurations"
EXPECTED_OPTIMIZATIONS["load_balancers"]="optimizing load balancer configurations"

# Security overhead expectations
EXPECTED_OPTIMIZATIONS["waf"]="optimizing WAF configurations and rate limits"
EXPECTED_OPTIMIZATIONS["security_groups"]="simplifying complex security group rules"
EXPECTED_OPTIMIZATIONS["iam_roles"]="optimizing IAM role configurations"

# Run tests for each category
for category_dir in "$TEST_DIR"/*/; do
    category=$(basename "$category_dir")
    category_tests=0
    category_detections=0
    
    echo "🧪 Testing category: $category"
    
    # Run tests for each subcategory
    for subcategory_dir in "$category_dir"*/; do
        if [[ -d "$subcategory_dir" ]]; then
            subcategory=$(basename "$subcategory_dir")
            subcategory_tests=0
            subcategory_detections=0
            
            echo "  📁 Subcategory: $subcategory"
            
            for test_file in "$subcategory_dir"*.json; do
                if [[ -f "$test_file" ]]; then
                    test_id=$(basename "$test_file" .json)
                    ((subcategory_tests++))
                    ((category_tests++))
                    ((total_tests++))
                    
                    # Run CostPilot
                    start_time=$(date +%s%N)
                    output=$($COSTPILOT_CMD scan "$test_file" 2>&1)
                    exit_code=$?
                    end_time=$(date +%s%N)
                    
                    execution_time=$(( (end_time - start_time) / 1000000 )) # Convert to ms
                    
                    # Analyze output for optimization detection
                    expected_opt="${EXPECTED_OPTIMIZATIONS[$subcategory]}"
                    detected=$(analyze_detection "$output" "$expected_opt")
                    
                    if [[ "$detected" == "true" ]]; then
                        ((subcategory_detections++))
                        ((category_detections++))
                        ((total_detections++))
                        echo "    ✅ $test_id"
                    else
                        echo "    ❌ $test_id"
                    fi
                    
                    # Log detailed results
                    log_test_result "$category" "$subcategory" "$test_id" "$exit_code" "$execution_time" "$output" "$detected" "$expected_opt"
                fi
            done
            
            # Subcategory summary
            subcategory_rate=0
            if [[ $subcategory_tests -gt 0 ]]; then
                subcategory_rate=$(( subcategory_detections * 100 / subcategory_tests ))
            fi
            echo "    📊 $subcategory: $subcategory_detections/$subcategory_tests detected ($subcategory_rate%)"
        fi
    done
    
    # Category summary
    category_rate=0
    if [[ $category_tests -gt 0 ]]; then
        category_rate=$(( category_detections * 100 / category_tests ))
    fi
    echo "📊 $category: $category_detections/$category_tests detected ($category_rate%)"
    echo ""
    
    # Store category stats
    category_stats+=("$category: $category_detections/$category_tests ($category_rate%)")
done

# Generate final summary
echo "🎯 MASSIVE test run complete!"
echo ""

# Calculate overall detection rate
overall_rate=0
if [[ $total_tests -gt 0 ]]; then
    overall_rate=$(( total_detections * 100 / total_tests ))
fi

echo "📈 OVERALL RESULTS (105+ tests):"
echo "   Total tests run: $total_tests"
echo "   Optimizations detected: $total_detections"
echo "   Overall detection rate: ${overall_rate}%"

if [[ $overall_rate -lt 50 ]]; then
    echo "⚠️  WARNING: Detection rate below 50% indicates significant gaps in CostPilot's optimization capabilities"
elif [[ $overall_rate -lt 75 ]]; then
    echo "⚠️  CAUTION: Detection rate below 75% indicates moderate gaps"
else
    echo "✅ GOOD: Detection rate above 75% indicates strong optimization capabilities"
fi

echo ""
echo "📊 CATEGORY BREAKDOWN:"
for stat in "${category_stats[@]}"; do
    echo "   $stat"
done

echo ""
echo "📄 Detailed results saved in: $RESULTS_DIR"
echo "💡 Use these results to guide CostPilot optimization enhancements!"
