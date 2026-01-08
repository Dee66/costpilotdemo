#!/bin/bash

# Generate meaningful EC2 instance rightsizing test files
# Focus on over-provisioned instances that should trigger optimization detections

echo "Generating EC2 instance rightsizing test files..."

# Create directory if it doesn't exist
mkdir -p optimization_tests/massive_suite/instance_rightsizing/compute_intensive

# Counter for file numbering
counter=2000

# Generate tests with clearly oversized compute instances for web workloads
echo "Creating oversized compute instances for web workloads..."
web_instance_types=("c5.9xlarge" "c5.12xlarge" "c5.18xlarge" "c5.24xlarge" "m5.8xlarge" "m5.12xlarge" "m5.16xlarge" "m5.24xlarge")
for instance_type in "${web_instance_types[@]}"; do
    cat > "optimization_tests/massive_suite/instance_rightsizing/compute_intensive/web_oversized_${instance_type//./_}_$counter.json" << EOF
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_instance.web_oversized_$counter",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "instance_type": "$instance_type",
          "ami": "ami-12345678",
          "tags": {
            "Name": "web-server-oversized-$counter",
            "Environment": "production",
            "Workload": "web-server",
            "Optimization": "instance-oversized"
          },
          "volume_tags": {
            "Name": "web-server-oversized-$counter"
          }
        }
      },
      "mode": "managed",
      "type": "aws_instance",
      "name": "web_oversized_$counter",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF
    ((counter++))
done

# Generate tests with memory-optimized instances for CPU-bound workloads
echo "Creating memory instances for CPU workloads..."
memory_instance_types=("r5.8xlarge" "r5.12xlarge" "r5.16xlarge" "r5.24xlarge" "r6g.8xlarge" "r6g.12xlarge" "r6g.16xlarge")
for instance_type in "${memory_instance_types[@]}"; do
    cat > "optimization_tests/massive_suite/instance_rightsizing/compute_intensive/memory_for_cpu_${instance_type//./_}_$counter.json" << EOF
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_instance.memory_for_cpu_$counter",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "instance_type": "$instance_type",
          "ami": "ami-12345678",
          "tags": {
            "Name": "cpu-workload-memory-instance-$counter",
            "Environment": "production",
            "Workload": "cpu-intensive",
            "Optimization": "wrong-instance-type"
          },
          "volume_tags": {
            "Name": "cpu-workload-memory-instance-$counter"
          }
        }
      },
      "mode": "managed",
      "type": "aws_instance",
      "name": "memory_for_cpu_$counter",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF
    ((counter++))
done

# Generate tests with very large instances for development workloads
echo "Creating massive instances for development..."
dev_instance_types=("c5.24xlarge" "m5.24xlarge" "r5.24xlarge" "c6g.16xlarge" "m6g.16xlarge")
for instance_type in "${dev_instance_types[@]}"; do
    cat > "optimization_tests/massive_suite/instance_rightsizing/compute_intensive/dev_massive_${instance_type//./_}_$counter.json" << EOF
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_instance.dev_massive_$counter",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "instance_type": "$instance_type",
          "ami": "ami-12345678",
          "tags": {
            "Name": "development-massive-$counter",
            "Environment": "development",
            "Workload": "development",
            "Optimization": "dev-oversized"
          },
          "volume_tags": {
            "Name": "development-massive-$counter"
          }
        }
      },
      "mode": "managed",
      "type": "aws_instance",
      "name": "dev_massive_$counter",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF
    ((counter++))
done

# Generate tests with GPU instances for non-GPU workloads
echo "Creating GPU instances for non-GPU workloads..."
gpu_instance_types=("p3.8xlarge" "p3.16xlarge" "g4dn.8xlarge" "g4dn.16xlarge" "g5.8xlarge")
for instance_type in "${gpu_instance_types[@]}"; do
    cat > "optimization_tests/massive_suite/instance_rightsizing/compute_intensive/gpu_for_web_${instance_type//./_}_$counter.json" << EOF
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_instance.gpu_for_web_$counter",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "instance_type": "$instance_type",
          "ami": "ami-12345678",
          "tags": {
            "Name": "web-server-gpu-$counter",
            "Environment": "production",
            "Workload": "web-server",
            "Optimization": "gpu-waste"
          },
          "volume_tags": {
            "Name": "web-server-gpu-$counter"
          }
        }
      },
      "mode": "managed",
      "type": "aws_instance",
      "name": "gpu_for_web_$counter",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF
    ((counter++))
done

echo "Generated $(($(find optimization_tests/massive_suite/instance_rightsizing/compute_intensive -name "*.json" | wc -l) - 1)) new EC2 compute-intensive test files"