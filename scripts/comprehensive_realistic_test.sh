#!/bin/bash

# Comprehensive CostPilot Test Suite Runner for Realistic Plans

BINARY="./bin/costpilot"
TEST_DIR="optimization_tests/realistic_plans"
OUTPUT_FILE="comprehensive_test_results_$(date +%Y%m%d_%H%M%S).txt"

echo "🚀 Running Comprehensive CostPilot Detection Analysis"
echo "=================================================="
echo "Testing all files in: $TEST_DIR"
echo ""

# Initialize counters
total_files=0
total_detections=0
error_files=0
high_priority=0
medium_priority=0
low_priority=0

# Create output file header
{
echo "=== Comprehensive CostPilot Test Results ==="
echo "Started: $(date)"
echo "Binary: $($BINARY --version | head -2 | tail -1)"
echo "Test Directory: $TEST_DIR"
echo ""
} > "$OUTPUT_FILE"

echo "🔍 Scanning test files..."

# Find all JSON files recursively
while IFS= read -r file; do
    ((total_files++))
    relative_path="${file#$TEST_DIR/}"

    # Progress indicator
    if (( total_files % 100 == 0 )); then
        echo "   Processed $total_files files... ($total_detections total detections)"
    fi

    # Run the test
    if output=$(timeout 30s "$BINARY" scan "$file" --format json 2>&1); then
        # Extract JSON part from output (skip warnings and banner)
        json_output=$(echo "$output" | sed -n '/^{/,$p')

        # Extract detections
        detections=$(echo "$json_output" | jq -r '.detections | length' 2>/dev/null || echo "0")

        if [[ "$detections" -gt 0 ]]; then
            ((total_detections += detections))

            # Count by priority (using severity field)
            high_count=$(echo "$json_output" | jq -r '[.detections[] | select(.severity == "High")] | length' 2>/dev/null || echo "0")
            medium_count=$(echo "$json_output" | jq -r '[.detections[] | select(.severity == "Medium")] | length' 2>/dev/null || echo "0")
            low_count=$(echo "$json_output" | jq -r '[.detections[] | select(.severity == "Low")] | length' 2>/dev/null || echo "0")

            ((high_priority += high_count))
            ((medium_priority += medium_count))
            ((low_priority += low_count))

            echo "$relative_path: $detections detections ($high_count high, $medium_count medium, $low_count low)" >> "$OUTPUT_FILE"
        else
            echo "$relative_path: 0 detections" >> "$OUTPUT_FILE"
        fi
    else
        ((error_files++))
        echo "$relative_path: ERROR - $(echo "$output" | head -1)" >> "$OUTPUT_FILE"
    fi
done < <(find "$TEST_DIR" -name "*.json" -type f)

# Generate summary
{
echo ""
echo "=== SUMMARY ==="
echo "Total files processed: $total_files"
echo "Files with errors: $error_files"
echo "Total detections: $total_detections"
echo "Detection breakdown by priority:"
echo "  High priority: $high_priority"
echo "  Medium priority: $medium_priority"
echo "  Low priority: $low_priority"
echo "Detection rate: $(( total_detections * 100 / (total_files - error_files) ))%"
echo "Completed: $(date)"
} >> "$OUTPUT_FILE"

# Display summary to console
echo ""
echo "📊 SUMMARY:"
echo "   Total files tested: $total_files"
echo "   Files with errors: $error_files"
echo "   Total detections: $total_detections"
echo "   Priority breakdown:"
echo "     High: $high_priority"
echo "     Medium: $medium_priority"
echo "     Low: $low_priority"
echo "   Detection rate: $(( total_detections * 100 / (total_files - error_files) ))%"
echo ""
echo "📄 Detailed results saved to: $OUTPUT_FILE"
echo ""
echo "✅ Comprehensive testing complete!"