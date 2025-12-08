# CostPilot Demo

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Status](https://img.shields.io/badge/status-stable-green.svg) ![Version](https://img.shields.io/badge/version-3.0.0-orange.svg)

Analyze infrastructure changes during pull requests and prevent costly cloud regressions before they merge.

> **⚠️ Important:** This repository is a deterministic demo environment.  
> Do not run `terraform apply`. It will create live AWS resources and incur charges.

---

## 🚀 Try the Live Demo

**https://dee66.github.io/costpilotdemo/**

Explore how CostPilot analyzes a realistic cost regression in PR 42:

- Baseline monthly cost
- Regression introduced in the pull request
- Four detailed findings
- Infrastructure impact mapping
- Trend chart crossing the SLO threshold
- Auto-fix suggestions

No installation required.

### 📸 Screenshot

```
[Screenshot: visual_assets/screenshots/hero.png]
```

---

## 📘 What This Repository Is

CostPilotDemo contains a deterministic scenario used for:

- Launch-day screenshots
- Documentation examples
- Walkthrough videos
- Public demo materials

All outputs in `snapshots/` are frozen and hash stable.

This repo does not run CostPilot. It exposes the controlled outputs produced during the pull request analysis for PR 42.

If you want to grasp CostPilot in under one minute, start with the live demo.

### ⚡ What You Can Do in 60 Seconds

- View the baseline cost
- Inspect the regression in PR 42
- Open all four findings
- See how changes propagate through AWS
- View the trend visualization
- Review the suggested fix

The demo requires no setup.

---

## 🗂️ Scenario Overview

This demo includes three Terraform configurations. All plans are pre-generated and safe to explore.

### Baseline (Cost-efficient starting point)

- Approximately $52 per month
- Lifecycle policies enabled
- Cost-optimized defaults

### PR Change (Regression scenario for PR 42)

- Approximately $388 per month
- Larger instance type
- Lifecycle policies removed
- Larger volumes and increased log retention

This is the scenario CostPilot flags during review.

### Noop Change (Low-noise validation)

- Cosmetic edits only
- Expected: zero findings
- Demonstrates low false positives

No AWS calls occur unless you intentionally execute Terraform commands.

---

## 🏃 Quick Start (Local Run)

Serve the demo locally:

```bash
cd demo
python3 -m http.server 8080
```

Open:

```
http://localhost:8080
```

This serves the same UI as the hosted demo using local files only.

---

## 🔍 PR 42 Walkthrough

CostPilot evaluates pull requests in four stages. The demo renders each stage using pre-generated outputs.

### Detect

Finds resource changes that influence cost:

- Attribute differences
- Severity levels
- Rule identifiers
- Policy violations

### Predict

Estimates cost impact:

- Baseline: $52 per month
- Regression: $388 per month
- Trend chart shows SLO threshold breach

### Explain

Provides structured rationale:

- Rules triggered
- Reason for increased cost
- Regression classification

### Suggest

Displays a deterministic patch:

- Reverts the regression
- Offers a cost-efficient alternative

All suggestions are static examples tied to this scenario.

---

## 📦 Golden Outputs

Canonical demo outputs are in `snapshots/`:

- `detect_v1.json`
- `predict_v1.json`
- `explain_v1.json`
- `snippet_v1.tf`
- `patch_v1.diff`

Golden outputs are frozen and versioned. They ensure reproducible demos, stable CI, and consistent documentation.

---

## 📁 Repository Structure

```
costpilotdemo/
  demo/                 UI for the live demo
  snapshots/            Frozen outputs for scenario v1
  infrastructure/       Baseline, PR change, noop stacks
  docs/                 Extended documentation
  tools/                Utility scripts
```

---

## 📚 Documentation

Extended documentation is located in `docs/`.

Recommended entry points:

- `docs/overview.md`
- `docs/scenarios/pr-42.md`
- `docs/architecture/`
- `docs/drift/`
- `docs/reproducibility/`

The README stays lightweight and directs deeper readers to the appropriate files.

---

## 🔒 Safety Notes

Terraform files in this repository are for demonstration only.

**Safe commands:**

```bash
terraform init
terraform validate
terraform plan
```

**Dangerous:**

```bash
terraform apply   # creates live AWS resources
```

See `infrastructure/terraform/SAFEGUARDS.md` for cleanup instructions.

---

## 📄 License

MIT License.

---

## 🎯 Call to Action

Open the demo, review PR 42, and see how CostPilot prevents cloud cost regressions before they merge:

**https://dee66.github.io/costpilotdemo/**