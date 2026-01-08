#!/bin/bash

# Generate additional test files to reach 3000 total

BASE_COUNT=$(find optimization_tests/massive_suite -name "*.json" | wc -l)
TARGET=3000
NEEDED=$((TARGET - BASE_COUNT))

echo "Current tests: $BASE_COUNT"
echo "Target: $TARGET"  
echo "Need to generate: $NEEDED more tests"

# Create directories
mkdir -p optimization_tests/massive_suite/{containers/ecs,instance_rightsizing/web_servers,storage_optimization/ebs_volumes,serverless/lambda_variants,network_optimization/vpc_endpoints,database/elasticache}

# Generate ECS tests
for i in $(seq 1 200); do
  cat > "optimization_tests/massive_suite/containers/ecs/ecs_fargate_varied_${i}.json" << ECS_EOF
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_ecs_task_definition.varied_task_${i}",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "family": "varied-task-${i}",
          "cpu": "$((1024 + (i % 3) * 1024))",
          "memory": "$((4096 + (i % 4) * 4096))",
          "network_mode": "awsvpc",
          "requires_compatibilities": ["FARGATE"],
          "container_definitions": "[{\"name\":\"app\",\"image\":\"nginx:latest\",\"cpu\":512,\"memory\":2048,\"essential\":true}]",
          "tags": {"Name": "varied-task-${i}", "Optimization": "fargate-sizing"}
        }
      },
      "mode": "managed",
      "type": "aws_ecs_task_definition",
      "name": "varied_task_${i}",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
ECS_EOF
done

# Generate EC2 tests
for i in $(seq 1 150); do
  instance_types=("m5.large" "m5.xlarge" "c5.large" "c5.xlarge" "r5.large" "r5.xlarge")
  type=${instance_types[$((i % 6))]}
  cat > "optimization_tests/massive_suite/instance_rightsizing/web_servers/web_server_${type//./_}_${i}.json" << EC2_EOF
{
  "format_version": "1.2",
  "terraform_version": "1.6.0", 
  "resource_changes": [
    {
      "address": "aws_instance.web_server_${i}",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "ami": "ami-12345678",
          "instance_type": "${type}",
          "tags": {"Name": "web-server-${i}", "Optimization": "instance-rightsizing"}
        }
      },
      "mode": "managed",
      "type": "aws_instance",
      "name": "web_server_${i}",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EC2_EOF
done

# Generate EBS tests
for i in $(seq 1 100); do
  sizes=(100 500 1000 2000)
  size=${sizes[$((i % 4))]}
  cat > "optimization_tests/massive_suite/storage_optimization/ebs_volumes/ebs_gp2_${size}gb_${i}.json" << EBS_EOF
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_ebs_volume.gp2_volume_${i}",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "availability_zone": "us-east-1a",
          "size": ${size},
          "type": "gp2",
          "tags": {"Name": "gp2-volume-${i}", "Optimization": "ebs-migration"}
        }
      },
      "mode": "managed",
      "type": "aws_ebs_volume",
      "name": "gp2_volume_${i}",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EBS_EOF
done

# Generate Lambda tests
for i in $(seq 1 120); do
  memory=$((128 + (i % 10) * 256))
  timeout=$((30 + (i % 5) * 60))
  cat > "optimization_tests/massive_suite/serverless/lambda_variants/lambda_mem${memory}_timeout${timeout}_${i}.json" << LAMBDA_EOF
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_lambda_function.variant_${i}",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "function_name": "lambda-variant-${i}",
          "runtime": "python3.9",
          "memory_size": ${memory},
          "timeout": ${timeout},
          "handler": "lambda_function.lambda_handler",
          "role": "arn:aws:iam::123456789012:role/lambda-role",
          "tags": {"Name": "lambda-variant-${i}", "Optimization": "lambda-optimization"}
        }
      },
      "mode": "managed",
      "type": "aws_lambda_function", 
      "name": "variant_${i}",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
LAMBDA_EOF
done

# Generate NAT Gateway tests
for i in $(seq 1 80); do
  cat > "optimization_tests/massive_suite/network_optimization/nat_gateways/nat_gateway_variant_${i}.json" << NAT_EOF
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_nat_gateway.variant_nat_${i}",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "allocation_id": "eipalloc-${i}",
          "subnet_id": "subnet-public-${i}",
          "tags": {"Name": "nat-gateway-${i}", "Optimization": "nat-gateway-cost"}
        }
      },
      "mode": "managed",
      "type": "aws_nat_gateway",
      "name": "variant_nat_${i}",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
NAT_EOF
done

# Generate VPC Endpoint tests
for i in $(seq 1 60); do
  services=("s3" "dynamodb" "s3" "dynamodb" "ecr.dkr" "ecr.api")
  service=${services[$((i % 6))]}
  cat > "optimization_tests/massive_suite/network_optimization/vpc_endpoints/vpc_endpoint_${service}_${i}.json" << VPC_EOF
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_vpc_endpoint.${service}_endpoint_${i}",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "vpc_id": "vpc-12345",
          "service_name": "com.amazonaws.us-east-1.${service}",
          "vpc_endpoint_type": "Gateway",
          "tags": {"Name": "${service}-endpoint-${i}", "Optimization": "vpc-endpoint"}
        }
      },
      "mode": "managed",
      "type": "aws_vpc_endpoint",
      "name": "${service}_endpoint_${i}",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
VPC_EOF
done

# Generate ElastiCache tests
for i in $(seq 1 40); do
  cat > "optimization_tests/massive_suite/database/elasticache/elasticache_cluster_${i}.json" << CACHE_EOF
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_elasticache_cluster.redis_${i}",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "cluster_id": "redis-cluster-${i}",
          "engine": "redis",
          "node_type": "cache.t3.micro",
          "num_cache_nodes": 1,
          "tags": {"Name": "redis-cluster-${i}", "Optimization": "cache-optimization"}
        }
      },
      "mode": "managed",
      "type": "aws_elasticache_cluster",
      "name": "redis_${i}",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
CACHE_EOF
done

echo "Generated additional test files"
FINAL_COUNT=$(find optimization_tests/massive_suite -name "*.json" | wc -l)
echo "Final test count: $FINAL_COUNT"
