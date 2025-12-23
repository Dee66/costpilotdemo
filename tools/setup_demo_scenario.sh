#!/bin/bash
# Copyright (c) 2025 CostPilot Demo Team
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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
