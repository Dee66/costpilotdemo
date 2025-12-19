#!/usr/bin/env python3
"""
Regression Test Suite
Adds ~250 granular tests for regression detection and edge case validation
Focus: Cost regressions, optimization removal, policy violations, edge cases, cross-file consistency


Refactored to use Template Method Pattern with TestSuite base class.
"""

import os
import re
import json
import sys
from pathlib import Path

# Import shared test framework
sys.path.insert(0, str(Path(__file__).parent))
from lib.test_suite import TestSuite
from typing import Dict, List, Any


def read_file(filepath: Path) -> str:
    """Read a file"""
    if not filepath.exists():
        return ""
    with open(filepath, 'r') as f:
        return f.read()


def read_json(filepath: Path) -> Dict[str, Any]:
    """Read JSON file"""
    if not filepath.exists():
        return {}
    with open(filepath, 'r') as f:
        return json.load(f)


class RegressionsTestSuite(TestSuite):
    """Test suite using Template Method pattern"""
    
    @property
    def tags(self) -> List[str]:
        return ["regressions", "edge-cases", "validation"]
    
    def run(self):
        """Template method - defines the test execution sequence"""
        self.test_ec2_instance_type_regression()
        self.test_ebs_volume_regression()
        self.test_s3_lifecycle_removal()
        self.test_cloudwatch_retention_regression()
        self.test_cost_prediction_accuracy()
        self.test_explain_root_cause_analysis()
        self.test_noop_scenario_handling()
        self.test_cross_file_consistency()
    
    def test_ec2_instance_type_regression(self):
        """Test EC2 instance type cost regressions - 30 tests"""
        self.section("EC2 INSTANCE TYPE REGRESSIONS (30 tests)")
    
        baseline_tf = self.repo_root / "infrastructure" / "terraform" / "baseline" / "main.tf"
        pr_tf = self.repo_root / "infrastructure" / "terraform" / "pr-change" / "main.tf"
        detect_json = self.repo_root / "snapshots" / "detect_v1.json"
    
        print("\n🖥️  Baseline Instance Type")
    
        if baseline_tf.exists():
            baseline_content = read_file(baseline_tf)
        
            self.test("baseline: uses t3.micro", "t3.micro" in baseline_content)
            self.test("baseline: does NOT use t3.large", "t3.large" not in baseline_content)
            self.test("baseline: does NOT use t3.xlarge", "t3.xlarge" not in baseline_content)
            self.test("baseline: does NOT use t3.2xlarge", "t3.2xlarge" not in baseline_content)
            self.test("baseline: instance_type defined", "instance_type" in baseline_content)
        
            # Count t3.micro occurrences
            micro_count = baseline_content.count("t3.micro")
            self.test("baseline: t3.micro appears in launch template",
                       micro_count >= 1,
                       f"Found {micro_count} occurrences")
        else:
            for _ in range(6):
                self.skip("baseline validation", "File not found")
    
        print("\n⚠️  PR Change Instance Type")
    
        if pr_tf.exists():
            pr_content = read_file(pr_tf)
        
            self.test("PR: uses t3.xlarge", "t3.xlarge" in pr_content)
            self.test("PR: does NOT use t3.micro", "t3.micro" not in pr_content)
            self.test("PR: instance type changed", 
                       "t3.xlarge" in pr_content and "t3.micro" not in pr_content)
        
            # Verify launch template contains the regression
            self.test("PR: launch template has t3.xlarge",
                       "aws_launch_template" in pr_content and "t3.xlarge" in pr_content)
        else:
            for _ in range(4):
                self.skip("PR validation", "File not found")
    
        print("\n🔍 Detection Output")
    
        if detect_json.exists():
            detect_data = read_json(detect_json)
            findings = detect_data.get("detection_results", {}).get("findings", [])
        
            # Find instance type finding
            instance_finding = None
            for finding in findings:
                if "instance_type" in finding.get("attribute_changed", ""):
                    instance_finding = finding
                    break
        
            self.test("detect: found instance_type change", instance_finding is not None)
        
            if instance_finding:
                self.test("detect: before_value is t3.micro",
                           instance_finding.get("before_value") == "t3.micro")
                self.test("detect: after_value is t3.xlarge",
                           instance_finding.get("after_value") == "t3.xlarge")
                self.test("detect: severity is high",
                           instance_finding.get("severity") == "high")
                self.test("detect: policy violation flagged",
                           instance_finding.get("policy_violation_detected") == True)
                self.test("detect: has policy:default-ec2-type rule",
                           "policy:default-ec2-type" in instance_finding.get("rule_ids", []))
                self.test("detect: cost_impact_likelihood is certain",
                           instance_finding.get("cost_impact_likelihood") == "certain")
                self.test("detect: resource_type is aws_launch_template",
                           instance_finding.get("resource_type") == "aws_launch_template")
                self.test("detect: classification is compute",
                           instance_finding.get("classification") == "compute")
        else:
            for _ in range(10):
                self.skip("detection validation", "File not found")


    def test_ebs_volume_regression(self):
        """Test EBS volume size regressions - 25 tests"""
        self.section("EBS VOLUME SIZE REGRESSIONS (25 tests)")
    
        baseline_tf = self.repo_root / "infrastructure" / "terraform" / "baseline" / "main.tf"
        pr_tf = self.repo_root / "infrastructure" / "terraform" / "pr-change" / "main.tf"
        detect_json = self.repo_root / "snapshots" / "detect_v1.json"
    
        print("\n💾 Baseline Volume Size")
    
        if baseline_tf.exists():
            baseline_content = read_file(baseline_tf)
        
            # Check for 20GB volume
            self.test("baseline: uses 20GB volume", 
                       "volume_size" in baseline_content and 
                       re.search(r'volume_size\s*=\s*20', baseline_content) is not None)
            self.test("baseline: does NOT use 200GB", 
                       "200" not in re.findall(r'volume_size\s*=\s*(\d+)', baseline_content))
            self.test("baseline: volume_type is gp3",
                       "gp3" in baseline_content)
            self.test("baseline: has EBS encryption",
                       "encrypted" in baseline_content and 
                       re.search(r'encrypted\s*=\s*true', baseline_content) is not None)
        else:
            for _ in range(4):
                self.skip("baseline validation", "File not found")
    
        print("\n⚠️  PR Change Volume Size")
    
        if pr_tf.exists():
            pr_content = read_file(pr_tf)
        
            # Check for 200GB volume
            self.test("PR: uses 200GB volume",
                       re.search(r'volume_size\s*=\s*200', pr_content) is not None)
            self.test("PR: does NOT use 20GB",
                       "20" not in [m for m in re.findall(r'volume_size\s*=\s*(\d+)', pr_content)])
            self.test("PR: 10x volume increase detected",
                       "200" in pr_content and "volume_size" in pr_content)
            self.test("PR: still uses gp3 type",
                       "gp3" in pr_content)
        else:
            for _ in range(4):
                self.skip("PR validation", "File not found")
    
        print("\n🔍 Detection Output")
    
        if detect_json.exists():
            detect_data = read_json(detect_json)
            findings = detect_data.get("detection_results", {}).get("findings", [])
        
            # Find EBS finding
            ebs_finding = None
            for finding in findings:
                if "volume_size" in finding.get("attribute_changed", ""):
                    ebs_finding = finding
                    break
        
            self.test("detect: found volume_size change", ebs_finding is not None)
        
            if ebs_finding:
                self.test("detect: before_value is 20", ebs_finding.get("before_value") == 20)
                self.test("detect: after_value is 200", ebs_finding.get("after_value") == 200)
                self.test("detect: severity is medium", ebs_finding.get("severity") == "medium")
                self.test("detect: classification is storage",
                           ebs_finding.get("classification") == "storage")
                self.test("detect: has ebs-volume-size-increase rule",
                           "ebs-volume-size-increase" in ebs_finding.get("rule_ids", []))
                self.test("detect: resource_type is aws_launch_template",
                           ebs_finding.get("resource_type") == "aws_launch_template")
        else:
            for _ in range(7):
                self.skip("detection validation", "File not found")


    def test_s3_lifecycle_removal(self):
        """Test S3 lifecycle policy removal - 30 tests"""
        self.section("S3 LIFECYCLE REMOVAL REGRESSIONS (30 tests)")
    
        baseline_tf = self.repo_root / "infrastructure" / "terraform" / "baseline" / "main.tf"
        pr_tf = self.repo_root / "infrastructure" / "terraform" / "pr-change" / "main.tf"
        detect_json = self.repo_root / "snapshots" / "detect_v1.json"
    
        print("\n🗄️  Baseline S3 Lifecycle")
    
        if baseline_tf.exists():
            baseline_content = read_file(baseline_tf)
        
            self.test("baseline: has lifecycle_configuration",
                       "aws_s3_bucket_lifecycle_configuration" in baseline_content)
            self.test("baseline: has lifecycle rule",
                       "rule {" in baseline_content or "rule =" in baseline_content)
            self.test("baseline: has GLACIER transition",
                       "GLACIER" in baseline_content)
            self.test("baseline: has GLACIER_IR transition",
                       "GLACIER_IR" in baseline_content)
            self.test("baseline: has expiration",
                       "expiration" in baseline_content)
            self.test("baseline: has 365-day expiration",
                       "365" in baseline_content)
            self.test("baseline: has transition days (90)",
                       "90" in baseline_content)
            self.test("baseline: has transition days (180)",
                       "180" in baseline_content)
            self.test("baseline: has incomplete upload cleanup",
                       "abort_incomplete_multipart_upload" in baseline_content)
            self.test("baseline: has noncurrent version expiration",
                       "noncurrent_version_expiration" in baseline_content)
        else:
            for _ in range(10):
                self.skip("baseline validation", "File not found")
    
        print("\n⚠️  PR Change S3 Lifecycle")
    
        if pr_tf.exists():
            pr_content = read_file(pr_tf)
        
            self.test("PR: lifecycle_configuration removed",
                       "aws_s3_bucket_lifecycle_configuration" not in pr_content)
            self.test("PR: no GLACIER transitions",
                       "GLACIER" not in pr_content)
            self.test("PR: no expiration rules",
                       "expiration {" not in pr_content and "expiration =" not in pr_content)
            self.test("PR: no cleanup rules",
                       "abort_incomplete_multipart_upload" not in pr_content)
            self.test("PR: S3 bucket still exists",
                       "aws_s3_bucket" in pr_content)
        else:
            for _ in range(5):
                self.skip("PR validation", "File not found")
    
        print("\n🔍 Detection Output")
    
        if detect_json.exists():
            detect_data = read_json(detect_json)
            findings = detect_data.get("detection_results", {}).get("findings", [])
        
            # Find S3 lifecycle finding
            s3_finding = None
            for finding in findings:
                if "lifecycle" in finding.get("attribute_changed", "").lower():
                    s3_finding = finding
                    break
        
            self.test("detect: found lifecycle change", s3_finding is not None)
        
            if s3_finding:
                self.test("detect: severity is medium", s3_finding.get("severity") == "medium")
                self.test("detect: classification is storage",
                           s3_finding.get("classification") == "storage")
                self.test("detect: has s3-lifecycle rule",
                           any("s3" in rule.lower() for rule in s3_finding.get("rule_ids", [])))
        else:
            for _ in range(4):
                self.skip("detection validation", "File not found")


    def test_cloudwatch_retention_regression(self):
        """Test CloudWatch log retention regressions - 25 tests"""
        self.section("CLOUDWATCH RETENTION REGRESSIONS (25 tests)")
    
        baseline_tf = self.repo_root / "infrastructure" / "terraform" / "baseline" / "main.tf"
        pr_tf = self.repo_root / "infrastructure" / "terraform" / "pr-change" / "main.tf"
        detect_json = self.repo_root / "snapshots" / "detect_v1.json"
    
        print("\n📊 Baseline CloudWatch")
    
        if baseline_tf.exists():
            baseline_content = read_file(baseline_tf)
        
            self.test("baseline: has cloudwatch_log_group",
                       "aws_cloudwatch_log_group" in baseline_content)
            self.test("baseline: has retention_in_days",
                       "retention_in_days" in baseline_content)
            self.test("baseline: retention is 30 days",
                       re.search(r'retention_in_days\s*=\s*30', baseline_content) is not None)
            self.test("baseline: retention is NOT 0",
                       re.search(r'retention_in_days\s*=\s*0', baseline_content) is None)
            self.test("baseline: has log group name",
                       "/aws/" in baseline_content or "log_group" in baseline_content)
        else:
            for _ in range(5):
                self.skip("baseline validation", "File not found")
    
        print("\n⚠️  PR Change CloudWatch")
    
        if pr_tf.exists():
            pr_content = read_file(pr_tf)
        
            self.test("PR: retention changed to 0 (infinite)",
                       re.search(r'retention_in_days\s*=\s*0', pr_content) is not None)
            self.test("PR: retention is NOT 30",
                       re.search(r'retention_in_days\s*=\s*30', pr_content) is None)
            self.test("PR: infinite retention regression",
                       "retention_in_days" in pr_content and "= 0" in pr_content)
            self.test("PR: cloudwatch_log_group still exists",
                       "aws_cloudwatch_log_group" in pr_content)
        else:
            for _ in range(4):
                self.skip("PR validation", "File not found")
    
        print("\n🔍 Detection Output")
    
        if detect_json.exists():
            detect_data = read_json(detect_json)
            findings = detect_data.get("detection_results", {}).get("findings", [])
        
            # Find CloudWatch finding
            cw_finding = None
            for finding in findings:
                if "retention" in finding.get("attribute_changed", "").lower():
                    cw_finding = finding
                    break
        
            self.test("detect: found retention change", cw_finding is not None)
        
            if cw_finding:
                self.test("detect: before_value is 30", cw_finding.get("before_value") == 30)
                self.test("detect: after_value is 0", cw_finding.get("after_value") == 0)
                self.test("detect: severity is medium", cw_finding.get("severity") == "medium")
                self.test("detect: classification is observability",
                           cw_finding.get("classification") == "observability")
                self.test("detect: has cloudwatch rule",
                           any("cloudwatch" in rule.lower() for rule in cw_finding.get("rule_ids", [])))
        else:
            for _ in range(6):
                self.skip("detection validation", "File not found")


    def test_cost_prediction_accuracy(self):
        """Test cost prediction calculations - 30 tests"""
        self.section("COST PREDICTION ACCURACY (30 tests)")
    
        predict_json = self.repo_root / "snapshots" / "predict_v1.json"
    
        if not predict_json.exists():
            for _ in range(30):
                self.skip("prediction validation", "predict_v1.json not found")
            return
    
        predict_data = read_json(predict_json)
    
        print("\n💰 Baseline Costs")
    
        baseline_costs = predict_data.get("cost_prediction", {}).get("baseline_monthly_costs", {})
    
        self.test("prediction: has baseline_monthly_costs", len(baseline_costs) > 0)
        self.test("prediction: baseline EC2 cost exists", "ec2" in baseline_costs)
        self.test("prediction: baseline EBS cost exists", "ebs" in baseline_costs)
        self.test("prediction: baseline S3 cost exists", "s3" in baseline_costs)
        self.test("prediction: baseline CloudWatch cost exists", 
                   "cloudwatch" in baseline_costs)
    
        if "ec2" in baseline_costs:
            ec2_cost = baseline_costs["ec2"]
            self.test("baseline EC2: cost is reasonable", 
                       0 < ec2_cost < 100,
                       f"Cost: ${ec2_cost}")
            self.test("baseline EC2: reflects t3.micro pricing",
                       ec2_cost < 20)
    
        print("\n📈 PR Costs")
    
        pr_costs = predict_data.get("cost_prediction", {}).get("pr_monthly_costs", {})
    
        self.test("prediction: has pr_monthly_costs", len(pr_costs) > 0)
        self.test("prediction: PR EC2 cost exists", "ec2" in pr_costs)
        self.test("prediction: PR EBS cost exists", "ebs" in pr_costs)
        self.test("prediction: PR S3 cost exists", "s3" in pr_costs)
    
        if "ec2" in pr_costs:
            pr_ec2_cost = pr_costs["ec2"]
            self.test("PR EC2: cost increased significantly",
                       pr_ec2_cost > baseline_costs.get("ec2", 0) * 10)
            self.test("PR EC2: reflects t3.xlarge pricing",
                       pr_ec2_cost > 100)
    
        print("\n📊 Cost Deltas")
    
        summary = predict_data.get("cost_prediction", {}).get("summary", {})
    
        self.test("prediction: has summary", len(summary) > 0)
        self.test("prediction: has baseline_total", "baseline_monthly_total" in summary)
        self.test("prediction: has pr_total", "pr_monthly_total" in summary)
        self.test("prediction: has delta", "monthly_delta" in summary)
        self.test("prediction: has percentage_increase", "percentage_increase" in summary)
    
        if "baseline_monthly_total" in summary and "pr_monthly_total" in summary:
            baseline_total = summary["baseline_monthly_total"]
            pr_total = summary["pr_monthly_total"]
        
            self.test("prediction: baseline total is reasonable",
                       40 < baseline_total < 100,
                       f"${baseline_total}")
            self.test("prediction: PR total is higher",
                       pr_total > baseline_total)
            self.test("prediction: significant increase",
                       pr_total > baseline_total * 5)
    
        if "monthly_delta" in summary:
            delta = summary["monthly_delta"]
            self.test("prediction: delta is positive", delta > 0)
            self.test("prediction: delta is substantial",
                       delta > 200,
                       f"${delta}")
    
        if "percentage_increase" in summary:
            pct = summary["percentage_increase"]
            self.test("prediction: percentage > 100%", pct > 100)
            self.test("prediction: percentage is reasonable",
                       100 < pct < 2000,
                       f"{pct}%")


    def test_explain_root_cause_analysis(self):
        """Test explanation quality - 25 tests"""
        self.section("ROOT CAUSE ANALYSIS QUALITY (25 tests)")
    
        explain_json = self.repo_root / "snapshots" / "explain_v1.json"
    
        if not explain_json.exists():
            for _ in range(25):
                self.skip("explanation validation", "explain_v1.json not found")
            return
    
        explain_data = read_json(explain_json)
    
        print("\n💡 Root Cause Analysis")
    
        explanations = explain_data.get("explanations", [])
    
        self.test("explain: has explanations", len(explanations) > 0,
                   f"Found {len(explanations)} explanations")
        self.test("explain: has multiple explanations", len(explanations) >= 3)
    
        for idx, explanation in enumerate(explanations[:3], 1):
            print(f"\n🔍 Explanation {idx}")
        
            self.test(f"explain[{idx}]: has finding_id", "finding_id" in explanation)
            self.test(f"explain[{idx}]: has root_cause", "root_cause" in explanation)
            self.test(f"explain[{idx}]: has severity_justification",
                       "severity_justification" in explanation)
            self.test(f"explain[{idx}]: has heuristic_provenance",
                       "heuristic_provenance" in explanation)
        
            if "root_cause" in explanation:
                root_cause = explanation["root_cause"]
                self.test(f"explain[{idx}]: root cause not empty",
                           len(root_cause) > 10)
                self.test(f"explain[{idx}]: root cause is descriptive",
                           len(root_cause) > 50)


    def test_noop_scenario_handling(self):
        """Test noop scenario produces no findings - 20 tests"""
        self.section("NOOP SCENARIO VALIDATION (20 tests)")
    
        noop_tf = self.repo_root / "infrastructure" / "terraform" / "noop-change" / "main.tf"
        baseline_tf = self.repo_root / "infrastructure" / "terraform" / "baseline" / "main.tf"
    
        print("\n🔄 Noop Change Validation")
    
        if not noop_tf.exists() or not baseline_tf.exists():
            for _ in range(20):
                self.skip("noop validation", "Files not found")
            return
    
        noop_content = read_file(noop_tf)
        baseline_content = read_file(baseline_tf)
    
        # Check that noop is cosmetically different but functionally identical
        self.test("noop: file exists", len(noop_content) > 0)
        self.test("noop: similar size to baseline",
                   0.8 * len(baseline_content) < len(noop_content) < 1.2 * len(baseline_content))
    
        # Check key resources are same
        self.test("noop: uses same instance type as baseline",
                   ("t3.micro" in noop_content) == ("t3.micro" in baseline_content))
        self.test("noop: uses same volume size",
                   re.search(r'volume_size\s*=\s*20', noop_content) is not None)
        self.test("noop: has lifecycle configuration",
                   "aws_s3_bucket_lifecycle_configuration" in noop_content)
        self.test("noop: has 30-day retention",
                   re.search(r'retention_in_days\s*=\s*30', noop_content) is not None)
    
        # Check for cosmetic differences (comments, whitespace)
        baseline_lines = baseline_content.count('\n')
        noop_lines = noop_content.count('\n')
        self.test("noop: different line count (cosmetic changes)",
                   abs(baseline_lines - noop_lines) > 0,
                   f"Baseline: {baseline_lines}, Noop: {noop_lines}")
    
        # Verify functional equivalence
        self.test("noop: has same VPC structure",
                   noop_content.count("aws_vpc") == baseline_content.count("aws_vpc"))
        self.test("noop: has same EC2 resources",
                   noop_content.count("aws_launch_template") == baseline_content.count("aws_launch_template"))
        self.test("noop: has same S3 resources",
                   noop_content.count("aws_s3_bucket") == baseline_content.count("aws_s3_bucket"))
        self.test("noop: has same CloudWatch resources",
                   noop_content.count("aws_cloudwatch") == baseline_content.count("aws_cloudwatch"))


    def test_cross_file_consistency(self):
        """Test consistency across files - 30 tests"""
        self.section("CROSS-FILE CONSISTENCY (30 tests)")
    
        detect_json = self.repo_root / "snapshots" / "detect_v1.json"
        predict_json = self.repo_root / "snapshots" / "predict_v1.json"
        explain_json = self.repo_root / "snapshots" / "explain_v1.json"
    
        if not all([detect_json.exists(), predict_json.exists(), explain_json.exists()]):
            for _ in range(30):
                self.skip("cross-file validation", "Files not found")
            return
    
        detect_data = read_json(detect_json)
        predict_data = read_json(predict_json)
        explain_data = read_json(explain_json)
    
        print("\n🔗 Finding Count Consistency")
    
        detect_findings = detect_data.get("detection_results", {}).get("findings", [])
        explain_explanations = explain_data.get("explanations", [])
    
        self.test("consistency: detect has findings", len(detect_findings) > 0)
        self.test("consistency: explain has explanations", len(explain_explanations) > 0)
        self.test("consistency: finding counts match",
                   len(detect_findings) == len(explain_explanations),
                   f"Detect: {len(detect_findings)}, Explain: {len(explain_explanations)}")
    
        print("\n🆔 Finding ID Alignment")
    
        detect_ids = [f.get("finding_id") for f in detect_findings]
        explain_ids = [e.get("finding_id") for e in explain_explanations]
    
        self.test("consistency: all detect findings have IDs",
                   all(fid for fid in detect_ids))
        self.test("consistency: all explain entries have IDs",
                   all(fid for fid in explain_ids))
        self.test("consistency: IDs are unique in detect",
                   len(detect_ids) == len(set(detect_ids)))
        self.test("consistency: finding IDs match across files",
                   set(detect_ids) == set(explain_ids))
    
        print("\n📅 Timestamp Consistency")
    
        detect_timestamp = detect_data.get("timestamp", "")
        predict_timestamp = predict_data.get("timestamp", "")
        explain_timestamp = explain_data.get("timestamp", "")
    
        self.test("consistency: detect has timestamp", len(detect_timestamp) > 0)
        self.test("consistency: predict has timestamp", len(predict_timestamp) > 0)
        self.test("consistency: explain has timestamp", len(explain_timestamp) > 0)
        self.test("consistency: timestamps match",
                   detect_timestamp == predict_timestamp == explain_timestamp)
    
        print("\n🎯 Scenario Version Consistency")
    
        detect_version = detect_data.get("scenario_version", "")
        predict_version = predict_data.get("scenario_version", "")
        explain_version = explain_data.get("scenario_version", "")
    
        self.test("consistency: detect has scenario_version", len(detect_version) > 0)
        self.test("consistency: predict has scenario_version", len(predict_version) > 0)
        self.test("consistency: explain has scenario_version", len(explain_version) > 0)
        self.test("consistency: scenario versions match",
                   detect_version == predict_version == explain_version)
    
        print("\n🔍 Resource Reference Consistency")
    
        # Check that resources in detect appear in predict
        detect_resources = [f.get("resource_address") for f in detect_findings]
    
        self.test("consistency: detect has resource addresses",
                   all(res for res in detect_resources))
        self.test("consistency: resource addresses well-formed",
                   all(res.startswith("aws_") for res in detect_resources if res))


def main():
    """Entry point for test execution"""
    suite = RegressionsTestSuite()
    suite.run()
    suite.print_summary()
    sys.exit(suite.get_exit_code())


if __name__ == "__main__":
    main()
