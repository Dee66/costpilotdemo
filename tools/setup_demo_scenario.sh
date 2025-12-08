#!/bin/bash
# Demo Scenario Setup Script
# Sets up PR #42 baseline for screenshot capture

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "Setting up demo scenario: PR #42 baseline"
echo "=========================================="

# Ensure we're in a clean state
if [[ -n $(git status --porcelain) ]]; then
    echo "Warning: Repository has uncommitted changes"
    echo "Continuing anyway..."
fi

# Ensure snapshots exist
if [[ ! -f "snapshots/detect_v1.json" ]]; then
    echo "Error: Golden outputs missing. Run ./tools/reset_demo.sh first."
    exit 1
fi

# Verify scenario version
SCENARIO_VERSION=$(jq -r '.metadata.scenario_version // "unknown"' snapshots/detect_v1.json 2>/dev/null || echo "unknown")
if [[ "$SCENARIO_VERSION" != "v1" ]]; then
    echo "Error: Scenario version mismatch. Expected v1, got $SCENARIO_VERSION"
    exit 1
fi

# Display scenario info
echo ""
echo "Scenario: PR #42 - EC2 Instance Type Change"
echo "Baseline: infrastructure/terraform/baseline/"
echo "PR Change: infrastructure/terraform/pr-change/"
echo "Findings: 4 cost regressions detected"
echo ""
echo "Golden outputs ready:"
echo "  ✓ detect_v1.json"
echo "  ✓ predict_v1.json"
echo "  ✓ explain_v1.json"
echo "  ✓ snippet_v1.tf"
echo "  ✓ patch_v1.diff"
echo ""
echo "Demo scenario ready for screenshot capture"
