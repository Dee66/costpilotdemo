#!/usr/bin/env python3
"""
CI/CD Deep Validation Suite
Adds ~100 granular tests for GitHub Actions workflow validation
Focus: Workflow structure, job dependencies, environment variables, secrets, conditions, safeguards
"""

import os
import re
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Any

# Color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class TestRunner:
    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.failures = []
    
    def test(self, name: str, condition: bool, reason: str = ""):
        if condition:
            self.passed += 1
            print(f"  {GREEN}✓{RESET} {name}")
        else:
            self.failed += 1
            msg = f"{name}" + (f": {reason}" if reason else "")
            self.failures.append(msg)
            print(f"  {RED}✗{RESET} {name}" + (f" - {reason}" if reason else ""))
    
    def skip(self, name: str, reason: str = ""):
        self.skipped += 1
        print(f"  {YELLOW}⊘{RESET} {name}" + (f" - {reason}" if reason else ""))
    
    def section(self, name: str):
        print(f"\n{BLUE}{'='*80}{RESET}")
        print(f"{BLUE}{name}{RESET}")
        print(f"{BLUE}{'='*80}{RESET}")


def load_workflow(filepath: Path) -> Dict[str, Any]:
    """Load GitHub Actions workflow YAML"""
    if not filepath.exists():
        return {}
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)


def test_workflow_structure(runner: TestRunner):
    """Validate workflow structure - 20 tests"""
    runner.section("WORKFLOW STRUCTURE VALIDATION (20 tests)")
    
    workflow_file = runner.repo_root / ".github" / "workflows" / "costpilot-ci.yml"
    
    if not workflow_file.exists():
        for _ in range(20):
            runner.skip("workflow validation", "costpilot-ci.yml not found")
        return
    
    workflow = load_workflow(workflow_file)
    
    print("\n📋 Required Fields")
    
    # Check required top-level fields
    runner.test("workflow: has name", "name" in workflow)
    runner.test("workflow: has 'on' triggers", "on" in workflow)
    runner.test("workflow: has jobs", "jobs" in workflow)
    runner.test("workflow: has permissions", "permissions" in workflow)
    runner.test("workflow: has env", "env" in workflow)
    
    # Validate workflow name
    if "name" in workflow:
        name = workflow["name"]
        runner.test("workflow: has descriptive name", len(name) > 5,
                   f"Name: {name}")
        runner.test("workflow: name contains 'CostPilot'", "CostPilot" in name)
    
    print("\n🔔 Trigger Configuration")
    
    # Check triggers
    if "on" in workflow:
        triggers = workflow["on"]
        runner.test("workflow: triggered on pull_request", "pull_request" in triggers)
        runner.test("workflow: triggered on push", "push" in triggers)
        runner.test("workflow: has workflow_dispatch", "workflow_dispatch" in triggers)
        
        # Check PR trigger configuration
        if "pull_request" in triggers and isinstance(triggers["pull_request"], dict):
            pr_config = triggers["pull_request"]
            runner.test("PR trigger: targets main branch",
                       "branches" in pr_config and "main" in pr_config.get("branches", []))
            runner.test("PR trigger: has path filters",
                       "paths" in pr_config)
    
    print("\n🔐 Permissions & Environment")
    
    # Check permissions
    if "permissions" in workflow:
        perms = workflow["permissions"]
        runner.test("permissions: has contents", "contents" in perms)
        runner.test("permissions: has pull-requests", "pull-requests" in perms)
        runner.test("permissions: contents is read", perms.get("contents") == "read")
        runner.test("permissions: pull-requests is write", perms.get("pull-requests") == "write")
    
    # Check environment variables
    if "env" in workflow:
        env = workflow["env"]
        runner.test("env: has TERRAFORM_VERSION", "TERRAFORM_VERSION" in env)
        runner.test("env: has AWS_REGION", "AWS_REGION" in env)


def test_job_dependencies(runner: TestRunner):
    """Validate job dependencies and ordering - 20 tests"""
    runner.section("JOB DEPENDENCIES VALIDATION (20 tests)")
    
    workflow_file = runner.repo_root / ".github" / "workflows" / "costpilot-ci.yml"
    
    if not workflow_file.exists():
        for _ in range(20):
            runner.skip("job dependencies", "Workflow file not found")
        return
    
    workflow = load_workflow(workflow_file)
    jobs = workflow.get("jobs", {})
    
    print("\n🔗 Job Structure")
    
    runner.test("workflow: has jobs", len(jobs) > 0,
               f"Found {len(jobs)} jobs")
    runner.test("workflow: has multiple jobs", len(jobs) >= 5,
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
        runner.test(f"jobs: includes '{job_name}'", job_name in jobs)
    
    print("\n➡️  Dependency Chains")
    
    # Check dependency relationships
    if "terraform-baseline" in jobs:
        baseline_job = jobs["terraform-baseline"]
        runner.test("terraform-baseline: depends on validate-protected-files",
                   "needs" in baseline_job and 
                   "validate-protected-files" in baseline_job.get("needs", ""))
    
    if "terraform-pr-change" in jobs:
        pr_job = jobs["terraform-pr-change"]
        runner.test("terraform-pr-change: depends on validate-protected-files",
                   "needs" in pr_job and 
                   "validate-protected-files" in pr_job.get("needs", ""))
    
    if "costpilot-scan" in jobs:
        scan_job = jobs["costpilot-scan"]
        needs = scan_job.get("needs", [])
        if isinstance(needs, str):
            needs = [needs]
        
        runner.test("costpilot-scan: has dependencies", len(needs) > 0)
        runner.test("costpilot-scan: depends on terraform jobs",
                   any(dep in ["terraform-baseline", "terraform-pr-change", "terraform-noop"] 
                       for dep in needs))
    
    print("\n🎯 Job Conditions")
    
    # Check conditional execution
    for job_name, job_config in list(jobs.items())[:5]:
        if "if" in job_config:
            condition = job_config["if"]
            runner.test(f"{job_name}: has execution condition", len(condition) > 0)


def test_terraform_validation_steps(runner: TestRunner):
    """Validate Terraform validation steps - 20 tests"""
    runner.section("TERRAFORM VALIDATION STEPS (20 tests)")
    
    workflow_file = runner.repo_root / ".github" / "workflows" / "costpilot-ci.yml"
    
    if not workflow_file.exists():
        for _ in range(20):
            runner.skip("terraform steps", "Workflow file not found")
        return
    
    workflow = load_workflow(workflow_file)
    jobs = workflow.get("jobs", {})
    
    # Check terraform-baseline job
    print("\n🏗️  Terraform Baseline Job")
    
    if "terraform-baseline" in jobs:
        baseline_job = jobs["terraform-baseline"]
        steps = baseline_job.get("steps", [])
        
        runner.test("terraform-baseline: has steps", len(steps) > 0)
        runner.test("terraform-baseline: has multiple steps", len(steps) >= 4)
        
        # Check for essential steps
        step_names = [step.get("name", "") for step in steps]
        
        runner.test("terraform-baseline: has Checkout step",
                   any("checkout" in name.lower() for name in step_names))
        runner.test("terraform-baseline: has Setup Terraform step",
                   any("setup terraform" in name.lower() for name in step_names))
        runner.test("terraform-baseline: has Terraform Init step",
                   any("init" in name.lower() for name in step_names))
        runner.test("terraform-baseline: has Terraform Validate step",
                   any("validate" in name.lower() for name in step_names))
        runner.test("terraform-baseline: has Terraform Plan step",
                   any("plan" in name.lower() for name in step_names))
    else:
        for _ in range(7):
            runner.skip("terraform-baseline validation", "Job not found")
    
    # Check terraform-pr-change job
    print("\n🔄 Terraform PR Change Job")
    
    if "terraform-pr-change" in jobs:
        pr_job = jobs["terraform-pr-change"]
        steps = pr_job.get("steps", [])
        
        runner.test("terraform-pr-change: has steps", len(steps) > 0)
        runner.test("terraform-pr-change: has multiple steps", len(steps) >= 4)
        
        # Check working directory
        has_working_dir = any("working-directory" in step for step in steps)
        runner.test("terraform-pr-change: uses working-directory", has_working_dir)
        
        # Verify working directory is pr-change
        for step in steps:
            if "working-directory" in step:
                working_dir = step["working-directory"]
                if "pr-change" in working_dir:
                    runner.test("terraform-pr-change: targets pr-change directory", True)
                    break
    else:
        for _ in range(4):
            runner.skip("terraform-pr-change validation", "Job not found")
    
    # Check terraform-noop job
    print("\n🔄 Terraform Noop Job")
    
    if "terraform-noop" in jobs:
        noop_job = jobs["terraform-noop"]
        steps = noop_job.get("steps", [])
        
        runner.test("terraform-noop: has steps", len(steps) > 0)
        
        # Verify noop targets correct directory
        for step in steps:
            if "working-directory" in step:
                working_dir = step["working-directory"]
                if "noop" in working_dir:
                    runner.test("terraform-noop: targets noop-change directory", True)
                    break
    else:
        runner.skip("terraform-noop validation", "Job not found")


def test_costpilot_scan_steps(runner: TestRunner):
    """Validate CostPilot scan steps - 20 tests"""
    runner.section("COSTPILOT SCAN STEPS (20 tests)")
    
    workflow_file = runner.repo_root / ".github" / "workflows" / "costpilot-ci.yml"
    
    if not workflow_file.exists():
        for _ in range(20):
            runner.skip("costpilot scan", "Workflow file not found")
        return
    
    workflow = load_workflow(workflow_file)
    jobs = workflow.get("jobs", {})
    
    if "costpilot-scan" not in jobs:
        for _ in range(20):
            runner.skip("costpilot-scan validation", "Job not found")
        return
    
    scan_job = jobs["costpilot-scan"]
    steps = scan_job.get("steps", [])
    
    print("\n🔍 CostPilot Steps")
    
    runner.test("costpilot-scan: has steps", len(steps) > 0)
    runner.test("costpilot-scan: has multiple steps", len(steps) >= 5)
    
    step_names = [step.get("name", "").lower() for step in steps]
    
    # Check for CostPilot operations
    runner.test("costpilot-scan: has Detect step",
               any("detect" in name for name in step_names))
    runner.test("costpilot-scan: has Predict step",
               any("predict" in name for name in step_names))
    runner.test("costpilot-scan: has Explain step",
               any("explain" in name for name in step_names))
    runner.test("costpilot-scan: has PR comment step",
               any("comment" in name for name in step_names))
    
    print("\n🆔 Step IDs")
    
    # Check for step IDs (needed for output reference)
    step_ids = [step.get("id", "") for step in steps if "id" in step]
    
    runner.test("costpilot-scan: steps have IDs", len(step_ids) > 0)
    runner.test("costpilot-scan: Detect has ID",
               any("detect" in step_id for step_id in step_ids))
    runner.test("costpilot-scan: Predict has ID",
               any("predict" in step_id for step_id in step_ids))
    runner.test("costpilot-scan: Explain has ID",
               any("explain" in step_id for step_id in step_ids))
    
    print("\n💬 PR Comment Integration")
    
    # Check PR comment step
    for step in steps:
        if "comment" in step.get("name", "").lower():
            runner.test("PR comment: has conditional execution",
                       "if" in step)
            runner.test("PR comment: uses github-script",
                       "uses" in step and "github-script" in step.get("uses", ""))
            runner.test("PR comment: has script content",
                       "with" in step and "script" in step.get("with", {}))
            break
    
    print("\n⏱️  Performance Checks")
    
    # Check for performance validation
    has_performance_check = any("performance" in name for name in step_names)
    runner.test("costpilot-scan: includes performance check", has_performance_check)
    
    # Check conditional execution for PR only
    if_condition = scan_job.get("if", "")
    runner.test("costpilot-scan: conditional on pull_request",
               "pull_request" in if_condition)


def test_safeguard_validations(runner: TestRunner):
    """Validate safeguard mechanisms - 15 tests"""
    runner.section("SAFEGUARD VALIDATIONS (15 tests)")
    
    workflow_file = runner.repo_root / ".github" / "workflows" / "costpilot-ci.yml"
    
    if not workflow_file.exists():
        for _ in range(15):
            runner.skip("safeguard validation", "Workflow file not found")
        return
    
    workflow = load_workflow(workflow_file)
    jobs = workflow.get("jobs", {})
    
    print("\n🛡️  Protected Files Validation")
    
    # Check for protected files validation job
    if "validate-protected-files" in jobs:
        protected_job = jobs["validate-protected-files"]
        steps = protected_job.get("steps", [])
        
        runner.test("validate-protected-files: exists", True)
        runner.test("validate-protected-files: has steps", len(steps) > 0)
        
        # Check for protection logic
        for step in steps:
            run_script = step.get("run", "")
            if "protected" in run_script.lower() or "safeguard" in run_script.lower():
                runner.test("validate-protected-files: has protection logic", True)
                runner.test("validate-protected-files: checks snapshots",
                           "snapshots" in run_script)
                runner.test("validate-protected-files: checks costpilot_artifacts",
                           "costpilot_artifacts" in run_script or "artifacts" in run_script)
                break
    else:
        for _ in range(5):
            runner.skip("protected files validation", "Job not found")
    
    print("\n🚫 Terraform Apply Safeguard")
    
    # Verify NO terraform apply exists
    workflow_content = workflow_file.read_text()
    
    runner.test("workflow: does NOT contain 'terraform apply'",
               "terraform apply" not in workflow_content.lower())
    runner.test("workflow: has safeguard comment",
               "SAFEGUARD" in workflow_content or "safeguard" in workflow_content)
    
    print("\n🔐 Hash Validation")
    
    # Check for hash verification job
    if "verify-deterministic-output" in jobs:
        verify_job = jobs["verify-deterministic-output"]
        steps = verify_job.get("steps", [])
        
        runner.test("verify-deterministic-output: exists", True)
        
        for step in steps:
            run_script = step.get("run", "")
            if "hash" in run_script.lower():
                runner.test("verify-deterministic-output: validates hashes", True)
                runner.test("verify-deterministic-output: checks golden manifest",
                           "golden" in run_script.lower() or "manifest" in run_script.lower())
                break
    else:
        for _ in range(3):
            runner.skip("hash verification", "Job not found")
    
    print("\n🧪 Noop Scenario Validation")
    
    # Check for noop validation
    if "validate-noop-scenario" in jobs:
        noop_val_job = jobs["validate-noop-scenario"]
        runner.test("validate-noop-scenario: exists", True)
        runner.test("validate-noop-scenario: has steps",
                   len(noop_val_job.get("steps", [])) > 0)
    else:
        for _ in range(2):
            runner.skip("noop scenario validation", "Job not found")


def test_policy_enforcement(runner: TestRunner):
    """Validate policy enforcement - 10 tests"""
    runner.section("POLICY ENFORCEMENT VALIDATION (10 tests)")
    
    workflow_file = runner.repo_root / ".github" / "workflows" / "costpilot-ci.yml"
    
    if not workflow_file.exists():
        for _ in range(10):
            runner.skip("policy enforcement", "Workflow file not found")
        return
    
    workflow = load_workflow(workflow_file)
    jobs = workflow.get("jobs", {})
    
    print("\n🛡️  Policy Validation Job")
    
    # Check for policy enforcement job
    if "validate-policy-enforcement" in jobs:
        policy_job = jobs["validate-policy-enforcement"]
        
        runner.test("validate-policy-enforcement: exists", True)
        runner.test("validate-policy-enforcement: has steps",
                   len(policy_job.get("steps", [])) > 0)
        
        # Check for policy violation detection
        for step in policy_job.get("steps", []):
            run_script = step.get("run", "")
            if "policy" in run_script.lower():
                runner.test("policy enforcement: checks violations", True)
                runner.test("policy enforcement: references detect output",
                           "detect" in run_script.lower())
                runner.test("policy enforcement: checks violation flag",
                           "policy_violation_detected" in run_script)
                break
    else:
        for _ in range(5):
            runner.skip("policy enforcement", "Job not found")
    
    print("\n📋 Policy Configuration")
    
    # Check for policy reference in workflow
    workflow_content = workflow_file.read_text()
    
    runner.test("workflow: references policy",
               "policy" in workflow_content.lower())
    runner.test("workflow: mentions policy violations",
               "policy_violation" in workflow_content or "violation" in workflow_content)
    runner.test("workflow: includes policy checks",
               "policy:default-ec2-type" in workflow_content or "policy:" in workflow_content)


def main():
    runner = TestRunner()
    
    print(f"{BLUE}╔════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BLUE}║                                                                            ║{RESET}")
    print(f"{BLUE}║           CI/CD DEEP VALIDATION SUITE (~100 tests)                        ║{RESET}")
    print(f"{BLUE}║                                                                            ║{RESET}")
    print(f"{BLUE}╚════════════════════════════════════════════════════════════════════════════╝{RESET}")
    
    # Run all test suites
    test_workflow_structure(runner)
    test_job_dependencies(runner)
    test_terraform_validation_steps(runner)
    test_costpilot_scan_steps(runner)
    test_safeguard_validations(runner)
    test_policy_enforcement(runner)
    
    # Print summary
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}TEST SUMMARY{RESET}")
    print(f"{BLUE}{'='*80}{RESET}")
    
    total = runner.passed + runner.failed + runner.skipped
    pass_rate = (runner.passed / total * 100) if total > 0 else 0
    
    print(f"\n{GREEN}✓ Passed:{RESET}  {runner.passed}/{total} ({pass_rate:.1f}%)")
    print(f"{RED}✗ Failed:{RESET}  {runner.failed}/{total}")
    print(f"{YELLOW}⊘ Skipped:{RESET} {runner.skipped}/{total}")
    
    if runner.failures:
        print(f"\n{RED}{'='*80}{RESET}")
        print(f"{RED}FAILURES ({len(runner.failures)}){RESET}")
        print(f"{RED}{'='*80}{RESET}")
        for failure in runner.failures[:20]:  # Show first 20
            print(f"{RED}✗{RESET} {failure}")
        if len(runner.failures) > 20:
            print(f"\n{YELLOW}... and {len(runner.failures) - 20} more failures{RESET}")
    
    print(f"\n{BLUE}{'='*80}{RESET}")
    
    # Exit code
    sys.exit(0 if runner.failed == 0 else 1)


if __name__ == "__main__":
    main()
