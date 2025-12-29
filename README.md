# CostPilot Demo: Zero-IAM FinOps for Terraform

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Status](https://img.shields.io/badge/status-stable-green.svg) ![Version](https://img.shields.io/badge/version-1.0.2-orange.svg)

Catch AWS cost regressions in Terraform PRs without IAM or network access—try the interactive demo now.

## What It Is

CostPilot is a GitHub-native, zero-permission FinOps engine that analyzes Terraform IaC locally to detect cost issues, predict monthly AWS spend, explain changes with auditable heuristics, and generate autofix snippets or patches. It runs offline, uses deterministic rules, and enforces policies/SLOs—all without touching live infrastructure or requiring credentials.

Perfect for teams wanting cost control in CI without the IAM hassle.

## Try the Demo

**Live Demo**: [https://dee66.github.io/costpilotdemo/](https://dee66.github.io/costpilotdemo/)

Explore detection, prediction, autofix, and more on sample Terraform plans.

### Run Locally
1. Clone: `git clone https://github.com/Dee66/costpilotdemo.git`
2. Install: `npm install`
3. Start: `npm start`
4. Open: [http://localhost:3000](http://localhost:3000)

Requires Node.js.

## Key Features

- **Detect Regressions**: Identify cost smells and risks in IaC.
- **Predict Costs**: Estimate monthly AWS spend with deterministic heuristics.
- **Explain Changes**: Auditable reasoning with heuristic references.
- **Autofix**: Generate snippets or patches for common issues.
- **Enforce Policies/SLOs**: Block expensive changes in CI.

All analysis is safe, offline, and reproducible.

## Learn More

- Full product spec: [docs/product.yml](docs/product.yml) (in main repo)
- CostPilot site: [Coming soon]

Star this repo if it helps prevent bill shocks! Questions? Open an issue.

---

Licensed under MIT.