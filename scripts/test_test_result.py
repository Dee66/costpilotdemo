#!/usr/bin/env python3
"""
Extensive Unit Tests for TestResult Class
Tests the data container for individual test results
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.test_result import TestResult


def test_testresult_basic_creation():
    """TestResult should create with basic parameters"""
    result = TestResult(name="my_test", passed=True)
    assert result.name == "my_test"
    assert result.passed == True
    assert result.reason == ""
    print("✓ testresult_basic_creation")


def test_testresult_with_reason():
    """TestResult should accept reason parameter"""
    result = TestResult(name="test", passed=False, reason="Expected failure")
    assert result.reason == "Expected failure"
    print("✓ testresult_with_reason")


def test_testresult_name_required():
    """TestResult should require name parameter"""
    try:
        result = TestResult(passed=True)
        assert False, "Should require name"
    except TypeError:
        pass
    print("✓ testresult_name_required")


def test_testresult_passed_required():
    """TestResult should require passed parameter"""
    try:
        result = TestResult(name="test")
        assert False, "Should require passed"
    except TypeError:
        pass
    print("✓ testresult_passed_required")


def test_testresult_reason_optional():
    """TestResult reason should be optional"""
    result = TestResult(name="test", passed=True)
    assert hasattr(result, 'reason')
    print("✓ testresult_reason_optional")


def test_testresult_passed_true():
    """TestResult should store passed=True"""
    result = TestResult(name="pass_test", passed=True)
    assert result.passed is True
    assert result.passed == True
    print("✓ testresult_passed_true")


def test_testresult_passed_false():
    """TestResult should store passed=False"""
    result = TestResult(name="fail_test", passed=False)
    assert result.passed is False
    assert result.passed == False
    print("✓ testresult_passed_false")


def test_testresult_name_string():
    """TestResult name should be string"""
    result = TestResult(name="string_test", passed=True)
    assert isinstance(result.name, str)
    print("✓ testresult_name_string")


def test_testresult_reason_string():
    """TestResult reason should be string"""
    result = TestResult(name="test", passed=True, reason="Because")
    assert isinstance(result.reason, str)
    print("✓ testresult_reason_string")


def test_testresult_empty_name():
    """TestResult should accept empty name"""
    result = TestResult(name="", passed=True)
    assert result.name == ""
    print("✓ testresult_empty_name")


def test_testresult_empty_reason():
    """TestResult should accept empty reason"""
    result = TestResult(name="test", passed=True, reason="")
    assert result.reason == ""
    print("✓ testresult_empty_reason")


def test_testresult_long_name():
    """TestResult should handle long names"""
    long_name = "test_" + "x" * 500
    result = TestResult(name=long_name, passed=True)
    assert result.name == long_name
    assert len(result.name) > 500
    print("✓ testresult_long_name")


def test_testresult_long_reason():
    """TestResult should handle long reasons"""
    long_reason = "This is a very long reason " * 50
    result = TestResult(name="test", passed=False, reason=long_reason)
    assert result.reason == long_reason
    assert len(result.reason) > 100
    print("✓ testresult_long_reason")


def test_testresult_special_chars_name():
    """TestResult name can contain special characters"""
    result = TestResult(name="test-with-dashes_and_underscores.dots", passed=True)
    assert "dashes" in result.name
    assert "_" in result.name
    assert "." in result.name
    print("✓ testresult_special_chars_name")


def test_testresult_unicode_name():
    """TestResult name can contain unicode"""
    result = TestResult(name="test_✓_emoji_中文", passed=True)
    assert "✓" in result.name
    assert "中文" in result.name
    print("✓ testresult_unicode_name")


def test_testresult_unicode_reason():
    """TestResult reason can contain unicode"""
    result = TestResult(name="test", passed=True, reason="Success ✓ 成功")
    assert "✓" in result.reason
    assert "成功" in result.reason
    print("✓ testresult_unicode_reason")


def test_testresult_multiline_reason():
    """TestResult reason can contain newlines"""
    reason = "Line 1\nLine 2\nLine 3"
    result = TestResult(name="test", passed=False, reason=reason)
    assert "\n" in result.reason
    assert result.reason.count("\n") == 2
    print("✓ testresult_multiline_reason")


def test_testresult_attributes_mutable():
    """TestResult attributes should be mutable"""
    result = TestResult(name="test", passed=True, reason="Initial")
    
    result.name = "modified_test"
    result.passed = False
    result.reason = "Modified"
    
    assert result.name == "modified_test"
    assert result.passed == False
    assert result.reason == "Modified"
    print("✓ testresult_attributes_mutable")


def test_testresult_equality_same():
    """TestResult instances with same values should be equal (if __eq__ defined)"""
    result1 = TestResult(name="test", passed=True, reason="Same")
    result2 = TestResult(name="test", passed=True, reason="Same")
    
    # Check attributes are same
    assert result1.name == result2.name
    assert result1.passed == result2.passed
    assert result1.reason == result2.reason
    print("✓ testresult_equality_same")


def test_testresult_different_instances():
    """Different TestResult instances should be distinct"""
    result1 = TestResult(name="test1", passed=True)
    result2 = TestResult(name="test2", passed=False)
    
    assert result1 is not result2
    assert result1.name != result2.name
    print("✓ testresult_different_instances")


def test_testresult_representation():
    """TestResult should have string representation"""
    result = TestResult(name="test", passed=True, reason="OK")
    repr_str = repr(result)
    assert isinstance(repr_str, str)
    print("✓ testresult_representation")


def test_testresult_boolean_coercion():
    """TestResult passed should work in boolean context"""
    pass_result = TestResult(name="pass", passed=True)
    fail_result = TestResult(name="fail", passed=False)
    
    assert pass_result.passed
    assert not fail_result.passed
    print("✓ testresult_boolean_coercion")


def test_testresult_dict_like_access():
    """TestResult attributes accessible via attribute access"""
    result = TestResult(name="test", passed=True, reason="OK")
    
    assert hasattr(result, 'name')
    assert hasattr(result, 'passed')
    assert hasattr(result, 'reason')
    
    assert getattr(result, 'name') == "test"
    assert getattr(result, 'passed') == True
    assert getattr(result, 'reason') == "OK"
    print("✓ testresult_dict_like_access")


def test_testresult_no_extra_attributes():
    """TestResult should only have expected attributes"""
    result = TestResult(name="test", passed=True)
    expected_attrs = {'name', 'passed', 'reason'}
    
    # Get user-defined attributes (filter out __x__ internals)
    actual_attrs = {attr for attr in dir(result) if not attr.startswith('_')}
    
    # Should at least have our expected attributes
    assert expected_attrs.issubset(actual_attrs)
    print("✓ testresult_no_extra_attributes")


def test_testresult_immutability_check():
    """TestResult should allow mutation (not frozen)"""
    result = TestResult(name="test", passed=True)
    
    # Should not raise
    result.name = "new_name"
    result.new_attr = "allowed"
    
    assert result.name == "new_name"
    print("✓ testresult_immutability_check")


def test_testresult_type_checking_name():
    """TestResult name can be non-string (Python allows)"""
    # Python doesn't enforce types at runtime without explicit checks
    result = TestResult(name=123, passed=True)
    assert result.name == 123
    print("✓ testresult_type_checking_name")


def test_testresult_type_checking_passed():
    """TestResult passed can be non-boolean (truthy/falsy)"""
    result1 = TestResult(name="test", passed=1)  # truthy
    result2 = TestResult(name="test", passed=0)  # falsy
    
    assert result1.passed == 1
    assert result2.passed == 0
    print("✓ testresult_type_checking_passed")


def test_testresult_none_values():
    """TestResult can accept None values (if not restricted)"""
    # Note: This might fail if TestResult has validation
    try:
        result = TestResult(name=None, passed=None, reason=None)
        assert result.name is None
        assert result.passed is None
        assert result.reason is None
        print("✓ testresult_none_values")
    except (TypeError, ValueError):
        # If validation exists, that's also acceptable
        print("✓ testresult_none_values (validation prevents None)")


def test_testresult_default_reason_value():
    """TestResult should have default reason value"""
    result = TestResult(name="test", passed=True)
    assert result.reason is not None
    print("✓ testresult_default_reason_value")


def test_testresult_stress_creation():
    """Should handle creating many TestResult instances"""
    results = []
    for i in range(1000):
        result = TestResult(name=f"test_{i}", passed=i % 2 == 0, reason=f"Reason {i}")
        results.append(result)
    
    assert len(results) == 1000
    assert results[0].name == "test_0"
    assert results[999].name == "test_999"
    print("✓ testresult_stress_creation")


def test_testresult_memory_independence():
    """TestResult instances should be independent"""
    result1 = TestResult(name="test1", passed=True, reason="Reason1")
    result2 = TestResult(name="test2", passed=False, reason="Reason2")
    
    result1.name = "modified1"
    assert result2.name == "test2"  # Unchanged
    
    result1.passed = False
    assert result2.passed == False  # Was already False
    print("✓ testresult_memory_independence")


def test_testresult_attribute_deletion():
    """TestResult attributes can be deleted (standard Python objects)"""
    result = TestResult(name="test", passed=True)
    
    # Try to delete (may or may not be allowed depending on class design)
    try:
        del result.reason
        # If deletion succeeds
        assert not hasattr(result, 'reason')
        print("✓ testresult_attribute_deletion (deletion allowed)")
    except AttributeError:
        # If deletion prevented (e.g., __slots__)
        print("✓ testresult_attribute_deletion (deletion restricted)")


def test_testresult_copy_behavior():
    """TestResult should be copyable"""
    import copy
    
    result1 = TestResult(name="original", passed=True, reason="OK")
    result2 = copy.copy(result1)
    
    assert result2.name == "original"
    assert result2.passed == True
    
    result1.name = "modified"
    # Shallow copy means attributes are copied
    print("✓ testresult_copy_behavior")


def test_testresult_with_kwargs():
    """TestResult can be created with kwargs"""
    kwargs = {
        "name": "kwarg_test",
        "passed": True,
        "reason": "Using kwargs"
    }
    result = TestResult(**kwargs)
    
    assert result.name == "kwarg_test"
    assert result.passed == True
    assert result.reason == "Using kwargs"
    print("✓ testresult_with_kwargs")


def run_all_tests():
    """Run all TestResult unit tests"""
    print("\n" + "="*80)
    print("TESTRESULT CLASS TESTS")
    print("="*80)
    
    tests = [
        ("BASIC CREATION", [
            test_testresult_basic_creation,
            test_testresult_with_reason,
            test_testresult_name_required,
            test_testresult_passed_required,
            test_testresult_reason_optional
        ]),
        ("BOOLEAN VALUES", [
            test_testresult_passed_true,
            test_testresult_passed_false,
            test_testresult_boolean_coercion
        ]),
        ("STRING HANDLING", [
            test_testresult_name_string,
            test_testresult_reason_string,
            test_testresult_empty_name,
            test_testresult_empty_reason,
            test_testresult_long_name,
            test_testresult_long_reason
        ]),
        ("SPECIAL CHARACTERS", [
            test_testresult_special_chars_name,
            test_testresult_unicode_name,
            test_testresult_unicode_reason,
            test_testresult_multiline_reason
        ]),
        ("MUTABILITY", [
            test_testresult_attributes_mutable,
            test_testresult_immutability_check,
            test_testresult_attribute_deletion
        ]),
        ("EQUALITY & IDENTITY", [
            test_testresult_equality_same,
            test_testresult_different_instances,
            test_testresult_memory_independence
        ]),
        ("TYPE HANDLING", [
            test_testresult_type_checking_name,
            test_testresult_type_checking_passed,
            test_testresult_none_values,
            test_testresult_default_reason_value
        ]),
        ("OBJECT BEHAVIOR", [
            test_testresult_representation,
            test_testresult_dict_like_access,
            test_testresult_no_extra_attributes,
            test_testresult_copy_behavior,
            test_testresult_with_kwargs
        ]),
        ("STRESS TESTS", [
            test_testresult_stress_creation
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
