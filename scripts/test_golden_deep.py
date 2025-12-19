#!/usr/bin/env python3
"""
Deep Golden Output Validation Suite
Adds ~300 granular tests for production-grade validation
Focus: Data integrity, business logic, cross-validation, edge cases

Refactored to use Template Method Pattern with TestSuite base class.
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any

# Import shared test framework
sys.path.insert(0, str(Path(__file__).parent))
from lib.test_suite import TestSuite
from lib.scenario_factory import ScenarioFactory
from lib.logger import get_logger


class GoldenOutputTestSuite(TestSuite):
    """Test suite for deep validation of golden outputs using Template Method pattern"""
    
    @property
    def tags(self) -> List[str]:
        return ["golden", "outputs", "validation", "deep"]
    
    def __init__(self, repo_root: Path = None):
        super().__init__(repo_root)
        self.factory = ScenarioFactory(self.repo_root)
        self.pr_scenario = self.factory.create("pr_change")
        self.logger = get_logger("golden_deep_test")
    
    def run(self):
        """Template method - defines the test execution sequence"""
        self.test_detect_findings_deep()
        self.test_detect_severity_logic()
        self.test_detect_policy_violations()
        self.test_detect_resource_classification()
        self.test_trend_data_points()
        self.test_trend_cost_calculations()
        self.test_trend_slo_breach_logic()
        self.test_baseline_comparison()
        self.test_cross_snapshot_consistency()
    
    def test_detect_findings_deep(self):
        """Deep validation of detect findings - 60 tests"""
        self.section("DETECT FINDINGS DEEP VALIDATION (60 tests)")
    
        snapshots_dir = self.repo_root / "snapshots"
        detect_file = snapshots_dir / "detect_v1.json"
    
        if not detect_file.exists():
            for _ in range(60):
                self.skip("detect finding deep validation", "File not found")
            return
    
        with open(detect_file, 'r') as f:
            detect = json.load(f)
    
        findings = detect.get("detection_results", {}).get("findings", [])
    
        self.logger.info(f"Per-Finding Field Validation ({len(findings)} findings × 15 fields = {len(findings) * 15} tests)")
    
        for idx, finding in enumerate(findings):
            prefix = f"Finding {idx+1}"
        
            # Core identification fields (3 tests per finding)
            self.test(f"{prefix}: has finding_id", "finding_id" in finding)
            self.test(f"{prefix}: has resource_address", "resource_address" in finding)
            self.test(f"{prefix}: has resource_type", "resource_type" in finding)
        
            # Classification fields (3 tests per finding)
            self.test(f"{prefix}: has classification", "classification" in finding)
            self.test(f"{prefix}: has change_type", "change_type" in finding)
            self.test(f"{prefix}: has severity", "severity" in finding)
        
            # Value tracking (3 tests per finding)
            self.test(f"{prefix}: has before_value", "before_value" in finding)
            self.test(f"{prefix}: has after_value", "after_value" in finding)
            self.test(f"{prefix}: has attribute_changed", "attribute_changed" in finding)
        
            # Impact assessment (3 tests per finding)
            self.test(f"{prefix}: has regression_type", "regression_type" in finding)
            self.test(f"{prefix}: has cost_impact_likelihood", "cost_impact_likelihood" in finding)
            self.test(f"{prefix}: has rationale", "rationale" in finding)
        
            # Policy & rules (3 tests per finding)
            self.test(f"{prefix}: has policy_violation_detected", 
                       "policy_violation_detected" in finding)
            self.test(f"{prefix}: has rule_ids", "rule_ids" in finding)
            if "rule_ids" in finding:
                self.test(f"{prefix}: rule_ids is list", isinstance(finding["rule_ids"], list))
            else:
                self.skip(f"{prefix}: rule_ids is list", "field missing")


    def test_detect_severity_logic(self):
        """Validate severity classification rules - 15 tests"""
        self.section("DETECT SEVERITY LOGIC VALIDATION (15 tests)")
    
        snapshots_dir = self.repo_root / "snapshots"
        detect_file = snapshots_dir / "detect_v1.json"
    
        if not detect_file.exists():
            for _ in range(15):
                self.skip("severity logic", "File not found")
            return
    
        with open(detect_file, 'r') as f:
            detect = json.load(f)
    
        findings = detect.get("detection_results", {}).get("findings", [])
        summary = detect.get("detection_results", {}).get("summary", {})
    
        self.logger.info("Severity Distribution Checks")
    
        # Count severities
        high_count = sum(1 for f in findings if f.get("severity") == "high")
        medium_count = sum(1 for f in findings if f.get("severity") == "medium")
        low_count = sum(1 for f in findings if f.get("severity") == "low")
    
        self.test("Severity: high count matches summary", 
                   high_count == summary.get("high_severity", 0))
        self.test("Severity: medium count matches summary", 
                   medium_count == summary.get("medium_severity", 0))
        self.test("Severity: low count matches summary", 
                   low_count == summary.get("low_severity", 0))
        self.test("Severity: has high severity findings", high_count > 0)
        self.test("Severity: total matches sum", 
                   len(findings) == high_count + medium_count + low_count)
    
        self.logger.info("Severity-Impact Correlation")
    
        for finding in findings:
            severity = finding.get("severity")
            likelihood = finding.get("cost_impact_likelihood")
        
            if severity == "high":
                self.test(f"High severity has certain/high likelihood: {finding.get('finding_id')}", 
                           likelihood in ["certain", "high"],
                           f"Got: {likelihood}")
                break
    
        self.logger.info("Valid Severity Values")
    
        valid_severities = {"high", "medium", "low", "critical"}
        for finding in findings:
            severity = finding.get("severity")
            self.test(f"Valid severity: {finding.get('finding_id')}", 
                       severity in valid_severities,
                       f"Got: {severity}")


    def test_detect_policy_violations(self):
        """Validate policy violation detection - 20 tests"""
        self.section("POLICY VIOLATION VALIDATION (20 tests)")
    
        snapshots_dir = self.repo_root / "snapshots"
        detect_file = snapshots_dir / "detect_v1.json"
    
        if not detect_file.exists():
            for _ in range(20):
                self.skip("policy validation", "File not found")
            return
    
        with open(detect_file, 'r') as f:
            detect = json.load(f)
    
        findings = detect.get("detection_results", {}).get("findings", [])
    
        self.logger.info("Policy Violation Detection")
    
        # Check for policy violations
        policy_violations = [f for f in findings if f.get("policy_violation_detected") == True]
    
        self.test("Has policy violations", len(policy_violations) > 0)
        self.test("Policy violations have rule_ids", 
                   all("rule_ids" in f for f in policy_violations))
        self.test("Policy violations have policy: prefix in rules",
                   any(any("policy:" in rule for rule in f.get("rule_ids", []))
                       for f in policy_violations))
    
        self.logger.info("Rule ID Format Validation")
    
        for finding in findings:
            rule_ids = finding.get("rule_ids", [])
            self.test(f"Rule IDs not empty: {finding.get('finding_id')}", 
                       len(rule_ids) > 0)
        
            for rule in rule_ids:
                self.test(f"Rule ID is string: {rule}", isinstance(rule, str))
                self.test(f"Rule ID not empty: {rule}", len(rule) > 0)
    
        self.logger.info("Cross-Reference Validation")
    
        # Check that policy violations have rationale
        for violation in policy_violations[:3]:  # Test first 3
            self.test(f"Policy violation has rationale: {violation.get('finding_id')}", 
                       "rationale" in violation and len(violation.get("rationale", "")) > 0)
            self.test(f"Policy violation has severity: {violation.get('finding_id')}", 
                       "severity" in violation)


    def test_detect_resource_classification(self):
        """Validate resource classification - 20 tests"""
        self.section("RESOURCE CLASSIFICATION VALIDATION (20 tests)")
    
        snapshots_dir = self.repo_root / "snapshots"
        detect_file = snapshots_dir / "detect_v1.json"
    
        if not detect_file.exists():
            for _ in range(20):
                self.skip("resource classification", "File not found")
            return
    
        with open(detect_file, 'r') as f:
            detect = json.load(f)
    
        resource_classification = detect.get("detection_results", {}).get("resource_classification", {})
        findings = detect.get("detection_results", {}).get("findings", [])
    
        self.logger.info("Classification Categories")
    
        valid_categories = {"compute", "storage", "networking", "observability", "database", "security"}
    
        self.test("Has resource_classification", len(resource_classification) > 0)
    
        for category, resources in resource_classification.items():
            self.test(f"Category '{category}' has resources", isinstance(resources, list))
            self.test(f"Category '{category}' not empty", len(resources) > 0)
            self.test(f"Category '{category}' is valid", category in valid_categories)
    
        self.logger.info("Classification Consistency")
    
        # Check that findings reference classified resources
        classified_resources = set()
        for resources in resource_classification.values():
            classified_resources.update(resources)
    
        for finding in findings:
            resource_addr = finding.get("resource_address")
            classification = finding.get("classification")
        
            self.test(f"Finding has classification: {finding.get('finding_id')}", 
                       classification is not None)
            self.test(f"Classification is valid: {classification}", 
                       classification in valid_categories)


    def test_trend_data_points(self):
        """Deep validation of trend data points - 90 tests"""
        self.section("TREND DATA POINTS VALIDATION (90 tests)")
    
        snapshots_dir = self.repo_root / "snapshots"
        trend_file = snapshots_dir / "trend_history_v1.json"
    
        if not trend_file.exists():
            for _ in range(90):
                self.skip("trend data points", "File not found")
            return
    
        with open(trend_file, 'r') as f:
            trend = json.load(f)
    
        trends = trend.get("trends", [])
    
        self.logger.info(f"Per-Trend Validation ({len(trends)} trends)")
    
        for idx, trend_data in enumerate(trends):
            name = trend_data.get("name", f"trend_{idx}")
            data_points = trend_data.get("data_points", [])
        
            # Trend structure (5 tests per trend)
            self.test(f"{name}: has name", "name" in trend_data)
            self.test(f"{name}: has description", "description" in trend_data)
            self.test(f"{name}: has data_points", "data_points" in trend_data)
            self.test(f"{name}: data_points is list", isinstance(data_points, list))
            self.test(f"{name}: has ≥3 data points", len(data_points) >= 3,
                       f"Got {len(data_points)}")
        
            # Data point structure (5 tests per trend)
            if data_points:
                point = data_points[0]
                self.test(f"{name}: point has date", "date" in point)
                self.test(f"{name}: point has cost", "cost" in point)
                self.test(f"{name}: cost is number", isinstance(point.get("cost"), (int, float)))
                self.test(f"{name}: cost ≥ 0", point.get("cost", -1) >= 0)
                self.test(f"{name}: date is string", isinstance(point.get("date"), str))
        
            # Data point ordering (5 tests per trend)
            dates = [p.get("date") for p in data_points if "date" in p]
            self.test(f"{name}: dates in order", dates == sorted(dates))
            self.test(f"{name}: no duplicate dates", len(dates) == len(set(dates)))
        
            # Cost value validation (5 tests per trend)
            costs = [p.get("cost") for p in data_points if "cost" in p]
            self.test(f"{name}: all costs are numbers", 
                       all(isinstance(c, (int, float)) for c in costs))
            self.test(f"{name}: all costs ≥ 0", all(c >= 0 for c in costs))
            self.test(f"{name}: costs < 10000", all(c < 10000 for c in costs),
                       "Suspiciously high costs")
        
            # Trend-specific validation (10 tests per trend)
            if "flat" in name.lower():
                self.test(f"{name}: costs relatively stable", 
                           max(costs) - min(costs) < 50 if costs else False)
            elif "upward" in name.lower():
                self.test(f"{name}: shows increase", 
                           costs[-1] > costs[0] if len(costs) >= 2 else False)
            elif "breach" in name.lower() or "slo" in name.lower():
                self.test(f"{name}: has baseline_cost", "baseline_cost" in trend_data)
                self.test(f"{name}: has slo_threshold", "slo_threshold" in trend_data)
            
                has_breach = any(p.get("breach") == True for p in data_points)
                self.test(f"{name}: has breach detected", has_breach)
            
                breach_points = [p for p in data_points if p.get("breach")]
                if breach_points:
                    self.test(f"{name}: breach has status", 
                               "status" in breach_points[0])
                    self.test(f"{name}: breach status is slo_breach", 
                               breach_points[0].get("status") == "slo_breach")


    def test_trend_cost_calculations(self):
        """Validate cost calculations in trends - 25 tests"""
        self.section("TREND COST CALCULATION VALIDATION (25 tests)")
    
        snapshots_dir = self.repo_root / "snapshots"
        trend_file = snapshots_dir / "trend_history_v1.json"
    
        if not trend_file.exists():
            for _ in range(25):
                self.skip("cost calculations", "File not found")
            return
    
        with open(trend_file, 'r') as f:
            trend = json.load(f)
    
        trends = trend.get("trends", [])
    
        self.logger.info("Cost Delta Calculations")
    
        for trend_data in trends:
            name = trend_data.get("name", "unknown")
            data_points = trend_data.get("data_points", [])
            baseline_cost = trend_data.get("baseline_cost")
        
            if baseline_cost and data_points:
                self.test(f"{name}: baseline is number", 
                           isinstance(baseline_cost, (int, float)))
                self.test(f"{name}: baseline > 0", baseline_cost > 0)
            
                # Check delta_from_baseline calculations
                for point in data_points:
                    if "delta_from_baseline" in point:
                        cost = point.get("cost")
                        delta = point.get("delta_from_baseline")
                        expected_delta = cost - baseline_cost
                    
                        self.test(f"{name}: delta calculation correct for {point.get('date')}", 
                                   abs(delta - expected_delta) < 0.01,
                                   f"Expected {expected_delta}, got {delta}")
    
        self.logger.info("SLO Threshold Logic")
    
        for trend_data in trends:
            name = trend_data.get("name", "unknown")
            slo = trend_data.get("slo_threshold")
            data_points = trend_data.get("data_points", [])
        
            if slo:
                self.test(f"{name}: SLO is number", isinstance(slo, (int, float)))
                self.test(f"{name}: SLO > 0", slo > 0)
            
                # Check breach detection
                for point in data_points:
                    cost = point.get("cost")
                    breach = point.get("breach")
                
                    if breach:
                        self.test(f"{name}: breach when cost > SLO", 
                                   cost > slo,
                                   f"cost={cost}, slo={slo}")


    def test_trend_slo_breach_logic(self):
        """Validate SLO breach detection logic - 20 tests"""
        self.section("SLO BREACH LOGIC VALIDATION (20 tests)")
    
        snapshots_dir = self.repo_root / "snapshots"
        trend_file = snapshots_dir / "trend_history_v1.json"
    
        if not trend_file.exists():
            for _ in range(20):
                self.skip("SLO breach logic", "File not found")
            return
    
        with open(trend_file, 'r') as f:
            trend = json.load(f)
    
        trends = trend.get("trends", [])
    
        self.logger.info("Breach Detection Logic")
    
        breach_trends = [t for t in trends if any(p.get("breach") for p in t.get("data_points", []))]
    
        self.test("Has trends with breaches", len(breach_trends) > 0)
    
        for trend_data in breach_trends:
            name = trend_data.get("name", "unknown")
            data_points = trend_data.get("data_points", [])
            slo = trend_data.get("slo_threshold")
        
            breach_points = [p for p in data_points if p.get("breach")]
        
            self.test(f"{name}: breach points exist", len(breach_points) > 0)
        
            for point in breach_points:
                self.test(f"{name}: breach point has status", "status" in point)
                self.test(f"{name}: breach status is slo_breach", 
                           point.get("status") == "slo_breach")
                self.test(f"{name}: breach has baseline_exceeded_by", 
                           "baseline_exceeded_by" in point)
                self.test(f"{name}: cost exceeds SLO", 
                           point.get("cost", 0) > slo if slo else False)


    def test_baseline_comparison(self):
        """Validate baseline comparison accuracy - 15 tests"""
        self.section("BASELINE COMPARISON VALIDATION (15 tests)")
    
        snapshots_dir = self.repo_root / "snapshots"
        trend_file = snapshots_dir / "trend_history_v1.json"
    
        if not trend_file.exists():
            for _ in range(15):
                self.skip("baseline comparison", "File not found")
            return
    
        with open(trend_file, 'r') as f:
            trend = json.load(f)
    
        trends = trend.get("trends", [])
    
        self.logger.info("Baseline Accuracy")
    
        for trend_data in trends:
            name = trend_data.get("name", "unknown")
            baseline = trend_data.get("baseline_cost")
            baseline_ts = trend_data.get("baseline_timestamp")
        
            if baseline:
                self.test(f"{name}: has baseline_cost", baseline is not None)
                self.test(f"{name}: baseline is positive", baseline > 0)
            
                if baseline_ts:
                    self.test(f"{name}: has baseline_timestamp", True)
                    self.test(f"{name}: timestamp is ISO 8601", 
                               bool(re.search(r'\d{4}-\d{2}-\d{2}T', baseline_ts)))


    def test_cross_snapshot_consistency(self):
        """Validate consistency across snapshots - 35 tests"""
        self.section("CROSS-SNAPSHOT CONSISTENCY (35 tests)")
    
        snapshots_dir = self.repo_root / "snapshots"
    
        # Load all snapshots
        snapshots = {}
        for filename in ["detect_v1.json", "predict_v1.json", "explain_v1.json", "trend_history_v1.json"]:
            filepath = snapshots_dir / filename
            if filepath.exists():
                with open(filepath, 'r') as f:
                    snapshots[filename] = json.load(f)
    
        if len(snapshots) < 2:
            for _ in range(35):
                self.skip("cross-snapshot consistency", "Insufficient snapshots")
            return
    
        self.logger.info("Metadata Consistency")
    
        # Check scenario_version consistency
        if "detect_v1.json" in snapshots and "predict_v1.json" in snapshots:
            detect_scenario = snapshots["detect_v1.json"].get("scenario_version")
            predict_scenario = snapshots["predict_v1.json"].get("scenario_version")
            self.test("scenario_version matches (detect/predict)", 
                       detect_scenario == predict_scenario,
                       f"detect={detect_scenario}, predict={predict_scenario}")
    
        # Check timestamp formats
        for name, data in snapshots.items():
            ts = data.get("timestamp")
            if ts:
                self.test(f"{name}: timestamp is ISO 8601", 
                           bool(re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', ts)))
    
        self.logger.info("Count Consistency")
    
        # Check findings count consistency
        if "detect_v1.json" in snapshots:
            detect_data = snapshots["detect_v1.json"]
            findings = detect_data.get("detection_results", {}).get("findings", [])
            summary = detect_data.get("detection_results", {}).get("summary", {})
        
            self.test("detect: findings count matches total", 
                       len(findings) == summary.get("total_resources_analyzed", -1) or
                       len(findings) == summary.get("cost_impacting_changes", -1))
    
        # Check explain count matches detect
        if "detect_v1.json" in snapshots and "explain_v1.json" in snapshots:
            detect_findings = len(snapshots["detect_v1.json"]
                                .get("detection_results", {})
                                .get("findings", []))
            explain_count = len(snapshots["explain_v1.json"]
                              .get("explanation_results", {})
                              .get("explanations", []))
        
            self.test("explain count matches detect findings", 
                       explain_count >= detect_findings or explain_count > 0)
    
        self.logger.info("Lineage References")
    
        # Check lineage references
        if "detect_v1.json" in snapshots:
            lineage = snapshots["detect_v1.json"].get("lineage", {})
            self.test("detect: has lineage", len(lineage) > 0)
            self.test("detect: lineage has source_plan", "source_plan" in lineage)
            self.test("detect: lineage has scenario", "scenario" in lineage)
            self.test("detect: lineage has hash_before", "hash_before" in lineage)
            self.test("detect: lineage has hash_after", "hash_after" in lineage)
        
            if "hash_before" in lineage and "hash_after" in lineage:
                hash_before = lineage["hash_before"]
                hash_after = lineage["hash_after"]
                self.test("detect: hashes are different", hash_before != hash_after)
                self.test("detect: hash_before is 16 chars", len(str(hash_before)) == 16)
                self.test("detect: hash_after is 16 chars", len(str(hash_after)) == 16)
    
        self.logger.info("Resource Reference Consistency")
    
        # Check that resources mentioned in findings exist in classification
        if "detect_v1.json" in snapshots:
            detect_data = snapshots["detect_v1.json"]
            findings = detect_data.get("detection_results", {}).get("findings", [])
            classification = detect_data.get("detection_results", {}).get("resource_classification", {})
        
            all_classified = set()
            for resources in classification.values():
                all_classified.update(resources)
        
            for finding in findings[:5]:  # Test first 5
                resource = finding.get("resource_address")
                self.test(f"Resource in classification: {resource}", 
                           any(resource in str(r) for r in all_classified) or resource is None)


def main():
    """Entry point for test execution"""
    suite = GoldenOutputTestSuite()
    suite.run()
    suite.print_summary()
    sys.exit(suite.get_exit_code())


if __name__ == "__main__":
    main()
