#!/bin/bash
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
