#!/bin/bash

# Generate REAL Terraform plan variations that represent actual user infrastructure
# Some will have cost issues, some won't - just like real user deployments
echo "Generating realistic Terraform plan variations..."

counter=1
total_scenarios=0

# Function to create test file with real Terraform plan structure
create_test() {
    local category=$1
    local scenario=$2
    local content=$3

    mkdir -p "optimization_tests/realistic_plans/$category"
    echo "$content" > "optimization_tests/realistic_plans/$category/${scenario}_${counter}.json"
    ((counter++))
    ((total_scenarios++))
}

# 1. WEB APPLICATION STACKS (1000 scenarios)
echo "=== GENERATING WEB APPLICATION STACKS ==="

# Standard web app with cost issues
for i in {1..1000}; do
    # Mix of good and bad configurations
    instance_types=("t3.micro" "t3.small" "m5.large" "c5.large" "m5.4xlarge")
    instance_type=${instance_types[$((RANDOM % ${#instance_types[@]}))]}
    environments=("production" "staging" "development" "test")
    env=${environments[$((RANDOM % ${#environments[@]}))]}
    db_sizes=(20 100 500 1000)
    db_size=${db_sizes[$((RANDOM % ${#db_sizes[@]}))]}

    create_test "web_apps" "web_app_stack_$i" '{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [{
    "address": "aws_instance.web_server",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "instance_type": "'$instance_type'",
        "ami": "ami-12345678",
        "tags": {
          "Name": "web-server-'$i'",
          "Environment": "'$env'",
          "Application": "web-app",
          "Team": "platform"
        }
      }
    },
    "mode": "managed",
    "type": "aws_instance",
    "name": "web_server",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }, {
    "address": "aws_db_instance.database",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "instance_class": "db.t3.micro",
        "engine": "mysql",
        "allocated_storage": '$db_size',
        "tags": {
          "Name": "app-db-'$i'",
          "Environment": "'$env'",
          "Application": "web-app"
        }
      }
    },
    "mode": "managed",
    "type": "aws_db_instance",
    "name": "database",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }, {
    "address": "aws_s3_bucket.static_assets",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "bucket": "web-app-assets-'$i'",
        "tags": {
          "Name": "static-assets-'$i'",
          "Environment": "'$env'",
          "Purpose": "static-content"
        }
      }
    },
    "mode": "managed",
    "type": "aws_s3_bucket",
    "name": "static_assets",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }]
}'
done

# 2. DATA PROCESSING PIPELINES (1000 scenarios)
echo "=== GENERATING DATA PROCESSING PIPELINES ==="

for i in {1..1000}; do
    # Realistic data pipeline configurations
    instance_types=("m5.large" "m5.xlarge" "c5.xlarge" "r5.large" "r5.xlarge")
    instance_type=${instance_types[$((RANDOM % ${#instance_types[@]}))]}
    lambda_memory=(128 256 512 1024 2048)
    lambda_mem=${lambda_memory[$((RANDOM % ${#lambda_memory[@]}))]}
    lambda_timeout=(30 60 120 300 600)
    lambda_time=${lambda_timeout[$((RANDOM % ${#lambda_timeout[@]}))]}

    create_test "data_pipelines" "data_pipeline_$i" '{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [{
    "address": "aws_instance.data_processor",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "instance_type": "'$instance_type'",
        "ami": "ami-87654321",
        "tags": {
          "Name": "data-processor-'$i'",
          "Environment": "production",
          "Application": "data-pipeline",
          "Team": "data"
        }
      }
    },
    "mode": "managed",
    "type": "aws_instance",
    "name": "data_processor",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }, {
    "address": "aws_lambda_function.data_transformer",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "function_name": "data-transformer-'$i'",
        "runtime": "python3.9",
        "handler": "lambda_function.lambda_handler",
        "memory_size": '$lambda_mem',
        "timeout": '$lambda_time',
        "architectures": ["x86_64"],
        "tags": {
          "Name": "data-transformer-'$i'",
          "Environment": "production",
          "Application": "data-pipeline"
        }
      }
    },
    "mode": "managed",
    "type": "aws_lambda_function",
    "name": "data_transformer",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }, {
    "address": "aws_s3_bucket.data_lake",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "bucket": "data-lake-bucket-'$i'",
        "tags": {
          "Name": "data-lake-'$i'",
          "Environment": "production",
          "DataClass": "processed-data"
        }
      }
    },
    "mode": "managed",
    "type": "aws_s3_bucket",
    "name": "data_lake",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }]
}'
done

# 3. MICROSERVICES ARCHITECTURES (1000 scenarios)
echo "=== GENERATING MICROSERVICES ARCHITECTURES ==="

for i in {1..1000}; do
    # Realistic microservices configurations
    services=("auth" "user" "payment" "notification" "api-gateway" "inventory")
    service=${services[$((RANDOM % ${#services[@]}))]}
    instance_types=("t3.micro" "t3.small" "t3.medium" "m5.large")
    instance_type=${instance_types[$((RANDOM % ${#instance_types[@]}))]}
    cache_types=("cache.t3.micro" "cache.t3.small" "cache.m5.large" "cache.r5.large")
    cache_type=${cache_types[$((RANDOM % ${#cache_types[@]}))]}

    create_test "microservices" "microservice_$service_$i" '{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [{
    "address": "aws_instance.'$service'_service",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "instance_type": "'$instance_type'",
        "ami": "ami-11223344",
        "tags": {
          "Name": "'$service'-service-'$i'",
          "Environment": "production",
          "Application": "microservices",
          "Service": "'$service'",
          "Team": "backend"
        }
      }
    },
    "mode": "managed",
    "type": "aws_instance",
    "name": "'$service'_service",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }, {
    "address": "aws_elasticache_cluster.'$service'_cache",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "cluster_id": "'$service'-cache-'$i'",
        "engine": "redis",
        "node_type": "'$cache_type'",
        "num_cache_nodes": 1,
        "tags": {
          "Name": "'$service'-cache-'$i'",
          "Environment": "production",
          "Application": "microservices",
          "Service": "'$service'"
        }
      }
    },
    "mode": "managed",
    "type": "aws_elasticache_cluster",
    "name": "'$service'_cache",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }, {
    "address": "aws_sqs_queue.'$service'_queue",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "name": "'$service'-queue-'$i'",
        "delay_seconds": 0,
        "max_message_size": 262144,
        "tags": {
          "Name": "'$service'-queue-'$i'",
          "Environment": "production",
          "Application": "microservices",
          "Service": "'$service'"
        }
      }
    },
    "mode": "managed",
    "type": "aws_sqs_queue",
    "name": "'$service'_queue",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }]
}'
done

# 4. DEVELOPMENT/TESTING ENVIRONMENTS (1000 scenarios)
echo "=== GENERATING DEV/TEST ENVIRONMENTS ==="

for i in {1..1000}; do
    # Development environments that might have oversized resources
    dev_instance_types=("t3.micro" "t3.small" "m5.large" "m5.2xlarge" "c5.2xlarge" "m5.4xlarge")
    dev_instance_type=${dev_instance_types[$((RANDOM % ${#dev_instance_types[@]}))]}
    environments=("development" "staging" "qa" "testing" "integration" "demo")
    env=${environments[$((RANDOM % ${#environments[@]}))]}
    db_instance_types=("db.t3.micro" "db.t3.small" "db.m5.large" "db.r5.large" "db.c5.large")
    db_instance_type=${db_instance_types[$((RANDOM % ${#db_instance_types[@]}))]}

    create_test "dev_environments" "dev_env_$env_$i" '{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [{
    "address": "aws_instance.dev_app_server",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "instance_type": "'$dev_instance_type'",
        "ami": "ami-55667788",
        "tags": {
          "Name": "dev-app-server-'$i'",
          "Environment": "'$env'",
          "Application": "dev-app",
          "Team": "development"
        }
      }
    },
    "mode": "managed",
    "type": "aws_instance",
    "name": "dev_app_server",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }, {
    "address": "aws_db_instance.dev_database",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "instance_class": "'$db_instance_type'",
        "engine": "postgres",
        "allocated_storage": 100,
        "tags": {
          "Name": "dev-database-'$i'",
          "Environment": "'$env'",
          "Application": "dev-app"
        }
      }
    },
    "mode": "managed",
    "type": "aws_db_instance",
    "name": "dev_database",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }]
}'
done

# 5. LEGACY SYSTEM MIGRATIONS (1000 scenarios)
echo "=== GENERATING LEGACY SYSTEM MIGRATIONS ==="

for i in {1..1000}; do
    # Legacy systems that might have old, inefficient configurations
    legacy_instance_types=("m4.large" "m4.xlarge" "m4.2xlarge" "c4.large" "c4.xlarge" "r4.large")
    legacy_instance_type=${legacy_instance_types[$((RANDOM % ${#legacy_instance_types[@]}))]}
    storage_sizes=(500 1000 2000 5000)
    storage_size=${storage_sizes[$((RANDOM % ${#storage_sizes[@]}))]}

    create_test "legacy_systems" "legacy_migration_$i" '{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [{
    "address": "aws_instance.legacy_app",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "instance_type": "'$legacy_instance_type'",
        "ami": "ami-99001122",
        "tags": {
          "Name": "legacy-app-'$i'",
          "Environment": "production",
          "Application": "legacy-system",
          "Migration": "in-progress",
          "Team": "migration"
        }
      }
    },
    "mode": "managed",
    "type": "aws_instance",
    "name": "legacy_app",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }, {
    "address": "aws_ebs_volume.legacy_storage",
    "change": {
      "actions": ["create"],
      "before": null,
      "after": {
        "size": '$storage_size',
        "type": "gp2",
        "availability_zone": "us-east-1a",
        "tags": {
          "Name": "legacy-storage-'$i'",
          "Environment": "production",
          "Application": "legacy-system"
        }
      }
    },
    "mode": "managed",
    "type": "aws_ebs_volume",
    "name": "legacy_storage",
    "provider_name": "registry.terraform.io/hashicorp/aws"
  }]
}'
done

echo "Generated $total_scenarios realistic Terraform plan variations"