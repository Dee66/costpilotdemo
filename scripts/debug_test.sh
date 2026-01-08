#!/bin/bash
set -e

echo "Testing costpilot command..."
output=$(../costpilot scan ../optimization_tests/instance_rightsizing/burstable_overprovision.json 2>&1)
exit_code=$?
echo "Exit code: $exit_code"
echo "Output:"
echo "$output"
echo "Done"
