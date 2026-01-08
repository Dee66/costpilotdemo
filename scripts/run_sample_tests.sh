#!/bin/bash
echo "🔬 Running CostPilot Detection Analysis on New Binary"
echo "=================================================="
echo ""

TOTAL_TESTS=0
TOTAL_DETECTIONS=0

# Function to test category
test_category() {
    local category=$1
    local description=$2
    local sample_file=$3
    
    if [[ -f "$sample_file" ]]; then
        echo "🧪 Testing $category: $description"
        echo "   File: $sample_file"
        
        ((TOTAL_TESTS++))
        
        # Run the test
        output=$(./costpilot scan "$sample_file" --format json 2>/dev/null)
        
        # Check for detections
        detections=$(echo "$output" | jq '.detections | length' 2>/dev/null || echo "0")
        
        if [[ "$detections" -gt 0 ]]; then
            echo "   ✅ DETECTED: $detections optimization(s) found"
            ((TOTAL_DETECTIONS++))
            
            # Show detection details
            echo "$output" | jq -r '.detections[] | "      - \(.message)"' 2>/dev/null || echo "      - Detection details unavailable"
        else
            echo "   ❌ NO DETECTIONS found"
        fi
        
        echo ""
    else
        echo "⚠️  Sample file not found: $sample_file"
        echo ""
    fi
}

# Test key categories
test_category "ECS Fargate" "Container optimization" "optimization_tests/massive_suite/containers/ecs/ecs_fargate_oversized_1.json"
test_category "EC2 Rightsizing" "Instance optimization" "optimization_tests/massive_suite/instance_rightsizing/bastion_hosts/bastion_c5_large_1.json"
test_category "RDS Storage" "Database optimization" "optimization_tests/massive_suite/storage_optimization/rds_instances/rds_db_m5_large_1000gb_30.json"
test_category "Lambda Memory" "Serverless optimization" "optimization_tests/massive_suite/serverless/lambda_high_memory_1.json"
test_category "EBS GP2->GP3" "Storage optimization" "optimization_tests/massive_suite/storage_optimization/ebs_volumes/ebs_gp2_to_gp3_1.json"
test_category "NAT Gateway" "Network optimization" "optimization_tests/massive_suite/network_optimization/nat_gateways/nat_gateway_optimization_1.json"
test_category "S3 Storage" "Object storage optimization" "optimization_tests/massive_suite/storage_optimization/s3_buckets/s3_standard_to_intelligent_1.json"

echo "�� SUMMARY:"
echo "   Total categories tested: $TOTAL_TESTS"
echo "   Categories with detections: $TOTAL_DETECTIONS"
echo "   Detection rate: $(( TOTAL_DETECTIONS * 100 / TOTAL_TESTS ))%"
echo ""
echo "💡 This is a sample analysis. Full 2000+ test suite would provide complete picture."
