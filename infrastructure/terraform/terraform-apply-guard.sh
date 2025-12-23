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
# Safeguard script - prevents terraform apply
# Usage: Run this instead of terraform apply to get a clear error message
#

set -e

echo ""
echo "🚨 ============================================== 🚨"
echo "🚨  TERRAFORM APPLY IS DISABLED IN THIS REPO   🚨"
echo "🚨 ============================================== 🚨"
echo ""
echo "This is a DEMONSTRATION REPOSITORY for CostPilot."
echo ""
echo "Running 'terraform apply' would create real AWS resources"
echo "and incur actual costs."
echo ""
echo "What you CAN do instead:"
echo "  ✓ terraform init      - Download providers"
echo "  ✓ terraform validate  - Check syntax"
echo "  ✓ terraform plan      - Generate plans"
echo "  ✓ terraform fmt       - Format code"
echo ""
echo "For demo purposes, use:"
echo "  • Pre-generated plan files in snapshots/"
echo "  • CostPilot CLI analysis on plan JSONs"
echo "  • Documentation in docs/"
echo ""
echo "See: infrastructure/terraform/SAFEGUARDS.md"
echo ""

exit 1
