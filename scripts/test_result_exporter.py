#!/usr/bin/env python3
"""
Unit tests for Result Exporters
Tests JSON, HTML, Markdown, and JUnit XML exporters
"""

import sys
from pathlib import Path
import json

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.result_exporter import (
    ResultExporter,
    JSONExporter,
    HTMLExporter,
    MarkdownExporter,
    JUnitXMLExporter,
    create_exporter
)


# Sample test data
SAMPLE_RESULTS = [
    {
        "name": "test_suite_1",
        "status": "success",
        "passed": 10,
        "failed": 0,
        "total": 10,
        "pass_rate": 100.0
    },
    {
        "name": "test_suite_2",
        "status": "failed",
        "passed": 8,
        "failed": 2,
        "total": 10,
        "pass_rate": 80.0
    },
    {
        "name": "test_suite_3",
        "status": "error",
        "passed": 0,
        "failed": 0,
        "total": 0,
        "pass_rate": 0.0,
        "error": "Module not found"
    }
]


def test_json_exporter_creates_valid_json():
    """JSON exporter should create valid JSON"""
    exporter = JSONExporter()
    output = exporter.export(SAMPLE_RESULTS)
    
    # Should be valid JSON
    data = json.loads(output)
    assert isinstance(data, dict)
    print("✓ json_exporter_creates_valid_json")


def test_json_exporter_has_summary():
    """JSON exporter should include summary"""
    exporter = JSONExporter()
    output = exporter.export(SAMPLE_RESULTS)
    data = json.loads(output)
    
    assert "summary" in data
    assert "suites" in data
    print("✓ json_exporter_has_summary")


def test_json_exporter_summary_fields():
    """JSON summary should have all required fields"""
    exporter = JSONExporter()
    output = exporter.export(SAMPLE_RESULTS)
    data = json.loads(output)
    summary = data["summary"]
    
    assert "total_suites" in summary
    assert "passed_suites" in summary
    assert "failed_suites" in summary
    assert "total_tests" in summary
    assert "passed_tests" in summary
    assert "failed_tests" in summary
    assert "timestamp" in summary
    print("✓ json_exporter_summary_fields")


def test_json_exporter_suite_structure():
    """JSON suites should have correct structure"""
    exporter = JSONExporter()
    output = exporter.export(SAMPLE_RESULTS)
    data = json.loads(output)
    
    assert len(data["suites"]) == 3
    suite = data["suites"][0]
    assert "name" in suite
    assert "status" in suite
    assert "passed" in suite
    assert "failed" in suite
    assert "reason" in suite
    print("✓ json_exporter_suite_structure")


def test_html_exporter_creates_valid_html():
    """HTML exporter should create valid HTML"""
    exporter = HTMLExporter()
    output = exporter.export(SAMPLE_RESULTS)
    
    assert output.startswith("<!DOCTYPE html>")
    assert "<html>" in output
    assert "</html>" in output
    assert "<head>" in output
    assert "<body>" in output
    print("✓ html_exporter_creates_valid_html")


def test_html_exporter_has_title():
    """HTML should have title"""
    exporter = HTMLExporter()
    output = exporter.export(SAMPLE_RESULTS)
    
    assert "<title>CostPilot Test Results</title>" in output
    print("✓ html_exporter_has_title")


def test_html_exporter_has_styles():
    """HTML should include CSS styles"""
    exporter = HTMLExporter()
    output = exporter.export(SAMPLE_RESULTS)
    
    assert "<style>" in output
    assert ".summary" in output
    assert ".suite" in output
    assert ".pass" in output
    assert ".fail" in output
    print("✓ html_exporter_has_styles")


def test_html_exporter_color_coded():
    """HTML should have color-coded pass/fail"""
    exporter = HTMLExporter()
    output = exporter.export(SAMPLE_RESULTS)
    
    assert "success" in output
    assert "failed" in output
    assert "error" in output
    print("✓ html_exporter_color_coded")


def test_html_exporter_expandable_details():
    """HTML should have expandable details"""
    exporter = HTMLExporter()
    output = exporter.export(SAMPLE_RESULTS)
    
    assert "toggleDetails" in output
    assert "suite-details" in output
    print("✓ html_exporter_expandable_details")


def test_markdown_exporter_creates_markdown():
    """Markdown exporter should create Markdown"""
    exporter = MarkdownExporter()
    output = exporter.export(SAMPLE_RESULTS)
    
    assert output.startswith("#")
    assert "##" in output
    print("✓ markdown_exporter_creates_markdown")


def test_markdown_exporter_has_title():
    """Markdown should have title"""
    exporter = MarkdownExporter()
    output = exporter.export(SAMPLE_RESULTS)
    
    assert "# 🧪 CostPilot Test Results" in output
    print("✓ markdown_exporter_has_title")


def test_markdown_exporter_has_checkboxes():
    """Markdown should have checkboxes for pass/fail"""
    exporter = MarkdownExporter()
    output = exporter.export(SAMPLE_RESULTS)
    
    assert "[x]" in output  # Passed
    assert "[ ]" in output  # Failed
    print("✓ markdown_exporter_has_checkboxes")


def test_markdown_exporter_has_links():
    """Markdown should have links to source files"""
    exporter = MarkdownExporter()
    output = exporter.export(SAMPLE_RESULTS)
    
    assert "[View Source]" in output
    assert ".py)" in output
    print("✓ markdown_exporter_has_links")


def test_junit_xml_exporter_creates_valid_xml():
    """JUnit XML exporter should create valid XML"""
    exporter = JUnitXMLExporter()
    output = exporter.export(SAMPLE_RESULTS)
    
    assert output.startswith('<?xml version="1.0"')
    assert "<testsuites" in output
    assert "</testsuites>" in output
    print("✓ junit_xml_exporter_creates_valid_xml")


def test_junit_xml_exporter_has_test_suites():
    """JUnit XML should have testsuite elements"""
    exporter = JUnitXMLExporter()
    output = exporter.export(SAMPLE_RESULTS)
    
    # Count only opening testsuite tags (not testsuites)
    assert "<testsuite " in output or '<testsuite>' in output
    assert "</testsuite>" in output
    # Count opening tags only (not testsuites plural)
    count = output.count("<testsuite ") + output.count("<testsuite>")
    assert count == 3, f"Expected 3 testsuite elements, got {count}"
    print("✓ junit_xml_exporter_has_test_suites")


def test_junit_xml_exporter_has_test_cases():
    """JUnit XML should have testcase elements"""
    exporter = JUnitXMLExporter()
    output = exporter.export(SAMPLE_RESULTS)
    
    assert "<testcase" in output
    print("✓ junit_xml_exporter_has_test_cases")


def test_junit_xml_exporter_has_failures():
    """JUnit XML should have failure elements"""
    exporter = JUnitXMLExporter()
    output = exporter.export(SAMPLE_RESULTS)
    
    assert "<failure" in output
    print("✓ junit_xml_exporter_has_failures")


def test_junit_xml_exporter_has_errors():
    """JUnit XML should have error elements"""
    exporter = JUnitXMLExporter()
    output = exporter.export(SAMPLE_RESULTS)
    
    assert "<error" in output
    print("✓ junit_xml_exporter_has_errors")


def test_create_exporter_json():
    """create_exporter should create JSONExporter"""
    exporter = create_exporter("json")
    assert isinstance(exporter, JSONExporter)
    print("✓ create_exporter_json")


def test_create_exporter_html():
    """create_exporter should create HTMLExporter"""
    exporter = create_exporter("html")
    assert isinstance(exporter, HTMLExporter)
    print("✓ create_exporter_html")


def test_create_exporter_markdown():
    """create_exporter should create MarkdownExporter"""
    exporter = create_exporter("markdown")
    assert isinstance(exporter, MarkdownExporter)
    print("✓ create_exporter_markdown")


def test_create_exporter_junit():
    """create_exporter should create JUnitXMLExporter"""
    exporter = create_exporter("junit")
    assert isinstance(exporter, JUnitXMLExporter)
    print("✓ create_exporter_junit")


def test_create_exporter_invalid():
    """create_exporter should raise ValueError for invalid format"""
    try:
        create_exporter("invalid")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Unknown format" in str(e)
    print("✓ create_exporter_invalid")


def test_json_write_to_file(tmp_path="/tmp"):
    """JSON exporter should write to file"""
    exporter = JSONExporter()
    output_path = f"{tmp_path}/test_results.json"
    exporter.export(SAMPLE_RESULTS, output_path)
    
    assert Path(output_path).exists()
    content = Path(output_path).read_text()
    data = json.loads(content)
    assert "summary" in data
    print("✓ json_write_to_file")


def test_html_write_to_file(tmp_path="/tmp"):
    """HTML exporter should write to file"""
    exporter = HTMLExporter()
    output_path = f"{tmp_path}/test_results.html"
    exporter.export(SAMPLE_RESULTS, output_path)
    
    assert Path(output_path).exists()
    content = Path(output_path).read_text()
    assert "<!DOCTYPE html>" in content
    print("✓ html_write_to_file")


def test_markdown_write_to_file(tmp_path="/tmp"):
    """Markdown exporter should write to file"""
    exporter = MarkdownExporter()
    output_path = f"{tmp_path}/test_results.md"
    exporter.export(SAMPLE_RESULTS, output_path)
    
    assert Path(output_path).exists()
    content = Path(output_path).read_text()
    assert "# 🧪 CostPilot Test Results" in content
    print("✓ markdown_write_to_file")


def test_junit_write_to_file(tmp_path="/tmp"):
    """JUnit XML exporter should write to file"""
    exporter = JUnitXMLExporter()
    output_path = f"{tmp_path}/test_results.xml"
    exporter.export(SAMPLE_RESULTS, output_path)
    
    assert Path(output_path).exists()
    content = Path(output_path).read_text()
    assert '<?xml version="1.0"' in content
    print("✓ junit_write_to_file")


def run_all_tests():
    """Run all exporter tests"""
    print("\n" + "="*80)
    print("RESULT EXPORTER TESTS")
    print("="*80)
    
    tests = [
        # JSON tests
        ("JSON EXPORTER", [
            test_json_exporter_creates_valid_json,
            test_json_exporter_has_summary,
            test_json_exporter_summary_fields,
            test_json_exporter_suite_structure,
            test_json_write_to_file
        ]),
        # HTML tests
        ("HTML EXPORTER", [
            test_html_exporter_creates_valid_html,
            test_html_exporter_has_title,
            test_html_exporter_has_styles,
            test_html_exporter_color_coded,
            test_html_exporter_expandable_details,
            test_html_write_to_file
        ]),
        # Markdown tests
        ("MARKDOWN EXPORTER", [
            test_markdown_exporter_creates_markdown,
            test_markdown_exporter_has_title,
            test_markdown_exporter_has_checkboxes,
            test_markdown_exporter_has_links,
            test_markdown_write_to_file
        ]),
        # JUnit XML tests
        ("JUNIT XML EXPORTER", [
            test_junit_xml_exporter_creates_valid_xml,
            test_junit_xml_exporter_has_test_suites,
            test_junit_xml_exporter_has_test_cases,
            test_junit_xml_exporter_has_failures,
            test_junit_xml_exporter_has_errors,
            test_junit_write_to_file
        ]),
        # Factory tests
        ("FACTORY FUNCTION", [
            test_create_exporter_json,
            test_create_exporter_html,
            test_create_exporter_markdown,
            test_create_exporter_junit,
            test_create_exporter_invalid
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
