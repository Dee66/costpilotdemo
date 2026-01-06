# Golden Version Sign-Off Template

## Purpose
This template is used when intentionally updating golden outputs with a new version (e.g., v1 → v2).

---

## Version Information

- **Current Golden Version:** v1
- **Proposed Golden Version:** v2
- **Date:** YYYY-MM-DD
- **Requestor:** @username

---

## Reason for Version Bump

**Select one or more:**
- [ ] Spec v2.0.0 feature addition
- [ ] Infrastructure changes (new resources, configuration updates)
- [ ] Bug fix in detection/prediction logic
- [ ] Schema improvements or field additions
- [ ] Marketing requirement (new screenshot/video content)
- [ ] Other: _____________________________

**Detailed Explanation:**
<!-- Describe why the golden version needs to be updated -->



---

## Impact Analysis

### Files Changed

List all golden outputs that will change:

- [ ] `detect_v1.json` → `detect_v2.json`
- [ ] `predict_v1.json` → `predict_v2.json`
- [ ] `explain_v1.json` → `explain_v2.json`
- [ ] `snippet_v1.tf` → `snippet_v2.tf`
- [ ] `patch_v1.diff` → `patch_v2.diff`
- [ ] `trend_history_v1.json` → `trend_history_v2.json`
- [ ] Other: _____________________________

### Drift Type

**Select primary drift type:**
- [ ] File drift (direct edits to protected files)
- [ ] Semantic drift (content/severity changes)
- [ ] Structural drift (schema/field changes)

### Marketing Impact

- [ ] **LOW** - No screenshot/video updates needed
- [ ] **MEDIUM** - Minor screenshot updates required
- [ ] **HIGH** - Full screenshot/video regeneration required

**Details:**
<!-- Describe which marketing materials need updates -->



---

## Validation Checklist

**Before requesting sign-off:**

- [ ] Updated Terraform source (not outputs directly)
- [ ] Ran `./tools/reset_demo.sh` successfully
- [ ] All hashes validated with `python3 tools/validate_golden_hashes.py`
- [ ] Updated `golden_outputs_manifest.json` with new hashes
- [ ] Updated `docs/product.yml` → `canonical_spec_hash`
- [ ] Updated README references (v1 → v2)
- [ ] Tested CI pipeline locally
- [ ] Documented changes in this sign-off request

---

## New Golden Output Hashes

<!-- Run: sha256sum snapshots/*.json | cut -d' ' -f1 | head -c 16 -->

```
detect_v2.json:  ________________
predict_v2.json: ________________
explain_v2.json: ________________
```

---

## Sign-Off Required

### Engineering Team
- [ ] **@engineer1** - Technical validation passed
- [ ] **@engineer2** - CI tests passing
- [ ] **@engineer3** - Drift remediation confirmed

### Marketing Team
- [ ] **@marketing1** - Screenshot impact reviewed
- [ ] **@marketing2** - Video assets updated (if needed)

### Documentation Team
- [ ] **@docs1** - README updated
- [ ] **@docs2** - Spec documentation aligned

---

## Final Approval

**Approved by:** @username  
**Approval Date:** YYYY-MM-DD  
**Golden Version v2 Release Date:** YYYY-MM-DD

---

## Post-Release Tasks

- [ ] Tag release: `git tag golden-v2`
- [ ] Update changelog
- [ ] Notify team of new golden version
- [ ] Archive old golden v1 outputs (if needed)
- [ ] Update marketing materials
- [ ] Update product documentation

---

## Rollback Plan

**If v2 has issues:**

1. Revert to v1:
   ```bash
   git checkout golden-v1 -- snapshots/
   ```

2. Update manifest:
   ```bash
   # Restore v1 hashes in golden_outputs_manifest.json
   ```

3. Notify team and document rollback reason

---

## Notes

<!-- Add any additional context or concerns -->


