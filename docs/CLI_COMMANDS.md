# CostPilot CLI Commands

## Overview

CostPilot is a Zero-IAM FinOps engine for Terraform that provides comprehensive cost analysis, policy management, and infrastructure optimization capabilities.

**Version:** costpilot 1.0.0 (Demo)

**Note:** This documentation describes the CostPilot CLI interface as demonstrated in this repository. The included binary is for demonstration purposes only and may not include all production features.

## Usage

```bash
costpilot [OPTIONS] <COMMAND>
```

## Global Options

- `-v, --verbose`: Enable verbose output
- `--format <FORMAT>`: Output format (json, text, markdown, pr-comment) [default: text]
- `-d, --debug`: Enable debug mode (shows internal operations and timing)
- `-h, --help`: Print help
- `-V, --version`: Print version

## Available Commands

### Core Analysis Commands

- **`scan`**: Scan Terraform plan for cost issues and predictions
- **`baseline`**: Manage cost baselines
- **`diff`**: Compare cost between two Terraform plans
- **`explain`**: Explain cost predictions with stepwise reasoning

### Infrastructure Management

- **`init`**: Initialize CostPilot configuration in current directory
- **`map`**: Generate dependency map
- **`group`**: Group resources for cost allocation
- **`validate`**: Validate configuration files

### Policy & Compliance

- **`policy`**: Manage policy lifecycle and approvals
- **`policy-dsl`**: Manage custom policy rules (DSL)
- **`policy-lifecycle`**: Manage policy lifecycle
- **`audit`**: Audit log and compliance reporting

### Monitoring & SLOs

- **`slo`**: Manage SLO monitoring and compliance
- **`slo-burn`**: Calculate SLO burn rate
- **`slo-check`**: Check SLO compliance
- **`performance`**: Performance monitoring and budgets

### Advanced Features

- **`trend`**: Analyze cost trends and generate reports
- **`anomaly`**: Detect cost anomalies
- **`usage`**: Usage metering and reporting
- **`feature`**: Manage feature flags for test-in-production

### Auto-Fix Capabilities

- **`autofix-patch`**: Generate autofix patches
- **`autofix-snippet`**: Generate autofix snippets
- **`autofix-drift-safe`**: Generate drift-safe autofix patches

### Heuristics & Escrow

- **`heuristics`**: Manage cost heuristics
- **`escrow`**: Manage escrow operations

### Help

- **`help`**: Print this message or the help of the given subcommand(s)
- **`version`**: Show version information

## Getting Help

For detailed help on any command, use:

```bash
costpilot <COMMAND> --help
```

For example:
```bash
costpilot scan --help
costpilot policy --help
```

## Testing Confirmation

The binary has been tested and confirmed working with:
- `--help`: Displays all commands and options
- `--version`: Shows version 1.0.0 (Demo)