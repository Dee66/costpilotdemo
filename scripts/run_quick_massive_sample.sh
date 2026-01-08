#!/bin/bash
# Quick Sample of Massive CostPilot Test Suite
# Runs a representative sample from each category

echo "🚀 MASSIVE CostPilot Test Suite - QUICK SAMPLE (18 tests)"
echo "📅 $(date)"
echo ""

# Configuration
COSTPILOT_CMD="../costpilot"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Initialize counters
total_tests=0
total_detections=0

# Function to run a test
run_test() {
    local test_file="$1"
    local expected="$2"
    
    ((total_tests++))
    
    echo "  📋 $(basename "$test_file" .json)"
    
    # Run CostPilot
    output=$($COSTPILOT_CMD scan "$test_file" 2>&1)
    exit_code=$?
    
    # Check for optimization detection
    if echo "$output" | grep -qi "optimization\|recommend\|rightsizing\|efficiency\|savings"; then
        ((total_detections++))
        echo "    ✅ DETECTED"
    else
        echo "    ❌ NOT DETECTED"
    fi
}

echo "🧪 INSTANCE RIGHTSIZING SAMPLES:"
echo "  Bastion Hosts:"
run_test "optimization_tests/massive_suite/instance_rightsizing/bastion_hosts/bastion_m5_large.json" "rightsizing bastion host"
run_test "optimization_tests/massive_suite/instance_rightsizing/bastion_hosts/bastion_heavy_m5_2xlarge.json" "rightsizing bastion host"

echo "  Web Servers:"
run_test "optimization_tests/massive_suite/instance_rightsizing/web_servers/web_m5_large_1.json" "web server optimization"
run_test "optimization_tests/massive_suite/instance_rightsizing/web_servers/web_heavy_m5_2xlarge.json" "web server optimization"

echo "  Databases:"
run_test "optimization_tests/massive_suite/instance_rightsizing/databases/db_c5_large_1.json" "database optimization"
run_test "optimization_tests/massive_suite/instance_rightsizing/databases/db_heavy_m5_2xlarge.json" "database optimization"

echo ""
echo "🧪 STORAGE OPTIMIZATION SAMPLES:"
echo "  EBS Volumes:"
run_test "optimization_tests/massive_suite/storage_optimization/ebs_volumes/ebs_1000gb_gp2.json" "EBS optimization"
run_test "optimization_tests/massive_suite/storage_optimization/ebs_volumes/massive_ebs_10000gb_gp2.json" "EBS optimization"

echo "  RDS Instances:"
run_test "optimization_tests/massive_suite/storage_optimization/rds_instances/rds_db_t3_micro_1000gb.json" "RDS optimization"
run_test "optimization_tests/massive_suite/storage_optimization/rds_instances/large_small_storage_db_t3_large_50gb.json" "RDS optimization"

echo ""
echo "🧪 ARCHITECTURE PATTERNS SAMPLES:"
echo "  Microservices:"
run_test "optimization_tests/massive_suite/architecture_patterns/microservices/3_microservices.json" "microservice consolidation"
run_test "optimization_tests/massive_suite/architecture_patterns/microservices/10_microservices_micro.json" "microservice consolidation"

echo "  Development Environments:"
run_test "optimization_tests/massive_suite/architecture_patterns/development_envs/3_dev_instances.json" "dev environment optimization"
run_test "optimization_tests/massive_suite/architecture_patterns/staging_envs/5_staging_instances.json" "staging environment optimization"

echo ""
echo "🧪 NETWORK OPTIMIZATION SAMPLES:"
run_test "optimization_tests/massive_suite/network_optimization/nat_gateways/nat_gateway_1.json" "NAT gateway optimization"
run_test "optimization_tests/massive_suite/network_optimization/vpc_endpoints/s3_endpoint.json" "VPC endpoint optimization"

echo ""
echo "🧪 SECURITY OVERHEAD SAMPLES:"
run_test "optimization_tests/massive_suite/security_overhead/waf/massive_waf_50000_limit.json" "WAF optimization"
run_test "optimization_tests/massive_suite/security_overhead/security_groups/sg_100_rules.json" "security group optimization"

echo ""
echo "🎯 SAMPLE TEST COMPLETE!"
echo ""

# Calculate detection rate
if [[ $total_tests -gt 0 ]]; then
    rate=$(( total_detections * 100 / total_tests ))
    echo "📈 SAMPLE RESULTS (18/105+ tests):"
    echo "   Tests run: $total_tests"
    echo "   Optimizations detected: $total_detections"
    echo "   Detection rate: ${rate}%"
    
    if [[ $rate -eq 0 ]]; then
        echo "🚨 CRITICAL: Zero detection rate indicates major gaps in CostPilot"
    elif [[ $rate -lt 50 ]]; then
        echo "⚠️  WARNING: Low detection rate indicates significant optimization gaps"
    fi
fi

echo ""
echo "💡 Full massive suite contains 105+ tests across all categories!"
echo "   Run 'find optimization_tests/massive_suite/ -name \"*.json\" | wc -l' to count all tests"
