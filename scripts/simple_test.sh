#!/bin/bash

# Simple CostPilot Test Suite Runner

BINARY="./costpilot"
TEST_DIR="optimization_tests/massive_suite"
OUTPUT_FILE="test_results_$(date +%Y%m%d_%H%M%S).txt"

echo "=== CostPilot Test Results ===" > "$OUTPUT_FILE"
echo "Started: $(date)" >> "$OUTPUT_FILE"
echo "Binary: $($BINARY --version | head -2 | tail -1)" >> "$OUTPUT_FILE"
echo >> "$OUTPUT_FILE"

total_files=0
total_detections=0
error_files=0

echo "Running tests on all 3000 files... This may take several minutes."

while IFS= read -r file; do
    ((total_files++))
    relative_path="${file#$TEST_DIR/}"

    if output=$(timeout 30s "$BINARY" scan "$file" --format json 2>&1); then
        # Extract JSON part from output (skip warnings and banner)
        json_output=$(echo "$output" | sed -n '/^{/,$p')
        # Extract number of detections
        detections=$(echo "$json_output" | jq -r '.detections | length' 2>/dev/null || echo "0")
        total_detections=$((total_detections + detections))

        echo "$relative_path: $detections detections" >> "$OUTPUT_FILE"
    else
        ((error_files++))
        echo "$relative_path: ERROR" >> "$OUTPUT_FILE"
    fi

    # Progress indicator
    if (( total_files % 100 == 0 )); then
        echo "Processed $total_files files... ($total_detections total detections)"
    fi
done < <(find "$TEST_DIR" -name "*.json" -type f)

# Summary
echo >> "$OUTPUT_FILE"
echo "=== SUMMARY ===" >> "$OUTPUT_FILE"
echo "Total files processed: $total_files" >> "$OUTPUT_FILE"
echo "Files with errors: $error_files" >> "$OUTPUT_FILE"
echo "Total detections: $total_detections" >> "$OUTPUT_FILE"
echo "Detection rate: $(( total_detections * 100 / (total_files - error_files) ))%" >> "$OUTPUT_FILE"
echo "Completed: $(date)" >> "$OUTPUT_FILE"

echo
echo "=== FINAL RESULTS ==="
echo "Total files: $total_files"
echo "Errors: $error_files"
echo "Total detections: $total_detections"
echo "Detection rate: $(( total_detections * 100 / (total_files - error_files) ))%"
echo
echo "Full results saved to: $OUTPUT_FILE"