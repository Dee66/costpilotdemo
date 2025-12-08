#!/usr/bin/env python3
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

