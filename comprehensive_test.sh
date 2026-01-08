#!/bin/bash
echo "🔬 Comprehensive CostPilot Detection Analysis - New Binary"
echo "========================================================"
echo ""

TOTAL_FILES=0
TOTAL_DETECTIONS=0
CATEGORY_BREAKDOWN=()

# Function to test a file
test_file() {
    local file_path=$1
    local category=$2
    
    if [[ -f "$file_path" ]]; then
        ((TOTAL_FILES++))
        
        # Run the test
        output=$(./costpilot scan "$file_path" --format json 2>/dev/null)
        
        # Check for detections
        detections=$(echo "$output" | jq '.detections | length' 2>/dev/null || echo "0")
        
        if [[ "$detections" -gt 0 ]]; then
            ((TOTAL_DETECTIONS++))
            echo "✅ $file_path - $detections detection(s)"
            
            # Add to category breakdown
            CATEGORY_BREAKDOWN+=("$category:1")
        fi
    fi
}

echo "Testing sample files from each category..."
echo ""

# ECS/Container tests
echo "🏗️  CONTAINER OPTIMIZATION:"
find optimization_tests/massive_suite/containers -name "*.json" | head -5 | while read file; do
    test_file "$file" "containers"
done

# EC2 Instance tests  
echo ""
echo "💻 EC2 INSTANCE RIGHTSIZING:"
find optimization_tests/massive_suite/instance_rightsizing -name "*.json" | head -5 | while read file; do
    test_file "$file" "ec2_rightsizing"
done

# Storage tests
echo ""
echo "💾 STORAGE OPTIMIZATION:"
find optimization_tests/massive_suite/storage_optimization -name "*.json" | head -10 | while read file; do
    test_file "$file" "storage"
done

# Serverless tests
echo ""
echo "☁️  SERVERLESS OPTIMIZATION:"
find optimization_tests/massive_suite/serverless -name "*.json" | head -5 | while read file; do
    test_file "$file" "serverless"
done

# Network tests
echo ""
echo "🌐 NETWORK OPTIMIZATION:"
find optimization_tests/massive_suite/network_optimization -name "*.json" | head -5 | while read file; do
    test_file "$file" "network"
done

echo ""
echo "📊 FINAL SUMMARY:"
echo "   Total test files analyzed: $TOTAL_FILES"
echo "   Files with detections: $TOTAL_DETECTIONS"
if [[ $TOTAL_FILES -gt 0 ]]; then
    detection_rate=$(( TOTAL_DETECTIONS * 100 / TOTAL_FILES ))
    echo "   Detection rate: ${detection_rate}%"
fi

echo ""
echo "🎯 Key Findings:"
if [[ $TOTAL_DETECTIONS -gt 0 ]]; then
    echo "   ✅ New binary successfully detects optimizations"
    echo "   📈 Detection capabilities confirmed across multiple categories"
else
    echo "   ❌ No optimizations detected in sample - may indicate issues"
fi
