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
Test Suite Base Class - Abstract base for all test suites
Part of SOLID refactoring: Open/Closed Principle
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from .test_result import TestResult
from .test_reporter import TestReporter


class TestSuite(ABC):
    """Abstract base class for all test suites"""
    
    def __init__(self, repo_root: Path = None):
        self.repo_root = repo_root or Path(__file__).parent.parent.parent
        self.results: List[TestResult] = []
        self.reporter = TestReporter()
    
    @property
    @abstractmethod
    def tags(self) -> List[str]:
        """Return list of tags for this test suite - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def run(self):
        """Run all tests in this suite - must be implemented by subclasses"""
        pass
    
    def add_result(self, name: str, passed: bool, reason: str = ""):
        """Add a test result"""
        result = TestResult(name=name, passed=passed, reason=reason)
        self.results.append(result)
        self.reporter.print_result(result)
    
    def test(self, name: str, condition: bool, reason: str = ""):
        """Convenience method for testing a condition"""
        self.add_result(name, condition, reason)
    
    def skip(self, name: str, reason: str = ""):
        """Mark a test as skipped"""
        from .test_reporter import YELLOW, RESET
        print(f"  {YELLOW}⊘{RESET} {name}" + 
              (f" - {reason}" if reason else ""))
    
    def section(self, name: str):
        """Print a section header"""
        self.reporter.print_section(name)
    
    def subsection(self, name: str):
        """Print a subsection header"""
        self.reporter.print_subsection(name)
    
    def get_summary(self) -> dict:
        """Get test execution summary"""
        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed)
        
        return {
            "total": len(self.results),
            "passed": passed,
            "failed": failed,
            "pass_rate": (passed / len(self.results) * 100) if self.results else 0
        }
    
    def print_summary(self):
        """Print test execution summary"""
        summary = self.get_summary()
        failures = [r.name + (f": {r.reason}" if r.reason else "") 
                   for r in self.results if not r.passed]
        
        self.reporter.print_summary(summary["passed"], summary["failed"])
        if failures:
            self.reporter.print_failures(failures)
    
    def get_exit_code(self) -> int:
        """Get exit code (0 for success, 1 for any failures)"""
        summary = self.get_summary()
        return 0 if summary["failed"] == 0 else 1
