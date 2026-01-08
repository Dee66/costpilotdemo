#!/bin/bash

# Generate comprehensive test scenarios with CORRECT Terraform plan JSON format
echo "Generating comprehensive test suite with proper JSON format..."

counter=1
total_scenarios=0

# Function to create test file with correct format
create_test() {
    local category=$1
    local scenario=$2
    local content=$3

    mkdir -p "optimization_tests/comprehensive_suite/$category"
    echo "$content" > "optimization_tests/comprehensive_suite/$category/${scenario}_${counter}.json"
    ((counter++))
    ((total_scenarios++))
}

# 1. CONTAINER OPTIMIZATION (800 scenarios)
echo "=== GENERATING CONTAINER SCENARIOS ==="
environments=("development" "staging" "testing" "qa" "dev" "test" "sandbox")
cpu_options=(1024 2048 4096)
memory_options=(2048 4096 8192 16384)

for env in "${environments[@]}"; do
    for cpu in "${cpu_options[@]}"; do
        for mem in "${memory_options[@]}"; do
            for i in {1..8}; do
                create_test "containers" "ecs_${env}_oversized_${cpu}cpu_${mem}mem" '{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [{
    "address": "aws_ecs_task_definition.'$env'_task_'$i'",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "family": "'$env'-app-task-'$i'",
        "cpu": "'$cpu'",
        "memory": "'$mem'",
        "network_mode": "awsvpc",
        "requires_compatibilities": ["FARGATE"],
        "container_definitions": "[{\"name\":\"app\",\"image\":\"nginx:latest\",\"cpu\":256,\"memory\":512,\"essential\":true}]",
        "tags": {"Environment": "'$env'", "Team": "backend", "Workload": "api"}
      }
    },
    "mode": "managed",
    "type": "aws_ecs_task_definition",
    "name": "'$env'_task_'$i'",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }]
}'
            done
        done
    done
done

# 2. COMPUTE OPTIMIZATION (1200 scenarios)
echo "=== GENERATING COMPUTE SCENARIOS ==="
expensive_instances=("m5.4xlarge" "m5.8xlarge" "c5.4xlarge" "c5.9xlarge" "r5.2xlarge" "r5.4xlarge" "m6i.4xlarge" "c6i.4xlarge")
dev_environments=("development" "dev" "staging" "test" "testing" "qa" "sandbox" "demo")

for env in "${dev_environments[@]}"; do
    for instance in "${expensive_instances[@]}"; do
        for i in {1..15}; do
            create_test "compute" "ec2_${env}_${instance//./_}" '{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [{
    "address": "aws_instance.'$env'_server_'$i'",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "instance_type": "'$instance'",
        "ami": "ami-12345678",
        "tags": {
          "Name": "'$env'-server-'$i'",
          "Environment": "'$env'",
          "Team": "engineering",
          "Purpose": "'$env'-workload"
        }
      }
    },
    "mode": "managed",
    "type": "aws_instance",
    "name": "'$env'_server_'$i'",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }]
}'
        done
    done
done

# 3. STORAGE OPTIMIZATION (1200 scenarios)
echo "=== GENERATING STORAGE SCENARIOS ==="

# S3 buckets without lifecycle policies (600 scenarios)
bucket_types=("data-lake" "logs" "backups" "static-assets" "temp-files" "archives" "user-uploads" "cache" "analytics" "reports")
for bucket_type in "${bucket_types[@]}"; do
    for i in {1..80}; do
        create_test "storage" "s3_no_lifecycle_${bucket_type}" '{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [{
    "address": "aws_s3_bucket.'$bucket_type'_'$i'",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "bucket": "'$bucket_type'-bucket-'$i'",
        "tags": {
          "Name": "'$bucket_type'-'$i'",
          "Environment": "production",
          "DataClass": "'$bucket_type'",
          "Retention": "long-term"
        }
      }
    },
    "mode": "managed",
    "type": "aws_s3_bucket",
    "name": "'$bucket_type'_'$i'",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }]
}'
    done
done

# EBS oversized volumes (300 scenarios)
volume_sizes=(1000 2000 5000)
volume_types=("gp2" "gp3" "io1")
for size in "${volume_sizes[@]}"; do
    for type in "${volume_types[@]}"; do
        for i in {1..25}; do
            create_test "storage" "ebs_oversized_${size}gb_${type}" '{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [{
    "address": "aws_ebs_volume.large_volume_'$i'",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "size": '$size',
        "type": "'$type'",
        "availability_zone": "us-east-1a",
        "tags": {
          "Name": "large-volume-'$i'",
          "Environment": "development",
          "Team": "backend",
          "Usage": "low"
        }
      }
    },
    "mode": "managed",
    "type": "aws_ebs_volume",
    "name": "large_volume_'$i'",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }]
}'
        done
    done
done

# RDS oversized storage (300 scenarios)
rds_instances=("db.t3.micro" "db.t3.small" "db.t3.medium")
for instance in "${rds_instances[@]}"; do
    for storage in 1000 2000 5000; do
        for i in {1..25}; do
            create_test "storage" "rds_oversized_storage_${instance//./_}_${storage}gb" '{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [{
    "address": "aws_db_instance.oversized_rds_'$i'",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "instance_class": "'$instance'",
        "engine": "mysql",
        "allocated_storage": '$storage',
        "max_allocated_storage": '$((storage * 2))',
        "tags": {
          "Name": "oversized-rds-'$i'",
          "Environment": "development",
          "Team": "data"
        }
      }
    },
    "mode": "managed",
    "type": "aws_db_instance",
    "name": "oversized_rds_'$i'",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }]
}'
        done
    done
done

# 4. SERVERLESS OPTIMIZATION (1000 scenarios)
echo "=== GENERATING SERVERLESS SCENARIOS ==="
memory_settings=(3008 2048 1024 512)
timeout_settings=(30 60 120 300 600 900)

# Lambda high memory, low timeout (inefficient) (500 scenarios)
for mem in "${memory_settings[@]}"; do
    for timeout in "${timeout_settings[@]}"; do
        if [ "$mem" -gt 1024 ] && [ "$timeout" -lt 120 ]; then
            for i in {1..35}; do
                create_test "serverless" "lambda_high_mem_low_timeout_${mem}mb_${timeout}s" '{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [{
    "address": "aws_lambda_function.inefficient_lambda_'$i'",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "function_name": "lambda-function-'$i'",
        "runtime": "python3.9",
        "handler": "lambda_function.lambda_handler",
        "memory_size": '$mem',
        "timeout": '$timeout',
        "architectures": ["x86_64"],
        "tags": {
          "Name": "lambda-'$i'",
          "Team": "backend",
          "Optimization": "memory-timeout-inefficient"
        }
      }
    },
    "mode": "managed",
    "type": "aws_lambda_function",
    "name": "inefficient_lambda_'$i'",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }]
}'
            done
        fi
    done
done

# Lambda low memory, high timeout (inefficient) (500 scenarios)
for mem in 128 256 512; do
    for timeout in 300 600 900; do
        for i in {1..70}; do
            create_test "serverless" "lambda_low_mem_high_timeout_${mem}mb_${timeout}s" '{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [{
    "address": "aws_lambda_function.timeout_lambda_'$i'",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "function_name": "timeout-function-'$i'",
        "runtime": "nodejs18.x",
        "handler": "index.handler",
        "memory_size": '$mem',
        "timeout": '$timeout',
        "architectures": ["x86_64"],
        "tags": {
          "Name": "timeout-lambda-'$i'",
          "Team": "data",
          "Optimization": "timeout-memory-inefficient"
        }
      }
    },
    "mode": "managed",
    "type": "aws_lambda_function",
    "name": "timeout_lambda_'$i'",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }]
}'
        done
    done
done

# 5. NETWORK OPTIMIZATION (300 scenarios)
echo "=== GENERATING NETWORK SCENARIOS ==="

# NAT Gateways (150 scenarios)
for i in {1..150}; do
    create_test "network" "nat_gateway_basic" '{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [{
    "address": "aws_nat_gateway.nat_'$i'",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "allocation_id": "eipalloc-'$i'",
        "subnet_id": "subnet-'$i'",
        "tags": {
          "Name": "nat-gateway-'$i'",
          "Environment": "production"
        }
      }
    },
    "mode": "managed",
    "type": "aws_nat_gateway",
    "name": "nat_'$i'",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }]
}'
done

# VPC Endpoints (150 scenarios)
endpoint_types=("Interface" "Gateway")
services=("s3" "dynamodb" "ec2" "rds" "lambda")
for type in "${endpoint_types[@]}"; do
    for service in "${services[@]}"; do
        for i in {1..15}; do
            create_test "network" "vpc_endpoint_${type,,}_${service}" '{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [{
    "address": "aws_vpc_endpoint.'$service'_endpoint_'$i'",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "vpc_endpoint_type": "'$type'",
        "service_name": "com.amazonaws.us-east-1.'$service'",
        "vpc_id": "vpc-12345",
        "tags": {
          "Name": "'$service'-endpoint-'$i'",
          "Environment": "production"
        }
      }
    },
    "mode": "managed",
    "type": "aws_vpc_endpoint",
    "name": "'$service'_endpoint_'$i'",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }]
}'
        done
    done
done

# 6. DATABASE OPTIMIZATION (300 scenarios)
echo "=== GENERATING DATABASE SCENARIOS ==="

# RDS expensive instances for development (150 scenarios)
dev_rds_instances=("db.r5.2xlarge" "db.m5.4xlarge" "db.c5.4xlarge")
for instance in "${dev_rds_instances[@]}"; do
    for i in {1..50}; do
        create_test "database" "rds_dev_expensive_${instance//./_}" '{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [{
    "address": "aws_db_instance.dev_rds_'$i'",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "instance_class": "'$instance'",
        "engine": "mysql",
        "allocated_storage": 100,
        "tags": {
          "Name": "dev-rds-'$i'",
          "Environment": "development",
          "Team": "data"
        }
      }
    },
    "mode": "managed",
    "type": "aws_db_instance",
    "name": "dev_rds_'$i'",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }]
}'
    done
done

# ElastiCache oversized (150 scenarios)
cache_instances=("cache.m5.large" "cache.r5.large" "cache.c5.large")
for instance in "${cache_instances[@]}"; do
    for i in {1..50}; do
        create_test "database" "elasticache_dev_oversized_${instance//./_}" '{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [{
    "address": "aws_elasticache_cluster.dev_cache_'$i'",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "cluster_id": "dev-cache-'$i'",
        "engine": "redis",
        "node_type": "'$instance'",
        "num_cache_nodes": 1,
        "tags": {
          "Name": "dev-cache-'$i'",
          "Environment": "development",
          "Team": "backend"
        }
      }
    },
    "mode": "managed",
    "type": "aws_elasticache_cluster",
    "name": "dev_cache_'$i'",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }]
}'
    done
done

# 7. MESSAGING OPTIMIZATION (200 scenarios)
echo "=== GENERATING MESSAGING SCENARIOS ==="

# SQS queues without DLQs (200 scenarios)
for i in {1..200}; do
    create_test "messaging" "sqs_no_dlq" '{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [{
    "address": "aws_sqs_queue.user_queue_'$i'",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "name": "user-queue-'$i'",
        "delay_seconds": 0,
        "max_message_size": 262144,
        "tags": {
          "Name": "user-queue-'$i'",
          "Environment": "production",
          "Team": "messaging"
        }
      }
    },
    "mode": "managed",
    "type": "aws_sqs_queue",
    "name": "user_queue_'$i'",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }]
}'
done

# 8. EDGE/CDN OPTIMIZATION (100 scenarios)
echo "=== GENERATING EDGE/CDN SCENARIOS ==="

# Lambda@Edge oversized (100 scenarios)
for i in {1..100}; do
    create_test "edge_cdn" "lambda_at_edge_oversized" '{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [{
    "address": "aws_lambda_function.edge_function_'$i'",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "function_name": "edge-function-'$i'",
        "runtime": "nodejs18.x",
        "handler": "index.handler",
        "memory_size": 2048,
        "timeout": 30,
        "publish": true,
        "tags": {
          "Name": "edge-function-'$i'",
          "Environment": "production",
          "Type": "lambda-at-edge"
        }
      }
    },
    "mode": "managed",
    "type": "aws_lambda_function",
    "name": "edge_function_'$i'",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }]
}'
done

echo "Generated comprehensive test suite with $total_scenarios scenarios"