#!/bin/bash

# Generate PROPER targeted test scenarios that actually trigger CostPilot detections
# Each scenario represents a real optimization opportunity

echo "Generating proper targeted test scenarios that will trigger detections..."

# 1. CONTAINER OPTIMIZATION SCENARIOS
echo "=== CONTAINER SCENARIOS ==="

# ECS Fargate - Oversized for development workload
cat > "optimization_tests/targeted_suite/containers/ecs_dev_oversized.json" << 'EOF'
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_ecs_task_definition.dev_api",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "family": "dev-api-task",
          "cpu": "2048",
          "memory": "4096",
          "network_mode": "awsvpc",
          "requires_compatibilities": ["FARGATE"],
          "container_definitions": "[{\"name\":\"api\",\"image\":\"node:16\",\"cpu\":256,\"memory\":512,\"essential\":true}]",
          "tags": {
            "Environment": "development",
            "Team": "backend",
            "Workload": "api"
          }
        }
      },
      "mode": "managed",
      "type": "aws_ecs_task_definition",
      "name": "dev_api",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF

# ECS Fargate - CPU/Memory mismatch (inefficient ratio)
cat > "optimization_tests/targeted_suite/containers/ecs_cpu_memory_mismatch.json" << 'EOF'
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_ecs_task_definition.mismatched_resources",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "family": "web-app-task",
          "cpu": "4096",
          "memory": "8192",
          "network_mode": "awsvpc",
          "requires_compatibilities": ["FARGATE"],
          "container_definitions": "[{\"name\":\"web\",\"image\":\"nginx\",\"cpu\":512,\"memory\":1024,\"essential\":true}]",
          "tags": {
            "Environment": "production",
            "Application": "web-app"
          }
        }
      },
      "mode": "managed",
      "type": "aws_ecs_task_definition",
      "name": "mismatched_resources",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF

# 2. COMPUTE OPTIMIZATION SCENARIOS
echo "=== COMPUTE SCENARIOS ==="

# EC2 - Development server using expensive instance type
cat > "optimization_tests/targeted_suite/compute/ec2_dev_expensive.json" << 'EOF'
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_instance.dev_database",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "instance_type": "m5.4xlarge",
          "ami": "ami-12345678",
          "tags": {
            "Name": "dev-database",
            "Environment": "development",
            "Team": "data",
            "Purpose": "development-testing"
          }
        }
      },
      "mode": "managed",
      "type": "aws_instance",
      "name": "dev_database",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF

# EC2 - Underutilized production instance
cat > "optimization_tests/targeted_suite/compute/ec2_prod_underutilized.json" << 'EOF'
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_instance.prod_app_server",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "instance_type": "c5.4xlarge",
          "ami": "ami-87654321",
          "tags": {
            "Name": "prod-app-server",
            "Environment": "production",
            "Application": "web-app",
            "Utilization": "low"
          }
        }
      },
      "mode": "managed",
      "type": "aws_instance",
      "name": "prod_app_server",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF

# 3. SERVERLESS OPTIMIZATION SCENARIOS
echo "=== SERVERLESS SCENARIOS ==="

# Lambda - High memory, low timeout (inefficient)
cat > "optimization_tests/targeted_suite/serverless/lambda_inefficient_memory.json" << 'EOF'
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_lambda_function.image_processor",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "function_name": "image-processor",
          "runtime": "python3.9",
          "handler": "lambda_function.lambda_handler",
          "memory_size": 3008,
          "timeout": 30,
          "architectures": ["x86_64"],
          "tags": {
            "Name": "image-processor",
            "Team": "media",
            "Optimization": "memory-timeout-ratio"
          }
        }
      },
      "mode": "managed",
      "type": "aws_lambda_function",
      "name": "image_processor",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF

# Lambda - Low memory, high timeout (inefficient)
cat > "optimization_tests/targeted_suite/serverless/lambda_inefficient_timeout.json" << 'EOF'
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_lambda_function.data_sync",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "function_name": "data-sync-function",
          "runtime": "nodejs18.x",
          "handler": "index.handler",
          "memory_size": 128,
          "timeout": 900,
          "architectures": ["x86_64"],
          "tags": {
            "Name": "data-sync",
            "Team": "data",
            "Optimization": "timeout-memory-ratio"
          }
        }
      },
      "mode": "managed",
      "type": "aws_lambda_function",
      "name": "data_sync",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF

# 4. STORAGE OPTIMIZATION SCENARIOS
echo "=== STORAGE SCENARIOS ==="

# S3 - No lifecycle policy
cat > "optimization_tests/targeted_suite/storage/s3_no_lifecycle.json" << 'EOF'
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_s3_bucket.data_lake",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "bucket": "company-data-lake-2026",
          "tags": {
            "Name": "data-lake",
            "Environment": "production",
            "DataClass": "analytics",
            "Retention": "long-term"
          }
        }
      },
      "mode": "managed",
      "type": "aws_s3_bucket",
      "name": "data_lake",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF

# EBS - Oversized volume
cat > "optimization_tests/targeted_suite/storage/ebs_oversized.json" << 'EOF'
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_ebs_volume.large_dev_volume",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "size": 1000,
          "type": "gp2",
          "availability_zone": "us-east-1a",
          "tags": {
            "Name": "dev-volume",
            "Environment": "development",
            "Team": "backend"
          }
        }
      },
      "mode": "managed",
      "type": "aws_ebs_volume",
      "name": "large_dev_volume",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF

# 5. NETWORK OPTIMIZATION SCENARIOS
echo "=== NETWORK SCENARIOS ==="

# NAT Gateway - Basic implementation
cat > "optimization_tests/targeted_suite/network/nat_gateway_basic.json" << 'EOF'
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_nat_gateway.public_nat",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "allocation_id": "eipalloc-12345678",
          "subnet_id": "subnet-12345678",
          "tags": {
            "Name": "public-nat-gateway",
            "Environment": "production"
          }
        }
      },
      "mode": "managed",
      "type": "aws_nat_gateway",
      "name": "public_nat",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF

# 6. DATABASE OPTIMIZATION SCENARIOS
echo "=== DATABASE SCENARIOS ==="

# RDS - Oversized storage for instance type
cat > "optimization_tests/targeted_suite/database/rds_oversized_storage.json" << 'EOF'
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_db_instance.dev_database",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "instance_class": "db.t3.micro",
          "engine": "mysql",
          "engine_version": "8.0",
          "allocated_storage": 1000,
          "max_allocated_storage": 2000,
          "db_name": "devdb",
          "username": "admin",
          "tags": {
            "Name": "dev-database",
            "Environment": "development",
            "Team": "backend"
          }
        }
      },
      "mode": "managed",
      "type": "aws_db_instance",
      "name": "dev_database",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF

# RDS - Expensive instance for development
cat > "optimization_tests/targeted_suite/database/rds_dev_expensive.json" << 'EOF'
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_db_instance.dev_mysql",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "instance_class": "db.r5.2xlarge",
          "engine": "mysql",
          "engine_version": "8.0",
          "allocated_storage": 100,
          "db_name": "devdb",
          "username": "admin",
          "tags": {
            "Name": "dev-mysql",
            "Environment": "development",
            "Team": "data"
          }
        }
      },
      "mode": "managed",
      "type": "aws_db_instance",
      "name": "dev_mysql",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF

echo "Generated 12 targeted test scenarios designed to trigger CostPilot detections."
echo "Each scenario represents a real optimization opportunity."