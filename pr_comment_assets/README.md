# PR Comment Assets

This directory contains text templates for CostPilot PR comments that would appear on GitHub pull requests.

## Purpose

These comment templates demonstrate how CostPilot integrates into GitHub PR workflows, providing actionable cost analysis directly in pull request comments.

## Files

### 1. `comment_detect.txt`
**Purpose**: Detection phase output for PR comment  
**Content**: Cost-impacting changes detected in PR #42  
**Must Include**:
- List of detected changes with severity
- Resource classifications
- Rule IDs
- Quick summary of findings count

### 2. `comment_predict.txt`
**Purpose**: Cost prediction for PR comment  
**Content**: Predicted monthly cost impact  
**Must Include**:
- Baseline cost ($52.43)
- Predicted new cost ($387.89)
- Delta (+$335.46, +639.82%)
- Breakdown by service/resource
- Low/high range estimates

### 3. `comment_explain.txt`
**Purpose**: Root cause analysis for PR comment  
**Content**: Explanation of why costs are changing  
**Must Include**:
- Root causes (instance type upgrade, lifecycle deletion, etc.)
- Heuristic provenance
- Severity justification
- Cross-service impact explanation

### 4. `comment_autofix.txt`
**Purpose**: Auto-fix suggestions for PR comment  
**Content**: Suggested code changes to reduce cost  
**Must Include**:
- Specific Terraform code snippets
- Before/after comparisons
- Expected cost savings per fix
- Priority order (fix high-severity first)

## Comment Requirements

All PR comments must:

✅ Reference **PR #42** for consistency  
✅ Show **baseline** and **pr-change** branch names  
✅ Display **dollar impact clearly** (e.g., +$335.46/month)  
✅ Show **severity levels** (high/medium/low)  
✅ Suggest **specific fixes** with code snippets  
✅ Be **copy-pastable** from actual CostPilot output  
✅ Be **readable at 1080p and mobile**  
✅ Match corresponding JSON outputs in `snapshots/`

## Comment Structure

### Standard Header
```
🤖 CostPilot Analysis — PR #42

Branch: feature/upgrade-instances → main
Baseline: infrastructure/terraform/baseline/
PR Stack: infrastructure/terraform/pr-change/
```

### Standard Footer
```
---
📊 View detailed analysis: [CostPilot Dashboard]
🔧 Auto-fix suggestions available
⚙️ CostPilot v1.0.0 | Scenario v1
```

## Usage in CI/CD

These comment templates are designed to be posted automatically by GitHub Actions:

```yaml
- name: Post CostPilot Comment
  uses: actions/github-script@v6
  with:
    script: |
      const fs = require('fs');
      const comment = fs.readFileSync('pr_comment_assets/comment_detect.txt', 'utf8');
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: comment
      });
```

## Validation

Before committing comment files:

1. **Verify readability**: Comments must be clear at 1080p and mobile
2. **Check formatting**: Markdown tables, code blocks must render correctly
3. **Validate data**: All costs must match `snapshots/predict_v1.json`
4. **Test GitHub rendering**: Use GitHub's markdown preview
5. **Mobile test**: View on mobile device (minimum 375px width)

## Mobile Readability Guidelines

- Use short table columns (≤ 20 chars per cell)
- Avoid horizontal scrolling
- Use line breaks to stack information vertically
- Test on 375px viewport (iPhone SE size)

## Example Formats

### Detect Summary (Mobile-Friendly)
```
🔍 **2 High-Severity Changes Detected**

1. EC2 Instance Type
   • t3.micro → t3.xlarge
   • Rule: EC2_INSTANCE_TYPE_CHANGE
   • Severity: HIGH

2. S3 Lifecycle Disabled
   • lifecycle_configuration: deleted
   • Rule: S3_LIFECYCLE_DISABLED
   • Severity: HIGH
```

### Cost Prediction (Clear Dollar Impact)
```
📊 **Monthly Cost Impact**

Baseline:  $52.43/month
Predicted: $387.89/month
Delta:     +$335.46 (+639.82%)

⚠️ Exceeds baseline by 6.4x
```

### Auto-Fix Snippet (Copy-Pastable)
```
🔧 **Suggested Fix: Revert to t3.micro**

resource "aws_launch_template" "main" {
  name_prefix   = "costpilot-demo-"
- instance_type = "t3.xlarge"  # ❌ High cost
+ instance_type = "t3.micro"   # ✅ Cost-efficient

  # ... rest of config
}

💰 Estimated savings: $128/month per instance
```

## Versioning

Comment templates are versioned alongside golden outputs:

- **v1**: Current version, matches `snapshots/*_v1.json`
- **v2**: Future version after spec updates

Any change to comment content requires:
1. Version bump (v1 → v2)
2. Update references in documentation
3. Team sign-off via `docs/GOLDEN_VERSION_SIGNOFF.md`

---

**Last Updated**: 2025-12-06  
**Version**: 1.0.0
