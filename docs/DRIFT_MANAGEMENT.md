# Drift Management

## Overview

This document defines **drift** in the CostPilot Demo repository and explains detection, prevention, and remediation strategies. Drift threatens the determinism, reproducibility, and marketing reliability of golden outputs.

---

## Drift Types

### 1. File Drift

**Definition:** Any change to protected directories that alters golden outputs.

**Protected Directories:**
- `snapshots/` - Golden outputs with frozen hashes
- `costpilot_artifacts/` - CI-generated outputs
- `.costpilot/demo/` - Demo-specific frozen outputs
- `video_assets/` - Screenshots and marketing materials

**Examples:**
- Direct edits to `snapshots/detect_v1.json`
- Modifications to `snapshots/trend_v1.svg`
- Updates to golden output hashes
- Changes to artifact directory structure

**Detection:**
- CI checks file changes against protected patterns
- Hash validation in `golden_outputs_manifest.json`
- Git diff analysis in pull requests

---

### 2. Semantic Drift

**Definition:** Meaningful deviation in detection, prediction, or explanation content without structural changes.

**Manifestations:**
- Severity score changes (HIGH → MEDIUM)
- Regression classification changes (cost_increase → unbounded_growth)
- Cost estimate variations beyond acceptable tolerance
- Root cause analysis content changes
- Heuristic provenance alterations

**Examples:**

**Before (Golden v1):**
```json
{
  "finding_id": "detect-001",
  "severity": "high",
  "regression_type": "cost_increase"
}
```

**After (Semantic Drift):**
```json
{
  "finding_id": "detect-001",
  "severity": "medium",
  "regression_type": "configuration_change"
}
```

**Detection:**
- Automated field comparison in CI
- Regression classification validation
- Severity consistency checks
- Cost range variance analysis

---

### 3. Structural Drift

**Definition:** Changes to canonical output schema or required fields.

**Manifestations:**
- Missing required fields
- Field type changes (string → number)
- Schema version mismatches
- New undocumented fields without version bump
- Breaking changes to Trust Triangle output format

**Examples:**

**Before (Golden v1):**
```json
{
  "format_version": "1.0",
  "findings": [
    {
      "finding_id": "detect-001",
      "severity": "high"
    }
  ]
}
```

**After (Structural Drift):**
```json
{
  "version": "2.0",
  "results": [
    {
      "id": "detect-001",
      "level": "high"
    }
  ]
}
```

**Detection:**
- JSON schema validation
- Required field presence checks
- Field type consistency validation
- Format version verification

---

## Actions on Drift

When drift is detected:

### 1. **Fail CI Immediately**
```yaml
- name: Detect Drift
  run: |
    if [[ drift detected ]]; then
      echo "❌ ERROR: Drift detected in golden outputs"
      exit 1
    fi
```

### 2. **Block PR Merge**
- PR cannot be merged until drift is resolved
- Clear error message indicates which files drifted
- Links to remediation documentation

### 3. **Require Reset Script Execution**
```bash
./tools/reset_demo.sh
```
- Regenerates all outputs from source
- Validates deterministic hashes
- Updates golden manifest if intentional

### 4. **Manual Sign-Off for New Golden Versions**
- Engineering team reviews drift cause
- Marketing team validates screenshot impact
- Version bump decision (v1 → v2)
- Update `golden_outputs_manifest.json`

---

## Drift Prevention

### During Development

1. **Never edit protected directories directly**
   - Modify Terraform source instead
   - Run reset_demo.sh to regenerate
   
2. **Use version control**
   ```bash
   git diff snapshots/
   ```
   - Review changes before committing
   - Understand why outputs changed

3. **Run CI locally before pushing**
   ```bash
   .github/workflows/costpilot-ci.yml
   ```

### In CI/CD

1. **Protected file checks**
   ```bash
   git diff --name-only origin/main...HEAD | grep -E 'snapshots/|costpilot_artifacts/'
   ```

2. **Hash validation**
   ```bash
   python3 tools/validate_golden_hashes.py
   ```

3. **Semantic consistency checks**
   - Compare finding severities
   - Validate cost estimate ranges
   - Check regression classifications

---

## Drift Remediation

### For Unintentional Drift

1. **Revert changes:**
   ```bash
   git checkout origin/main -- snapshots/
   ```

2. **Run reset script:**
   ```bash
   ./tools/reset_demo.sh
   ```

3. **Verify determinism:**
   ```bash
   python3 tools/validate_golden_hashes.py
   ```

### For Intentional Changes (New Golden Version)

1. **Document the reason:**
   - Create issue explaining why v2 is needed
   - Link to spec changes or feature additions

2. **Update version references:**
   - Bump version in file names (v1 → v2)
   - Update `golden_outputs_manifest.json`
   - Update README references
   - Update marketing materials

3. **Recalculate hashes:**
   ```bash
   python3 scripts/add_lineage_metadata.py
   ```

4. **Update spec hash:**
   ```bash
   sha256sum docs/product.yml | cut -d' ' -f1
   ```
   Update in `docs/product.yml` → `expected_pr_scenario.canonical_spec_hash`

5. **Get team sign-off:**
   - Engineering: Technical validation
   - Marketing: Screenshot/video impact
   - Documentation: README updates

---

## Drift Detection in CI

### Current Implementation

Located in `.github/workflows/costpilot-ci.yml`:

```yaml
- name: Check for changes to protected directories
  run: |
    CHANGED_FILES=$(git diff --name-only origin/main...HEAD)
    
    PROTECTED_DIRS=("snapshots/" "costpilot_artifacts/" "video_assets/")
    
    for file in $CHANGED_FILES; do
      for protected_dir in "${PROTECTED_DIRS[@]}"; do
        if [[ "$file" == "$protected_dir"* ]]; then
          echo "❌ ERROR: Change detected in protected directory: $file"
          exit 1
        fi
      done
    done
```

### Future Enhancements

- **Semantic diff validation**
- **Schema consistency checks**
- **Automated version bump detection**
- **Marketing asset impact analysis**

---

## Monitoring & Alerts

### Hash Verification

Run after every snapshot regeneration:

```bash
cd /home/user/costpilotdemo
for file in snapshots/*.json; do
  current_hash=$(sha256sum "$file" | cut -d' ' -f1 | head -c 16)
  manifest_hash=$(jq -r ".golden_outputs.$(basename $file .json).hash" snapshots/golden_outputs_manifest.json)
  
  if [[ "$current_hash" != "$manifest_hash" ]]; then
    echo "❌ DRIFT: $file (expected: $manifest_hash, got: $current_hash)"
  fi
done
```

### Continuous Validation

Add to cron or pre-commit hooks:

```bash
#!/bin/bash
# .git/hooks/pre-commit

./tools/validate_golden_hashes.sh || {
  echo "❌ Golden output validation failed"
  echo "Run: ./tools/reset_demo.sh"
  exit 1
}
```

---

## Best Practices

### DO ✅

- Modify Terraform source, not outputs
- Run reset_demo.sh after infrastructure changes
- Validate hashes before committing
- Document reasons for golden version bumps
- Review drift errors carefully

### DON'T ❌

- Edit files in snapshots/ directly
- Commit without hash validation
- Ignore drift detection errors
- Bump versions without team sign-off
- Mix structural and semantic changes

---

## Glossary

| Term | Definition |
|------|------------|
| **Golden Output** | Frozen, versioned snapshot used for marketing and CI validation |
| **Drift** | Unintended deviation from golden outputs |
| **Hash Stability** | Property where outputs remain byte-identical across regenerations |
| **Semantic Drift** | Content changes without structural modifications |
| **Structural Drift** | Schema or field changes breaking compatibility |

---

## See Also

- `snapshots/golden_outputs_manifest.json` - Golden output registry
- `tools/reset_demo.sh` - Output regeneration script
- `.github/workflows/costpilot-ci.yml` - CI drift detection
- `docs/product.yml` - Canonical specification

---

**Last Updated:** 2025-12-06  
**Spec Version:** 2.0.0  
**Drift Policy Version:** 1.0
