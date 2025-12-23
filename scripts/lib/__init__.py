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
Test Framework - Main entry point for test infrastructure
Consolidates imports for easy use in test files
"""

from .test_result import TestResult
from .test_reporter import TestReporter
from .test_suite import TestSuite
from .scenario_factory import Scenario, ScenarioFactory, create_scenario
from .result_exporter import (
    ResultExporter,
    JSONExporter,
    HTMLExporter,
    MarkdownExporter,
    JUnitXMLExporter,
    create_exporter
)
from .timing import (
    timed,
    get_timing_data,
    get_timing_summary,
    get_slow_functions,
    print_timing_report,
    clear_timing_data,
    export_timing_data,
    TimingContext
)

__all__ = [
    'TestResult', 
    'TestReporter', 
    'TestSuite', 
    'Scenario', 
    'ScenarioFactory', 
    'create_scenario',
    'ResultExporter',
    'JSONExporter',
    'HTMLExporter',
    'MarkdownExporter',
    'JUnitXMLExporter',
    'create_exporter',
    'timed',
    'get_timing_data',
    'get_timing_summary',
    'get_slow_functions',
    'print_timing_report',
    'clear_timing_data',
    'export_timing_data',
    'TimingContext'
]

