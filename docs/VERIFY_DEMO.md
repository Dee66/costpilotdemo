# Verify Demo

This guide provides step-by-step instructions to verify that the CostPilot demo environment produces the expected outputs on a clean machine.

## Prerequisites

- **CostPilot Binary**: Version 3.0.0 or later
- **Python**: 3.9+
- **Terraform**: 1.6+
- **Git**: Latest

## Step 1: Clone and Setup

```bash
git clone https://github.com/costpilot/demo.git
cd demo
```

## Step 2: Verify Repository Integrity

```bash
python scripts/validate_repository.py
```

Expected: Exit code 0, no errors.

## Step 3: Reproduce Terraform Plans

### Baseline Plan
```bash
cd infrastructure/terraform/baseline
terraform init
terraform plan -out=tfplan.binary
terraform show -json tfplan.binary > ../../../snapshots/plan_before.json
```

### PR Change Plan
```bash
cd ../pr_change
terraform plan -out=tfplan.binary
terraform show -json tfplan.binary > ../../../snapshots/plan_after.json
```

### Plan Diff
```bash
python scripts/generate_plan_diff.py snapshots/plan_before.json snapshots/plan_after.json > snapshots/plan_diff.json
```

## Step 4: Run CostPilot Analysis

```bash
# Detect
costpilot detect --baseline infrastructure/terraform/baseline --pr infrastructure/terraform/pr_change --output snapshots/detect_v1.json

# Predict
costpilot predict --input snapshots/detect_v1.json --output snapshots/predict_v1.json

# Explain
costpilot explain --input snapshots/predict_v1.json --output snapshots/explain_v1.json

# Autofix
costpilot autofix --input snapshots/explain_v1.json --output snapshots/autofix_v1.patch
```

## Expected Exit Codes

- All commands: 0 (success)
- No warnings or errors in stderr

## Expected Hashes

Run `python scripts/compute_hash_manifest.py` and verify `hash_manifest.json` matches the canonical hashes.

## Validation

```bash
python scripts/validate_repository.py
python scripts/test_regressions.py
```

All tests should pass with exit code 0.