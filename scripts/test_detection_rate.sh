#!/bin/bash

# Test CostPilot CLI detection rate on all 5000 realistic Terraform plan variations
echo "Testing CostPilot CLI detection rate on 5000 realistic Terraform plans..."

total_files=0
files_with_optimizations=0
total_optimizations=0

# Function to test a single file
test_file() {
    local file_path=$1
    local output

    # Run costpilot scan and capture output
    output=$(./bin/costpilot scan "$file_path" 2>/dev/null)

    # Check if output contains optimization opportunities
    if echo "$output" | grep -q "optimization opportunities detected"; then
        # Extract number of optimizations
        optimizations=$(echo "$output" | grep "optimization opportunities detected" | sed 's/.*\([0-9]\+\) optimization opportunities detected.*/\1/')
        ((files_with_optimizations++))
        ((total_optimizations += optimizations))
        echo "✓ $file_path: $optimizations optimizations"
    else
        echo "✗ $file_path: 0 optimizations"
    fi

    ((total_files++))
}

# Test all files in each category
echo "=== TESTING WEB APPLICATION STACKS ==="
for file in optimization_tests/realistic_plans/web_apps/*.json; do
    test_file "$file"
done

echo "=== TESTING DATA PROCESSING PIPELINES ==="
for file in optimization_tests/realistic_plans/data_pipelines/*.json; do
    test_file "$file"
done

echo "=== TESTING MICROSERVICES ARCHITECTURES ==="
for file in optimization_tests/realistic_plans/microservices/*.json; do
    test_file "$file"
done

echo "=== TESTING DEV/TEST ENVIRONMENTS ==="
for file in optimization_tests/realistic_plans/dev_environments/*.json; do
    test_file "$file"
done

echo "=== TESTING LEGACY SYSTEM MIGRATIONS ==="
for file in optimization_tests/realistic_plans/legacy_systems/*.json; do
    test_file "$file"
done

# Calculate detection rate
detection_rate=$(echo "scale=2; ($files_with_optimizations / $total_files) * 100" | bc)
average_optimizations_per_file=$(echo "scale=2; $total_optimizations / $total_files" | bc)

echo ""
echo "=== DETECTION RESULTS ==="
echo "Total files tested: $total_files"
echo "Files with optimizations: $files_with_optimizations"
echo "Detection rate: $detection_rate%"
echo "Total optimizations found: $total_optimizations"
echo "Average optimizations per file: $average_optimizations_per_file"