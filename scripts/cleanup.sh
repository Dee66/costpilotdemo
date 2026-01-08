#!/bin/bash
# Comprehensive CostPilot Project Cleanup Script
# This script organizes ALL files in the project root directory

set -e

echo "🧹 COMPREHENSIVE CostPilot Project Cleanup"
echo "========================================="
echo ""

# Step 1: Create backup
echo "📦 Step 1: Creating backup commit..."
git add . || true
git commit -m "backup before comprehensive cleanup $(date)" || echo "No changes to commit"

# Step 2: Create all necessary directories
echo "📁 Step 2: Creating organized directory structure..."
mkdir -p bin config licenses web assets demo test_data

# Step 3: Remove temporary files (safe to delete)
echo "🗑️  Step 3: Removing temporary test outputs..."
rm -f comprehensive_test_results_*.txt test_run_output.log summary.txt
rm -f test_results_20260107_082230.txt test_results_20260106_*.txt
rm -f *.tmp *.log 2>/dev/null || true
echo "   ✅ Removed temporary files"

# Step 4: Move web files
echo "🌐 Step 4: Moving web interface files..."
mv index.html terminal_demo.html web/ 2>/dev/null && echo "   → Moved web files to web/" || true

# Step 5: Move web assets
echo "🎨 Step 5: Moving web assets..."
mv favicon.svg styles.css animations.js script.js findingsManager.js roiCalculator.js record_terminal_click.js assets/ 2>/dev/null && echo "   → Moved web assets to assets/" || true

# Step 6: Move configuration files
echo "⚙️  Step 6: Moving configuration files..."
mv costpilot.yml config/ 2>/dev/null && echo "   → Moved config to config/" || true

# Step 7: Move license files
echo "🔐 Step 7: Moving license files..."
mv license.json license.yml licenses/ 2>/dev/null && echo "   → Moved licenses to licenses/" || true

# Step 8: Move binary
echo "🔧 Step 8: Moving binary executable..."
mv costpilot bin/ 2>/dev/null && echo "   → Moved binary to bin/" || true

# Step 9: Move demo data
echo "📊 Step 9: Moving demo data..."
mv demo_plan.json demo/ 2>/dev/null && echo "   → Moved demo data to demo/" || true

# Step 10: Move infrastructure artifacts
echo "🏗️  Step 10: Moving infrastructure artifacts..."
mv lambda_function.zip infrastructure/ 2>/dev/null && echo "   → Moved lambda function to infrastructure/" || true

# Step 11: Move test results
echo "🧪 Step 11: Moving test results..."
mv test_results_20260108_145119.txt test_results/ 2>/dev/null && echo "   → Moved test results to test_results/" || true

# Step 12: Reorganize existing directories
echo "📂 Step 12: Reorganizing existing directories..."
mv diagrams/ docs/ 2>/dev/null && echo "   → Moved diagrams to docs/" || true
mv optimization_tests/ test_framework/ 2>/dev/null && echo "   → Moved optimization tests to test_framework/" || true
mv snapshots/ test_framework/ 2>/dev/null && echo "   → Moved snapshots to test_framework/" || true
mv stress_tests/ test_framework/ 2>/dev/null && echo "   → Moved stress tests to test_framework/" || true
mv video_assets/ assets/ 2>/dev/null && echo "   → Moved video assets to assets/" || true
mv visual_assets/ assets/ 2>/dev/null && echo "   → Moved visual assets to assets/" || true

# Step 13: Move remaining scripts (but keep cleanup.sh in root temporarily)
echo "📄 Step 13: Moving remaining scripts..."
for file in *.sh; do
    if [[ "$file" != "cleanup.sh" && -f "$file" ]]; then
        mv "$file" scripts/ 2>/dev/null && echo "   → Moved $file to scripts/"
    fi
done

# Step 14: Move remaining documentation
echo "📚 Step 14: Moving remaining documentation..."
for file in *.md; do
    if [[ "$file" != "README.md" && -f "$file" ]]; then  # Keep main README in root
        mv "$file" docs/ 2>/dev/null && echo "   → Moved $file to docs/"
    fi
done

# Step 15: Move cleanup script itself to scripts/
echo "🗑️  Step 15: Moving cleanup script to scripts/..."
mv cleanup.sh scripts/ 2>/dev/null && echo "   → Moved cleanup script to scripts/" || true

echo ""
echo "🎉 COMPREHENSIVE CLEANUP COMPLETE!"
echo "=================================="

# Count remaining files
REMAINING=$(ls -1 | wc -l)
echo "Root directory now has: $REMAINING items"

echo ""
echo "📋 New organization:"
echo "├── bin/              - Executables and binaries"
echo "├── config/           - Configuration files"
echo "├── licenses/         - License files"
echo "├── web/              - Web interface files"
echo "├── assets/           - Static assets (CSS, JS, images, videos)"
echo "├── demo/             - Demo data and examples"
echo "├── test_data/        - Test data and results"
echo "├── scripts/          - Automation scripts"
echo "├── docs/             - Documentation and diagrams"
echo "├── infrastructure/   - Infrastructure as code"
echo "├── test_framework/   - Test infrastructure"
echo "├── sales_demo/       - Sales demo materials"
echo "├── test_results/     - Test results and reports"
echo "├── node_modules/     - Dependencies (npm)"
echo "├── .costpilot/       - CostPilot internal data"
echo "├── .terraform/       - Terraform state"
echo "└── README.md         - Main project README"

echo ""
echo "🔍 Next steps:"
echo "• Update .gitignore to reflect new structure"
echo "• Test that npm start still works"
echo "• Update any hardcoded paths in scripts"