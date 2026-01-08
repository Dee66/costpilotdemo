#!/bin/bash

# Generate meaningful Lambda function optimization test files
# Focus on memory allocation and timeout configurations that should trigger detections

echo "Generating Lambda function optimization test files..."

# Create directory if it doesn't exist
mkdir -p optimization_tests/massive_suite/serverless/lambda_memory_optimization

# Counter for file numbering
counter=3000

# Generate tests with obviously oversized memory for simple functions
echo "Creating oversized memory tests..."
memory_sizes=(2048 4096 8192 10240 12288 15360)
for memory in "${memory_sizes[@]}"; do
    cat > "optimization_tests/massive_suite/serverless/lambda_memory_optimization/lambda_oversized_memory_${memory}mb_$counter.json" << EOF
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_lambda_function.oversized_memory_$counter",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "function_name": "simple-api-handler-$counter",
          "runtime": "python3.9",
          "handler": "lambda_function.lambda_handler",
          "memory_size": $memory,
          "timeout": 30,
          "environment": {
            "variables": {
              "ENV": "production"
            }
          },
          "tags": {
            "Name": "oversized-memory-lambda-$counter",
            "Optimization": "lambda-memory-oversized"
          }
        }
      },
      "mode": "managed",
      "type": "aws_lambda_function",
      "name": "oversized_memory_$counter",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF
    ((counter++))
done

# Generate tests with very long timeouts for simple operations
echo "Creating long timeout tests..."
timeouts=(900 1800 3600 7200)  # 15min, 30min, 1hr, 2hr
for timeout in "${timeouts[@]}"; do
    cat > "optimization_tests/massive_suite/serverless/lambda_memory_optimization/lambda_long_timeout_${timeout}s_$counter.json" << EOF
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_lambda_function.long_timeout_$counter",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "function_name": "simple-processor-$counter",
          "runtime": "nodejs18.x",
          "handler": "index.handler",
          "memory_size": 256,
          "timeout": $timeout,
          "environment": {
            "variables": {
              "PROCESSING_TYPE": "simple"
            }
          },
          "tags": {
            "Name": "long-timeout-lambda-$counter",
            "Optimization": "lambda-timeout-excessive"
          }
        }
      },
      "mode": "managed",
      "type": "aws_lambda_function",
      "name": "long_timeout_$counter",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF
    ((counter++))
done

# Generate tests with high memory but very short timeouts
echo "Creating inefficient memory-timeout combinations..."
combinations=(
  "4096:10"
  "8192:30"
  "10240:60"
  "15360:120"
)
for combo in "${combinations[@]}"; do
    memory=$(echo $combo | cut -d: -f1)
    timeout=$(echo $combo | cut -d: -f2)
    cat > "optimization_tests/massive_suite/serverless/lambda_memory_optimization/lambda_inefficient_${memory}mb_${timeout}s_$counter.json" << EOF
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_lambda_function.inefficient_$counter",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "function_name": "data-processor-$counter",
          "runtime": "java11",
          "handler": "com.example.Handler",
          "memory_size": $memory,
          "timeout": $timeout,
          "environment": {
            "variables": {
              "WORKLOAD": "light-processing"
            }
          },
          "tags": {
            "Name": "inefficient-lambda-$counter",
            "Optimization": "lambda-memory-timeout-mismatch"
          }
        }
      },
      "mode": "managed",
      "type": "aws_lambda_function",
      "name": "inefficient_$counter",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF
    ((counter++))
done

# Generate tests with provisioned concurrency for unpredictable workloads
echo "Creating provisioned concurrency waste tests..."
for concurrency in 10 25 50 100; do
    cat > "optimization_tests/massive_suite/serverless/lambda_memory_optimization/lambda_provisioned_concurrency_${concurrency}_$counter.json" << EOF
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_lambda_function.provisioned_concurrency_$counter",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "function_name": "rarely-called-api-$counter",
          "runtime": "python3.9",
          "handler": "app.handler",
          "memory_size": 512,
          "timeout": 30,
          "reserved_concurrent_executions": $concurrency,
          "environment": {
            "variables": {
              "USAGE_PATTERN": "rare"
            }
          },
          "tags": {
            "Name": "provisioned-concurrency-waste-$counter",
            "Optimization": "lambda-provisioned-waste"
          }
        }
      },
      "mode": "managed",
      "type": "aws_lambda_function",
      "name": "provisioned_concurrency_$counter",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF
    ((counter++))
done

echo "Generated $(($(find optimization_tests/massive_suite/serverless/lambda_memory_optimization -name "*.json" | wc -l))) new Lambda optimization test files"