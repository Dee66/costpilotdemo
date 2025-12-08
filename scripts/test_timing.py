#!/usr/bin/env python3
"""
Unit tests for Timing Module
Tests decorator, context manager, and reporting functions
"""

import sys
from pathlib import Path
import time
import json

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.timing import (
    timed,
    get_timing_data,
    get_timing_summary,
    get_slow_functions,
    clear_timing_data,
    export_timing_data,
    TimingContext
)


def test_timed_decorator_records_execution():
    """@timed decorator should record execution time"""
    clear_timing_data()
    
    @timed
    def sample_func():
        time.sleep(0.01)  # 10ms
    
    sample_func()
    
    data = get_timing_data()
    assert "sample_func" in data
    assert len(data["sample_func"]) == 1
    assert data["sample_func"][0] >= 0.01
    print("✓ timed_decorator_records_execution")


def test_timed_decorator_multiple_calls():
    """@timed decorator should record multiple calls"""
    clear_timing_data()
    
    @timed
    def another_func():
        time.sleep(0.005)
    
    another_func()
    another_func()
    another_func()
    
    data = get_timing_data()
    assert "another_func" in data
    assert len(data["another_func"]) == 3
    print("✓ timed_decorator_multiple_calls")


def test_timing_summary_calculates_stats():
    """get_timing_summary should calculate statistics"""
    clear_timing_data()
    
    @timed
    def stats_func():
        time.sleep(0.001)
    
    stats_func()
    stats_func()
    
    summary = get_timing_summary()
    assert "stats_func" in summary
    stats = summary["stats_func"]
    assert "total" in stats
    assert "count" in stats
    assert "avg" in stats
    assert "min" in stats
    assert "max" in stats
    assert stats["count"] == 2
    print("✓ timing_summary_calculates_stats")


def test_get_slow_functions_filters_by_threshold():
    """get_slow_functions should filter by threshold"""
    clear_timing_data()
    
    @timed
    def fast_func():
        time.sleep(0.001)  # 1ms
    
    @timed
    def slow_func():
        time.sleep(0.015)  # 15ms
    
    fast_func()
    slow_func()
    
    # Get functions slower than 10ms
    slow_funcs = get_slow_functions(threshold_ms=10)
    
    assert len(slow_funcs) == 1
    assert slow_funcs[0][0] == "slow_func"
    assert slow_funcs[0][1] >= 10  # Time in ms
    print("✓ get_slow_functions_filters_by_threshold")


def test_timing_context_manager():
    """TimingContext should time code blocks"""
    clear_timing_data()
    
    with TimingContext("my_operation"):
        time.sleep(0.005)
    
    data = get_timing_data()
    assert "my_operation" in data
    assert len(data["my_operation"]) == 1
    assert data["my_operation"][0] >= 0.005
    print("✓ timing_context_manager")


def test_timing_context_multiple_uses():
    """TimingContext should work multiple times"""
    clear_timing_data()
    
    with TimingContext("repeated_op"):
        time.sleep(0.001)
    
    with TimingContext("repeated_op"):
        time.sleep(0.001)
    
    data = get_timing_data()
    assert len(data["repeated_op"]) == 2
    print("✓ timing_context_multiple_uses")


def test_clear_timing_data():
    """clear_timing_data should clear all data"""
    @timed
    def temp_func():
        pass
    
    temp_func()
    assert len(get_timing_data()) > 0
    
    clear_timing_data()
    assert len(get_timing_data()) == 0
    print("✓ clear_timing_data")


def test_export_timing_data_json():
    """export_timing_data should export JSON"""
    clear_timing_data()
    
    @timed
    def export_test():
        time.sleep(0.001)
    
    export_test()
    
    output_path = "/tmp/timing_export.json"
    export_timing_data(output_path, format="json")
    
    assert Path(output_path).exists()
    
    with open(output_path) as f:
        data = json.load(f)
        assert "summary" in data
        assert "raw_data" in data
        assert "export_test" in data["summary"]
    
    print("✓ export_timing_data_json")


def test_export_timing_data_csv():
    """export_timing_data should export CSV"""
    clear_timing_data()
    
    @timed
    def csv_test():
        time.sleep(0.001)
    
    csv_test()
    
    output_path = "/tmp/timing_export.csv"
    export_timing_data(output_path, format="csv")
    
    assert Path(output_path).exists()
    
    content = Path(output_path).read_text()
    assert "Function,Total (ms),Count,Avg (ms)" in content
    assert "csv_test" in content
    
    print("✓ export_timing_data_csv")


def test_timed_decorator_preserves_return_value():
    """@timed decorator should preserve return value"""
    clear_timing_data()
    
    @timed
    def returns_value():
        return 42
    
    result = returns_value()
    assert result == 42
    print("✓ timed_decorator_preserves_return_value")


def test_timed_decorator_preserves_function_name():
    """@timed decorator should preserve function metadata"""
    clear_timing_data()
    
    @timed
    def named_function():
        """This is a docstring"""
        pass
    
    assert named_function.__name__ == "named_function"
    assert named_function.__doc__ == "This is a docstring"
    print("✓ timed_decorator_preserves_function_name")


def test_get_slow_functions_sorted_descending():
    """get_slow_functions should sort by time descending"""
    clear_timing_data()
    
    @timed
    def slowest():
        time.sleep(0.03)  # 30ms
    
    @timed
    def medium():
        time.sleep(0.02)  # 20ms
    
    @timed
    def slower():
        time.sleep(0.015)  # 15ms
    
    slowest()
    medium()
    slower()
    
    slow_funcs = get_slow_functions(threshold_ms=10)
    
    assert len(slow_funcs) == 3
    assert slow_funcs[0][0] == "slowest"
    assert slow_funcs[1][0] == "medium"
    assert slow_funcs[2][0] == "slower"
    print("✓ get_slow_functions_sorted_descending")


def test_timing_summary_empty():
    """get_timing_summary should handle empty data"""
    clear_timing_data()
    summary = get_timing_summary()
    assert isinstance(summary, dict)
    assert len(summary) == 0
    print("✓ timing_summary_empty")


def test_timing_context_exception_handling():
    """TimingContext should still record time if exception occurs"""
    clear_timing_data()
    
    try:
        with TimingContext("exception_op"):
            time.sleep(0.001)
            raise ValueError("Test error")
    except ValueError:
        pass
    
    data = get_timing_data()
    assert "exception_op" in data
    assert len(data["exception_op"]) == 1
    print("✓ timing_context_exception_handling")


def run_all_tests():
    """Run all timing tests"""
    print("\n" + "="*80)
    print("TIMING MODULE TESTS")
    print("="*80)
    
    tests = [
        ("DECORATOR TESTS", [
            test_timed_decorator_records_execution,
            test_timed_decorator_multiple_calls,
            test_timed_decorator_preserves_return_value,
            test_timed_decorator_preserves_function_name
        ]),
        ("SUMMARY TESTS", [
            test_timing_summary_calculates_stats,
            test_timing_summary_empty,
            test_get_slow_functions_filters_by_threshold,
            test_get_slow_functions_sorted_descending
        ]),
        ("CONTEXT MANAGER TESTS", [
            test_timing_context_manager,
            test_timing_context_multiple_uses,
            test_timing_context_exception_handling
        ]),
        ("UTILITY TESTS", [
            test_clear_timing_data,
            test_export_timing_data_json,
            test_export_timing_data_csv
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
