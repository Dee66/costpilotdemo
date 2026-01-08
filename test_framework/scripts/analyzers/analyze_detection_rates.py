#!/usr/bin/env python3
# test_framework/scripts/analyzers/analyze_detection_rates.py

import json
import os
from pathlib import Path
from collections import defaultdict

class TestAnalyzer:
    def __init__(self, results_dir="test_results"):
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def analyze_results(self, test_output_files):
        """Analyze CostPilot detection results across test suites"""
        summary = {
            "total_tests": 0,
            "total_detections": 0,
            "by_category": defaultdict(lambda: {"tests": 0, "detections": 0}),
            "detection_rate": 0.0
        }

        for output_file in test_output_files:
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    results = json.load(f)

                for category, category_results in results.get("by_category", {}).items():
                    summary["by_category"][category]["tests"] += category_results["tests"]
                    summary["by_category"][category]["detections"] += category_results["detections"]

                summary["total_tests"] += results.get("total_tests", 0)
                summary["total_detections"] += results.get("total_detections", 0)

        if summary["total_tests"] > 0:
            summary["detection_rate"] = summary["total_detections"] / summary["total_tests"]

        return summary

    def generate_report(self, summary):
        """Generate comprehensive analysis report"""
        report = f"""# CostPilot Test Framework Analysis Report

## Executive Summary
- **Total Tests Run**: {summary['total_tests']}
- **Total Detections**: {summary['total_detections']}
- **Overall Detection Rate**: {summary['detection_rate']:.1%}

## Category Breakdown

| Category | Tests | Detections | Detection Rate |
|----------|-------|------------|----------------|
"""

        for category, stats in summary["by_category"].items():
            rate = stats["detections"] / stats["tests"] if stats["tests"] > 0 else 0
            report += f"| {category} | {stats['tests']} | {stats['detections']} | {rate:.1%} |\n"

        report += "\n## Recommendations\n\n"

        for category, stats in summary["by_category"].items():
            rate = stats["detections"] / stats["tests"] if stats["tests"] > 0 else 0
            if rate < 0.8:
                report += f"- **{category}**: Detection rate ({rate:.1%}) below target. Requires optimization improvements.\n"

        return report

if __name__ == "__main__":
    analyzer = TestAnalyzer()

    # Find all test result files
    result_files = list(Path("test_results").glob("*_results.json"))

    summary = analyzer.analyze_results(result_files)
    report = analyzer.generate_report(summary)

    with open("test_results/comprehensive_analysis.md", 'w') as f:
        f.write(report)

    print("✅ Analysis report generated: test_results/comprehensive_analysis.md")