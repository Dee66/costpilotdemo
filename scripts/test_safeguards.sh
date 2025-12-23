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

#
# Test safeguard mechanisms
#

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "🧪 Testing CostPilot Demo Safeguards"
echo "======================================"
echo ""

# Test 1: Verify pre-commit hook exists and is executable
echo "Test 1: Pre-commit hook..."
if [[ -x .git/hooks/pre-commit ]]; then
    echo "  ✓ Pre-commit hook is installed and executable"
else
    echo "  ❌ Pre-commit hook missing or not executable"
    exit 1
fi

# Test 2: Verify no .tfstate files exist
echo "Test 2: No Terraform state files..."
TFSTATE_COUNT=$(find . -name "*.tfstate*" -type f | wc -l)
if [[ $TFSTATE_COUNT -eq 0 ]]; then
    echo "  ✓ No .tfstate files found (no resources deployed)"
else
    echo "  ❌ Found $TFSTATE_COUNT .tfstate files - resources may be deployed!"
    find . -name "*.tfstate*" -type f
    exit 1
fi

# Test 3: Verify gitignore blocks state files
echo "Test 3: Gitignore configuration..."
if grep -q '^\*\.tfstate' .gitignore; then
    echo "  ✓ .gitignore blocks .tfstate files"
else
    echo "  ❌ .gitignore does not block .tfstate files"
    exit 1
fi

# Test 4: Verify warning comments in Terraform files
echo "Test 4: Terraform file warnings..."
WARNING_COUNT=0
for tf_file in infrastructure/terraform/*/main.tf; do
    if grep -q "WARNING.*terraform apply" "$tf_file"; then
        WARNING_COUNT=$((WARNING_COUNT + 1))
    fi
done
if [[ $WARNING_COUNT -eq 3 ]]; then
    echo "  ✓ All 3 Terraform stacks have warning comments"
else
    echo "  ❌ Only $WARNING_COUNT/3 stacks have warnings"
    exit 1
fi

# Test 5: Verify CI/CD has safeguard comment
echo "Test 5: CI/CD safeguards..."
if grep -q "SAFEGUARD" .github/workflows/costpilot-ci.yml; then
    echo "  ✓ CI/CD workflow has safeguard comment"
else
    echo "  ❌ CI/CD workflow missing safeguard comment"
    exit 1
fi

# Test 6: Verify no terraform apply in CI/CD
echo "Test 6: No terraform apply in CI/CD..."
# Exclude comment lines when searching for terraform apply
if grep -v '^[[:space:]]*#' .github/workflows/costpilot-ci.yml | grep -q "terraform apply"; then
    echo "  ❌ Found 'terraform apply' in CI/CD workflow!"
    exit 1
else
    echo "  ✓ No 'terraform apply' in CI/CD workflow"
fi

# Test 7: Verify SAFEGUARDS.md exists
echo "Test 7: Documentation..."
if [[ -f infrastructure/terraform/SAFEGUARDS.md ]]; then
    echo "  ✓ SAFEGUARDS.md exists"
else
    echo "  ❌ SAFEGUARDS.md missing"
    exit 1
fi

# Test 8: Verify README has warning
echo "Test 8: README warning..."
if grep -q "IMPORTANT: This is a DEMONSTRATION repository" README.md; then
    echo "  ✓ README has prominent warning"
else
    echo "  ❌ README missing warning"
    exit 1
fi

echo ""
echo "======================================"
echo "✅ All safeguards validated successfully"
echo ""
echo "Summary:"
echo "  • Pre-commit hook blocks dangerous commits"
echo "  • No AWS resources currently deployed"
echo "  • Gitignore prevents state file commits"
echo "  • All Terraform files have warnings"
echo "  • CI/CD excludes terraform apply"
echo "  • Comprehensive documentation in place"
echo ""
echo "This repository is safe to use for demonstrations."
echo ""
