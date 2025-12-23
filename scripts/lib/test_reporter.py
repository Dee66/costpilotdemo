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
Test Reporter - Handles formatting and display of test results
Part of SOLID refactoring: Single Responsibility Principle
"""

from typing import List
from .test_result import TestResult


# Color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'


class TestReporter:
    """Formats and displays test results"""
    
    @staticmethod
    def format_result(result: TestResult) -> str:
        """Format a single test result for display"""
        if result.passed:
            symbol = f"{GREEN}✓{RESET}"
        else:
            symbol = f"{RED}✗{RESET}"
        
        reason_str = f" - {result.reason}" if result.reason else ""
        return f"  {symbol} {result.name}{reason_str}"
    
    @staticmethod
    def format_section(name: str) -> str:
        """Format a section header"""
        separator = "=" * 80
        return f"\n{BLUE}{separator}{RESET}\n{BLUE}{name}{RESET}\n{BLUE}{separator}{RESET}"
    
    @staticmethod
    def format_subsection(name: str) -> str:
        """Format a subsection header"""
        return f"\n{CYAN}{name}{RESET}"
    
    @staticmethod
    def format_summary(passed: int, failed: int, skipped: int = 0) -> str:
        """Format final summary"""
        total = passed + failed + skipped
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        lines = [
            "",
            f"{BOLD}{'='*80}{RESET}",
            f"{BOLD}SUMMARY{RESET}",
            f"{BOLD}{'='*80}{RESET}",
            f"Total:   {total}",
            f"{GREEN}Passed:  {passed}{RESET}",
        ]
        
        if failed > 0:
            lines.append(f"{RED}Failed:  {failed}{RESET}")
        
        if skipped > 0:
            lines.append(f"{YELLOW}Skipped: {skipped}{RESET}")
        
        lines.append(f"Pass Rate: {pass_rate:.1f}%")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_failures(failures: List[str]) -> str:
        """Format list of failures"""
        if not failures:
            return ""
        
        lines = [
            "",
            f"{RED}{BOLD}FAILURES:{RESET}",
        ]
        
        for i, failure in enumerate(failures, 1):
            lines.append(f"{RED}{i}. {failure}{RESET}")
        
        return "\n".join(lines)
    
    @staticmethod
    def print_result(result: TestResult):
        """Print a single test result"""
        print(TestReporter.format_result(result))
    
    @staticmethod
    def print_section(name: str):
        """Print a section header"""
        print(TestReporter.format_section(name))
    
    @staticmethod
    def print_subsection(name: str):
        """Print a subsection header"""
        print(TestReporter.format_subsection(name))
    
    @staticmethod
    def print_summary(passed: int, failed: int, skipped: int = 0):
        """Print final summary"""
        print(TestReporter.format_summary(passed, failed, skipped))
    
    @staticmethod
    def print_failures(failures: List[str]):
        """Print list of failures"""
        failures_text = TestReporter.format_failures(failures)
        if failures_text:
            print(failures_text)
