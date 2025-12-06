#!/usr/bin/env python3
"""
Test Framework - Main entry point for test infrastructure
Consolidates imports for easy use in test files
"""

from .test_result import TestResult
from .test_reporter import TestReporter
from .test_suite import TestSuite

__all__ = ['TestResult', 'TestReporter', 'TestSuite']
