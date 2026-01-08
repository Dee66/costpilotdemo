#!/bin/bash

# CostPilot Test Suite Runner
# Runs the CostPilot binary against all test files and collects results

set -e

BINARY="./bin/costpilot"
TEST_DIR="optimization_tests/massive_suite"
OUTPUT_DIR="test_results_$(date +%Y%m%d_%H%M%S)"
LOG_FILE="${OUTPUT_DIR}/test_log.txt"
SUMMARY_FILE="${OUTPUT_DIR}/summary.json"

echo "=== CostPilot Test Suite Runner ==="
echo "Binary: $BINARY"
echo "Test Directory: $TEST_DIR"
echo "Output Directory: $OUTPUT_DIR"
echo "Starting tests at $(date)"
echo

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Initialize counters
total_files=0
processed_files=0
detection_count=0
error_count=0
total_cost=0

# Function to process a single test file
process_file() {
    local file="$1"
    local relative_path="${file#$TEST_DIR/}"

    ((total_files++))

    # Run costpilot scan
    if output=$(timeout 30s "$BINARY" scan "$file" --format json 2>&1); then
        # Extract detection count from JSON output
        detections=$(echo "$output" | jq -r '.detections | length' 2>/dev/null || echo "0")
        monthly_cost=$(echo "$output" | jq -r '.summary.monthly_cost' 2>/dev/null || echo "0")

        ((processed_files++))
        detection_count=$((detection_count + detections))
        total_cost=$(echo "$total_cost + $monthly_cost" | bc -l 2>/dev/null || echo "$total_cost")

        # Log successful processing
        echo "✅ $relative_path: $detections detections, \$$monthly_cost/month" >> "$LOG_FILE"
    else
        ((error_count++))
        echo "❌ $relative_path: ERROR - $output" >> "$LOG_FILE"
    fi
}

# Find all JSON files and process them sequentially
echo "Finding and processing test files..."
while IFS= read -r file; do
    process_file "$file"
    # Show progress every 100 files
    if (( total_files % 100 == 0 )); then
        echo "Processed $total_files files... ($processed_files successful, $detection_count detections)"
    fi
done < <(find "$TEST_DIR" -name "*.json" -type f)

# Generate summary
echo "=== Test Results Summary ===" > "$SUMMARY_FILE"
echo "Test Run Date: $(date)" >> "$SUMMARY_FILE"
echo "Binary Version: $($BINARY --version | head -2 | tail -1)" >> "$SUMMARY_FILE"
echo "Total Test Files: $total_files" >> "$SUMMARY_FILE"
echo "Successfully Processed: $processed_files" >> "$SUMMARY_FILE"
echo "Errors: $error_count" >> "$SUMMARY_FILE"
echo "Total Detections: $detection_count" >> "$SUMMARY_FILE"
echo "Total Monthly Cost: \$$total_cost" >> "$SUMMARY_FILE"
detection_rate=$(echo "scale=2; if ($processed_files > 0) $detection_count * 100 / $processed_files else 0" | bc -l 2>/dev/null || echo "0")
echo "Detection Rate: ${detection_rate}%" >> "$SUMMARY_FILE"

# Print summary to console
cat "$SUMMARY_FILE"
echo
echo "Detailed results saved to: $OUTPUT_DIR/"
echo "Log file: $LOG_FILE"
echo "Summary: $SUMMARY_FILE"