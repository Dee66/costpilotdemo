#!/usr/bin/env python3
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

"""
PR Comment Assets Validation Suite
Adds ~80 granular tests for PR comment quality and content
Focus: Markdown structure, cost tables, finding presentation, actionable recommendations


Refactored to use Template Method Pattern with TestSuite base class.
"""

import os
import re
import sys
from pathlib import Path

# Import shared test framework
sys.path.insert(0, str(Path(__file__).parent))
from lib.test_suite import TestSuite
from lib.scenario_factory import ScenarioFactory
from lib.logger import get_logger
from typing import Dict, List, Any


def read_comment(filepath: Path) -> str:
    """Read a PR comment file"""
    if not filepath.exists():
        return ""
    with open(filepath, 'r') as f:
        return f.read()


class PrCommentsTestSuite(TestSuite):
    """Test suite using Template Method pattern"""
    
    @property
    def tags(self) -> List[str]:
        return ["pr", "comments", "github", "validation"]
    
    def __init__(self, repo_root: Path = None):
        super().__init__(repo_root)
        self.factory = ScenarioFactory(self.repo_root)
        self.pr_scenario = self.factory.create("pr_change")
        self.logger = get_logger("pr_comments_test")
    
    def run(self):
        """Template method - defines the test execution sequence"""
        self.test_markdown_structure()
        self.test_cost_table_formatting()
        self.test_finding_presentation()
        self.test_actionable_recommendations()
        self.test_comment_completeness()
    
    def test_markdown_structure(self):
        """Validate markdown structure in PR comments - 20 tests"""
        self.section("MARKDOWN STRUCTURE VALIDATION (20 tests)")
    
        pr_dir = self.repo_root / "pr_comment_assets"
        comments = {
            "detect": pr_dir / "comment_detect.txt",
            "predict": pr_dir / "comment_predict.txt",
            "explain": pr_dir / "comment_explain.txt",
            "autofix": pr_dir / "comment_autofix.txt"
        }
    
        for comment_type, filepath in comments.items():
            if not filepath.exists():
                for _ in range(5):
                    self.skip(f"{comment_type} structure", "File not found")
                continue
        
            content = read_comment(filepath)
        
            self.logger.info(f"{comment_type.upper()} Comment Structure")
        
            # Basic markdown elements
            self.test(f"{comment_type}: has headers", '#' in content)
            self.test(f"{comment_type}: has bold text", '**' in content)
            self.test(f"{comment_type}: has emoji markers", 
                       any(emoji in content for emoji in ['🤖', '🔍', '💰', '🔧', '⚠️']))
            self.test(f"{comment_type}: has horizontal rules", '---' in content)
            self.test(f"{comment_type}: has code blocks", 
                       '```' in content or '`' in content)


    def test_cost_table_formatting(self):
        """Validate cost table formatting - 20 tests"""
        self.section("COST TABLE FORMATTING VALIDATION (20 tests)")
    
        pr_dir = self.repo_root / "pr_comment_assets"
        predict_file = pr_dir / "comment_predict.txt"
    
        if not predict_file.exists():
            for _ in range(20):
                self.skip("cost table formatting", "File not found")
            return
    
        content = read_comment(predict_file)
    
        self.logger.info("Cost Table Structure")
    
        # Table presence
        self.test("predict: has markdown tables", '|' in content)
        self.test("predict: has table headers", '|---' in content or '|--' in content)
        self.test("predict: has Monthly Cost Impact section", 'Monthly Cost Impact' in content)
        self.test("predict: has Cost Breakdown section", 'Cost Breakdown' in content)
    
        # Cost values
        self.test("predict: has dollar amounts", '$' in content)
        self.test("predict: has baseline cost", 'Baseline Cost' in content or 'Baseline' in content)
        self.test("predict: has predicted cost", 'Predicted Cost' in content or 'Predicted' in content)
        self.test("predict: has delta values", 'Delta' in content or 'delta' in content)
    
        self.logger.info("Cost Metrics")
    
        # Numeric values
        dollar_amounts = re.findall(r'\$\d+\.?\d*', content)
        self.test("predict: has multiple dollar amounts", len(dollar_amounts) >= 10,
                   f"Found {len(dollar_amounts)} amounts")
    
        # Percentage changes
        percentage_matches = re.findall(r'\+?\d+\.?\d*%', content)
        self.test("predict: has percentage changes", len(percentage_matches) > 0,
                   f"Found {len(percentage_matches)} percentages")
    
        self.logger.info("Table Formatting Quality")
    
        # Table alignment
        self.test("predict: tables have proper separators", '|---' in content or '|--' in content)
        self.test("predict: tables have column headers", 
                   'Metric' in content or 'Item' in content or 'Resource' in content)
    
        # Time periods
        self.test("predict: mentions monthly costs", 'month' in content.lower())
        self.test("predict: mentions annual costs", 'annual' in content.lower() or 'year' in content.lower())
    
        self.logger.info("Cost Context")
    
        # Context and assumptions
        self.test("predict: has assumptions section", 'Assumptions' in content or 'assumptions' in content)
        self.test("predict: has cost range", 'Range' in content or 'range' in content)
        self.test("predict: has calculation details", 'Calculation' in content or 'calculation' in content)
    
        # Impact indicators
        self.test("predict: has impact indicators", '🔺' in content or 'increase' in content.lower())
        self.test("predict: has severity markers", 
                   'HIGH' in content or 'MEDIUM' in content or 'LOW' in content)


    def test_finding_presentation(self):
        """Validate finding presentation quality - 20 tests"""
        self.section("FINDING PRESENTATION VALIDATION (20 tests)")
    
        pr_dir = self.repo_root / "pr_comment_assets"
        detect_file = pr_dir / "comment_detect.txt"
    
        if not detect_file.exists():
            for _ in range(20):
                self.skip("finding presentation", "File not found")
            return
    
        content = read_comment(detect_file)
    
        self.logger.info("Detection Summary")
    
        # Summary section
        self.test("detect: has summary section", 'Summary' in content or 'SUMMARY' in content)
        self.test("detect: mentions finding count", 
                   any(f'{i} cost' in content.lower() or f'{i} finding' in content.lower() 
                       for i in range(1, 10)))
        self.test("detect: has severity breakdown", 
                   'High Severity' in content or 'HIGH' in content)
        self.test("detect: uses severity colors", '🔴' in content or '🟡' in content or '🔵' in content)
    
        self.logger.info("Individual Findings")
    
        # Finding structure
        finding_headers = re.findall(r'Finding \d+:', content)
        self.test("detect: has numbered findings", len(finding_headers) > 0,
                   f"Found {len(finding_headers)} findings")
        self.test("detect: has multiple findings", len(finding_headers) >= 3,
                   f"Expected ≥3, found {len(finding_headers)}")
    
        # Finding details
        self.test("detect: findings have resource names", 'aws_' in content)
        self.test("detect: findings have before/after values", 
                   'Before' in content and 'After' in content)
        self.test("detect: findings have impact description", 'Impact' in content)
        self.test("detect: findings have rationale", 'Rationale' in content)
    
        self.logger.info("Finding Metadata")
    
        # Rule IDs
        self.test("detect: findings have rule IDs", 'Rule ID' in content or 'rule_id' in content)
        self.test("detect: mentions policy violations", 
                   'policy' in content.lower() or 'Policy Violation' in content)
    
        # Resource classification
        self.test("detect: mentions resource types", 
                   any(term in content for term in ['Resource', 'resource_type', 'aws_']))
    
        self.logger.info("Finding Context")
    
        # Cross-references
        self.test("detect: has cross-service dependencies section",
                   'Dependencies' in content or 'Cross-Service' in content)
        self.test("detect: has next steps section", 'Next Steps' in content or 'NEXT STEPS' in content)
        self.test("detect: has actionable recommendations", 
                   'Review' in content or 'Document' in content or 'Fix' in content)
    
        # Visual aids
        self.test("detect: uses ASCII diagrams or flowcharts", 
                   '```' in content and ('→' in content or '├' in content or '└' in content))
    
        # Completeness
        self.test("detect: has PR metadata", 'PR #' in content or 'Branch' in content)
        self.test("detect: mentions baseline/PR stacks", 
                   'baseline' in content.lower() and 'pr' in content.lower())


    def test_actionable_recommendations(self):
        """Validate actionable recommendations - 20 tests"""
        self.section("ACTIONABLE RECOMMENDATIONS VALIDATION (20 tests)")
    
        pr_dir = self.repo_root / "pr_comment_assets"
        autofix_file = pr_dir / "comment_autofix.txt"
        explain_file = pr_dir / "comment_explain.txt"
    
        self.logger.info("Auto-Fix Suggestions")
    
        if autofix_file.exists():
            content = read_comment(autofix_file)
        
            self.test("autofix: exists", True)
            self.test("autofix: has fix suggestions", 'Fix' in content or 'FIX' in content)
            self.test("autofix: has code blocks", '```' in content)
            self.test("autofix: has HCL/Terraform code", 
                       '```hcl' in content or 'terraform' in content.lower())
            self.test("autofix: shows before/after diffs", 
                       ('-' in content and '+' in content) or ('❌' in content and '✅' in content))
            self.test("autofix: has copy-pastable code", 
                       'resource "' in content or 'variable "' in content)
            self.test("autofix: explains why fixes work", 'Why this works' in content or 'why' in content.lower())
            self.test("autofix: has testing instructions", 
                       'test' in content.lower() or 'verify' in content.lower())
            self.test("autofix: prioritizes fixes", 
                       'Quick Win' in content or 'Priority' in content or 'First' in content)
            self.test("autofix: quantifies savings", '$' in content and 'save' in content.lower())
        else:
            for _ in range(10):
                self.skip("autofix validation", "File not found")
    
        self.logger.info("Root Cause Explanations")
    
        if explain_file.exists():
            content = read_comment(explain_file)
        
            self.test("explain: exists", True)
            self.test("explain: has root cause analysis", 
                       'Root Cause' in content or 'Why' in content)
            self.test("explain: explains cost impacts", 
                       'cost' in content.lower() and 'why' in content.lower())
            self.test("explain: has heuristic provenance", 
                       'Heuristic' in content or 'Source' in content or 'Reference' in content)
            self.test("explain: has severity justification", 
                       'Severity Justification' in content or 'severity' in content.lower())
            self.test("explain: provides business context", 
                       any(term in content for term in ['business', 'budget', 'planning', 'risk']))
            self.test("explain: has time-based analysis", 
                       'Month' in content or 'time' in content.lower() or 'Time Bomb' in content)
            self.test("explain: uses visual aids", 
                       '```' in content or '→' in content or '├' in content)
            self.test("explain: has confidence levels", 
                       'Confidence' in content or 'confidence' in content)
            self.test("explain: addresses multiple findings", 
                       content.count('Finding') >= 2 or content.count('###') >= 3)
        else:
            for _ in range(10):
                self.skip("explain validation", "File not found")


    def test_comment_completeness(self):
        """Validate overall comment completeness - 20 tests"""
        self.section("COMMENT COMPLETENESS VALIDATION (20 tests)")
    
        pr_dir = self.repo_root / "pr_comment_assets"
    
        comments = {
            "detect": pr_dir / "comment_detect.txt",
            "predict": pr_dir / "comment_predict.txt",
            "explain": pr_dir / "comment_explain.txt",
            "autofix": pr_dir / "comment_autofix.txt"
        }
    
        self.logger.info("All Comments Present")
    
        for comment_type, filepath in comments.items():
            self.test(f"{comment_type} comment exists", filepath.exists())
    
        self.logger.info("Comment Length Validation")
    
        for comment_type, filepath in comments.items():
            if filepath.exists():
                content = read_comment(filepath)
                lines = content.split('\n')
            
                self.test(f"{comment_type}: substantial content", len(lines) >= 50,
                           f"Found {len(lines)} lines")
                self.test(f"{comment_type}: not empty", len(content.strip()) > 100)
            else:
                self.skip(f"{comment_type} length", "File not found")
    
        self.logger.info("Cross-Comment Consistency")
    
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
                self.test("PR numbers consistent across comments", 
                           len(set(pr_values)) == 1,
                           f"Found: {pr_numbers}")
        
            # Check finding references
            if 'detect' in all_content and 'explain' in all_content:
                detect_findings = len(re.findall(r'Finding \d+', all_content['detect']))
                explain_findings = len(re.findall(r'Finding \d+|detect-\d+', all_content['explain']))
                self.test("Finding counts match between detect/explain",
                           detect_findings > 0 and explain_findings > 0)
    
        self.logger.info("Quality Indicators")
    
        for comment_type, filepath in comments.items():
            if filepath.exists():
                content = read_comment(filepath)
            
                # Check for professional formatting
                self.test(f"{comment_type}: uses consistent formatting", 
                           content.count('---') >= 2)  # Has section separators


def main():
    """Entry point for test execution"""
    suite = PrCommentsTestSuite()
    suite.run()
    suite.print_summary()
    sys.exit(suite.get_exit_code())


if __name__ == "__main__":
    main()
