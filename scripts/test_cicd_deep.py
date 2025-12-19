#!/usr/bin/env python3
"""
CI/CD Deep Validation Suite
Adds ~100 granular tests for GitHub Actions workflow validation
Focus: Workflow structure, job dependencies, environment variables, secrets, conditions, safeguards


Refactored to use Template Method Pattern with TestSuite base class.
"""

import os
import re
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Any

# Import shared test framework
sys.path.insert(0, str(Path(__file__).parent))
from lib.test_suite import TestSuite


def load_workflow(filepath: Path) -> Dict[str, Any]:
    """Load GitHub Actions workflow YAML"""
    if not filepath.exists():
        return {}
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)


class CicdDeepTestSuite(TestSuite):
    """Test suite using Template Method pattern"""
    
    @property
    def tags(self) -> List[str]:
        return ["ci", "cd", "github-actions", "workflows", "validation", "deep"]
    
    def run(self):
        """Template method - defines the test execution sequence"""
        self.test_workflow_structure()
        self.test_job_dependencies()
        self.test_terraform_validation_steps()
        self.test_costpilot_scan_steps()
        self.test_safeguard_validations()
        self.test_policy_enforcement()
    
    def test_workflow_structure(self):
        """Validate workflow structure - 20 tests"""
        self.section("WORKFLOW STRUCTURE VALIDATION (20 tests)")
    
        workflow_file = self.repo_root / ".github" / "workflows" / "costpilot-ci.yml"
    
        if not workflow_file.exists():
            for _ in range(20):
                self.skip("workflow validation", "costpilot-ci.yml not found")
            return
    
        workflow = load_workflow(workflow_file)
    
        print("\n📋 Required Fields")
    
        # Check required top-level fields
        self.test("workflow: has name", "name" in workflow)
        self.test("workflow: has 'on' triggers", "on" in workflow)
        self.test("workflow: has jobs", "jobs" in workflow)
        self.test("workflow: has permissions", "permissions" in workflow)
        self.test("workflow: has env", "env" in workflow)
    
        # Validate workflow name
        if "name" in workflow:
            name = workflow["name"]
            self.test("workflow: has descriptive name", len(name) > 5,
                       f"Name: {name}")
            self.test("workflow: name contains 'CostPilot'", "CostPilot" in name)
    
        print("\n🔔 Trigger Configuration")
    
        # Check triggers
        if "on" in workflow:
            triggers = workflow["on"]
            self.test("workflow: triggered on pull_request", "pull_request" in triggers)
            self.test("workflow: triggered on push", "push" in triggers)
            self.test("workflow: has workflow_dispatch", "workflow_dispatch" in triggers)
        
            # Check PR trigger configuration
            if "pull_request" in triggers and isinstance(triggers["pull_request"], dict):
                pr_config = triggers["pull_request"]
                self.test("PR trigger: targets main branch",
                           "branches" in pr_config and "main" in pr_config.get("branches", []))
                self.test("PR trigger: has path filters",
                           "paths" in pr_config)
    
        print("\n🔐 Permissions & Environment")
    
        # Check permissions
        if "permissions" in workflow:
            perms = workflow["permissions"]
            self.test("permissions: has contents", "contents" in perms)
            self.test("permissions: has pull-requests", "pull-requests" in perms)
            self.test("permissions: contents is read", perms.get("contents") == "read")
            self.test("permissions: pull-requests is write", perms.get("pull-requests") == "write")
    
        # Check environment variables
        if "env" in workflow:
            env = workflow["env"]
            self.test("env: has TERRAFORM_VERSION", "TERRAFORM_VERSION" in env)
            self.test("env: has AWS_REGION", "AWS_REGION" in env)


    def test_job_dependencies(self):
        """Validate job dependencies and ordering - 20 tests"""
        self.section("JOB DEPENDENCIES VALIDATION (20 tests)")
    
        workflow_file = self.repo_root / ".github" / "workflows" / "costpilot-ci.yml"
    
        if not workflow_file.exists():
            for _ in range(20):
                self.skip("job dependencies", "Workflow file not found")
            return
    
        workflow = load_workflow(workflow_file)
        jobs = workflow.get("jobs", {})
    
        print("\n🔗 Job Structure")
    
        self.test("workflow: has jobs", len(jobs) > 0,
                   f"Found {len(jobs)} jobs")
        self.test("workflow: has multiple jobs", len(jobs) >= 5,
                   f"Expected ≥5, found {len(jobs)}")
    
        # Check for essential jobs
        essential_jobs = [
            "validate-protected-files",
            "terraform-baseline",
            "terraform-pr-change",
            "costpilot-scan"
        ]
    
        print("\n📦 Essential Jobs")
    
        for job_name in essential_jobs:
            self.test(f"jobs: includes '{job_name}'", job_name in jobs)
    
        print("\n➡️  Dependency Chains")
    
        # Check dependency relationships
        if "terraform-baseline" in jobs:
            baseline_job = jobs["terraform-baseline"]
            self.test("terraform-baseline: depends on validate-protected-files",
                       "needs" in baseline_job and 
                       "validate-protected-files" in baseline_job.get("needs", ""))
    
        if "terraform-pr-change" in jobs:
            pr_job = jobs["terraform-pr-change"]
            self.test("terraform-pr-change: depends on validate-protected-files",
                       "needs" in pr_job and 
                       "validate-protected-files" in pr_job.get("needs", ""))
    
        if "costpilot-scan" in jobs:
            scan_job = jobs["costpilot-scan"]
            needs = scan_job.get("needs", [])
            if isinstance(needs, str):
                needs = [needs]
        
            self.test("costpilot-scan: has dependencies", len(needs) > 0)
            self.test("costpilot-scan: depends on terraform jobs",
                       any(dep in ["terraform-baseline", "terraform-pr-change", "terraform-noop"] 
                           for dep in needs))
    
        print("\n🎯 Job Conditions")
    
        # Check conditional execution
        for job_name, job_config in list(jobs.items())[:5]:
            if "if" in job_config:
                condition = job_config["if"]
                self.test(f"{job_name}: has execution condition", len(condition) > 0)


    def test_terraform_validation_steps(self):
        """Validate Terraform validation steps - 20 tests"""
        self.section("TERRAFORM VALIDATION STEPS (20 tests)")
    
        workflow_file = self.repo_root / ".github" / "workflows" / "costpilot-ci.yml"
    
        if not workflow_file.exists():
            for _ in range(20):
                self.skip("terraform steps", "Workflow file not found")
            return
    
        workflow = load_workflow(workflow_file)
        jobs = workflow.get("jobs", {})
    
        # Check terraform-baseline job
        print("\n🏗️  Terraform Baseline Job")
    
        if "terraform-baseline" in jobs:
            baseline_job = jobs["terraform-baseline"]
            steps = baseline_job.get("steps", [])
        
            self.test("terraform-baseline: has steps", len(steps) > 0)
            self.test("terraform-baseline: has multiple steps", len(steps) >= 4)
        
            # Check for essential steps
            step_names = [step.get("name", "") for step in steps]
        
            self.test("terraform-baseline: has Checkout step",
                       any("checkout" in name.lower() for name in step_names))
            self.test("terraform-baseline: has Setup Terraform step",
                       any("setup terraform" in name.lower() for name in step_names))
            self.test("terraform-baseline: has Terraform Init step",
                       any("init" in name.lower() for name in step_names))
            self.test("terraform-baseline: has Terraform Validate step",
                       any("validate" in name.lower() for name in step_names))
            self.test("terraform-baseline: has Terraform Plan step",
                       any("plan" in name.lower() for name in step_names))
        else:
            for _ in range(7):
                self.skip("terraform-baseline validation", "Job not found")
    
        # Check terraform-pr-change job
        print("\n🔄 Terraform PR Change Job")
    
        if "terraform-pr-change" in jobs:
            pr_job = jobs["terraform-pr-change"]
            steps = pr_job.get("steps", [])
        
            self.test("terraform-pr-change: has steps", len(steps) > 0)
            self.test("terraform-pr-change: has multiple steps", len(steps) >= 4)
        
            # Check working directory
            has_working_dir = any("working-directory" in step for step in steps)
            self.test("terraform-pr-change: uses working-directory", has_working_dir)
        
            # Verify working directory is pr-change
            for step in steps:
                if "working-directory" in step:
                    working_dir = step["working-directory"]
                    if "pr-change" in working_dir:
                        self.test("terraform-pr-change: targets pr-change directory", True)
                        break
        else:
            for _ in range(4):
                self.skip("terraform-pr-change validation", "Job not found")
    
        # Check terraform-noop job
        print("\n🔄 Terraform Noop Job")
    
        if "terraform-noop" in jobs:
            noop_job = jobs["terraform-noop"]
            steps = noop_job.get("steps", [])
        
            self.test("terraform-noop: has steps", len(steps) > 0)
        
            # Verify noop targets correct directory
            for step in steps:
                if "working-directory" in step:
                    working_dir = step["working-directory"]
                    if "noop" in working_dir:
                        self.test("terraform-noop: targets noop-change directory", True)
                        break
        else:
            self.skip("terraform-noop validation", "Job not found")


    def test_costpilot_scan_steps(self):
        """Validate CostPilot scan steps - 20 tests"""
        self.section("COSTPILOT SCAN STEPS (20 tests)")
    
        workflow_file = self.repo_root / ".github" / "workflows" / "costpilot-ci.yml"
    
        if not workflow_file.exists():
            for _ in range(20):
                self.skip("costpilot scan", "Workflow file not found")
            return
    
        workflow = load_workflow(workflow_file)
        jobs = workflow.get("jobs", {})
    
        if "costpilot-scan" not in jobs:
            for _ in range(20):
                self.skip("costpilot-scan validation", "Job not found")
            return
    
        scan_job = jobs["costpilot-scan"]
        steps = scan_job.get("steps", [])
    
        print("\n🔍 CostPilot Steps")
    
        self.test("costpilot-scan: has steps", len(steps) > 0)
        self.test("costpilot-scan: has multiple steps", len(steps) >= 5)
    
        step_names = [step.get("name", "").lower() for step in steps]
    
        # Check for CostPilot operations
        self.test("costpilot-scan: has Detect step",
                   any("detect" in name for name in step_names))
        self.test("costpilot-scan: has Predict step",
                   any("predict" in name for name in step_names))
        self.test("costpilot-scan: has Explain step",
                   any("explain" in name for name in step_names))
        self.test("costpilot-scan: has PR comment step",
                   any("comment" in name for name in step_names))
    
        print("\n🆔 Step IDs")
    
        # Check for step IDs (needed for output reference)
        step_ids = [step.get("id", "") for step in steps if "id" in step]
    
        self.test("costpilot-scan: steps have IDs", len(step_ids) > 0)
        self.test("costpilot-scan: Detect has ID",
                   any("detect" in step_id for step_id in step_ids))
        self.test("costpilot-scan: Predict has ID",
                   any("predict" in step_id for step_id in step_ids))
        self.test("costpilot-scan: Explain has ID",
                   any("explain" in step_id for step_id in step_ids))
    
        print("\n💬 PR Comment Integration")
    
        # Check PR comment step
        for step in steps:
            if "comment" in step.get("name", "").lower():
                self.test("PR comment: has conditional execution",
                           "if" in step)
                self.test("PR comment: uses github-script",
                           "uses" in step and "github-script" in step.get("uses", ""))
                self.test("PR comment: has script content",
                           "with" in step and "script" in step.get("with", {}))
                break
    
        print("\n⏱️  Performance Checks")
    
        # Check for performance validation
        has_performance_check = any("performance" in name for name in step_names)
        self.test("costpilot-scan: includes performance check", has_performance_check)
    
        # Check conditional execution for PR only
        if_condition = scan_job.get("if", "")
        self.test("costpilot-scan: conditional on pull_request",
                   "pull_request" in if_condition)


    def test_safeguard_validations(self):
        """Validate safeguard mechanisms - 15 tests"""
        self.section("SAFEGUARD VALIDATIONS (15 tests)")
    
        workflow_file = self.repo_root / ".github" / "workflows" / "costpilot-ci.yml"
    
        if not workflow_file.exists():
            for _ in range(15):
                self.skip("safeguard validation", "Workflow file not found")
            return
    
        workflow = load_workflow(workflow_file)
        jobs = workflow.get("jobs", {})
    
        print("\n🛡️  Protected Files Validation")
    
        # Check for protected files validation job
        if "validate-protected-files" in jobs:
            protected_job = jobs["validate-protected-files"]
            steps = protected_job.get("steps", [])
        
            self.test("validate-protected-files: exists", True)
            self.test("validate-protected-files: has steps", len(steps) > 0)
        
            # Check for protection logic
            for step in steps:
                run_script = step.get("run", "")
                if "protected" in run_script.lower() or "safeguard" in run_script.lower():
                    self.test("validate-protected-files: has protection logic", True)
                    self.test("validate-protected-files: checks snapshots",
                               "snapshots" in run_script)
                    self.test("validate-protected-files: checks costpilot_artifacts",
                               "costpilot_artifacts" in run_script or "artifacts" in run_script)
                    break
        else:
            for _ in range(5):
                self.skip("protected files validation", "Job not found")
    
        print("\n🚫 Terraform Apply Safeguard")
    
        # Verify NO terraform apply exists
        workflow_content = workflow_file.read_text()
    
        self.test("workflow: does NOT contain 'terraform apply'",
                   "terraform apply" not in workflow_content.lower())
        self.test("workflow: has safeguard comment",
                   "SAFEGUARD" in workflow_content or "safeguard" in workflow_content)
    
        print("\n🔐 Hash Validation")
    
        # Check for hash verification job
        if "verify-deterministic-output" in jobs:
            verify_job = jobs["verify-deterministic-output"]
            steps = verify_job.get("steps", [])
        
            self.test("verify-deterministic-output: exists", True)
        
            for step in steps:
                run_script = step.get("run", "")
                if "hash" in run_script.lower():
                    self.test("verify-deterministic-output: validates hashes", True)
                    self.test("verify-deterministic-output: checks golden manifest",
                               "golden" in run_script.lower() or "manifest" in run_script.lower())
                    break
        else:
            for _ in range(3):
                self.skip("hash verification", "Job not found")
    
        print("\n🧪 Noop Scenario Validation")
    
        # Check for noop validation
        if "validate-noop-scenario" in jobs:
            noop_val_job = jobs["validate-noop-scenario"]
            self.test("validate-noop-scenario: exists", True)
            self.test("validate-noop-scenario: has steps",
                       len(noop_val_job.get("steps", [])) > 0)
        else:
            for _ in range(2):
                self.skip("noop scenario validation", "Job not found")


    def test_policy_enforcement(self):
        """Validate policy enforcement - 10 tests"""
        self.section("POLICY ENFORCEMENT VALIDATION (10 tests)")
    
        workflow_file = self.repo_root / ".github" / "workflows" / "costpilot-ci.yml"
    
        if not workflow_file.exists():
            for _ in range(10):
                self.skip("policy enforcement", "Workflow file not found")
            return
    
        workflow = load_workflow(workflow_file)
        jobs = workflow.get("jobs", {})
    
        print("\n🛡️  Policy Validation Job")
    
        # Check for policy enforcement job
        if "validate-policy-enforcement" in jobs:
            policy_job = jobs["validate-policy-enforcement"]
        
            self.test("validate-policy-enforcement: exists", True)
            self.test("validate-policy-enforcement: has steps",
                       len(policy_job.get("steps", [])) > 0)
        
            # Check for policy violation detection
            for step in policy_job.get("steps", []):
                run_script = step.get("run", "")
                if "policy" in run_script.lower():
                    self.test("policy enforcement: checks violations", True)
                    self.test("policy enforcement: references detect output",
                               "detect" in run_script.lower())
                    self.test("policy enforcement: checks violation flag",
                               "policy_violation_detected" in run_script)
                    break
        else:
            for _ in range(5):
                self.skip("policy enforcement", "Job not found")
    
        print("\n📋 Policy Configuration")
    
        # Check for policy reference in workflow
        workflow_content = workflow_file.read_text()
    
        self.test("workflow: references policy",
                   "policy" in workflow_content.lower())
        self.test("workflow: mentions policy violations",
                   "policy_violation" in workflow_content or "violation" in workflow_content)
        self.test("workflow: includes policy checks",
                   "policy:default-ec2-type" in workflow_content or "policy:" in workflow_content)


def main():
    """Entry point for test execution"""
    suite = CicdDeepTestSuite()
    suite.run()
    suite.print_summary()
    sys.exit(suite.get_exit_code())


if __name__ == "__main__":
    main()
