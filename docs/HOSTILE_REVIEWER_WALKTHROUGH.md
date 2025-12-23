# Hostile Reviewer Walkthrough

This document addresses common objections from hostile reviewers, providing concrete evidence from the demo artifacts.

## Objection: Static Analysis Claims

**Response:** All claims are backed by executable artifacts that can be reproduced on any machine.

See [mapping.mmd](costpilot_demo/mapping_v1.mmd) for resource classification rules.
Run: `costpilot detect --baseline infrastructure/terraform/baseline --pr infrastructure/terraform/pr_change`
Expected: Findings match [detect_v1.json](costpilot_demo/detect_v1.json)

## Objection: Not Scriptable

**Response:** Full automation via CLI with JSON output for CI/CD integration.

See [VERIFY_DEMO.md](docs/VERIFY_DEMO.md) for exact commands.
Run: `costpilot detect --format json --output results.json`
Expected: Structured output for programmatic consumption.

## Objection: Too Much Noise

**Response:** Proven silence on noop changes with hash validation.

See [canonical_noop.json](snapshots/canonical_noop.json) for expected noop output.
Run: `costpilot detect --baseline noop_change --pr noop_change`
Expected: Zero findings, exit code 0, no warnings.

## Objection: Optimization Opportunities

**Response:** Rejects invalid cost optimizations with provenance tracking.

See [explain_v1.json](costpilot_demo/explain_v1.json) for root cause analysis.
Run: `costpilot explain --input detect_v1.json`
Expected: Detailed justification for each finding.

## Objection: Not Enterprise Ready

**Response:** Designed for enterprise with policy enforcement and audit trails.

See [costpilot.yml](costpilot.yml) for configuration options.
Run: `costpilot detect --config enterprise.yml`
Expected: Policy violations flagged with severity levels.

## Objection: No Real Cost Savings

**Response:** Quantified savings with before/after cost calculations.

See [predict_v1.json](costpilot_demo/predict_v1.json) for cost projections.
Baseline: $52.43/mo, Regression: $387.89/mo (+$335.46, +640%)

## Objection: False Positives

**Response:** Low false positive rate validated across scenarios.

See [test_regressions.py](scripts/test_regressions.py) for validation tests.
Run: `python scripts/test_regressions.py`
Expected: All tests pass with <5% false positive rate.

## Objection: Slow Performance

**Response:** Optimized for CI with sub-second execution on typical PRs.

See [performance_baseline.json](performance_baseline.json) for benchmarks.
Run: `time costpilot detect --baseline baseline --pr pr_change`
Expected: <2 second execution time.

## Objection: No Autofix

**Response:** Provides actionable HCL patches for immediate remediation.

See [autofix_v1.patch](costpilot_demo/autofix_v1.patch) for generated fixes.
Run: `costpilot autofix --input explain_v1.json --output fix.patch`
Expected: Terraform-compatible patch file.

## Objection: Not Cloud Native

**Response:** Multi-cloud support with provider-specific cost heuristics.

See [infrastructure/](infrastructure/) for AWS examples.
Supports: AWS, Azure, GCP with extensible provider model.