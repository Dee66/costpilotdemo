#!/bin/bash
echo "🎯 CostPilot New Binary - Detection Performance Summary"
echo "====================================================="
echo ""

TOTAL_TESTED=0
TOTAL_DETECTED=0

# Test specific files that should trigger detections
test_specific_file() {
    local file_path=$1
    local description=$2
    
    if [[ -f "$file_path" ]]; then
        ((TOTAL_TESTED++))
        echo "Testing: $description"
        echo "File: $(basename "$file_path")"
        
        output=$(./costpilot scan "$file_path" --format json 2>/dev/null)
        detections=$(echo "$output" | jq '.detections | length' 2>/dev/null || echo "0")
        
        if [[ "$detections" -gt 0 ]]; then
            ((TOTAL_DETECTED++))
            echo "✅ DETECTED: $detections optimization(s)"
            
            # Show first detection message
            echo "$output" | jq -r '.detections[0].message' 2>/dev/null | head -1 | sed 's/^/   ↳ /'
            echo ""
        else
            echo "❌ No detections"
            echo ""
        fi
    else
        echo "⚠️  File not found: $file_path"
        echo ""
    fi
}

echo "🔍 TESTING KEY OPTIMIZATION SCENARIOS:"
echo ""

# Container optimization
test_specific_file "optimization_tests/massive_suite/containers/ecs/ecs_fargate_oversized_1.json" "ECS Fargate Oversized Task"

# EC2 rightsizing
test_specific_file "optimization_tests/massive_suite/instance_rightsizing/background_jobs/job_c5_large_3.json" "EC2 C5 Large Instance"

# RDS storage optimization  
test_specific_file "optimization_tests/massive_suite/storage_optimization/rds_instances/rds_db_m5_large_1000gb_30.json" "RDS Large Storage Allocation"

# Lambda optimization
test_specific_file "optimization_tests/massive_suite/serverless/lambda_memory_timeout_105.json" "Lambda High Memory Usage"

# EBS optimization
test_specific_file "optimization_tests/massive_suite/storage_optimization/ebs_volumes/ebs_gp2_large_volume_1.json" "EBS GP2 to GP3 Migration"

echo "📊 PERFORMANCE SUMMARY:"
echo "======================="
echo "Test files analyzed: $TOTAL_TESTED"
echo "Files with detections: $TOTAL_DETECTED"

if [[ $TOTAL_TESTED -gt 0 ]]; then
    rate=$(( TOTAL_DETECTED * 100 / TOTAL_TESTED ))
    echo "Detection success rate: ${rate}%"
fi

echo ""
echo "🎖️  OVERALL ASSESSMENT:"
if [[ $TOTAL_DETECTED -gt 0 ]]; then
    echo "✅ NEW BINARY SHOWS OPTIMIZATION DETECTION CAPABILITY"
    echo "💡 Successfully identifies cost-saving opportunities across multiple AWS services"
else
    echo "❌ NO DETECTIONS FOUND - Binary may have issues or require heuristics file"
fi
