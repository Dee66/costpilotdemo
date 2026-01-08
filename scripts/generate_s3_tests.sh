#!/bin/bash

# Generate meaningful S3 storage optimization test files
# Focus on storage classes and lifecycle policies that should trigger detections

echo "Generating S3 storage optimization test files..."

# Create directory if it doesn't exist
mkdir -p optimization_tests/massive_suite/storage_optimization/s3_storage_classes

# Counter for file numbering
counter=4000

# Generate tests with Standard storage for archival data
echo "Creating Standard storage for old data tests..."
ages=("365" "730" "1095" "1825")  # 1yr, 2yr, 3yr, 5yr
for age in "${ages[@]}"; do
    cat > "optimization_tests/massive_suite/storage_optimization/s3_storage_classes/s3_old_data_standard_${age}days_$counter.json" << EOF
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_s3_bucket.old_data_standard_$counter",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "bucket": "old-data-bucket-$counter",
          "tags": {
            "Name": "old-data-standard-$counter",
            "DataAge": "${age}days",
            "StorageClass": "STANDARD",
            "Optimization": "s3-storage-class-expensive"
          }
        }
      },
      "mode": "managed",
      "type": "aws_s3_bucket",
      "name": "old_data_standard_$counter",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    },
    {
      "address": "aws_s3_bucket_lifecycle_configuration.old_data_standard_$counter",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "bucket": "old-data-bucket-$counter",
          "rule": [
            {
              "id": "old-data-transition",
              "status": "Enabled",
              "transition": [
                {
                  "days": 30,
                  "storage_class": "STANDARD_IA"
                },
                {
                  "days": 90,
                  "storage_class": "GLACIER"
                }
              ]
            }
          ]
        }
      },
      "mode": "managed",
      "type": "aws_s3_bucket_lifecycle_configuration",
      "name": "old_data_standard_$counter",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF
    ((counter++))
done

# Generate tests with no lifecycle policies for large buckets
echo "Creating no lifecycle policy tests..."
sizes=("100" "500" "1000" "5000")  # GB
for size in "${sizes[@]}"; do
    cat > "optimization_tests/massive_suite/storage_optimization/s3_storage_classes/s3_no_lifecycle_${size}gb_$counter.json" << EOF
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_s3_bucket.no_lifecycle_$counter",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "bucket": "large-bucket-no-lifecycle-$counter",
          "tags": {
            "Name": "large-bucket-no-lifecycle-$counter",
            "DataSize": "${size}GB",
            "HasLifecycle": "false",
            "Optimization": "s3-no-lifecycle-policy"
          }
        }
      },
      "mode": "managed",
      "type": "aws_s3_bucket",
      "name": "no_lifecycle_$counter",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF
    ((counter++))
done

# Generate tests with inefficient lifecycle transitions
echo "Creating inefficient lifecycle tests..."
transitions=(
  "30:GLACIER"      # Too aggressive to Glacier
  "1:DEEP_ARCHIVE"  # Way too aggressive
  "90:STANDARD_IA"  # Should be Glacier
  "365:STANDARD_IA" # Should be Glacier or Deep Archive
)
for transition in "${transitions[@]}"; do
    days=$(echo $transition | cut -d: -f1)
    storage_class=$(echo $transition | cut -d: -f2)
    cat > "optimization_tests/massive_suite/storage_optimization/s3_storage_classes/s3_inefficient_lifecycle_${days}days_${storage_class,,}_$counter.json" << EOF
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_s3_bucket.inefficient_lifecycle_$counter",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "bucket": "inefficient-lifecycle-bucket-$counter",
          "tags": {
            "Name": "inefficient-lifecycle-$counter",
            "TransitionDays": "$days",
            "StorageClass": "$storage_class",
            "Optimization": "s3-lifecycle-inefficient"
          }
        }
      },
      "mode": "managed",
      "type": "aws_s3_bucket",
      "name": "inefficient_lifecycle_$counter",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    },
    {
      "address": "aws_s3_bucket_lifecycle_configuration.inefficient_lifecycle_$counter",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "bucket": "inefficient-lifecycle-bucket-$counter",
          "rule": [
            {
              "id": "data-transition",
              "status": "Enabled",
              "transition": [
                {
                  "days": $days,
                  "storage_class": "$storage_class"
                }
              ]
            }
          ]
        }
      },
      "mode": "managed",
      "type": "aws_s3_bucket_lifecycle_configuration",
      "name": "inefficient_lifecycle_$counter",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF
    ((counter++))
done

# Generate tests with frequent access patterns but expensive storage
echo "Creating frequent access expensive storage tests..."
scenarios=(
  "logs:STANDARD"
  "temp:STANDARD"
  "cache:STANDARD_IA"
  "frequent:GLACIER"
)
for scenario in "${scenarios[@]}"; do
    data_type=$(echo $scenario | cut -d: -f1)
    storage_class=$(echo $scenario | cut -d: -f2)
    cat > "optimization_tests/massive_suite/storage_optimization/s3_storage_classes/s3_frequent_${data_type}_${storage_class,,}_$counter.json" << EOF
{
  "format_version": "1.2",
  "terraform_version": "1.6.0",
  "resource_changes": [
    {
      "address": "aws_s3_bucket.frequent_access_$counter",
      "change": {
        "actions": ["create"],
        "before": null,
        "after": {
          "bucket": "frequent-${data_type}-bucket-$counter",
          "tags": {
            "Name": "frequent-${data_type}-$counter",
            "AccessPattern": "frequent",
            "DataType": "$data_type",
            "StorageClass": "$storage_class",
            "Optimization": "s3-storage-class-mismatch"
          }
        }
      },
      "mode": "managed",
      "type": "aws_s3_bucket",
      "name": "frequent_access_$counter",
      "provider_name": "registry.terraform.io/hashicorp/aws"
    }
  ]
}
EOF
    ((counter++))
done

echo "Generated $(($(find optimization_tests/massive_suite/storage_optimization/s3_storage_classes -name "*.json" | wc -l))) new S3 storage optimization test files"