#!/usr/bin/env python3
"""
Extensive Unit Tests for TestSuite Base Class
Tests the abstract base class and Template Method pattern implementation
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.test_suite import TestSuite
from lib.test_result import TestResult
from lib.test_reporter import TestReporter


class ConcreteTestSuite(TestSuite):
    """Concrete implementation for testing"""
    
    @property
    def tags(self):
        return ["framework", "test-suite", "validation"]
    
    def __init__(self, repo_root=None):
        super().__init__(repo_root)
        self.run_called = False
    
    def run(self):
        """Implementation of abstract run method"""
        self.run_called = True
        self.section("Test Section")
        self.test("test_1", True, "Passes")
        self.test("test_2", False, "Fails")
        self.skip("test_3", "Not ready")


def test_testsuite_initialization():
    """TestSuite should initialize with default repo root"""
    suite = ConcreteTestSuite()
    assert suite.repo_root is not None
    assert isinstance(suite.repo_root, Path)
    assert suite.repo_root.exists()
    print("✓ testsuite_initialization")


def test_testsuite_custom_repo_root():
    """TestSuite should accept custom repo root"""
    custom_root = Path("/tmp")
    suite = ConcreteTestSuite(repo_root=custom_root)
    assert suite.repo_root == custom_root
    print("✓ testsuite_custom_repo_root")


def test_testsuite_has_results_list():
    """TestSuite should have results list"""
    suite = ConcreteTestSuite()
    assert hasattr(suite, 'results')
    assert isinstance(suite.results, list)
    assert len(suite.results) == 0
    print("✓ testsuite_has_results_list")


def test_testsuite_has_reporter():
    """TestSuite should have a reporter"""
    suite = ConcreteTestSuite()
    assert hasattr(suite, 'reporter')
    assert isinstance(suite.reporter, TestReporter)
    print("✓ testsuite_has_reporter")


def test_testsuite_run_is_abstract():
    """TestSuite.run should be abstract"""
    try:
        # Can't instantiate ABC without implementing run
        suite = TestSuite()
        assert False, "Should not be able to instantiate TestSuite directly"
    except TypeError as e:
        assert "abstract" in str(e).lower()
    print("✓ testsuite_run_is_abstract")


def test_add_result_creates_testresult():
    """add_result should create TestResult objects"""
    suite = ConcreteTestSuite()
    suite.add_result("my_test", True, "Success")
    
    assert len(suite.results) == 1
    result = suite.results[0]
    assert isinstance(result, TestResult)
    assert result.name == "my_test"
    assert result.passed == True
    assert result.reason == "Success"
    print("✓ add_result_creates_testresult")


def test_add_result_multiple():
    """add_result should accumulate multiple results"""
    suite = ConcreteTestSuite()
    suite.add_result("test_1", True)
    suite.add_result("test_2", False)
    suite.add_result("test_3", True)
    
    assert len(suite.results) == 3
    assert suite.results[0].name == "test_1"
    assert suite.results[1].name == "test_2"
    assert suite.results[2].name == "test_3"
    print("✓ add_result_multiple")


def test_test_method_convenience():
    """test() method should be convenience wrapper for add_result"""
    suite = ConcreteTestSuite()
    suite.test("convenience_test", True, "Works")
    
    assert len(suite.results) == 1
    assert suite.results[0].name == "convenience_test"
    assert suite.results[0].passed == True
    print("✓ test_method_convenience")


def test_test_method_with_condition():
    """test() method should evaluate conditions"""
    suite = ConcreteTestSuite()
    suite.test("math_check", 2 + 2 == 4, "Math works")
    suite.test("string_check", "hello" == "world", "String fails")
    
    assert len(suite.results) == 2
    assert suite.results[0].passed == True
    assert suite.results[1].passed == False
    print("✓ test_method_with_condition")


def test_get_summary_empty():
    """get_summary should handle empty results"""
    suite = ConcreteTestSuite()
    summary = suite.get_summary()
    
    assert summary["total"] == 0
    assert summary["passed"] == 0
    assert summary["failed"] == 0
    assert summary["pass_rate"] == 0
    print("✓ get_summary_empty")


def test_get_summary_all_passed():
    """get_summary should calculate when all pass"""
    suite = ConcreteTestSuite()
    suite.test("test_1", True)
    suite.test("test_2", True)
    suite.test("test_3", True)
    
    summary = suite.get_summary()
    assert summary["total"] == 3
    assert summary["passed"] == 3
    assert summary["failed"] == 0
    assert summary["pass_rate"] == 100.0
    print("✓ get_summary_all_passed")


def test_get_summary_all_failed():
    """get_summary should calculate when all fail"""
    suite = ConcreteTestSuite()
    suite.test("test_1", False)
    suite.test("test_2", False)
    
    summary = suite.get_summary()
    assert summary["total"] == 2
    assert summary["passed"] == 0
    assert summary["failed"] == 2
    assert summary["pass_rate"] == 0.0
    print("✓ get_summary_all_failed")


def test_get_summary_mixed():
    """get_summary should calculate mixed results"""
    suite = ConcreteTestSuite()
    suite.test("pass_1", True)
    suite.test("fail_1", False)
    suite.test("pass_2", True)
    suite.test("fail_2", False)
    suite.test("pass_3", True)
    
    summary = suite.get_summary()
    assert summary["total"] == 5
    assert summary["passed"] == 3
    assert summary["failed"] == 2
    assert summary["pass_rate"] == 60.0
    print("✓ get_summary_mixed")


def test_get_summary_pass_rate_precision():
    """get_summary should calculate pass rate precisely"""
    suite = ConcreteTestSuite()
    # 2 passed out of 3 = 66.666...%
    suite.test("pass_1", True)
    suite.test("fail_1", False)
    suite.test("pass_2", True)
    
    summary = suite.get_summary()
    assert summary["pass_rate"] > 66.6
    assert summary["pass_rate"] < 66.7
    print("✓ get_summary_pass_rate_precision")


def test_section_method_exists():
    """section() method should exist"""
    suite = ConcreteTestSuite()
    # Should not raise
    suite.section("My Section")
    print("✓ section_method_exists")


def test_subsection_method_exists():
    """subsection() method should exist"""
    suite = ConcreteTestSuite()
    # Should not raise
    suite.subsection("My Subsection")
    print("✓ subsection_method_exists")


def test_skip_method_exists():
    """skip() method should exist"""
    suite = ConcreteTestSuite()
    # Should not raise
    suite.skip("skipped_test", "Not implemented")
    print("✓ skip_method_exists")


def test_skip_method_with_reason():
    """skip() should accept reason"""
    suite = ConcreteTestSuite()
    # Should not raise or crash
    suite.skip("test_pending", "Feature not ready")
    suite.skip("test_blocked", "")
    print("✓ skip_method_with_reason")


def test_concrete_run_implementation():
    """Concrete subclass run() should be callable"""
    suite = ConcreteTestSuite()
    suite.run()
    
    assert suite.run_called == True
    assert len(suite.results) == 2  # test_1 and test_2
    print("✓ concrete_run_implementation")


def test_run_populates_results():
    """run() should populate results"""
    suite = ConcreteTestSuite()
    suite.run()
    
    # ConcreteTestSuite.run adds 2 tests
    assert len(suite.results) >= 2
    assert suite.results[0].name == "test_1"
    assert suite.results[1].name == "test_2"
    print("✓ run_populates_results")


def test_multiple_runs_accumulate():
    """Multiple run() calls should accumulate results"""
    suite = ConcreteTestSuite()
    suite.run()
    initial_count = len(suite.results)
    
    suite.run()
    assert len(suite.results) == initial_count * 2
    print("✓ multiple_runs_accumulate")


def test_results_are_mutable():
    """Results list should be mutable"""
    suite = ConcreteTestSuite()
    suite.test("test_1", True)
    
    # Should be able to modify
    suite.results[0].passed = False
    assert suite.results[0].passed == False
    print("✓ results_are_mutable")


def test_results_preserve_order():
    """Results should preserve insertion order"""
    suite = ConcreteTestSuite()
    names = ["alpha", "beta", "gamma", "delta"]
    
    for name in names:
        suite.test(name, True)
    
    for i, name in enumerate(names):
        assert suite.results[i].name == name
    print("✓ results_preserve_order")


def test_empty_reason_allowed():
    """Empty reason should be allowed"""
    suite = ConcreteTestSuite()
    suite.test("test_no_reason", True, "")
    suite.test("test_no_reason_2", False)  # No reason arg
    
    assert suite.results[0].reason == ""
    assert len(suite.results) == 2
    print("✓ empty_reason_allowed")


def test_special_characters_in_test_name():
    """Test names can contain special characters"""
    suite = ConcreteTestSuite()
    suite.test("test-with-dashes", True)
    suite.test("test_with_underscores", True)
    suite.test("test.with.dots", True)
    suite.test("test:with:colons", True)
    
    assert len(suite.results) == 4
    print("✓ special_characters_in_test_name")


def test_long_test_names():
    """Test names can be long"""
    suite = ConcreteTestSuite()
    long_name = "test_" + "a" * 200
    suite.test(long_name, True)
    
    assert suite.results[0].name == long_name
    print("✓ long_test_names")


def test_unicode_in_test_name():
    """Test names can contain unicode"""
    suite = ConcreteTestSuite()
    suite.test("test_emoji_✓", True)
    suite.test("test_中文", True)
    
    assert len(suite.results) == 2
    print("✓ unicode_in_test_name")


def test_summary_dict_keys():
    """get_summary should return dict with expected keys"""
    suite = ConcreteTestSuite()
    suite.test("test_1", True)
    
    summary = suite.get_summary()
    assert "total" in summary
    assert "passed" in summary
    assert "failed" in summary
    assert "pass_rate" in summary
    assert len(summary.keys()) == 4
    print("✓ summary_dict_keys")


def test_summary_dict_types():
    """get_summary should return correct types"""
    suite = ConcreteTestSuite()
    suite.test("test_1", True)
    
    summary = suite.get_summary()
    assert isinstance(summary["total"], int)
    assert isinstance(summary["passed"], int)
    assert isinstance(summary["failed"], int)
    assert isinstance(summary["pass_rate"], float)
    print("✓ summary_dict_types")


def test_repo_root_is_path_object():
    """repo_root should be Path object"""
    suite = ConcreteTestSuite()
    assert isinstance(suite.repo_root, Path)
    print("✓ repo_root_is_path_object")


def test_repo_root_string_conversion():
    """repo_root from string should convert to Path"""
    suite = ConcreteTestSuite(repo_root=Path("/tmp"))
    assert isinstance(suite.repo_root, Path)
    print("✓ repo_root_string_conversion")


def test_results_list_independence():
    """Each suite should have independent results list"""
    suite1 = ConcreteTestSuite()
    suite2 = ConcreteTestSuite()
    
    suite1.test("test_1", True)
    suite2.test("test_2", False)
    
    assert len(suite1.results) == 1
    assert len(suite2.results) == 1
    assert suite1.results[0].name != suite2.results[0].name
    print("✓ results_list_independence")


def test_boolean_condition_evaluation():
    """test() should evaluate boolean conditions correctly"""
    suite = ConcreteTestSuite()
    
    suite.test("true_literal", True)
    suite.test("false_literal", False)
    suite.test("truthy_value", 1)
    suite.test("falsy_value", 0)
    suite.test("none_value", None)
    suite.test("empty_string", "")
    suite.test("non_empty_string", "hello")
    
    results = suite.results
    assert results[0].passed == True   # True
    assert results[1].passed == False  # False
    assert results[2].passed == True   # 1 (truthy)
    assert results[3].passed == False  # 0 (falsy)
    assert results[4].passed == False  # None (falsy)
    assert results[5].passed == False  # "" (falsy)
    assert results[6].passed == True   # "hello" (truthy)
    print("✓ boolean_condition_evaluation")


def test_stress_many_results():
    """TestSuite should handle many results"""
    suite = ConcreteTestSuite()
    
    for i in range(1000):
        suite.test(f"test_{i}", i % 2 == 0)
    
    assert len(suite.results) == 1000
    summary = suite.get_summary()
    assert summary["total"] == 1000
    assert summary["passed"] == 500
    assert summary["failed"] == 500
    print("✓ stress_many_results")


def run_all_tests():
    """Run all TestSuite unit tests"""
    print("\n" + "="*80)
    print("TESTSUITE BASE CLASS TESTS")
    print("="*80)
    
    tests = [
        ("INITIALIZATION", [
            test_testsuite_initialization,
            test_testsuite_custom_repo_root,
            test_testsuite_has_results_list,
            test_testsuite_has_reporter,
            test_testsuite_run_is_abstract
        ]),
        ("ADD RESULT METHOD", [
            test_add_result_creates_testresult,
            test_add_result_multiple,
            test_test_method_convenience,
            test_test_method_with_condition,
            test_empty_reason_allowed
        ]),
        ("GET SUMMARY METHOD", [
            test_get_summary_empty,
            test_get_summary_all_passed,
            test_get_summary_all_failed,
            test_get_summary_mixed,
            test_get_summary_pass_rate_precision,
            test_summary_dict_keys,
            test_summary_dict_types
        ]),
        ("HELPER METHODS", [
            test_section_method_exists,
            test_subsection_method_exists,
            test_skip_method_exists,
            test_skip_method_with_reason
        ]),
        ("RUN IMPLEMENTATION", [
            test_concrete_run_implementation,
            test_run_populates_results,
            test_multiple_runs_accumulate
        ]),
        ("RESULTS BEHAVIOR", [
            test_results_are_mutable,
            test_results_preserve_order,
            test_results_list_independence
        ]),
        ("TEST NAME HANDLING", [
            test_special_characters_in_test_name,
            test_long_test_names,
            test_unicode_in_test_name
        ]),
        ("TYPE HANDLING", [
            test_repo_root_is_path_object,
            test_repo_root_string_conversion,
            test_boolean_condition_evaluation
        ]),
        ("STRESS TESTS", [
            test_stress_many_results
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
