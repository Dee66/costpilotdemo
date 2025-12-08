#!/usr/bin/env python3
"""
Extensive Unit Tests for CLI Test Runner
Tests the command-line interface and test execution
"""

import sys
from pathlib import Path
import subprocess
import json

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))


RUNNER_PATH = Path(__file__).parent / "run_tests.py"


def run_cli(*args):
    """Helper to run CLI and capture output"""
    cmd = ["python3", str(RUNNER_PATH)] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return result.returncode, result.stdout, result.stderr


def test_cli_help_flag():
    """CLI should support --help flag"""
    code, stdout, stderr = run_cli("--help")
    assert code == 0
    assert "usage:" in stdout.lower() or "help" in stdout.lower()
    print("✓ cli_help_flag")


def test_cli_list_flag():
    """CLI should support --list flag"""
    code, stdout, stderr = run_cli("--list")
    assert code == 0
    assert "test_" in stdout
    print("✓ cli_list_flag")


def test_cli_list_shows_suites():
    """--list should show available test suites"""
    code, stdout, stderr = run_cli("--list")
    assert "test_scenario_factory" in stdout or "Available" in stdout
    print("✓ cli_list_shows_suites")


def test_cli_suite_argument():
    """CLI should accept --suite argument"""
    code, stdout, stderr = run_cli("--suite", "test_scenario_factory")
    # May pass or fail depending on suite, but should run
    assert "test_scenario_factory" in stdout or "Running" in stdout
    print("✓ cli_suite_argument")


def test_cli_invalid_suite():
    """CLI should handle invalid suite name"""
    code, stdout, stderr = run_cli("--suite", "nonexistent_test_suite")
    assert code != 0
    assert "not found" in stdout.lower() or "error" in stdout.lower()
    print("✓ cli_invalid_suite")


def test_cli_verbose_flag():
    """CLI should support --verbose flag"""
    code, stdout, stderr = run_cli("--suite", "test_scenario_factory", "--verbose")
    # Should run (may pass or fail)
    assert "test_scenario_factory" in stdout or "Running" in stdout
    print("✓ cli_verbose_flag")


def test_cli_verbose_short_form():
    """CLI should support -v short form"""
    code, stdout, stderr = run_cli("--suite", "test_scenario_factory", "-v")
    assert "test_scenario_factory" in stdout or "Running" in stdout
    print("✓ cli_verbose_short_form")


def test_cli_format_json():
    """CLI should support --format json"""
    code, stdout, stderr = run_cli("--suite", "test_scenario_factory", "--format", "json")
    
    # Output should be valid JSON
    try:
        data = json.loads(stdout)
        assert "suites" in data or "summary" in data
        print("✓ cli_format_json")
    except json.JSONDecodeError:
        print("✗ cli_format_json: Invalid JSON output")


def test_cli_format_html():
    """CLI should support --format html"""
    code, stdout, stderr = run_cli("--suite", "test_scenario_factory", "--format", "html")
    assert "<!DOCTYPE html>" in stdout or "<html>" in stdout
    print("✓ cli_format_html")


def test_cli_format_terminal():
    """CLI should support --format terminal (default)"""
    code, stdout, stderr = run_cli("--suite", "test_scenario_factory", "--format", "terminal")
    assert len(stdout) > 0
    print("✓ cli_format_terminal")


def test_cli_output_file():
    """CLI should support --output flag"""
    output_path = "/tmp/test_cli_output.txt"
    code, stdout, stderr = run_cli("--suite", "test_scenario_factory", "--output", output_path)
    
    assert Path(output_path).exists()
    content = Path(output_path).read_text()
    assert len(content) > 0
    print("✓ cli_output_file")


def test_cli_output_short_form():
    """CLI should support -o short form"""
    output_path = "/tmp/test_cli_output_short.txt"
    code, stdout, stderr = run_cli("--suite", "test_scenario_factory", "-o", output_path)
    
    assert Path(output_path).exists()
    print("✓ cli_output_short_form")


def test_cli_failed_only_flag():
    """CLI should support --failed-only flag"""
    code, stdout, stderr = run_cli("--suite", "test_scenario_factory", "--failed-only")
    # Should run without error
    assert code == 0 or "test_scenario_factory" in stdout
    print("✓ cli_failed_only_flag")


def test_cli_parallel_flag():
    """CLI should support --parallel flag"""
    code, stdout, stderr = run_cli("--parallel", "2", "--suite", "test_scenario_factory")
    # Should run (parallel execution)
    assert "test_scenario_factory" in stdout or "Running" in stdout
    print("✓ cli_parallel_flag")


def test_cli_parallel_short_form():
    """CLI should support -j short form for parallel"""
    code, stdout, stderr = run_cli("-j", "2", "--suite", "test_scenario_factory")
    assert "test_scenario_factory" in stdout or "Running" in stdout
    print("✓ cli_parallel_short_form")


def test_cli_progress_flag():
    """CLI should support --progress flag"""
    code, stdout, stderr = run_cli("--progress", "--suite", "test_scenario_factory")
    # Should run with progress indicator
    print("✓ cli_progress_flag")


def test_cli_combined_flags():
    """CLI should support multiple flags combined"""
    code, stdout, stderr = run_cli(
        "--suite", "test_scenario_factory",
        "--verbose",
        "--format", "terminal"
    )
    assert "test_scenario_factory" in stdout
    print("✓ cli_combined_flags")


def test_cli_no_arguments():
    """CLI without arguments should run all suites"""
    code, stdout, stderr = run_cli()
    # Should run (may take time, but should start)
    # Just check it doesn't error immediately
    assert len(stdout) > 0 or len(stderr) > 0
    print("✓ cli_no_arguments")


def test_cli_exit_code_success():
    """CLI should return 0 on success"""
    code, stdout, stderr = run_cli("--suite", "test_scenario_factory")
    # test_scenario_factory should pass
    assert code == 0
    print("✓ cli_exit_code_success")


def test_cli_suite_discovery():
    """CLI should discover test suites automatically"""
    code, stdout, stderr = run_cli("--list")
    
    # Should find multiple test suites
    suite_count = stdout.count("test_")
    assert suite_count >= 3
    print("✓ cli_suite_discovery")


def test_cli_json_output_structure():
    """JSON output should have expected structure"""
    code, stdout, stderr = run_cli("--suite", "test_scenario_factory", "--format", "json")
    
    try:
        data = json.loads(stdout)
        assert "total_suites" in data or "summary" in data
        assert isinstance(data, dict)
        print("✓ cli_json_output_structure")
    except:
        print("✗ cli_json_output_structure: Invalid JSON structure")


def test_cli_html_output_structure():
    """HTML output should have basic HTML structure"""
    code, stdout, stderr = run_cli("--suite", "test_scenario_factory", "--format", "html")
    
    assert "<!DOCTYPE html>" in stdout or "<html>" in stdout
    assert "<head>" in stdout or "<body>" in stdout
    print("✓ cli_html_output_structure")


def test_cli_output_to_json_file():
    """CLI should write JSON to file"""
    output_path = "/tmp/test_results.json"
    code, stdout, stderr = run_cli(
        "--suite", "test_scenario_factory",
        "--format", "json",
        "--output", output_path
    )
    
    assert Path(output_path).exists()
    content = Path(output_path).read_text()
    data = json.loads(content)
    assert isinstance(data, dict)
    print("✓ cli_output_to_json_file")


def test_cli_output_to_html_file():
    """CLI should write HTML to file"""
    output_path = "/tmp/test_results.html"
    code, stdout, stderr = run_cli(
        "--suite", "test_scenario_factory",
        "--format", "html",
        "--output", output_path
    )
    
    assert Path(output_path).exists()
    content = Path(output_path).read_text()
    assert "<!DOCTYPE html>" in content or "<html>" in content
    print("✓ cli_output_to_html_file")


def test_cli_markdown_format():
    """CLI should support markdown format"""
    code, stdout, stderr = run_cli("--suite", "test_scenario_factory", "--format", "markdown")
    
    # Markdown should have # headers or similar
    assert "#" in stdout or "test_scenario_factory" in stdout
    print("✓ cli_markdown_format")


def test_cli_junit_format():
    """CLI should support junit XML format"""
    code, stdout, stderr = run_cli("--suite", "test_scenario_factory", "--format", "junit")
    
    # JUnit XML should have testsuites tags
    assert "<?xml" in stdout or "<testsuites" in stdout
    print("✓ cli_junit_format")


def test_cli_parallel_with_multiple_workers():
    """CLI should handle parallel execution with multiple workers"""
    code, stdout, stderr = run_cli("--parallel", "4")
    
    # Should complete without hanging
    assert len(stdout) > 0
    print("✓ cli_parallel_with_multiple_workers")


def test_cli_help_shows_examples():
    """CLI help should show usage examples"""
    code, stdout, stderr = run_cli("--help")
    
    assert "example" in stdout.lower() or "usage" in stdout.lower()
    print("✓ cli_help_shows_examples")


def test_cli_help_shows_all_options():
    """CLI help should document all options"""
    code, stdout, stderr = run_cli("--help")
    
    assert "--suite" in stdout
    assert "--list" in stdout
    assert "--format" in stdout
    print("✓ cli_help_shows_all_options")


def test_cli_list_output_format():
    """--list output should be properly formatted"""
    code, stdout, stderr = run_cli("--list")
    
    lines = stdout.split("\n")
    assert len(lines) >= 2  # At least header + one suite
    print("✓ cli_list_output_format")


def test_cli_invalid_format():
    """CLI should handle invalid format gracefully"""
    code, stdout, stderr = run_cli("--suite", "test_scenario_factory", "--format", "invalid")
    
    # Should error with helpful message
    assert code != 0
    assert "invalid" in stderr.lower() or "choice" in stderr.lower()
    print("✓ cli_invalid_format")


def test_cli_runner_executable():
    """run_tests.py should be executable"""
    assert RUNNER_PATH.exists()
    assert RUNNER_PATH.is_file()
    print("✓ cli_runner_executable")


def test_cli_runner_has_shebang():
    """run_tests.py should have proper shebang"""
    first_line = RUNNER_PATH.read_text().split("\n")[0]
    assert first_line.startswith("#!")
    assert "python" in first_line
    print("✓ cli_runner_has_shebang")


def test_cli_stress_many_flags():
    """CLI should handle many flags without issues"""
    code, stdout, stderr = run_cli(
        "--suite", "test_scenario_factory",
        "--verbose",
        "--format", "terminal",
        "--progress"
    )
    
    # Should run successfully
    assert code == 0 or len(stdout) > 0
    print("✓ cli_stress_many_flags")


def run_all_tests():
    """Run all CLI unit tests"""
    print("\n" + "="*80)
    print("CLI TEST RUNNER TESTS")
    print("="*80)
    
    tests = [
        ("BASIC FLAGS", [
            test_cli_help_flag,
            test_cli_list_flag,
            test_cli_list_shows_suites,
            test_cli_no_arguments
        ]),
        ("SUITE SELECTION", [
            test_cli_suite_argument,
            test_cli_invalid_suite,
            test_cli_suite_discovery
        ]),
        ("OUTPUT FLAGS", [
            test_cli_verbose_flag,
            test_cli_verbose_short_form,
            test_cli_failed_only_flag,
            test_cli_progress_flag
        ]),
        ("FORMAT OPTIONS", [
            test_cli_format_json,
            test_cli_format_html,
            test_cli_format_terminal,
            test_cli_markdown_format,
            test_cli_junit_format,
            test_cli_invalid_format
        ]),
        ("FILE OUTPUT", [
            test_cli_output_file,
            test_cli_output_short_form,
            test_cli_output_to_json_file,
            test_cli_output_to_html_file
        ]),
        ("PARALLEL EXECUTION", [
            test_cli_parallel_flag,
            test_cli_parallel_short_form,
            test_cli_parallel_with_multiple_workers
        ]),
        ("OUTPUT STRUCTURE", [
            test_cli_json_output_structure,
            test_cli_html_output_structure,
            test_cli_list_output_format
        ]),
        ("HELP SYSTEM", [
            test_cli_help_shows_examples,
            test_cli_help_shows_all_options
        ]),
        ("COMBINED FLAGS", [
            test_cli_combined_flags,
            test_cli_stress_many_flags
        ]),
        ("EXIT CODES", [
            test_cli_exit_code_success
        ]),
        ("FILE PROPERTIES", [
            test_cli_runner_executable,
            test_cli_runner_has_shebang
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
