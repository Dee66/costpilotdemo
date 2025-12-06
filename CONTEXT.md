# CostPilot Demo Repository - Context Summary

## 📋 Overview

This repository is the **canonical demonstration environment** for CostPilot. All marketing screenshots, videos, product documentation examples, and PR walk-throughs MUST originate from this repo. The environment is designed to be deterministic, hash-stable, and drift-safe.

## 🎯 Key Objectives

1. **Deterministic & Reproducible**: End-to-end demonstration of CostPilot
2. **Trust Triangle**: Showcase Detect → Predict → Explain workflow
3. **Autofix Demo**: Snippet-based patches for EC2 + S3 only
4. **Mapping & Trends**: Demonstrate visual cost propagation
5. **Launch Assets**: Provide materials for marketing and videos
6. **Public-Safe**: Lightweight and suitable for public consumption

## 📁 Repository Structure

```
CostPilotDemo/
├── README.md                          # Main documentation
├── checklist.md                       # Implementation progress tracker
├── costpilot.yml                      # CostPilot configuration
├── .gitignore                         # Git ignore rules
│
├── docs/                              # Specification documents
│   ├── products.yml                   # Product specification
│   └── checklist.yml                  # Implementation checklist
│
├── .github/
│   └── workflows/
│       └── costpilot-ci.yml          # CI/CD pipeline
│
├── infrastructure/
│   └── terraform/
│       ├── baseline/                  # Cost-efficient baseline
│       │   ├── main.tf
│       │   ├── variables.tf
│       │   └── outputs.tf
│       ├── pr-change/                 # Regression scenarios
│       │   ├── main.tf
│       │   ├── variables.tf
│       │   └── outputs.tf
│       └── noop-change/               # No-op validation
│           ├── main.tf
│           ├── variables.tf
│           └── outputs.tf
│
├── snapshots/                         # Frozen reference outputs
│   ├── plan_before.json
│   ├── plan_after.json
│   ├── plan_diff.json
│   ├── detect_v1.json
│   ├── predict_v1.json
│   ├── explain_v1.json
│   ├── snippet_v1.tf
│   ├── patch_v1.diff
│   ├── mapping_v1.mmd
│   └── trend_v1.svg
│
├── costpilot_demo/                    # Demo-specific outputs
│   ├── detect_v1.json
│   ├── predict_v1.json
│   ├── explain_v1.json
│   ├── snippet_v1.tf
│   ├── patch_v1.diff
│   ├── mapping_v1.mmd
│   ├── trend_history.json
│   └── trend_v1.svg
│
├── costpilot_artifacts/               # Dynamic CostPilot outputs
│   ├── output_detect.json
│   ├── output_predict.json
│   ├── output_explain.json
│   ├── output_snippet.tf
│   ├── output_patch.diff
│   ├── output_mapping.mmd
│   └── output_trend.json
│
├── tools/                             # Utility scripts
│   ├── README.md                      # Tools documentation
│   ├── reset_demo.sh                  # Demo reset script
│   └── update_progress.py             # Progress tracker
│
└── scripts/                           # Generation scripts
    ├── generate_snapshots.sh
    ├── generate_mapping.sh
    ├── generate_trend.sh
    └── verify_hashes.sh
```

## 🔺 The Trust Triangle

CostPilot's core workflow consists of three stages:

### 1. **Detect** 🔍
- Resource classification
- Rule IDs
- Severity scoring

### 2. **Predict** 📊
- Heuristic references
- Cost ranges (low, high)
- Cold start assumptions

### 3. **Explain** 💡
- Root cause analysis
- Regression type
- Severity score
- Heuristic provenance
- Delta justification

## 🎭 Demo Scenarios

### Baseline Stack
- **Purpose**: Cost-efficient baseline for comparison
- **Resources**:
  - EC2 t3.micro autoscaling group
  - ALB + Target Group + Listener
  - S3 bucket with lifecycle enabled
  - CloudWatch Logs (30-day retention)

### PR Regression Stack
- **Purpose**: Introduce realistic cost regressions
- **Obvious Regressions**:
  - EC2: t3.micro → t3.xlarge
  - S3: Lifecycle disabled
- **Subtle Regressions**:
  - CloudWatch: 30 days → infinite retention
  - EBS: 20GB → 200GB

### Noop Change
- **Purpose**: Validate low false-positive rate
- **Expected**: No findings

## 🔧 Implementation Progress

**Total Tasks**: 151  
**Current Progress**: Track in `checklist.md`

### Update Progress
```bash
python3 tools/update_progress.py
```

## 📊 Deterministic Constraints

All outputs must be:
- ✅ Hash-stable across runs
- ✅ Float precision: 2 decimal places
- ✅ Whitespace normalized
- ✅ Ordering enforced
- ✅ Layout seeds fixed
- ✅ Themes consistent

## 🎨 Output Requirements

### Required Artifacts
- `detect_v1.json` - Detection results
- `predict_v1.json` - Cost predictions
- `explain_v1.json` - Explanations
- `snippet_v1.tf` - Code snippets
- `patch_v1.diff` - Patch previews
- `mapping_v1.mmd` - Mermaid diagrams
- `trend_history.json` - Trend data
- `trend_v1.svg` - Trend visualizations

### Patch Preview Scope
**Supported Resources**:
- EC2 instance types
- S3 lifecycle rules

**Why Limited?**
> Networking and NAT gateway rewrites require broader context not available to deterministic snippet-mode demonstration.

## 🚀 CI/CD Pipeline

### Guardrails
**Protected Directories**:
- `snapshots/*`
- `costpilot_artifacts/*`
- `video_assets/*`

**Allowed Changes**:
- `infrastructure/terraform/pr-change/*`
- `README.md`
- `costpilot.yml`

### Validation Checks
- ✅ Deterministic output verification
- ✅ Noop produces no findings
- ✅ Drift detection
- ✅ Hash consistency

## ⚡ Performance Targets

- **Detect**: < 200ms
- **Predict**: < 300ms
- **Explain**: < 300ms

## 📝 Documentation Standards

### README Requirements
- Hero copy with value proposition
- Statement of purpose
- Quickstart steps
- Sample PR walkthrough
- Mapping examples
- Trend examples
- Trust Triangle explanation
- Scope limitations
- Scenario versioning

## 🔐 Version Control

- **Scenario Version**: v1
- **Spec Version**: 1.0.0
- **Git Branch**: main (baseline)
- **PR Branch**: feature/cost-regression-demo
- **Sample PR**: #42

## 🎓 Usage Guide

### For Contributors
1. Check `checklist.md` for current progress
2. Pick an unchecked task
3. Implement according to `docs/products.yml` spec
4. Mark task complete: `- [x]`
5. Run: `python3 tools/update_progress.py`
6. Commit changes

### For Reviewers
1. Verify deterministic output
2. Check hash consistency
3. Validate Trust Triangle completeness
4. Ensure no drift in protected files
5. Confirm documentation accuracy

## 🚫 Explicit Exclusions

This demo does NOT include:
- Enterprise features
- Enterprise policies
- Exemptions demo
- SLO burn reports
- Team attribution

**Rationale**: Keep it lightweight, public-safe, and MVP-aligned.

## 📄 License

MIT License - Safe for public tutorials, demos, and launch content.

## 🔗 Key Files

- **Spec**: `docs/products.yml`
- **Checklist**: `docs/checklist.yml`
- **Progress**: `checklist.md`
- **Tracker**: `tools/update_progress.py`
- **Reset**: `tools/reset_demo.sh`

---

*Last Updated: 2025-12-06*  
*Context maintained for entire conversation*
