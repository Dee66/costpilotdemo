#!/bin/bash
set -e

echo "Testing full logic..."

# Simulate the variables
test_id="burstable_overprovision"
category="instance_rightsizing"
TIMESTAMP="test"
expected_opt="rightsizing t3.large to smaller instance"

# Run CostPilot
start_time=$(date +%s%N)
output=$(../costpilot scan ../optimization_tests/instance_rightsizing/burstable_overprovision.json 2>&1)
exit_code=$?
end_time=$(date +%s%N)

execution_time=$(( (end_time - start_time) / 1000000 )) # Convert to ms

echo "Exit code: $exit_code"
echo "Execution time: $execution_time ms"

# Analyze output for optimization detection
detected=$(analyze_detection "$output" "$expected_opt")

echo "Detected: $detected"

if [[ "$detected" == "true" ]]; then
    echo "Optimization detected"
else
    echo "Optimization NOT detected"
fi

# Test log function
log_test_result "$category" "$test_id" "$exit_code" "$execution_time" "$output" "$detected" "$expected_opt"

echo "Done"

# Analyze detection function
analyze_detection() {
    local output="$1"
    local expected="$2"
    
    echo "Analyzing output: $output" >&2
    
    # Simple analysis - check if output contains optimization-related keywords
    if echo "$output" | grep -qi "cost\|optimization\|recommend\|rightsizing\|efficiency\|savings"; then
        echo "true"
    else
        echo "false"
    fi
}

# Log individual test result
log_test_result() {
    local category="$1"
    local test_id="$2"
    local exit_code="$3"
    local execution_time="$4"
    local output="$5"
    local detected="$6"
    local expected="$7"
    
    echo "Logging result for $category/$test_id"
    
    # Create individual test result file
    local result_file="../test_results/${category}_${test_id}_result.json"
    echo "Result file: $result_file"
    
    cat > "$result_file" << RESULT_EOF
{
  "test_id": "$test_id",
  "category": "$category",
  "timestamp": "$TIMESTAMP",
  "exit_code": $exit_code,
  "execution_time_ms": $execution_time,
  "optimization_expected": "$expected",
  "optimization_detected": $detected,
  "costpilot_output": "$(echo "$output" | sed 's/"/\\"/g' | sed 's/$/\\n/' | tr -d '\n')"
}
RESULT_EOF

    echo "Result logged"
}
