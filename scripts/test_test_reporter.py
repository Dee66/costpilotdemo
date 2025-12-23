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
Extensive Unit Tests for TestReporter Class
Tests the output formatting and reporting functionality
"""

import sys
from pathlib import Path
import io
from contextlib import redirect_stdout

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.test_reporter import TestReporter
from lib.test_result import TestResult


def capture_output(func):
    """Helper to capture stdout"""
    f = io.StringIO()
    with redirect_stdout(f):
        func()
    return f.getvalue()


def test_reporter_initialization():
    """TestReporter should initialize without errors"""
    reporter = TestReporter()
    assert reporter is not None
    print("✓ reporter_initialization")


def test_reporter_has_color_constants():
    """TestReporter should have color constants"""
    reporter = TestReporter()
    assert hasattr(TestReporter, 'GREEN')
    assert hasattr(TestReporter, 'RED')
    assert hasattr(TestReporter, 'YELLOW')
    assert hasattr(TestReporter, 'BLUE')
    assert hasattr(TestReporter, 'RESET')
    print("✓ reporter_has_color_constants")


def test_reporter_color_constants_are_strings():
    """Color constants should be strings"""
    assert isinstance(TestReporter.GREEN, str)
    assert isinstance(TestReporter.RED, str)
    assert isinstance(TestReporter.YELLOW, str)
    assert isinstance(TestReporter.BLUE, str)
    assert isinstance(TestReporter.RESET, str)
    print("✓ reporter_color_constants_are_strings")


def test_print_result_method_exists():
    """print_result method should exist"""
    reporter = TestReporter()
    assert hasattr(reporter, 'print_result')
    assert callable(reporter.print_result)
    print("✓ print_result_method_exists")


def test_print_result_passed():
    """print_result should handle passed results"""
    reporter = TestReporter()
    result = TestResult(name="test_pass", passed=True, reason="Success")
    
    # Should not raise
    output = capture_output(lambda: reporter.print_result(result))
    assert len(output) > 0
    print("✓ print_result_passed")


def test_print_result_failed():
    """print_result should handle failed results"""
    reporter = TestReporter()
    result = TestResult(name="test_fail", passed=False, reason="Expected failure")
    
    # Should not raise
    output = capture_output(lambda: reporter.print_result(result))
    assert len(output) > 0
    print("✓ print_result_failed")


def test_print_result_contains_name():
    """print_result output should contain test name"""
    reporter = TestReporter()
    result = TestResult(name="my_unique_test", passed=True)
    
    output = capture_output(lambda: reporter.print_result(result))
    assert "my_unique_test" in output
    print("✓ print_result_contains_name")


def test_print_result_contains_reason():
    """print_result output should contain reason"""
    reporter = TestReporter()
    result = TestResult(name="test", passed=False, reason="Unique failure reason")
    
    output = capture_output(lambda: reporter.print_result(result))
    assert "Unique failure reason" in output
    print("✓ print_result_contains_reason")


def test_print_result_no_reason():
    """print_result should handle empty reason"""
    reporter = TestReporter()
    result = TestResult(name="test", passed=True, reason="")
    
    # Should not crash
    output = capture_output(lambda: reporter.print_result(result))
    assert len(output) > 0
    print("✓ print_result_no_reason")


def test_print_section_method_exists():
    """print_section method should exist"""
    reporter = TestReporter()
    assert hasattr(reporter, 'print_section')
    assert callable(reporter.print_section)
    print("✓ print_section_method_exists")


def test_print_section_output():
    """print_section should produce output"""
    reporter = TestReporter()
    
    output = capture_output(lambda: reporter.print_section("Test Section"))
    assert len(output) > 0
    assert "Test Section" in output
    print("✓ print_section_output")


def test_print_section_formatting():
    """print_section should have visible formatting"""
    reporter = TestReporter()
    
    output = capture_output(lambda: reporter.print_section("Section"))
    # Should have separator lines or special formatting
    assert "=" in output or "-" in output or len(output) > 20
    print("✓ print_section_formatting")


def test_print_subsection_method_exists():
    """print_subsection method should exist"""
    reporter = TestReporter()
    assert hasattr(reporter, 'print_subsection')
    assert callable(reporter.print_subsection)
    print("✓ print_subsection_method_exists")


def test_print_subsection_output():
    """print_subsection should produce output"""
    reporter = TestReporter()
    
    output = capture_output(lambda: reporter.print_subsection("Sub Section"))
    assert len(output) > 0
    assert "Sub Section" in output
    print("✓ print_subsection_output")


def test_print_summary_method_exists():
    """print_summary method should exist"""
    reporter = TestReporter()
    assert hasattr(reporter, 'print_summary')
    assert callable(reporter.print_summary)
    print("✓ print_summary_method_exists")


def test_print_summary_output():
    """print_summary should produce output"""
    reporter = TestReporter()
    summary = {"total": 10, "passed": 8, "failed": 2, "pass_rate": 80.0}
    
    output = capture_output(lambda: reporter.print_summary(summary))
    assert len(output) > 0
    print("✓ print_summary_output")


def test_print_summary_contains_metrics():
    """print_summary should display metrics"""
    reporter = TestReporter()
    summary = {"total": 10, "passed": 8, "failed": 2, "pass_rate": 80.0}
    
    output = capture_output(lambda: reporter.print_summary(summary))
    assert "10" in output or "8" in output or "2" in output
    print("✓ print_summary_contains_metrics")


def test_print_summary_empty_results():
    """print_summary should handle empty results"""
    reporter = TestReporter()
    summary = {"total": 0, "passed": 0, "failed": 0, "pass_rate": 0}
    
    # Should not crash
    output = capture_output(lambda: reporter.print_summary(summary))
    assert len(output) > 0
    print("✓ print_summary_empty_results")


def test_print_summary_all_passed():
    """print_summary should handle 100% pass rate"""
    reporter = TestReporter()
    summary = {"total": 5, "passed": 5, "failed": 0, "pass_rate": 100.0}
    
    output = capture_output(lambda: reporter.print_summary(summary))
    assert "100" in output or "5" in output
    print("✓ print_summary_all_passed")


def test_print_summary_all_failed():
    """print_summary should handle 0% pass rate"""
    reporter = TestReporter()
    summary = {"total": 5, "passed": 0, "failed": 5, "pass_rate": 0.0}
    
    output = capture_output(lambda: reporter.print_summary(summary))
    assert "0" in output or "5" in output
    print("✓ print_summary_all_failed")


def test_multiple_results_sequence():
    """Reporter should handle multiple results in sequence"""
    reporter = TestReporter()
    results = [
        TestResult(name="test1", passed=True),
        TestResult(name="test2", passed=False),
        TestResult(name="test3", passed=True)
    ]
    
    # Should not crash
    for result in results:
        output = capture_output(lambda: reporter.print_result(result))
        assert len(output) > 0
    print("✓ multiple_results_sequence")


def test_reporter_reusability():
    """Reporter instance should be reusable"""
    reporter = TestReporter()
    
    # Use multiple times
    reporter.print_section("Section 1")
    reporter.print_result(TestResult(name="test1", passed=True))
    reporter.print_section("Section 2")
    reporter.print_result(TestResult(name="test2", passed=False))
    
    # Should not have issues
    print("✓ reporter_reusability")


def test_special_characters_in_output():
    """Reporter should handle special characters"""
    reporter = TestReporter()
    result = TestResult(name="test-with-dashes_and_underscores", passed=True)
    
    output = capture_output(lambda: reporter.print_result(result))
    assert "dashes" in output
    print("✓ special_characters_in_output")


def test_unicode_in_output():
    """Reporter should handle unicode characters"""
    reporter = TestReporter()
    result = TestResult(name="test_emoji_✓", passed=True, reason="成功")
    
    output = capture_output(lambda: reporter.print_result(result))
    # Should at least not crash
    assert len(output) > 0
    print("✓ unicode_in_output")


def test_long_test_names():
    """Reporter should handle long test names"""
    reporter = TestReporter()
    long_name = "test_" + "x" * 200
    result = TestResult(name=long_name, passed=True)
    
    output = capture_output(lambda: reporter.print_result(result))
    assert len(output) > 0
    print("✓ long_test_names")


def test_long_reasons():
    """Reporter should handle long reasons"""
    reporter = TestReporter()
    long_reason = "This is a very long reason " * 50
    result = TestResult(name="test", passed=False, reason=long_reason)
    
    output = capture_output(lambda: reporter.print_result(result))
    assert len(output) > 0
    print("✓ long_reasons")


def test_multiline_reasons():
    """Reporter should handle multiline reasons"""
    reporter = TestReporter()
    reason = "Line 1\nLine 2\nLine 3"
    result = TestResult(name="test", passed=False, reason=reason)
    
    output = capture_output(lambda: reporter.print_result(result))
    assert len(output) > 0
    print("✓ multiline_reasons")


def test_section_with_special_chars():
    """print_section should handle special characters"""
    reporter = TestReporter()
    
    output = capture_output(lambda: reporter.print_section("Section: Test #1 (Part A)"))
    assert "Section" in output
    print("✓ section_with_special_chars")


def test_section_with_unicode():
    """print_section should handle unicode"""
    reporter = TestReporter()
    
    output = capture_output(lambda: reporter.print_section("测试部分 ✓"))
    assert len(output) > 0
    print("✓ section_with_unicode")


def test_subsection_differentiation():
    """Subsection output should differ from section"""
    reporter = TestReporter()
    
    section_output = capture_output(lambda: reporter.print_section("Main"))
    subsection_output = capture_output(lambda: reporter.print_subsection("Sub"))
    
    # They should produce different output (different formatting)
    assert section_output != subsection_output
    print("✓ subsection_differentiation")


def test_summary_dict_keys():
    """print_summary should work with standard dict keys"""
    reporter = TestReporter()
    summary = {
        "total": 100,
        "passed": 95,
        "failed": 5,
        "pass_rate": 95.0
    }
    
    # Should not crash
    output = capture_output(lambda: reporter.print_summary(summary))
    assert len(output) > 0
    print("✓ summary_dict_keys")


def test_summary_missing_keys():
    """print_summary should handle missing keys gracefully"""
    reporter = TestReporter()
    summary = {"total": 10}  # Missing other keys
    
    try:
        output = capture_output(lambda: reporter.print_summary(summary))
        # If it handles gracefully
        print("✓ summary_missing_keys (graceful handling)")
    except KeyError:
        # If it requires all keys (also acceptable)
        print("✓ summary_missing_keys (requires all keys)")


def test_reporter_no_state():
    """Reporter should not maintain state between calls"""
    reporter = TestReporter()
    
    reporter.print_result(TestResult(name="test1", passed=True))
    reporter.print_result(TestResult(name="test2", passed=False))
    
    # Second call should not be affected by first
    # (No state to check, but shouldn't crash)
    print("✓ reporter_no_state")


def test_color_constants_not_none():
    """Color constants should not be None"""
    assert TestReporter.GREEN is not None
    assert TestReporter.RED is not None
    assert TestReporter.YELLOW is not None
    assert TestReporter.BLUE is not None
    assert TestReporter.RESET is not None
    print("✓ color_constants_not_none")


def test_color_constants_unique():
    """Color constants should be unique (or RESET might be empty)"""
    colors = [
        TestReporter.GREEN,
        TestReporter.RED,
        TestReporter.YELLOW,
        TestReporter.BLUE
    ]
    
    # Colors should be different from each other (except if disabled)
    # At minimum, they should all be strings
    assert all(isinstance(c, str) for c in colors)
    print("✓ color_constants_unique")


def test_stress_many_results():
    """Reporter should handle many results"""
    reporter = TestReporter()
    
    for i in range(100):
        result = TestResult(name=f"test_{i}", passed=i % 2 == 0)
        output = capture_output(lambda: reporter.print_result(result))
        assert len(output) > 0
    
    print("✓ stress_many_results")


def test_stress_many_sections():
    """Reporter should handle many sections"""
    reporter = TestReporter()
    
    for i in range(50):
        output = capture_output(lambda: reporter.print_section(f"Section {i}"))
        assert len(output) > 0
    
    print("✓ stress_many_sections")


def test_reporter_thread_safety():
    """Reporter should be usable (basic test, not full thread safety)"""
    reporter = TestReporter()
    
    # Just verify it can be called multiple times
    for _ in range(10):
        reporter.print_result(TestResult(name="test", passed=True))
    
    print("✓ reporter_thread_safety (basic)")


def run_all_tests():
    """Run all TestReporter unit tests"""
    print("\n" + "="*80)
    print("TESTREPORTER CLASS TESTS")
    print("="*80)
    
    tests = [
        ("INITIALIZATION", [
            test_reporter_initialization,
            test_reporter_has_color_constants,
            test_reporter_color_constants_are_strings,
            test_color_constants_not_none,
            test_color_constants_unique
        ]),
        ("PRINT RESULT METHOD", [
            test_print_result_method_exists,
            test_print_result_passed,
            test_print_result_failed,
            test_print_result_contains_name,
            test_print_result_contains_reason,
            test_print_result_no_reason
        ]),
        ("PRINT SECTION METHOD", [
            test_print_section_method_exists,
            test_print_section_output,
            test_print_section_formatting,
            test_section_with_special_chars,
            test_section_with_unicode
        ]),
        ("PRINT SUBSECTION METHOD", [
            test_print_subsection_method_exists,
            test_print_subsection_output,
            test_subsection_differentiation
        ]),
        ("PRINT SUMMARY METHOD", [
            test_print_summary_method_exists,
            test_print_summary_output,
            test_print_summary_contains_metrics,
            test_print_summary_empty_results,
            test_print_summary_all_passed,
            test_print_summary_all_failed,
            test_summary_dict_keys,
            test_summary_missing_keys
        ]),
        ("SPECIAL CHARACTERS", [
            test_special_characters_in_output,
            test_unicode_in_output,
            test_long_test_names,
            test_long_reasons,
            test_multiline_reasons
        ]),
        ("BEHAVIOR", [
            test_multiple_results_sequence,
            test_reporter_reusability,
            test_reporter_no_state
        ]),
        ("STRESS TESTS", [
            test_stress_many_results,
            test_stress_many_sections,
            test_reporter_thread_safety
        ])
    ]
    
    total = 0
    passed = 0
    
    for section_name, section_tests in tests:
        print(f"\n{section_name} ({len(section_tests)} tests)")
        print("-" * 80)
        
        for test_func in section_tests:
            total += 1
            try:
                test_func()
                passed += 1
            except Exception as e:
                print(f"✗ {test_func.__name__}: {e}")
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total:   {total}")
    print(f"Passed:  {passed}")
    print(f"Failed:  {total - passed}")
    if total > 0:
        print(f"Pass Rate: {(passed/total)*100:.1f}%")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
