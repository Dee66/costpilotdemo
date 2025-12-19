#!/usr/bin/env python3
"""
Unified Test Runner CLI
Single entry point for running all test suites with filtering and formatting options
"""

import argparse
import sys
import json
import time
import multiprocessing as mp
from pathlib import Path
from typing import List, Optional, Dict
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Import test framework
sys.path.insert(0, str(Path(__file__).parent))
from lib.test_suite import TestSuite


def discover_test_suites(test_dir: Path = None) -> List[Path]:
    """
    Auto-discover test suite files
    
    Args:
        test_dir: Directory to search for test files (default: scripts/)
        
    Returns:
        List of test file paths
    """
    if test_dir is None:
        test_dir = Path(__file__).parent
    
    # Find all test_*.py files except test_comprehensive.py
    test_files = []
    for test_file in test_dir.glob("test_*.py"):
        if test_file.name != "test_comprehensive.py" and test_file.name != __file__:
            test_files.append(test_file)
    
    return sorted(test_files)


def load_suite_module(test_file: Path):
    """
    Dynamically load a test suite module
    
    Args:
        test_file: Path to test file
        
    Returns:
        Loaded module
    """
    import importlib.util
    
    spec = importlib.util.spec_from_file_location(test_file.stem, test_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    return module


def run_suite(test_file: Path, verbose: bool = False) -> dict:
    """
    Run a single test suite
    
    Args:
        test_file: Path to test file
        verbose: Enable verbose output
        
    Returns:
        Dictionary with suite results
    """
    try:
        module = load_suite_module(test_file)
        
        # Find TestSuite subclass in module
        suite_class = None
        for name in dir(module):
            obj = getattr(module, name)
            if (isinstance(obj, type) and 
                issubclass(obj, TestSuite) and 
                obj is not TestSuite):
                suite_class = obj
                break
        
        if suite_class is None:
            return {
                "name": test_file.stem,
                "status": "error",
                "error": "No TestSuite subclass found",
                "passed": 0,
                "failed": 0,
                "total": 0
            }
        
        # Run the suite
        suite = suite_class()
        suite.run()
        summary = suite.get_summary()
        
        if not verbose:
            # Only show summary in non-verbose mode
            suite.print_summary()
        
        return {
            "name": test_file.stem,
            "status": "success" if summary["failed"] == 0 else "failed",
            "passed": summary["passed"],
            "failed": summary["failed"],
            "total": summary["total"],
            "pass_rate": summary["pass_rate"]
        }
        
    except Exception as e:
        return {
            "name": test_file.stem,
            "status": "error",
            "error": str(e),
            "passed": 0,
            "failed": 0,
            "total": 0
        }


def run_suites_sequential(test_files: List[Path], args) -> List[dict]:
    """
    Run test suites sequentially
    
    Args:
        test_files: List of test file paths
        args: Parsed command-line arguments
        
    Returns:
        List of test results
    """
    results = []
    total = len(test_files)
    
    for idx, test_file in enumerate(test_files, 1):
        if args.format == "terminal":
            if args.progress:
                print(f"\n[{idx}/{total}] ", end="", flush=True)
            print(f"\n{'='*80}")
            print(f"Running: {test_file.stem}")
            print(f"{'='*80}")
        
        result = run_suite(test_file, verbose=args.verbose)
        results.append(result)
    
    return results


def run_suite_wrapper(test_file_path: str, verbose: bool) -> dict:
    """
    Wrapper for running suite in multiprocessing (must be picklable)
    
    Args:
        test_file_path: String path to test file
        verbose: Verbose flag
        
    Returns:
        Test result dictionary
    """
    return run_suite(Path(test_file_path), verbose=verbose)


def run_suites_parallel(test_files: List[Path], args) -> List[dict]:
    """
    Run test suites in parallel using multiprocessing
    
    Args:
        test_files: List of test file paths
        args: Parsed command-line arguments
        
    Returns:
        List of test results
    """
    n_workers = min(args.parallel, len(test_files), mp.cpu_count())
    
    if args.format == "terminal":
        print(f"Running {len(test_files)} suites with {n_workers} workers...\n")
    
    # Convert Path objects to strings for pickling
    test_file_strs = [str(f) for f in test_files]
    
    # Create pool and run tests
    with mp.Pool(processes=n_workers) as pool:
        # Use starmap to pass multiple arguments
        tasks = [(path, args.verbose) for path in test_file_strs]
        results = pool.starmap(run_suite_wrapper, tasks)
    
    return results


class TestFileChangeHandler(FileSystemEventHandler):
    """Handler for file system events in watch mode"""
    
    def __init__(self, callback):
        self.callback = callback
        self.last_run = 0
        self.debounce_seconds = 1.0
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Only watch .py and .tf files
        if not (event.src_path.endswith('.py') or event.src_path.endswith('.tf')):
            return
        
        # Debounce rapid file changes
        current_time = time.time()
        if current_time - self.last_run < self.debounce_seconds:
            return
        
        self.last_run = current_time
        self.callback()


def run_watch_mode(args) -> int:
    """
    Run tests in watch mode - rerun when files change
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code
    """
    repo_root = Path(__file__).parent.parent
    scripts_dir = Path(__file__).parent
    
    print("="*80)
    print("WATCH MODE - Monitoring for file changes")
    print("="*80)
    print(f"Watching: {repo_root}")
    print("Press Ctrl+C to exit\n")
    
    def run_tests():
        print(f"\n{time.strftime('%H:%M:%S')} - Change detected, running tests...\n")
        
        # Discover and filter test files
        test_files = discover_test_suites()
        if args.suite:
            test_files = [f for f in test_files if f.stem == args.suite]
        
        # Run tests
        if args.parallel and args.parallel > 1:
            results = run_suites_parallel(test_files, args)
        else:
            results = run_suites_sequential(test_files, args)
        
        # Print summary
        passed = sum(1 for r in results if r["status"] == "success")
        total = len(results)
        
        print(f"\n{'='*80}")
        print(f"Watch run complete: {passed}/{total} suites passed")
        print(f"{'='*80}\n")
        print("Waiting for changes...")
    
    # Initial run
    run_tests()
    
    # Set up file watcher
    event_handler = TestFileChangeHandler(run_tests)
    observer = Observer()
    observer.schedule(event_handler, str(repo_root), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n\nWatch mode stopped")
    
    observer.join()
    return 0


def print_overall_summary(results: List[dict], print_summary: bool = True):
    """
    Print summary of all test suite runs
    
    Args:
        results: List of suite result dictionaries
        print_summary: Whether to print (False when using other formats)
    """
    if not print_summary:
        return
    
    print("\n" + "="*80)
    print("OVERALL SUMMARY")
    print("="*80)
    
    total_passed = sum(r.get("passed", 0) for r in results)
    total_failed = sum(r.get("failed", 0) for r in results)
    total_tests = sum(r.get("total", 0) for r in results)
    
    suites_passed = sum(1 for r in results if r["status"] == "success")
    suites_failed = sum(1 for r in results if r["status"] == "failed")
    suites_error = sum(1 for r in results if r["status"] == "error")
    
    print(f"Test Suites: {len(results)}")
    print(f"  Passed: {suites_passed}")
    print(f"  Failed: {suites_failed}")
    print(f"  Errors: {suites_error}")
    print()
    print(f"Total Tests: {total_tests}")
    print(f"  Passed: {total_passed}")
    print(f"  Failed: {total_failed}")
    
    if total_tests > 0:
        pass_rate = (total_passed / total_tests) * 100
        print(f"Pass Rate: {pass_rate:.1f}%")
    
    print()
    
    # List failed suites
    failed_suites = [r for r in results if r["status"] != "success"]
    if failed_suites:
        print("Failed/Error Suites:")
        for result in failed_suites:
            status_icon = "❌" if result["status"] == "failed" else "⚠️"
            if result["status"] == "error":
                print(f"  {status_icon} {result['name']}: {result.get('error', 'Unknown error')}")
            else:
                print(f"  {status_icon} {result['name']}: {result['failed']} failures")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Unified test runner for CostPilot demo test suites",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all test suites
  python3 scripts/run_tests.py
  
  # Run specific suite
  python3 scripts/run_tests.py --suite test_golden_deep
  
  # Run suites with specific tag
  python3 scripts/run_tests.py --tag validation
  
  # Run with verbose output
  python3 scripts/run_tests.py --verbose
  
  # List available suites
  python3 scripts/run_tests.py --list
  
  # Output as JSON
  python3 scripts/run_tests.py --format json
  
  # Write results to file
  python3 scripts/run_tests.py --output results.txt
        """
    )
    
    parser.add_argument(
        "--suite",
        help="Run specific test suite (e.g., test_golden_deep)"
    )
    
    parser.add_argument(
        "--tag",
        help="Run test suites with specific tag (e.g., golden, infrastructure, validation)"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available test suites and exit"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output (show all test results)"
    )
    
    parser.add_argument(
        "--failed-only",
        action="store_true",
        help="Only show failed tests (hide passing tests)"
    )
    
    parser.add_argument(
        "--parallel", "-j",
        type=int,
        metavar="N",
        help="Run N test suites in parallel (default: 1)"
    )
    
    parser.add_argument(
        "--watch", "-w",
        action="store_true",
        help="Watch mode: rerun tests when files change"
    )
    
    parser.add_argument(
        "--progress",
        action="store_true",
        help="Show progress bar for long-running tests"
    )
    
    parser.add_argument(
        "--format",
        choices=["terminal", "json", "html", "markdown", "junit"],
        default="terminal",
        help="Output format (default: terminal)"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Write output to file instead of stdout"
    )
    
    args = parser.parse_args()
    
    # Watch mode
    if args.watch:
        return run_watch_mode(args)
    
    # Discover test suites
    test_files = discover_test_suites()
    
    if args.list:
        print("Available test suites:")
        for test_file in test_files:
            print(f"  - {test_file.stem}")
        return 0
    
    # Filter by suite name if specified
    if args.suite:
        test_files = [f for f in test_files if f.stem == args.suite]
        if not test_files:
            print(f"Error: Test suite '{args.suite}' not found")
            return 1
    
    # Filter by tag if specified
    if args.tag:
        filtered_files = []
        for test_file in test_files:
            try:
                module = load_suite_module(test_file)
                # Get the test suite class (assuming it's the only class in the module)
                suite_class = None
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and 
                        issubclass(attr, TestSuite) and 
                        attr != TestSuite):
                        suite_class = attr
                        break
                
                if suite_class and hasattr(suite_class, 'tags'):
                    if args.tag in suite_class.tags:
                        filtered_files.append(test_file)
            except Exception as e:
                print(f"Warning: Could not load {test_file.stem} for tag filtering: {e}")
        
        if not filtered_files:
            print(f"Error: No test suites found with tag '{args.tag}'")
            return 1
        test_files = filtered_files
    
    if args.format == "terminal":
        print(f"Running {len(test_files)} test suite(s)...\n")
    
    # Run test suites (parallel or sequential)
    if args.parallel and args.parallel > 1:
        results = run_suites_parallel(test_files, args)
    else:
        results = run_suites_sequential(test_files, args)
    
    # Format and output results
    output = format_results(results, args.format)
    
    if args.output:
        # Write to file
        with open(args.output, 'w') as f:
            f.write(output)
        if args.format == "terminal":
            print(f"\nResults written to {args.output}")
    else:
        # Print to stdout
        print(output)
    
    # Exit with appropriate code
    all_passed = all(r["status"] == "success" for r in results)
    return 0 if all_passed else 1


def format_results(results: List[dict], format_type: str) -> str:
    """
    Format test results in specified format
    
    Args:
        results: List of test suite results
        format_type: Output format (terminal, json, html, markdown, junit)
        
    Returns:
        Formatted output string
    """
    # Use result exporters from lib if available
    if format_type in ["json", "html", "markdown", "junit"]:
        try:
            from lib.result_exporter import create_exporter
            exporter = create_exporter(format_type)
            return exporter.export(results)
        except ImportError:
            # Fallback to built-in formatters
            pass
    
    if format_type == "json":
        return format_json(results)
    elif format_type == "html":
        return format_html(results)
    elif format_type == "markdown":
        return format_markdown(results)
    elif format_type == "junit":
        return format_junit(results)
    else:  # terminal
        return format_terminal(results)


def format_markdown(results: List[dict]) -> str:
    """Format results as Markdown (fallback if lib not available)"""
    lines = ["# Test Results", "", "## Suites", ""]
    for r in results:
        status = "✅" if r["status"] == "success" else "❌"
        lines.append(f"- {status} {r.get('name', 'unknown')}: {r.get('passed', 0)}/{r.get('total', 0)} passed")
    return "\n".join(lines)


def format_junit(results: List[dict]) -> str:
    """Format results as JUnit XML (fallback if lib not available)"""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<testsuites>']
    for r in results:
        name = r.get('name', 'unknown')
        total = r.get('total', 0)
        failed = r.get('failed', 0)
        lines.append(f'  <testsuite name="{name}" tests="{total}" failures="{failed}"/>')
    lines.append('</testsuites>')
    return "\n".join(lines)


def format_json(results: List[dict]) -> str:
    """Format results as JSON"""
    output = {
        "total_suites": len(results),
        "passed_suites": sum(1 for r in results if r["status"] == "success"),
        "failed_suites": sum(1 for r in results if r["status"] == "failed"),
        "suites": results
    }
    return json.dumps(output, indent=2)


def format_html(results: List[dict]) -> str:
    """Format results as HTML"""
    total_passed = sum(1 for r in results if r["status"] == "success")
    total_failed = len(results) - total_passed
    
    html = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "<title>CostPilot Test Results</title>",
        "<style>",
        "body { font-family: Arial, sans-serif; margin: 20px; }",
        ".summary { background: #f0f0f0; padding: 15px; margin: 20px 0; border-radius: 5px; }",
        ".suite { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }",
        ".success { border-left: 5px solid #4caf50; }",
        ".failed { border-left: 5px solid #f44336; }",
        ".pass { color: #4caf50; font-weight: bold; }",
        ".fail { color: #f44336; font-weight: bold; }",
        "</style>",
        "</head>",
        "<body>",
        "<h1>CostPilot Test Results</h1>",
        f"<div class='summary'>",
        f"<h2>Summary</h2>",
        f"<p>Total Suites: {len(results)}</p>",
        f"<p class='pass'>Passed: {total_passed}</p>",
        f"<p class='fail'>Failed: {total_failed}</p>",
        f"</div>",
    ]
    
    for result in results:
        status_class = "success" if result["status"] == "success" else "failed"
        html.append(f"<div class='suite {status_class}'>")
        html.append(f"<h3>{result.get('name', result.get('suite', 'Unknown'))}</h3>")
        html.append(f"<p>Status: <span class='{result['status']}'>{result['status']}</span></p>")
        html.append(f"<p>Tests: {result.get('passed', 0)} passed, {result.get('failed', 0)} failed</p>")
        html.append("</div>")
    
    html.extend(["</body>", "</html>"])
    return "\n".join(html)


def format_terminal(results: List[dict]) -> str:
    """Format results for terminal output"""
    lines = []
    for r in results:
        lines.append(f"\n{'='*80}")
        lines.append(f"Suite: {r.get('name', r.get('suite', 'unknown'))}")
        lines.append(f"{'='*80}")
        lines.append(f"Status: {r['status']}")
        if 'passed' in r and 'failed' in r:
            lines.append(f"Passed: {r['passed']}, Failed: {r['failed']}")
    
    # Overall summary
    lines.append(f"\n{'='*80}")
    lines.append("OVERALL SUMMARY")
    lines.append(f"{'='*80}")
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "success")
    failed = total - passed
    lines.append(f"Total Suites: {total}")
    lines.append(f"  Passed: {passed}")
    lines.append(f"  Failed: {failed}")
    
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
