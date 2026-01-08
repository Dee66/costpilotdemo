#!/bin/bash

# Generate meaningful ECS Fargate test files
# Focus on CPU/memory combinations that should trigger optimization detections

echo "Generating ECS Fargate optimization test files..."

# Create directory if it doesn't exist
mkdir -p optimization_tests/massive_suite/containers/ecs

# Counter for file numbering
counter=1000

# Generate tests with oversized CPU allocations
echo "Creating oversized CPU tests..."
for cpu in 4096 8192 16384; do
    for memory in 4096 8192 16384 32768; do
        cat > "optimization_tests/massive_suite/containers/ecs/ecs_fargate_oversized_cpu_${cpu}cpu_${memory}mb_$counter.json" << EOF
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_ecs_task_definition.oversized_cpu_$counter",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "family": "oversized-cpu-task-$counter",
          "cpu": "$cpu",
          "memory": "$memory",
          "network_mode": "awsvpc",
          "requires_compatibilities": ["FARGATE"],
          "container_definitions": "[{\"name\":\"web-app\",\"image\":\"nginx:latest\",\"cpu\":256,\"memory\":512,\"essential\":true}]",
          "tags": {"Name": "oversized-cpu-$counter", "Optimization": "fargate-cpu-oversized"}
        }
      },
      "mode": "managed",
      "type": "aws_ecs_task_definition",
      "name": "oversized_cpu_$counter",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF
        ((counter++))
    done
done

# Generate tests with inefficient CPU:memory ratios
echo "Creating inefficient ratio tests..."
ratios=("0.25" "0.5" "8" "16")
for ratio in "${ratios[@]}"; do
    for cpu in 1024 2048 4096; do
        # Calculate memory based on ratio
        if [[ "$ratio" == "0.25" ]]; then
            memory=$((cpu / 4))
        elif [[ "$ratio" == "0.5" ]]; then
            memory=$((cpu / 2))
        elif [[ "$ratio" == "8" ]]; then
            memory=$((cpu * 8))
        else # 16
            memory=$((cpu * 16))
        fi

        cat > "optimization_tests/massive_suite/containers/ecs/ecs_fargate_inefficient_ratio_${ratio}_${cpu}cpu_$counter.json" << EOF
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_ecs_task_definition.inefficient_ratio_$counter",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "family": "inefficient-ratio-task-$counter",
          "cpu": "$cpu",
          "memory": "$memory",
          "network_mode": "awsvpc",
          "requires_compatibilities": ["FARGATE"],
          "container_definitions": "[{\"name\":\"app\",\"image\":\"node:14\",\"cpu\":$((cpu/4)),\"memory\":$((memory/4)),\"essential\":true}]",
          "tags": {"Name": "inefficient-ratio-$counter", "Optimization": "fargate-ratio-inefficient"}
        }
      },
      "mode": "managed",
      "type": "aws_ecs_task_definition",
      "name": "inefficient_ratio_$counter",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF
        ((counter++))
    done
done

# Generate tests with very high memory for simple workloads
echo "Creating high memory tests..."
for memory in 65536 131072 262144; do
    for cpu in 256 512 1024; do
        cat > "optimization_tests/massive_suite/containers/ecs/ecs_fargate_high_memory_${memory}mb_${cpu}cpu_$counter.json" << EOF
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_ecs_task_definition.high_memory_$counter",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "family": "high-memory-task-$counter",
          "cpu": "$cpu",
          "memory": "$memory",
          "network_mode": "awsvpc",
          "requires_compatibilities": ["FARGATE"],
          "container_definitions": "[{\"name\":\"simple-api\",\"image\":\"python:3.9-slim\",\"cpu\":128,\"memory\":256,\"essential\":true}]",
          "tags": {"Name": "high-memory-$counter", "Optimization": "fargate-memory-oversized"}
        }
      },
      "mode": "managed",
      "type": "aws_ecs_task_definition",
      "name": "high_memory_$counter",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF
        ((counter++))
    done
done

echo "Generated $(($(find optimization_tests/massive_suite/containers/ecs -name "ecs_fargate_*.json" | wc -l) - 303)) new ECS Fargate test files"