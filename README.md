# CostPilot Demo: Zero-IAM FinOps for Terraform

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Status](https://img.shields.io/badge/status-stable-green.svg) ![Version](https://img.shields.io/badge/version-1.0.2-orange.svg)

Catch AWS cost regressions in Terraform PRs without IAM or network access—try the interactive demo now.

## What It Is

CostPilot is a GitHub-native, zero-permission FinOps engine that analyzes Terraform IaC locally to detect cost issues, predict monthly AWS spend, explain changes with auditable heuristics, and generate autofix snippets or patches. It runs offline, uses deterministic rules, and enforces policies/SLOs—all without touching live infrastructure or requiring credentials.

Perfect for teams wanting cost control in CI without the IAM hassle.

**Live Demo**: [https://dee66.github.io/costpilotdemo/](https://dee66.github.io/costpilotdemo/)

## Getting the Real CLI

This repository contains a **demo-only implementation** for showcasing CostPilot’s behavior and outputs.

To install the actual CostPilot CLI (Linux / macOS / Windows binaries):

👉 https://shieldcraft-ai.com/costpilot

That page contains:
- Download instructions
- Pricing options
- License delivery details


For detailed usage instructions, see the documentation links below.

## Safety Notes

⚠️ **Demo Repository Only**

This repository does **not** contain the production CostPilot binary.
It exists solely to demonstrate deterministic outputs, CI flows, and UX.

For the real, licensed CLI, see:
👉 https://shieldcraft-ai.com/costpilot


## Reproducibility

All analysis is deterministic and reproducible:
- Same input plan → same output every time
- No external API calls or network dependencies
- Versioned snapshots ensure consistent testing
- PR #42 introduced the baseline terraform configuration

The baseline and pr-change stacks demonstrate typical cost regression scenarios.

## Key Features

- **Detect Regressions**: Identify cost smells and risks in IaC.
- **Predict Costs**: Estimate monthly AWS spend with deterministic heuristics.
- **Explain Changes**: Auditable reasoning with heuristic references.
- **Autofix**: Generate snippets or patches for common issues.
- **Enforce Policies/SLOs**: Block expensive changes in CI.

All analysis is safe, offline, and reproducible.

Star this repo if it helps prevent bill shocks! Questions? Open an issue.

---

Licensed under MIT.