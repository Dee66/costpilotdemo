#!/bin/bash

# Generate TARGETED test scenarios that actually trigger CostPilot detections
# Based on analysis of what patterns CostPilot actually detects

echo "Generating targeted optimization test scenarios..."

counter=8000

# 1. ECS Fargate - CPU/Memory mismatches (should trigger container optimization)
echo "Generating ECS CPU/memory mismatch scenarios..."
cat > "optimization_tests/massive_suite/containers/ecs/ecs_cpu_memory_mismatch_$counter.json" << 'EOF'
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_ecs_task_definition.oversized_task",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "family": "oversized-app",
          "cpu": "4096",
          "memory": "8192",
          "network_mode": "awsvpc",
          "requires_compatibilities": ["FARGATE"],
          "container_definitions": "[{\"name\":\"app\",\"image\":\"nginx:latest\",\"cpu\":256,\"memory\":512,\"essential\":true}]",
          "tags": {"Environment": "development", "Optimization": "cpu-memory-mismatch"}
        }
      },
      "mode": "managed",
      "type": "aws_ecs_task_definition",
      "name": "oversized_task",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF
((counter++))

# 2. EC2 instances in development with expensive types (should trigger rightsizing)
echo "Generating EC2 development instance scenarios..."
cat > "optimization_tests/massive_suite/instance_rightsizing/development/dev_m5_4xlarge_$counter.json" << 'EOF'
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_instance.dev_server",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "instance_type": "m5.4xlarge",
          "ami": "ami-12345678",
          "tags": {
            "Name": "dev-server",
            "Environment": "development",
            "Team": "backend",
            "Optimization": "dev-rightsizing"
          }
        }
      },
      "mode": "managed",
      "type": "aws_instance",
      "name": "dev_server",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF
((counter++))

# 3. Lambda with high memory but low timeout (inefficient)
echo "Generating Lambda memory/timeout mismatch scenarios..."
cat > "optimization_tests/massive_suite/serverless/lambda_inefficient/lambda_high_mem_low_timeout_$counter.json" << 'EOF'
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_lambda_function.inefficient_lambda",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "function_name": "inefficient-function",
          "runtime": "python3.9",
          "handler": "lambda_function.lambda_handler",
          "memory_size": 3008,
          "timeout": 30,
          "tags": {
            "Name": "inefficient-lambda",
            "Optimization": "memory-timeout-mismatch"
          }
        }
      },
      "mode": "managed",
      "type": "aws_lambda_function",
      "name": "inefficient_lambda",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF
((counter++))

# 4. RDS with oversized storage
echo "Generating RDS oversized storage scenarios..."
cat > "optimization_tests/massive_suite/storage_optimization/rds_oversized/rds_oversized_storage_$counter.json" << 'EOF'
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_db_instance.oversized_rds",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "instance_class": "db.t3.micro",
          "engine": "mysql",
          "allocated_storage": 1000,
          "max_allocated_storage": 2000,
          "tags": {
            "Name": "oversized-rds",
            "Environment": "development",
            "Optimization": "storage-rightsizing"
          }
        }
      },
      "mode": "managed",
      "type": "aws_db_instance",
      "name": "oversized_rds",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF
((counter++))

# 5. NAT Gateway without optimization
echo "Generating NAT Gateway scenarios..."
cat > "optimization_tests/massive_suite/network_optimization/nat_gateway/nat_gateway_basic_$counter.json" << 'EOF'
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_nat_gateway.basic_nat",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "allocation_id": "eipalloc-12345",
          "subnet_id": "subnet-12345",
          "tags": {
            "Name": "basic-nat-gateway",
            "Optimization": "nat-gateway-optimization"
          }
        }
      },
      "mode": "managed",
      "type": "aws_nat_gateway",
      "name": "basic_nat",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF
((counter++))

echo "Generated targeted test scenarios. Run CostPilot on these files to verify detections."