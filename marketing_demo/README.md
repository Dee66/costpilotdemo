# CostPilot Demo

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Status](https://img.shields.io/badge/status-stable-green.svg) ![Version](https://img.shields.io/badge/version-3.0.0-orange.svg)

> **🚨 DEMO NOTICE:** This is a demonstration repository only. See [DEMO.md](DEMO.md) for important warnings.

Analyze infrastructure changes during pull requests and prevent costly cloud regressions before they merge.

> **⚠️ Important:** This repository is a deterministic demo environment.  
> Do not run `terraform apply`. It will create live AWS resources and incur charges.

## 🎯 Demo First Rule

**This repository is the source-of-truth for all CostPilot marketing claims.**

- Any feature not demonstrated here may not appear in marketing materials
- All screenshots, videos, and examples must originate from this exact repository
- External blog posts, docs, and videos must be reproducible from this repo
- Marketing assets must be derived from demo outputs, not vice versa
- Demo drift from the product spec is a release-blocking CI failure

For the canonical product specification: [Product Spec](docs/product.yml)

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

### 🔍 Verification

For complete verification instructions: [Verify Demo Guide](docs/VERIFY_DEMO.md)

For hostile reviewers: [Hostile Reviewer Walkthrough](docs/HOSTILE_REVIEWER_WALKTHROUGH.md)

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

Start the interactive demo with a single command:

```bash
# Option 1: Use the wrapper script (recommended)
./start_demo.sh

# Option 2: Use the Python script directly
python3 scripts/start_demo.py

# Option 3: Manual server start (legacy)
cd demo && python3 -m http.server 8000
```

The startup script will:
- ✅ Validate all demo components are present
- ✅ Start the web server on http://localhost:8000
- ✅ Automatically open your browser
- ✅ Display access URLs for all demo features

**Demo URLs:**
- **Main Demo**: http://localhost:8000/
- **Interactive Demo**: http://localhost:8000/demo/
- **ROI Calculator**: http://localhost:8000/docs/ROI_CALCULATOR.md

**Command Options:**
```bash
./start_demo.sh --help
./start_demo.sh --port 8080          # Custom port
./start_demo.sh --no-browser         # Don't open browser
./start_demo.sh --validate-only      # Just check components
```

---

## 🚀 Getting Started

Follow these steps to set up and run the demo:

### Prerequisites

Ensure you have the following installed:
- [Node.js](https://nodejs.org/) (v16 or higher)
- [npm](https://www.npmjs.com/) (comes with Node.js)
- [Terraform](https://www.terraform.io/) (v1.3 or higher)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/CostPilotDemo.git
   cd CostPilotDemo/marketing_demo
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

### Running the Demo

1. Start the demo server:
   ```bash
   npm start
   ```

2. Open your browser and navigate to `http://localhost:3000`.

### Cleaning Up

To remove any temporary files or reset the demo:
```bash
npm run clean
```

---

## �️ CostPilot CLI Demo

This repository includes a demonstration CLI binary that showcases CostPilot's command-line interface and output formats.

**Demo Features:**
- Command-line interface examples
- Output format demonstrations
- Static analysis of pre-generated Terraform plans

**Note:** This is a demo binary for illustration purposes. For actual CostPilot functionality, refer to the official product documentation.

**Documentation:** [CLI Command Reference](docs/CLI_COMMANDS.md)

---

## �🔍 PR 42 Walkthrough

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

- [docs/overview.md](docs/overview.md)
- [docs/scenarios/pr-42.md](docs/scenarios/pr-42.md)
- [docs/architecture/](docs/architecture/)
- [docs/drift/](docs/drift/)
- [docs/reproducibility/](docs/reproducibility/)

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

## � Business Impact Metrics

### User Experience
- **Time to Understanding**: Reduced from 30+ minutes to <3 minutes via interactive demo
- **Self-Service Demo Completion**: Target 50% (tracked via GitHub Pages analytics)
- **Video Watch Completion**: Target 80% for 3-minute walkthrough

### Community Growth
- **GitHub Stars**: Target 5x increase (current: baseline tracking)
- **Forks**: Target 5x increase (current: baseline tracking)

### Development Velocity
- **Test Execution Time**: Reduced by 20% through optimization
- **CI Pipeline**: <5 minute runtime with comprehensive validation

---

## �📄 License

MIT License.

---

## 🎯 Call to Action

Open the demo, review PR 42, and see how CostPilot prevents cloud cost regressions before they merge:

**https://dee66.github.io/costpilotdemo/**