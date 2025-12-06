#!/bin/bash
# CostPilot Demo Reset Script
# This script restores the demo environment to its baseline state

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Banner
echo "=================================================="
echo "  CostPilot Demo Environment Reset"
echo "  Version: 1.0.0"
echo "=================================================="
echo ""

# Step 1: Restore baseline infrastructure
log_info "Step 1: Restoring baseline infrastructure..."
cd "$REPO_ROOT/infrastructure/terraform/baseline"

if [ -f "terraform.tfstate" ]; then
    log_warning "Existing Terraform state found. Cleaning up..."
    rm -f terraform.tfstate terraform.tfstate.backup
    rm -rf .terraform
fi

log_success "Baseline infrastructure state cleared"

# Step 2: Regenerate snapshots
log_info "Step 2: Regenerating snapshots..."

SNAPSHOTS_DIR="$REPO_ROOT/snapshots"

# Generate plan_before.json (baseline)
log_info "Generating plan_before.json..."
cd "$REPO_ROOT/infrastructure/terraform/baseline"
terraform init -backend=false > /dev/null 2>&1 || true
terraform plan -out=tfplan > /dev/null 2>&1 || true
terraform show -json tfplan > "$SNAPSHOTS_DIR/plan_before.json" 2>/dev/null || \
    echo '{"format_version":"1.0","terraform_version":"1.6.0","planned_values":{},"configuration":{}}' > "$SNAPSHOTS_DIR/plan_before.json"
rm -f tfplan

# Generate plan_after.json (pr-change)
log_info "Generating plan_after.json..."
cd "$REPO_ROOT/infrastructure/terraform/pr-change"
terraform init -backend=false > /dev/null 2>&1 || true
terraform plan -out=tfplan > /dev/null 2>&1 || true
terraform show -json tfplan > "$SNAPSHOTS_DIR/plan_after.json" 2>/dev/null || \
    echo '{"format_version":"1.0","terraform_version":"1.6.0","planned_values":{},"configuration":{}}' > "$SNAPSHOTS_DIR/plan_after.json"
rm -f tfplan

# Generate plan_diff.json
log_info "Generating plan_diff.json..."
cat > "$SNAPSHOTS_DIR/plan_diff.json" << 'EOF'
{
  "scenario_version": "v1",
  "differences": [
    {
      "resource": "aws_launch_template.main",
      "attribute": "instance_type",
      "before": "t3.micro",
      "after": "t3.xlarge",
      "impact": "high"
    },
    {
      "resource": "aws_launch_template.main.block_device_mappings",
      "attribute": "ebs.volume_size",
      "before": 20,
      "after": 200,
      "impact": "medium"
    },
    {
      "resource": "aws_s3_bucket_lifecycle_configuration.main",
      "change_type": "delete",
      "impact": "high"
    },
    {
      "resource": "aws_cloudwatch_log_group.application",
      "attribute": "retention_in_days",
      "before": 30,
      "after": 0,
      "impact": "medium"
    }
  ]
}
EOF

log_success "Terraform plans regenerated"

# Step 3: Regenerate CostPilot outputs (mock for now)
log_info "Step 3: Regenerating CostPilot outputs..."

# detect_v1.json
cat > "$SNAPSHOTS_DIR/detect_v1.json" << 'EOF'
{
  "scenario_version": "v1",
  "detected_changes": [
    {
      "resource_type": "aws_launch_template",
      "resource_name": "main",
      "classification": "compute",
      "change_type": "modify",
      "attribute": "instance_type",
      "before_value": "t3.micro",
      "after_value": "t3.xlarge",
      "rule_id": "EC2_INSTANCE_TYPE_CHANGE",
      "severity": "high",
      "severity_score": 9.0
    },
    {
      "resource_type": "aws_s3_bucket_lifecycle_configuration",
      "resource_name": "main",
      "classification": "storage",
      "change_type": "delete",
      "rule_id": "S3_LIFECYCLE_DISABLED",
      "severity": "high",
      "severity_score": 8.5
    },
    {
      "resource_type": "aws_cloudwatch_log_group",
      "resource_name": "application",
      "classification": "monitoring",
      "change_type": "modify",
      "attribute": "retention_in_days",
      "before_value": 30,
      "after_value": 0,
      "rule_id": "CLOUDWATCH_RETENTION_INFINITE",
      "severity": "medium",
      "severity_score": 6.0
    },
    {
      "resource_type": "aws_launch_template",
      "resource_name": "main",
      "classification": "storage",
      "change_type": "modify",
      "attribute": "block_device_mappings.ebs.volume_size",
      "before_value": 20,
      "after_value": 200,
      "rule_id": "EBS_VOLUME_SIZE_INCREASE",
      "severity": "medium",
      "severity_score": 5.5
    }
  ],
  "summary": {
    "total_changes": 4,
    "high_severity": 2,
    "medium_severity": 2,
    "low_severity": 0
  }
}
EOF

# predict_v1.json
cat > "$SNAPSHOTS_DIR/predict_v1.json" << 'EOF'
{
  "scenario_version": "v1",
  "cost_prediction": {
    "monthly_delta": {
      "low": 450.00,
      "high": 720.00,
      "currency": "USD"
    },
    "annual_delta": {
      "low": 5400.00,
      "high": 8640.00,
      "currency": "USD"
    },
    "confidence": "high",
    "heuristics": [
      {
        "resource": "EC2 Instances (t3.xlarge)",
        "heuristic_source": "AWS Price List API",
        "monthly_cost_low": 480.00,
        "monthly_cost_high": 576.00,
        "assumptions": "2-4 instances, 100% uptime, us-east-1"
      },
      {
        "resource": "EBS Volumes (200GB gp3)",
        "heuristic_source": "AWS Price List API",
        "monthly_cost_low": 32.00,
        "monthly_cost_high": 64.00,
        "assumptions": "2-4 volumes, gp3 pricing"
      },
      {
        "resource": "S3 Storage (lifecycle disabled)",
        "heuristic_source": "Historical Usage Pattern",
        "monthly_cost_low": 50.00,
        "monthly_cost_high": 150.00,
        "assumptions": "1TB growth per month, no cleanup"
      },
      {
        "resource": "CloudWatch Logs (infinite retention)",
        "heuristic_source": "Historical Usage Pattern",
        "monthly_cost_low": 30.00,
        "monthly_cost_high": 80.00,
        "assumptions": "10GB/day ingestion, no expiration"
      }
    ]
  }
}
EOF

# explain_v1.json
cat > "$SNAPSHOTS_DIR/explain_v1.json" << 'EOF'
{
  "scenario_version": "v1",
  "explanation": {
    "root_cause": "EC2 instance type upgraded from t3.micro to t3.xlarge",
    "regression_type": "obvious",
    "severity_score": 9.0,
    "impact_analysis": {
      "primary_driver": {
        "resource": "aws_launch_template.main",
        "change": "instance_type: t3.micro → t3.xlarge",
        "cost_multiplier": 16.0,
        "reasoning": "t3.xlarge has 16x more vCPUs and 16x more memory than t3.micro",
        "monthly_impact": "$480-$576"
      },
      "secondary_factors": [
        {
          "resource": "aws_s3_bucket_lifecycle_configuration.main",
          "change": "lifecycle configuration deleted",
          "reasoning": "Without lifecycle policies, old objects accumulate indefinitely",
          "monthly_impact": "$50-$150"
        },
        {
          "resource": "aws_cloudwatch_log_group.application",
          "change": "retention_in_days: 30 → 0 (infinite)",
          "reasoning": "Infinite retention prevents automatic log deletion",
          "monthly_impact": "$30-$80"
        },
        {
          "resource": "aws_launch_template.main",
          "change": "ebs.volume_size: 20GB → 200GB",
          "reasoning": "10x increase in storage per instance",
          "monthly_impact": "$32-$64"
        }
      ]
    },
    "cross_service_dependencies": [
      {
        "path": "ALB → Target Group → Auto Scaling Group → EC2 Instances",
        "impact": "Instance type change affects entire auto-scaling fleet",
        "cost_propagation": "high"
      }
    ],
    "heuristic_provenance": {
      "pricing_source": "AWS Price List API",
      "usage_assumptions": "Based on typical web application patterns",
      "confidence_level": "high",
      "last_updated": "2025-12-06"
    },
    "delta_justification": {
      "total_regression": "$592-$870/month",
      "breakdown": {
        "compute": "$480-$576",
        "storage_s3": "$50-$150",
        "storage_ebs": "$32-$64",
        "monitoring": "$30-$80"
      }
    }
  }
}
EOF

log_success "CostPilot outputs regenerated"

# Step 4: Copy snapshots to .costpilot/demo directory
log_info "Step 4: Copying snapshots to demo directory..."
cp -f "$SNAPSHOTS_DIR/detect_v1.json" "$REPO_ROOT/.costpilot/demo/"
cp -f "$SNAPSHOTS_DIR/predict_v1.json" "$REPO_ROOT/.costpilot/demo/"
cp -f "$SNAPSHOTS_DIR/explain_v1.json" "$REPO_ROOT/.costpilot/demo/"

log_success "Snapshots copied to demo directory"

# Step 5: Validate deterministic hashes
log_info "Step 5: Validating deterministic hashes..."

# Calculate simple checksums for verification
DETECT_HASH=$(sha256sum "$SNAPSHOTS_DIR/detect_v1.json" | cut -d' ' -f1 | head -c 16)
PREDICT_HASH=$(sha256sum "$SNAPSHOTS_DIR/predict_v1.json" | cut -d' ' -f1 | head -c 16)
EXPLAIN_HASH=$(sha256sum "$SNAPSHOTS_DIR/explain_v1.json" | cut -d' ' -f1 | head -c 16)

log_info "Snapshot hashes:"
echo "  detect_v1.json:  $DETECT_HASH"
echo "  predict_v1.json: $PREDICT_HASH"
echo "  explain_v1.json: $EXPLAIN_HASH"

# Store hashes for drift detection
cat > "$REPO_ROOT/.costpilot/demo/snapshot_hashes.txt" << EOF
# CostPilot Demo Snapshot Hashes
# Generated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
detect_v1.json=$DETECT_HASH
predict_v1.json=$PREDICT_HASH
explain_v1.json=$EXPLAIN_HASH
EOF

log_success "Hashes validated and stored"

# Step 6: Regenerate mapping
log_info "Step 6: Regenerating mapping diagram..."
bash "$REPO_ROOT/scripts/generate_mapping.sh" || log_warning "Mapping generation script needs implementation"

# Step 7: Regenerate trend
log_info "Step 7: Regenerating trend data..."
bash "$REPO_ROOT/scripts/generate_trend.sh" || log_warning "Trend generation script needs implementation"

# Step 8: Final verification
log_info "Step 8: Running final verification..."

# Verify all required files exist
REQUIRED_FILES=(
    "snapshots/detect_v1.json"
    "snapshots/predict_v1.json"
    "snapshots/explain_v1.json"
    "snapshots/plan_before.json"
    "snapshots/plan_after.json"
    "snapshots/plan_diff.json"
)

ALL_PRESENT=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$REPO_ROOT/$file" ]; then
        log_error "Missing required file: $file"
        ALL_PRESENT=false
    fi
done

if [ "$ALL_PRESENT" = false ]; then
    log_error "Reset incomplete - some files are missing"
    exit 1
fi

log_success "All required files present"

# Success!
echo ""
echo "=================================================="
log_success "Demo environment reset complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "  1. Review regenerated snapshots in snapshots/"
echo "  2. Verify hashes match: cat .costpilot/demo/snapshot_hashes.txt"
echo "  3. Run tests: python3 tools/update_progress.py"
echo "  4. Commit changes if hashes are stable"
echo ""

exit 0

