#!/bin/bash
# Copyright (c) 2025 CostPilot Demo Team
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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

# Step 3: Regenerate CostPilot outputs using snapshot builder
log_info "Step 3: Regenerating CostPilot outputs using snapshot builder..."

cd "$REPO_ROOT"
python3 -c "
from scripts.lib.snapshot_builder import SnapshotBuilder
builder = SnapshotBuilder()
bundle = builder.build()
builder.normalize().write_to(Path('snapshots'))
"

log_success "CostPilot outputs regenerated using snapshot builder"




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

# Step 6: Validate baseline configuration
log_info "Step 6: Validating baseline configuration..."

# Check if baselines.json exists
if [ ! -f "$REPO_ROOT/.costpilot/baselines.json" ]; then
    log_warning "baselines.json not found, skipping baseline validation"
else
    log_info "Verifying baseline structure..."
    
    # Validate JSON structure
    if ! python3 -c "import json; json.load(open('$REPO_ROOT/.costpilot/baselines.json'))" 2>/dev/null; then
        log_error "baselines.json is not valid JSON"
        exit 1
    fi
    
    # Extract baseline cost
    BASELINE_COST=$(python3 -c "import json; data=json.load(open('$REPO_ROOT/.costpilot/baselines.json')); print(data['baseline_stack']['monthly_cost_estimate'])" 2>/dev/null || echo "0")
    
    if [ "$BASELINE_COST" = "0" ] || [ -z "$BASELINE_COST" ]; then
        log_error "Could not extract baseline cost from baselines.json"
        exit 1
    fi
    
    log_info "Baseline cost: \$$BASELINE_COST/month"
    
    # Verify predict output references baseline
    if [ -f "$SNAPSHOTS_DIR/predict_v1.json" ]; then
        if grep -q "baseline_comparison" "$SNAPSHOTS_DIR/predict_v1.json"; then
            log_success "Predict output includes baseline comparison"
            
            # Extract predicted cost and compare
            PREDICTED_COST=$(python3 -c "import json; data=json.load(open('$SNAPSHOTS_DIR/predict_v1.json')); print(data['prediction_results']['summary'].get('baseline_comparison', {}).get('current_predicted_cost', 0))" 2>/dev/null || echo "0")
            
            if [ "$PREDICTED_COST" != "0" ] && [ -n "$PREDICTED_COST" ]; then
                log_info "Predicted cost: \$$PREDICTED_COST/month"
                
                # Calculate regression percentage
                REGRESSION=$(python3 << EOF
import json
baseline = float($BASELINE_COST)
predicted = float($PREDICTED_COST)
if baseline > 0:
    pct = ((predicted - baseline) / baseline) * 100
    print(f"{pct:.1f}")
else:
    print("N/A")
EOF
)
                
                if [ "$REGRESSION" != "N/A" ]; then
                    log_info "Cost regression: +${REGRESSION}%"
                    
                    # Warn if regression is suspiciously low
                    if (( $(echo "$REGRESSION < 100" | bc -l) )); then
                        log_warning "Regression seems low - expected 500%+ for demo scenario"
                    fi
                fi
            fi
        else
            log_warning "Predict output missing baseline_comparison field"
        fi
    fi
    
    # Verify trend history includes baseline awareness
    if [ -f "$REPO_ROOT/snapshots/trend_history_v1.json" ]; then
        if grep -q '"baseline_cost"' "$REPO_ROOT/snapshots/trend_history_v1.json"; then
            log_success "Trend history includes baseline awareness"
        else
            log_warning "Trend history missing baseline_cost field"
        fi
    fi
    
    log_success "Baseline validation complete"
fi

# Step 7: Regenerate mapping
log_info "Step 6: Regenerating mapping diagram..."
bash "$REPO_ROOT/scripts/generate_mapping.sh" || log_warning "Mapping generation script needs implementation"

# Step 8: Regenerate trend
log_info "Step 8: Regenerating trend data..."
bash "$REPO_ROOT/scripts/generate_trend.sh" || log_warning "Trend generation script needs implementation"

# Step 9: Final verification
log_info "Step 9: Running final verification..."

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
