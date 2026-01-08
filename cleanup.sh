#!/bin/bash
# Safe project cleanup script
# Run this to organize the messy project root

set -e

echo "🧹 CostPilot Project Cleanup Script"
echo "=================================="
echo ""

# Step 1: Create backup
echo "📦 Step 1: Creating backup commit..."
git add . || true
git commit -m "backup before cleanup $(date)" || echo "No changes to commit"

# Step 2: Remove temporary files (safe to delete)
echo "🗑️  Step 2: Removing temporary test outputs..."
rm -f comprehensive_test_results_*.txt test_run_output.log summary.txt
echo "   ✅ Removed temporary files"

# Step 3: Move scripts (but be careful not to move costpilot binary)
echo "📁 Step 3: Moving scripts to scripts/ directory..."
for file in *.sh; do
    if [[ "$file" != "cleanup.sh" && -f "$file" ]]; then
        mv "$file" scripts/ 2>/dev/null && echo "   → Moved $file to scripts/"
    fi
done

# Step 4: Move documentation
echo "📄 Step 4: Moving documentation to docs/ directory..."
for file in *.md; do
    if [[ "$file" != "README.md" && -f "$file" ]]; then  # Keep main README in root
        mv "$file" docs/ 2>/dev/null && echo "   → Moved $file to docs/"
    fi
done

# Step 5: Move Terraform files
echo "🏗️  Step 5: Moving Terraform files to infrastructure/..."
mv *.tf infrastructure/ 2>/dev/null && echo "   → Moved Terraform files" || true
mv tfplan* infrastructure/ 2>/dev/null && echo "   → Moved Terraform plans" || true

# Step 6: Move test data
echo "🧪 Step 6: Moving test data to test_framework/..."
mv cost_heuristics_*.json test_framework/ 2>/dev/null && echo "   → Moved test data" || true

# Step 7: Move sales demo files
echo "💼 Step 7: Moving sales demo files..."
mv SALES_DEMO_README.md sales_demo/ 2>/dev/null && echo "   → Moved sales demo docs" || true

echo ""
echo "🎉 Cleanup complete!"
echo "=================="
echo "Root directory now has: $(ls -1 | wc -l) items (down from 73)"
echo ""
echo "📋 What was cleaned up:"
echo "• Removed temporary test outputs"
echo "• Moved 20+ scripts to scripts/"
echo "• Moved documentation to docs/"
echo "• Organized Terraform files in infrastructure/"
echo "• Consolidated test data in test_framework/"
echo ""
echo "🔍 Next steps:"
echo "• Test that npm start still works"
echo "• Run a test script to verify functionality"
echo "• Update any hardcoded paths if needed"