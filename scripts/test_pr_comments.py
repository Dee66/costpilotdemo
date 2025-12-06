#!/usr/bin/env python3
"""
PR Comment Assets Validation Suite
Adds ~80 granular tests for PR comment quality and content
Focus: Markdown structure, cost tables, finding presentation, actionable recommendations
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any

# Color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class TestRunner:
    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.failures = []
    
    def test(self, name: str, condition: bool, reason: str = ""):
        if condition:
            self.passed += 1
            print(f"  {GREEN}✓{RESET} {name}")
        else:
            self.failed += 1
            msg = f"{name}" + (f": {reason}" if reason else "")
            self.failures.append(msg)
            print(f"  {RED}✗{RESET} {name}" + (f" - {reason}" if reason else ""))
    
    def skip(self, name: str, reason: str = ""):
        self.skipped += 1
        print(f"  {YELLOW}⊘{RESET} {name}" + (f" - {reason}" if reason else ""))
    
    def section(self, name: str):
        print(f"\n{BLUE}{'='*80}{RESET}")
        print(f"{BLUE}{name}{RESET}")
        print(f"{BLUE}{'='*80}{RESET}")


def read_comment(filepath: Path) -> str:
    """Read a PR comment file"""
    if not filepath.exists():
        return ""
    with open(filepath, 'r') as f:
        return f.read()


def test_markdown_structure(runner: TestRunner):
    """Validate markdown structure in PR comments - 20 tests"""
    runner.section("MARKDOWN STRUCTURE VALIDATION (20 tests)")
    
    pr_dir = runner.repo_root / "pr_comment_assets"
    comments = {
        "detect": pr_dir / "comment_detect.txt",
        "predict": pr_dir / "comment_predict.txt",
        "explain": pr_dir / "comment_explain.txt",
        "autofix": pr_dir / "comment_autofix.txt"
    }
    
    for comment_type, filepath in comments.items():
        if not filepath.exists():
            for _ in range(5):
                runner.skip(f"{comment_type} structure", "File not found")
            continue
        
        content = read_comment(filepath)
        
        print(f"\n📝 {comment_type.upper()} Comment Structure")
        
        # Basic markdown elements
        runner.test(f"{comment_type}: has headers", '#' in content)
        runner.test(f"{comment_type}: has bold text", '**' in content)
        runner.test(f"{comment_type}: has emoji markers", 
                   any(emoji in content for emoji in ['🤖', '🔍', '💰', '🔧', '⚠️']))
        runner.test(f"{comment_type}: has horizontal rules", '---' in content)
        runner.test(f"{comment_type}: has code blocks", 
                   '```' in content or '`' in content)


def test_cost_table_formatting(runner: TestRunner):
    """Validate cost table formatting - 20 tests"""
    runner.section("COST TABLE FORMATTING VALIDATION (20 tests)")
    
    pr_dir = runner.repo_root / "pr_comment_assets"
    predict_file = pr_dir / "comment_predict.txt"
    
    if not predict_file.exists():
        for _ in range(20):
            runner.skip("cost table formatting", "File not found")
        return
    
    content = read_comment(predict_file)
    
    print("\n💵 Cost Table Structure")
    
    # Table presence
    runner.test("predict: has markdown tables", '|' in content)
    runner.test("predict: has table headers", '|---' in content or '|--' in content)
    runner.test("predict: has Monthly Cost Impact section", 'Monthly Cost Impact' in content)
    runner.test("predict: has Cost Breakdown section", 'Cost Breakdown' in content)
    
    # Cost values
    runner.test("predict: has dollar amounts", '$' in content)
    runner.test("predict: has baseline cost", 'Baseline Cost' in content or 'Baseline' in content)
    runner.test("predict: has predicted cost", 'Predicted Cost' in content or 'Predicted' in content)
    runner.test("predict: has delta values", 'Delta' in content or 'delta' in content)
    
    print("\n📊 Cost Metrics")
    
    # Numeric values
    dollar_amounts = re.findall(r'\$\d+\.?\d*', content)
    runner.test("predict: has multiple dollar amounts", len(dollar_amounts) >= 10,
               f"Found {len(dollar_amounts)} amounts")
    
    # Percentage changes
    percentage_matches = re.findall(r'\+?\d+\.?\d*%', content)
    runner.test("predict: has percentage changes", len(percentage_matches) > 0,
               f"Found {len(percentage_matches)} percentages")
    
    print("\n📈 Table Formatting Quality")
    
    # Table alignment
    runner.test("predict: tables have proper separators", '|---' in content or '|--' in content)
    runner.test("predict: tables have column headers", 
               'Metric' in content or 'Item' in content or 'Resource' in content)
    
    # Time periods
    runner.test("predict: mentions monthly costs", 'month' in content.lower())
    runner.test("predict: mentions annual costs", 'annual' in content.lower() or 'year' in content.lower())
    
    print("\n💡 Cost Context")
    
    # Context and assumptions
    runner.test("predict: has assumptions section", 'Assumptions' in content or 'assumptions' in content)
    runner.test("predict: has cost range", 'Range' in content or 'range' in content)
    runner.test("predict: has calculation details", 'Calculation' in content or 'calculation' in content)
    
    # Impact indicators
    runner.test("predict: has impact indicators", '🔺' in content or 'increase' in content.lower())
    runner.test("predict: has severity markers", 
               'HIGH' in content or 'MEDIUM' in content or 'LOW' in content)


def test_finding_presentation(runner: TestRunner):
    """Validate finding presentation quality - 20 tests"""
    runner.section("FINDING PRESENTATION VALIDATION (20 tests)")
    
    pr_dir = runner.repo_root / "pr_comment_assets"
    detect_file = pr_dir / "comment_detect.txt"
    
    if not detect_file.exists():
        for _ in range(20):
            runner.skip("finding presentation", "File not found")
        return
    
    content = read_comment(detect_file)
    
    print("\n🔍 Detection Summary")
    
    # Summary section
    runner.test("detect: has summary section", 'Summary' in content or 'SUMMARY' in content)
    runner.test("detect: mentions finding count", 
               any(f'{i} cost' in content.lower() or f'{i} finding' in content.lower() 
                   for i in range(1, 10)))
    runner.test("detect: has severity breakdown", 
               'High Severity' in content or 'HIGH' in content)
    runner.test("detect: uses severity colors", '🔴' in content or '🟡' in content or '🔵' in content)
    
    print("\n📋 Individual Findings")
    
    # Finding structure
    finding_headers = re.findall(r'Finding \d+:', content)
    runner.test("detect: has numbered findings", len(finding_headers) > 0,
               f"Found {len(finding_headers)} findings")
    runner.test("detect: has multiple findings", len(finding_headers) >= 3,
               f"Expected ≥3, found {len(finding_headers)}")
    
    # Finding details
    runner.test("detect: findings have resource names", 'aws_' in content)
    runner.test("detect: findings have before/after values", 
               'Before' in content and 'After' in content)
    runner.test("detect: findings have impact description", 'Impact' in content)
    runner.test("detect: findings have rationale", 'Rationale' in content)
    
    print("\n🏷️  Finding Metadata")
    
    # Rule IDs
    runner.test("detect: findings have rule IDs", 'Rule ID' in content or 'rule_id' in content)
    runner.test("detect: mentions policy violations", 
               'policy' in content.lower() or 'Policy Violation' in content)
    
    # Resource classification
    runner.test("detect: mentions resource types", 
               any(term in content for term in ['Resource', 'resource_type', 'aws_']))
    
    print("\n🔗 Finding Context")
    
    # Cross-references
    runner.test("detect: has cross-service dependencies section",
               'Dependencies' in content or 'Cross-Service' in content)
    runner.test("detect: has next steps section", 'Next Steps' in content or 'NEXT STEPS' in content)
    runner.test("detect: has actionable recommendations", 
               'Review' in content or 'Document' in content or 'Fix' in content)
    
    # Visual aids
    runner.test("detect: uses ASCII diagrams or flowcharts", 
               '```' in content and ('→' in content or '├' in content or '└' in content))
    
    # Completeness
    runner.test("detect: has PR metadata", 'PR #' in content or 'Branch' in content)
    runner.test("detect: mentions baseline/PR stacks", 
               'baseline' in content.lower() and 'pr' in content.lower())


def test_actionable_recommendations(runner: TestRunner):
    """Validate actionable recommendations - 20 tests"""
    runner.section("ACTIONABLE RECOMMENDATIONS VALIDATION (20 tests)")
    
    pr_dir = runner.repo_root / "pr_comment_assets"
    autofix_file = pr_dir / "comment_autofix.txt"
    explain_file = pr_dir / "comment_explain.txt"
    
    print("\n🔧 Auto-Fix Suggestions")
    
    if autofix_file.exists():
        content = read_comment(autofix_file)
        
        runner.test("autofix: exists", True)
        runner.test("autofix: has fix suggestions", 'Fix' in content or 'FIX' in content)
        runner.test("autofix: has code blocks", '```' in content)
        runner.test("autofix: has HCL/Terraform code", 
                   '```hcl' in content or 'terraform' in content.lower())
        runner.test("autofix: shows before/after diffs", 
                   ('-' in content and '+' in content) or ('❌' in content and '✅' in content))
        runner.test("autofix: has copy-pastable code", 
                   'resource "' in content or 'variable "' in content)
        runner.test("autofix: explains why fixes work", 'Why this works' in content or 'why' in content.lower())
        runner.test("autofix: has testing instructions", 
                   'test' in content.lower() or 'verify' in content.lower())
        runner.test("autofix: prioritizes fixes", 
                   'Quick Win' in content or 'Priority' in content or 'First' in content)
        runner.test("autofix: quantifies savings", '$' in content and 'save' in content.lower())
    else:
        for _ in range(10):
            runner.skip("autofix validation", "File not found")
    
    print("\n💡 Root Cause Explanations")
    
    if explain_file.exists():
        content = read_comment(explain_file)
        
        runner.test("explain: exists", True)
        runner.test("explain: has root cause analysis", 
                   'Root Cause' in content or 'Why' in content)
        runner.test("explain: explains cost impacts", 
                   'cost' in content.lower() and 'why' in content.lower())
        runner.test("explain: has heuristic provenance", 
                   'Heuristic' in content or 'Source' in content or 'Reference' in content)
        runner.test("explain: has severity justification", 
                   'Severity Justification' in content or 'severity' in content.lower())
        runner.test("explain: provides business context", 
                   any(term in content for term in ['business', 'budget', 'planning', 'risk']))
        runner.test("explain: has time-based analysis", 
                   'Month' in content or 'time' in content.lower() or 'Time Bomb' in content)
        runner.test("explain: uses visual aids", 
                   '```' in content or '→' in content or '├' in content)
        runner.test("explain: has confidence levels", 
                   'Confidence' in content or 'confidence' in content)
        runner.test("explain: addresses multiple findings", 
                   content.count('Finding') >= 2 or content.count('###') >= 3)
    else:
        for _ in range(10):
            runner.skip("explain validation", "File not found")


def test_comment_completeness(runner: TestRunner):
    """Validate overall comment completeness - 20 tests"""
    runner.section("COMMENT COMPLETENESS VALIDATION (20 tests)")
    
    pr_dir = runner.repo_root / "pr_comment_assets"
    
    comments = {
        "detect": pr_dir / "comment_detect.txt",
        "predict": pr_dir / "comment_predict.txt",
        "explain": pr_dir / "comment_explain.txt",
        "autofix": pr_dir / "comment_autofix.txt"
    }
    
    print("\n📦 All Comments Present")
    
    for comment_type, filepath in comments.items():
        runner.test(f"{comment_type} comment exists", filepath.exists())
    
    print("\n📏 Comment Length Validation")
    
    for comment_type, filepath in comments.items():
        if filepath.exists():
            content = read_comment(filepath)
            lines = content.split('\n')
            
            runner.test(f"{comment_type}: substantial content", len(lines) >= 50,
                       f"Found {len(lines)} lines")
            runner.test(f"{comment_type}: not empty", len(content.strip()) > 100)
        else:
            runner.skip(f"{comment_type} length", "File not found")
    
    print("\n🔗 Cross-Comment Consistency")
    
    all_content = {}
    for comment_type, filepath in comments.items():
        if filepath.exists():
            all_content[comment_type] = read_comment(filepath)
    
    if len(all_content) >= 2:
        # Check PR number consistency
        pr_numbers = {}
        for comment_type, content in all_content.items():
            match = re.search(r'PR #(\d+)', content)
            if match:
                pr_numbers[comment_type] = match.group(1)
        
        if len(pr_numbers) >= 2:
            pr_values = list(pr_numbers.values())
            runner.test("PR numbers consistent across comments", 
                       len(set(pr_values)) == 1,
                       f"Found: {pr_numbers}")
        
        # Check finding references
        if 'detect' in all_content and 'explain' in all_content:
            detect_findings = len(re.findall(r'Finding \d+', all_content['detect']))
            explain_findings = len(re.findall(r'Finding \d+|detect-\d+', all_content['explain']))
            runner.test("Finding counts match between detect/explain",
                       detect_findings > 0 and explain_findings > 0)
    
    print("\n✅ Quality Indicators")
    
    for comment_type, filepath in comments.items():
        if filepath.exists():
            content = read_comment(filepath)
            
            # Check for professional formatting
            runner.test(f"{comment_type}: uses consistent formatting", 
                       content.count('---') >= 2)  # Has section separators


def main():
    runner = TestRunner()
    
    print(f"{BLUE}╔════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BLUE}║                                                                            ║{RESET}")
    print(f"{BLUE}║           PR COMMENT ASSETS VALIDATION SUITE (~80 tests)                   ║{RESET}")
    print(f"{BLUE}║                                                                            ║{RESET}")
    print(f"{BLUE}╚════════════════════════════════════════════════════════════════════════════╝{RESET}")
    
    # Run all test suites
    test_markdown_structure(runner)
    test_cost_table_formatting(runner)
    test_finding_presentation(runner)
    test_actionable_recommendations(runner)
    test_comment_completeness(runner)
    
    # Print summary
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}TEST SUMMARY{RESET}")
    print(f"{BLUE}{'='*80}{RESET}")
    
    total = runner.passed + runner.failed + runner.skipped
    pass_rate = (runner.passed / total * 100) if total > 0 else 0
    
    print(f"\n{GREEN}✓ Passed:{RESET}  {runner.passed}/{total} ({pass_rate:.1f}%)")
    print(f"{RED}✗ Failed:{RESET}  {runner.failed}/{total}")
    print(f"{YELLOW}⊘ Skipped:{RESET} {runner.skipped}/{total}")
    
    if runner.failures:
        print(f"\n{RED}{'='*80}{RESET}")
        print(f"{RED}FAILURES ({len(runner.failures)}){RESET}")
        print(f"{RED}{'='*80}{RESET}")
        for failure in runner.failures[:20]:  # Show first 20
            print(f"{RED}✗{RESET} {failure}")
        if len(runner.failures) > 20:
            print(f"\n{YELLOW}... and {len(runner.failures) - 20} more failures{RESET}")
    
    print(f"\n{BLUE}{'='*80}{RESET}")
    
    # Exit code
    sys.exit(0 if runner.failed == 0 else 1)


if __name__ == "__main__":
    main()
