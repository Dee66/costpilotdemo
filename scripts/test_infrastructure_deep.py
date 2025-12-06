#!/usr/bin/env python3
"""
Deep Infrastructure Validation Suite
Adds ~150 granular tests for Terraform infrastructure validation
Focus: Resource attributes, dependencies, variables, providers, cost policies
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Set

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


def read_tf_file(filepath: Path) -> str:
    """Read a Terraform file"""
    if not filepath.exists():
        return ""
    with open(filepath, 'r') as f:
        return f.read()


def extract_resources(content: str) -> List[Dict[str, str]]:
    """Extract resource blocks from Terraform content"""
    resources = []
    pattern = r'resource\s+"([^"]+)"\s+"([^"]+)"\s*\{'
    for match in re.finditer(pattern, content):
        resources.append({
            'type': match.group(1),
            'name': match.group(2),
            'full_name': f"{match.group(1)}.{match.group(2)}"
        })
    return resources


def test_terraform_resource_attributes(runner: TestRunner):
    """Validate Terraform resource attributes - 40 tests"""
    runner.section("TERRAFORM RESOURCE ATTRIBUTE VALIDATION (40 tests)")
    
    infra_dir = runner.repo_root / "infrastructure" / "terraform"
    baseline_file = infra_dir / "baseline" / "main.tf"
    pr_file = infra_dir / "pr-change" / "main.tf"
    
    if not baseline_file.exists():
        for _ in range(40):
            runner.skip("resource attributes", "baseline main.tf not found")
        return
    
    baseline_content = read_tf_file(baseline_file)
    pr_content = read_tf_file(pr_file) if pr_file.exists() else ""
    
    print("\n🔧 Baseline Stack Resource Attributes")
    
    # VPC attributes
    runner.test("baseline: VPC has cidr_block", 'cidr_block' in baseline_content)
    runner.test("baseline: VPC enables DNS hostnames", 'enable_dns_hostnames = true' in baseline_content)
    runner.test("baseline: VPC enables DNS support", 'enable_dns_support = true' in baseline_content)
    
    # Launch template attributes
    runner.test("baseline: launch_template has instance_type", 
               'instance_type = "t3.micro"' in baseline_content)
    runner.test("baseline: launch_template uses t3.micro", 
               '"t3.micro"' in baseline_content)
    runner.test("baseline: launch_template has user_data", 'user_data' in baseline_content)
    runner.test("baseline: launch_template has block_device_mappings", 
               'block_device_mappings' in baseline_content)
    
    # EBS volume attributes (baseline)
    runner.test("baseline: EBS volume_size = 20GB", 
               'volume_size           = 20' in baseline_content or
               'volume_size = 20' in baseline_content)
    runner.test("baseline: EBS volume_type = gp3", 
               'volume_type           = "gp3"' in baseline_content or
               'volume_type = "gp3"' in baseline_content)
    runner.test("baseline: EBS encryption enabled", 
               'encrypted             = true' in baseline_content or
               'encrypted = true' in baseline_content)
    
    # Auto Scaling Group attributes
    runner.test("baseline: ASG has min_size", 'min_size' in baseline_content)
    runner.test("baseline: ASG has max_size", 'max_size' in baseline_content)
    runner.test("baseline: ASG has desired_capacity", 'desired_capacity' in baseline_content)
    runner.test("baseline: ASG min_size = 2", 'min_size         = 2' in baseline_content or
               'min_size = 2' in baseline_content)
    
    # S3 bucket attributes
    runner.test("baseline: S3 bucket has name", 'bucket =' in baseline_content)
    runner.test("baseline: S3 versioning enabled", 'Enabled' in baseline_content)
    runner.test("baseline: S3 lifecycle exists", 'lifecycle_configuration' in baseline_content)
    
    # CloudWatch attributes
    runner.test("baseline: CloudWatch log group exists", 'aws_cloudwatch_log_group' in baseline_content)
    runner.test("baseline: log retention set to 30 days", 
               'retention_in_days = 30' in baseline_content)
    
    # Load balancer attributes
    runner.test("baseline: ALB is application type", 
               'load_balancer_type = "application"' in baseline_content)
    runner.test("baseline: ALB has security_groups", 'security_groups' in baseline_content)
    
    if pr_content:
        print("\n⚠️  PR Stack Resource Attributes (Cost Regressions)")
        
        # PR changes - cost increases
        runner.test("PR: instance_type changed to t3.xlarge", 
                   'instance_type = "t3.xlarge"' in pr_content)
        runner.test("PR: EBS volume_size increased to 200GB", 
                   'volume_size           = 200' in pr_content or
                   'volume_size = 200' in pr_content)
        runner.test("PR: CloudWatch retention set to 0 (infinite)", 
                   'retention_in_days = 0' in pr_content)
        
        # Verify lifecycle policy removed
        has_lifecycle = 'lifecycle_configuration' in pr_content
        runner.test("PR: S3 lifecycle policy removed", not has_lifecycle)
    
    print("\n🔐 Security Attributes")
    
    # Security group validation
    runner.test("baseline: ALB security group exists", 'aws_security_group" "alb"' in baseline_content)
    runner.test("baseline: EC2 security group exists", 'aws_security_group" "ec2"' in baseline_content)
    runner.test("baseline: security group has ingress rules", 'ingress {' in baseline_content)
    runner.test("baseline: security group has egress rules", 'egress {' in baseline_content)
    
    # Metadata options
    runner.test("baseline: IMDSv2 required", 'http_tokens                 = "required"' in baseline_content)
    
    print("\n🏷️  Tagging Standards")
    
    # Tag validation
    runner.test("baseline: resources have Name tags", 'Name = ' in baseline_content)
    runner.test("baseline: resources have Environment tags", 'Environment' in baseline_content)
    runner.test("baseline: provider has default_tags", 'default_tags' in baseline_content)
    runner.test("baseline: Project tag exists", 'Project' in baseline_content)
    runner.test("baseline: ManagedBy tag exists", 'ManagedBy' in baseline_content)
    
    print("\n📦 Data Sources")
    
    # Data sources
    runner.test("baseline: uses data source for AMI", 'data.aws_ami' in baseline_content)
    runner.test("baseline: uses data source for account ID", 
               'data.aws_caller_identity' in baseline_content)


def test_resource_dependencies(runner: TestRunner):
    """Validate resource dependency chains - 30 tests"""
    runner.section("RESOURCE DEPENDENCY CHAIN VALIDATION (30 tests)")
    
    infra_dir = runner.repo_root / "infrastructure" / "terraform"
    baseline_file = infra_dir / "baseline" / "main.tf"
    
    if not baseline_file.exists():
        for _ in range(30):
            runner.skip("resource dependencies", "File not found")
        return
    
    content = read_tf_file(baseline_file)
    
    print("\n🔗 VPC Dependencies")
    
    # VPC → Subnet dependencies
    runner.test("Subnet references VPC", 'vpc_id      = aws_vpc.main.id' in content or
               'vpc_id = aws_vpc.main.id' in content)
    runner.test("Internet Gateway references VPC", 'vpc_id = aws_vpc.main.id' in content)
    runner.test("Route table references VPC", 'vpc_id = aws_vpc.main.id' in content)
    runner.test("Security group references VPC", 'vpc_id      = aws_vpc.main.id' in content or
               'vpc_id = aws_vpc.main.id' in content)
    
    print("\n🔗 Network Dependencies")
    
    # Route table associations
    runner.test("Route table association references subnet", 
               'subnet_id      = aws_subnet' in content)
    runner.test("Route table association references route table", 
               'route_table_id = aws_route_table' in content)
    runner.test("Route references internet gateway", 
               'gateway_id = aws_internet_gateway' in content)
    
    print("\n🔗 Compute Dependencies")
    
    # Launch template → Security group
    runner.test("Launch template references security group", 
               'vpc_security_group_ids = [aws_security_group.ec2.id]' in content)
    
    # ASG dependencies
    runner.test("ASG references subnets", 'vpc_zone_identifier' in content)
    runner.test("ASG references target group", 'target_group_arns' in content)
    runner.test("ASG references launch template", 'launch_template {' in content)
    runner.test("ASG launch template has id", 'id      = aws_launch_template.main.id' in content)
    
    print("\n🔗 Load Balancer Dependencies")
    
    # ALB dependencies
    runner.test("ALB references security group", 
               'security_groups    = [aws_security_group.alb.id]' in content)
    runner.test("ALB references subnets", 
               'subnets            = [aws_subnet.public_a.id, aws_subnet.public_b.id]' in content)
    
    # Target group
    runner.test("Target group references VPC", 
               'vpc_id   = aws_vpc.main.id' in content or
               'vpc_id = aws_vpc.main.id' in content)
    
    # Listener dependencies
    runner.test("Listener references ALB", 'load_balancer_arn = aws_lb.main.arn' in content)
    runner.test("Listener references target group", 
               'target_group_arn = aws_lb_target_group.main.arn' in content)
    
    print("\n🔗 S3 Dependencies")
    
    # S3 bucket dependencies
    runner.test("S3 versioning references bucket", 
               'bucket = aws_s3_bucket.main.id' in content)
    runner.test("S3 lifecycle references bucket", 
               'bucket = aws_s3_bucket.main.id' in content)
    
    print("\n🔗 Security Group Dependencies")
    
    # Security group ingress rules
    runner.test("EC2 SG ingress references ALB SG", 
               'security_groups = [aws_security_group.alb.id]' in content)
    
    print("\n📊 Dependency Count Validation")
    
    # Count resource references
    vpc_refs = content.count('aws_vpc.main')
    subnet_refs = content.count('aws_subnet.')
    sg_refs = content.count('aws_security_group.')
    
    runner.test("VPC referenced multiple times", vpc_refs >= 3, f"Found {vpc_refs} refs")
    runner.test("Subnets referenced multiple times", subnet_refs >= 4, f"Found {subnet_refs} refs")
    runner.test("Security groups referenced multiple times", sg_refs >= 3, f"Found {sg_refs} refs")
    
    # Verify no dangling references
    runner.test("No undefined resource references", 
               'aws_vpc.undefined' not in content and 'aws_subnet.undefined' not in content)
    
    # Cross-resource validation
    runner.test("Launch template + ASG linked", 
               'aws_launch_template.main' in content and 'aws_autoscaling_group.main' in content)
    runner.test("ALB + Target Group + Listener chain complete",
               'aws_lb.main' in content and 
               'aws_lb_target_group.main' in content and
               'aws_lb_listener.main' in content)


def test_variables_and_outputs(runner: TestRunner):
    """Validate variables and outputs - 25 tests"""
    runner.section("VARIABLES AND OUTPUTS VALIDATION (25 tests)")
    
    infra_dir = runner.repo_root / "infrastructure" / "terraform" / "baseline"
    variables_file = infra_dir / "variables.tf"
    outputs_file = infra_dir / "outputs.tf"
    main_file = infra_dir / "main.tf"
    
    print("\n📥 Variables File")
    
    if variables_file.exists():
        var_content = read_tf_file(variables_file)
        
        runner.test("variables.tf exists", True)
        runner.test("variables: has aws_region", 'variable "aws_region"' in var_content)
        runner.test("variables: has project_name", 'variable "project_name"' in var_content)
        runner.test("variables: aws_region has description", 
                   'description' in var_content)
        runner.test("variables: aws_region has default", 'default' in var_content)
        runner.test("variables: aws_region has type", 'type' in var_content)
        
        # Check variable usage in main
        if main_file.exists():
            main_content = read_tf_file(main_file)
            runner.test("main.tf uses var.aws_region", 'var.aws_region' in main_content)
            runner.test("main.tf uses var.project_name", 'var.project_name' in main_content)
    else:
        for _ in range(8):
            runner.skip("variables validation", "variables.tf not found")
    
    print("\n📤 Outputs File")
    
    if outputs_file.exists():
        out_content = read_tf_file(outputs_file)
        
        runner.test("outputs.tf exists", True)
        runner.test("outputs: has output declarations", 'output "' in out_content)
        runner.test("outputs: has value expressions", 'value =' in out_content)
        runner.test("outputs: has descriptions", 'description' in out_content)
        
        # Check for common outputs
        runner.test("outputs: has ALB DNS output", 
                   'alb' in out_content.lower() or 'load_balancer' in out_content.lower())
        runner.test("outputs: has VPC output", 'vpc' in out_content.lower())
        
        # Output format validation
        output_blocks = re.findall(r'output\s+"([^"]+)"', out_content)
        runner.test("outputs: has multiple outputs", len(output_blocks) >= 3,
                   f"Found {len(output_blocks)} outputs")
        runner.test("outputs: output names use underscores", 
                   all('_' in name or len(name) < 5 for name in output_blocks))
    else:
        for _ in range(8):
            runner.skip("outputs validation", "outputs.tf not found")
    
    print("\n🔗 Variable-Output Integration")
    
    if variables_file.exists() and outputs_file.exists():
        var_content = read_tf_file(variables_file)
        out_content = read_tf_file(outputs_file)
        main_content = read_tf_file(main_file) if main_file.exists() else ""
        
        # Check that variables are used
        var_names = re.findall(r'variable\s+"([^"]+)"', var_content)
        runner.test("Variables used in main.tf", 
                   any(f'var.{var}' in main_content for var in var_names))
        
        # Check that outputs reference resources
        runner.test("Outputs reference resources", 
                   'aws_' in out_content)
        runner.test("Outputs use resource attributes", '.id' in out_content or '.arn' in out_content)
    else:
        for _ in range(3):
            runner.skip("variable-output integration", "Files not found")
    
    print("\n✅ Variable Validation Rules")
    
    if variables_file.exists():
        var_content = read_tf_file(variables_file)
        
        # All variables should have types
        var_blocks = re.findall(r'variable\s+"[^"]+"\s*\{[^}]+\}', var_content, re.DOTALL)
        runner.test("All variables have type declarations", 
                   all('type' in block for block in var_blocks))
        runner.test("All variables have descriptions",
                   all('description' in block for block in var_blocks))


def test_provider_configuration(runner: TestRunner):
    """Validate provider configuration - 15 tests"""
    runner.section("PROVIDER CONFIGURATION VALIDATION (15 tests)")
    
    infra_dir = runner.repo_root / "infrastructure" / "terraform"
    
    stacks = ["baseline", "pr-change", "noop-change"]
    
    for stack in stacks:
        stack_dir = infra_dir / stack
        main_file = stack_dir / "main.tf"
        
        if not main_file.exists():
            for _ in range(5):
                runner.skip(f"{stack} provider config", "main.tf not found")
            continue
        
        content = read_tf_file(main_file)
        
        print(f"\n⚙️  {stack.upper()} Provider Configuration")
        
        # Terraform block
        runner.test(f"{stack}: has terraform block", 'terraform {' in content)
        runner.test(f"{stack}: has required_version", 'required_version' in content)
        runner.test(f"{stack}: has required_providers", 'required_providers' in content)
        runner.test(f"{stack}: specifies AWS provider", 'aws = {' in content)
        runner.test(f"{stack}: has provider version constraint", 'version = "~>' in content)


def test_cost_policy_rules(runner: TestRunner):
    """Validate cost policy enforcement - 20 tests"""
    runner.section("COST POLICY RULES VALIDATION (20 tests)")
    
    infra_dir = runner.repo_root / "infrastructure" / "terraform"
    baseline_file = infra_dir / "baseline" / "main.tf"
    pr_file = infra_dir / "pr-change" / "main.tf"
    
    if not baseline_file.exists():
        for _ in range(20):
            runner.skip("cost policy rules", "Files not found")
        return
    
    baseline_content = read_tf_file(baseline_file)
    pr_content = read_tf_file(pr_file) if pr_file.exists() else ""
    
    print("\n💰 Baseline Cost Optimization Policies")
    
    # Instance type policy
    runner.test("Policy: baseline uses cost-efficient instance (t3.micro)", 
               '"t3.micro"' in baseline_content)
    runner.test("Policy: baseline uses gp3 volumes (not gp2)", 
               '"gp3"' in baseline_content)
    runner.test("Policy: baseline EBS volume ≤ 20GB", 
               'volume_size           = 20' in baseline_content or
               'volume_size = 20' in baseline_content)
    runner.test("Policy: baseline ASG min_size ≤ 2", 
               'min_size         = 2' in baseline_content or
               'min_size = 2' in baseline_content)
    runner.test("Policy: baseline log retention set (30 days)", 
               'retention_in_days = 30' in baseline_content)
    runner.test("Policy: baseline has S3 lifecycle policy", 
               'lifecycle_configuration' in baseline_content)
    
    print("\n⚠️  PR Cost Regression Detection")
    
    if pr_content:
        # Detect policy violations
        runner.test("Regression: PR uses expensive instance (t3.xlarge)", 
                   '"t3.xlarge"' in pr_content)
        runner.test("Regression: PR increases EBS volume to 200GB", 
                   'volume_size           = 200' in pr_content or
                   'volume_size = 200' in pr_content)
        runner.test("Regression: PR removes log retention (0 = infinite)", 
                   'retention_in_days = 0' in pr_content)
        runner.test("Regression: PR removes S3 lifecycle optimization",
                   'lifecycle_configuration' not in pr_content or
                   pr_content.count('lifecycle_configuration') < baseline_content.count('lifecycle_configuration'))
    else:
        for _ in range(4):
            runner.skip("PR regression detection", "PR file not found")
    
    print("\n🔒 Mandatory Security Policies")
    
    # Security best practices
    runner.test("Policy: EBS encryption enabled", 'encrypted             = true' in baseline_content)
    runner.test("Policy: IMDSv2 required", 'http_tokens                 = "required"' in baseline_content)
    runner.test("Policy: S3 versioning enabled", 'Enabled' in baseline_content)
    
    print("\n📊 Resource Limits")
    
    # Resource count limits
    runner.test("Policy: ASG max_size ≤ 10", 
               'max_size         = 4' in baseline_content or 'max_size = 4' in baseline_content)
    
    # Lifecycle policies
    runner.test("Policy: prevent_destroy on VPC", 'prevent_destroy = true' in baseline_content)
    
    print("\n🏷️  Tagging Policy")
    
    # Required tags
    runner.test("Policy: default_tags configured", 'default_tags' in baseline_content)
    runner.test("Policy: Project tag present", 'Project' in baseline_content)
    runner.test("Policy: Environment tag present", 'Environment' in baseline_content)
    runner.test("Policy: ManagedBy tag present", 'ManagedBy' in baseline_content)


def test_safeguard_validation(runner: TestRunner):
    """Validate safeguard documentation and scripts - 20 tests"""
    runner.section("SAFEGUARD VALIDATION (20 tests)")
    
    infra_dir = runner.repo_root / "infrastructure" / "terraform"
    safeguards_md = infra_dir / "SAFEGUARDS.md"
    guard_script = infra_dir / "terraform-apply-guard.sh"
    
    print("\n🛡️  Safeguard Documentation")
    
    if safeguards_md.exists():
        content = read_tf_file(safeguards_md)
        
        runner.test("SAFEGUARDS.md exists", True)
        runner.test("Safeguards: mentions DO NOT APPLY", 
                   'DO NOT' in content.upper() or 'WARNING' in content.upper())
        runner.test("Safeguards: explains demo purpose", 
                   'demo' in content.lower() or 'demonstration' in content.lower())
        runner.test("Safeguards: warns about costs", 
                   'cost' in content.lower() or 'bill' in content.lower())
        runner.test("Safeguards: has guard script reference", 
                   'guard' in content.lower() or 'script' in content.lower())
    else:
        for _ in range(5):
            runner.skip("safeguards doc", "SAFEGUARDS.md not found")
    
    print("\n🚨 Guard Script")
    
    if guard_script.exists():
        content = read_tf_file(guard_script)
        
        runner.test("terraform-apply-guard.sh exists", True)
        runner.test("Guard script: is bash script", '#!/bin/bash' in content or '#!/usr/bin/env bash' in content)
        runner.test("Guard script: checks for 'apply' command", 
                   'apply' in content.lower())
        runner.test("Guard script: has exit logic", 'exit' in content)
        runner.test("Guard script: has warning message", 
                   'WARNING' in content.upper() or 'ERROR' in content.upper())
    else:
        for _ in range(5):
            runner.skip("guard script", "terraform-apply-guard.sh not found")
    
    print("\n⚠️  Warning Comments in Terraform Files")
    
    # Check all main.tf files for warnings
    for stack in ["baseline", "pr-change", "noop-change"]:
        stack_file = infra_dir / stack / "main.tf"
        if stack_file.exists():
            content = read_tf_file(stack_file)
            runner.test(f"{stack}: has WARNING comment", 
                       'WARNING' in content.upper() or '⚠️' in content)
            runner.test(f"{stack}: has DO NOT APPLY comment", 
                       'DO NOT' in content.upper())
        else:
            runner.skip(f"{stack} warnings", "File not found")
    
    print("\n🔒 Additional Safety Checks")
    
    # Check that no backend configuration exists (prevents accidental state)
    baseline_file = infra_dir / "baseline" / "main.tf"
    if baseline_file.exists():
        content = read_tf_file(baseline_file)
        runner.test("No remote backend configured (safety)", 
                   'backend "s3"' not in content and 'backend "remote"' not in content)


def main():
    runner = TestRunner()
    
    print(f"{BLUE}╔════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BLUE}║                                                                            ║{RESET}")
    print(f"{BLUE}║        DEEP INFRASTRUCTURE VALIDATION SUITE (~150 tests)                   ║{RESET}")
    print(f"{BLUE}║                                                                            ║{RESET}")
    print(f"{BLUE}╚════════════════════════════════════════════════════════════════════════════╝{RESET}")
    
    # Run all test suites
    test_terraform_resource_attributes(runner)
    test_resource_dependencies(runner)
    test_variables_and_outputs(runner)
    test_provider_configuration(runner)
    test_cost_policy_rules(runner)
    test_safeguard_validation(runner)
    
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
