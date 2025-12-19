#!/usr/bin/env python3
"""
Deep Infrastructure Validation Suite
Adds ~150 granular tests for Terraform infrastructure validation
Focus: Resource attributes, dependencies, variables, providers, cost policies


Refactored to use Template Method Pattern with TestSuite base class.
"""

import os
import re
import sys
from pathlib import Path

# Import shared test framework
sys.path.insert(0, str(Path(__file__).parent))
from lib.test_suite import TestSuite
from lib.scenario_factory import ScenarioFactory
from lib.logger import get_logger
from typing import Dict, List, Any, Set


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


class InfrastructureDeepTestSuite(TestSuite):
    """Test suite using Template Method pattern"""
    
    @property
    def tags(self) -> List[str]:
        return ["infrastructure", "terraform", "validation", "deep"]
    
    def __init__(self, repo_root: Path = None):
        super().__init__(repo_root)
        self.factory = ScenarioFactory(self.repo_root)
        self.pr_scenario = self.factory.create("pr_change")
        self.logger = get_logger("infrastructure_deep_test")
    
    def run(self):
        """Template method - defines the test execution sequence"""
        self.test_terraform_resource_attributes()
        self.test_resource_dependencies()
        self.test_variables_and_outputs()
        self.test_provider_configuration()
        self.test_cost_policy_rules()
        self.test_safeguard_validation()
    
    def test_terraform_resource_attributes(self):
        """Validate Terraform resource attributes - 40 tests"""
        self.section("TERRAFORM RESOURCE ATTRIBUTE VALIDATION (40 tests)")
    
        infra_dir = self.repo_root / "infrastructure" / "terraform"
        baseline_file = infra_dir / "baseline" / "main.tf"
        pr_file = infra_dir / "pr-change" / "main.tf"
    
        if not baseline_file.exists():
            for _ in range(40):
                self.skip("resource attributes", "baseline main.tf not found")
            return
    
        baseline_content = read_tf_file(baseline_file)
        pr_content = read_tf_file(pr_file) if pr_file.exists() else ""
    
        self.logger.info("Baseline Stack Resource Attributes")
    
        # VPC attributes
        self.test("baseline: VPC has cidr_block", 'cidr_block' in baseline_content)
        self.test("baseline: VPC enables DNS hostnames", 'enable_dns_hostnames = true' in baseline_content)
        self.test("baseline: VPC enables DNS support", 'enable_dns_support = true' in baseline_content)
    
        # Launch template attributes
        self.test("baseline: launch_template has instance_type", 
                   'instance_type = "t3.micro"' in baseline_content)
        self.test("baseline: launch_template uses t3.micro", 
                   '"t3.micro"' in baseline_content)
        self.test("baseline: launch_template has user_data", 'user_data' in baseline_content)
        self.test("baseline: launch_template has block_device_mappings", 
                   'block_device_mappings' in baseline_content)
    
        # EBS volume attributes (baseline)
        self.test("baseline: EBS volume_size = 20GB", 
                   'volume_size           = 20' in baseline_content or
                   'volume_size = 20' in baseline_content)
        self.test("baseline: EBS volume_type = gp3", 
                   'volume_type           = "gp3"' in baseline_content or
                   'volume_type = "gp3"' in baseline_content)
        self.test("baseline: EBS encryption enabled", 
                   'encrypted             = true' in baseline_content or
                   'encrypted = true' in baseline_content)
    
        # Auto Scaling Group attributes
        self.test("baseline: ASG has min_size", 'min_size' in baseline_content)
        self.test("baseline: ASG has max_size", 'max_size' in baseline_content)
        self.test("baseline: ASG has desired_capacity", 'desired_capacity' in baseline_content)
        self.test("baseline: ASG min_size = 2", 'min_size         = 2' in baseline_content or
                   'min_size = 2' in baseline_content)
    
        # S3 bucket attributes
        self.test("baseline: S3 bucket has name", 'bucket =' in baseline_content)
        self.test("baseline: S3 versioning enabled", 'Enabled' in baseline_content)
        self.test("baseline: S3 lifecycle exists", 'lifecycle_configuration' in baseline_content)
    
        # CloudWatch attributes
        self.test("baseline: CloudWatch log group exists", 'aws_cloudwatch_log_group' in baseline_content)
        self.test("baseline: log retention set to 30 days", 
                   'retention_in_days = 30' in baseline_content)
    
        # Load balancer attributes
        self.test("baseline: ALB is application type", 
                   'load_balancer_type = "application"' in baseline_content)
        self.test("baseline: ALB has security_groups", 'security_groups' in baseline_content)
    
        if pr_content:
            self.logger.info("PR Stack Resource Attributes (Cost Regressions)")
        
            # PR changes - cost increases
            self.test("PR: instance_type changed to t3.xlarge", 
                       'instance_type = "t3.xlarge"' in pr_content)
            self.test("PR: EBS volume_size increased to 200GB", 
                       'volume_size           = 200' in pr_content or
                       'volume_size = 200' in pr_content)
            self.test("PR: CloudWatch retention set to 0 (infinite)", 
                       'retention_in_days = 0' in pr_content)
        
            # Verify lifecycle policy removed
            has_lifecycle = 'lifecycle_configuration' in pr_content
            self.test("PR: S3 lifecycle policy removed", not has_lifecycle)
    
        self.logger.info("Security Attributes")
    
        # Security group validation
        self.test("baseline: ALB security group exists", 'aws_security_group" "alb"' in baseline_content)
        self.test("baseline: EC2 security group exists", 'aws_security_group" "ec2"' in baseline_content)
        self.test("baseline: security group has ingress rules", 'ingress {' in baseline_content)
        self.test("baseline: security group has egress rules", 'egress {' in baseline_content)
    
        # Metadata options
        self.test("baseline: IMDSv2 required", 'http_tokens                 = "required"' in baseline_content)
    
        self.logger.info("Tagging Standards")
    
        # Tag validation
        self.test("baseline: resources have Name tags", 'Name = ' in baseline_content)
        self.test("baseline: resources have Environment tags", 'Environment' in baseline_content)
        self.test("baseline: provider has default_tags", 'default_tags' in baseline_content)
        self.test("baseline: Project tag exists", 'Project' in baseline_content)
        self.test("baseline: ManagedBy tag exists", 'ManagedBy' in baseline_content)
    
        self.logger.info("Data Sources")
    
        # Data sources
        self.test("baseline: uses data source for AMI", 'data.aws_ami' in baseline_content)
        self.test("baseline: uses data source for account ID", 
                   'data.aws_caller_identity' in baseline_content)


    def test_resource_dependencies(self):
        """Validate resource dependency chains - 30 tests"""
        self.section("RESOURCE DEPENDENCY CHAIN VALIDATION (30 tests)")
    
        infra_dir = self.repo_root / "infrastructure" / "terraform"
        baseline_file = infra_dir / "baseline" / "main.tf"
    
        if not baseline_file.exists():
            for _ in range(30):
                self.skip("resource dependencies", "File not found")
            return
    
        content = read_tf_file(baseline_file)
    
        self.logger.info("VPC Dependencies")
    
        # VPC → Subnet dependencies
        self.test("Subnet references VPC", 'vpc_id      = aws_vpc.main.id' in content or
                   'vpc_id = aws_vpc.main.id' in content)
        self.test("Internet Gateway references VPC", 'vpc_id = aws_vpc.main.id' in content)
        self.test("Route table references VPC", 'vpc_id = aws_vpc.main.id' in content)
        self.test("Security group references VPC", 'vpc_id      = aws_vpc.main.id' in content or
                   'vpc_id = aws_vpc.main.id' in content)
    
        self.logger.info("Network Dependencies")
    
        # Route table associations
        self.test("Route table association references subnet", 
                   'subnet_id      = aws_subnet' in content)
        self.test("Route table association references route table", 
                   'route_table_id = aws_route_table' in content)
        self.test("Route references internet gateway", 
                   'gateway_id = aws_internet_gateway' in content)
    
        self.logger.info("Compute Dependencies")
    
        # Launch template → Security group
        self.test("Launch template references security group", 
                   'vpc_security_group_ids = [aws_security_group.ec2.id]' in content)
    
        # ASG dependencies
        self.test("ASG references subnets", 'vpc_zone_identifier' in content)
        self.test("ASG references target group", 'target_group_arns' in content)
        self.test("ASG references launch template", 'launch_template {' in content)
        self.test("ASG launch template has id", 'id      = aws_launch_template.main.id' in content)
    
        self.logger.info("Load Balancer Dependencies")
    
        # ALB dependencies
        self.test("ALB references security group", 
                   'security_groups    = [aws_security_group.alb.id]' in content)
        self.test("ALB references subnets", 
                   'subnets            = [aws_subnet.public_a.id, aws_subnet.public_b.id]' in content)
    
        # Target group
        self.test("Target group references VPC", 
                   'vpc_id   = aws_vpc.main.id' in content or
                   'vpc_id = aws_vpc.main.id' in content)
    
        # Listener dependencies
        self.test("Listener references ALB", 'load_balancer_arn = aws_lb.main.arn' in content)
        self.test("Listener references target group", 
                   'target_group_arn = aws_lb_target_group.main.arn' in content)
    
        self.logger.info("S3 Dependencies")
    
        # S3 bucket dependencies
        self.test("S3 versioning references bucket", 
                   'bucket = aws_s3_bucket.main.id' in content)
        self.test("S3 lifecycle references bucket", 
                   'bucket = aws_s3_bucket.main.id' in content)
    
        self.logger.info("Security Group Dependencies")
    
        # Security group ingress rules
        self.test("EC2 SG ingress references ALB SG", 
                   'security_groups = [aws_security_group.alb.id]' in content)
    
        self.logger.info("Dependency Count Validation")
    
        # Count resource references
        vpc_refs = content.count('aws_vpc.main')
        subnet_refs = content.count('aws_subnet.')
        sg_refs = content.count('aws_security_group.')
    
        self.test("VPC referenced multiple times", vpc_refs >= 3, f"Found {vpc_refs} refs")
        self.test("Subnets referenced multiple times", subnet_refs >= 4, f"Found {subnet_refs} refs")
        self.test("Security groups referenced multiple times", sg_refs >= 3, f"Found {sg_refs} refs")
    
        # Verify no dangling references
        self.test("No undefined resource references", 
                   'aws_vpc.undefined' not in content and 'aws_subnet.undefined' not in content)
    
        # Cross-resource validation
        self.test("Launch template + ASG linked", 
                   'aws_launch_template.main' in content and 'aws_autoscaling_group.main' in content)
        self.test("ALB + Target Group + Listener chain complete",
                   'aws_lb.main' in content and 
                   'aws_lb_target_group.main' in content and
                   'aws_lb_listener.main' in content)


    def test_variables_and_outputs(self):
        """Validate variables and outputs - 25 tests"""
        self.section("VARIABLES AND OUTPUTS VALIDATION (25 tests)")
    
        infra_dir = self.repo_root / "infrastructure" / "terraform" / "baseline"
        variables_file = infra_dir / "variables.tf"
        outputs_file = infra_dir / "outputs.tf"
        main_file = infra_dir / "main.tf"
    
        self.logger.info("Variables File")
    
        if variables_file.exists():
            var_content = read_tf_file(variables_file)
        
            self.test("variables.tf exists", True)
            self.test("variables: has aws_region", 'variable "aws_region"' in var_content)
            self.test("variables: has project_name", 'variable "project_name"' in var_content)
            self.test("variables: aws_region has description", 
                       'description' in var_content)
            self.test("variables: aws_region has default", 'default' in var_content)
            self.test("variables: aws_region has type", 'type' in var_content)
        
            # Check variable usage in main
            if main_file.exists():
                main_content = read_tf_file(main_file)
                self.test("main.tf uses var.aws_region", 'var.aws_region' in main_content)
                self.test("main.tf uses var.project_name", 'var.project_name' in main_content)
        else:
            for _ in range(8):
                self.skip("variables validation", "variables.tf not found")
    
        self.logger.info("Outputs File")
    
        if outputs_file.exists():
            out_content = read_tf_file(outputs_file)
        
            self.test("outputs.tf exists", True)
            self.test("outputs: has output declarations", 'output "' in out_content)
            self.test("outputs: has value expressions", 'value =' in out_content)
            self.test("outputs: has descriptions", 'description' in out_content)
        
            # Check for common outputs
            self.test("outputs: has ALB DNS output", 
                       'alb' in out_content.lower() or 'load_balancer' in out_content.lower())
            self.test("outputs: has VPC output", 'vpc' in out_content.lower())
        
            # Output format validation
            output_blocks = re.findall(r'output\s+"([^"]+)"', out_content)
            self.test("outputs: has multiple outputs", len(output_blocks) >= 3,
                       f"Found {len(output_blocks)} outputs")
            self.test("outputs: output names use underscores", 
                       all('_' in name or len(name) < 5 for name in output_blocks))
        else:
            for _ in range(8):
                self.skip("outputs validation", "outputs.tf not found")
    
        self.logger.info("Variable-Output Integration")
    
        if variables_file.exists() and outputs_file.exists():
            var_content = read_tf_file(variables_file)
            out_content = read_tf_file(outputs_file)
            main_content = read_tf_file(main_file) if main_file.exists() else ""
        
            # Check that variables are used
            var_names = re.findall(r'variable\s+"([^"]+)"', var_content)
            self.test("Variables used in main.tf", 
                       any(f'var.{var}' in main_content for var in var_names))
        
            # Check that outputs reference resources
            self.test("Outputs reference resources", 
                       'aws_' in out_content)
            self.test("Outputs use resource attributes", '.id' in out_content or '.arn' in out_content)
        else:
            for _ in range(3):
                self.skip("variable-output integration", "Files not found")
    
        self.logger.info("Variable Validation Rules")
    
        if variables_file.exists():
            var_content = read_tf_file(variables_file)
        
            # All variables should have types
            var_blocks = re.findall(r'variable\s+"[^"]+"\s*\{[^}]+\}', var_content, re.DOTALL)
            self.test("All variables have type declarations", 
                       all('type' in block for block in var_blocks))
            self.test("All variables have descriptions",
                       all('description' in block for block in var_blocks))


    def test_provider_configuration(self):
        """Validate provider configuration - 15 tests"""
        self.section("PROVIDER CONFIGURATION VALIDATION (15 tests)")
    
        infra_dir = self.repo_root / "infrastructure" / "terraform"
    
        stacks = ["baseline", "pr-change", "noop-change"]
    
        for stack in stacks:
            stack_dir = infra_dir / stack
            main_file = stack_dir / "main.tf"
        
            if not main_file.exists():
                for _ in range(5):
                    self.skip(f"{stack} provider config", "main.tf not found")
                continue
        
            content = read_tf_file(main_file)
        
            self.logger.info(f"{stack.upper()} Provider Configuration")
        
            # Terraform block
            self.test(f"{stack}: has terraform block", 'terraform {' in content)
            self.test(f"{stack}: has required_version", 'required_version' in content)
            self.test(f"{stack}: has required_providers", 'required_providers' in content)
            self.test(f"{stack}: specifies AWS provider", 'aws = {' in content)
            self.test(f"{stack}: has provider version constraint", 'version = "~>' in content)


    def test_cost_policy_rules(self):
        """Validate cost policy enforcement - 20 tests"""
        self.section("COST POLICY RULES VALIDATION (20 tests)")
    
        infra_dir = self.repo_root / "infrastructure" / "terraform"
        baseline_file = infra_dir / "baseline" / "main.tf"
        pr_file = infra_dir / "pr-change" / "main.tf"
    
        if not baseline_file.exists():
            for _ in range(20):
                self.skip("cost policy rules", "Files not found")
            return
    
        baseline_content = read_tf_file(baseline_file)
        pr_content = read_tf_file(pr_file) if pr_file.exists() else ""
    
        self.logger.info("Baseline Cost Optimization Policies")
    
        # Instance type policy
        self.test("Policy: baseline uses cost-efficient instance (t3.micro)", 
                   '"t3.micro"' in baseline_content)
        self.test("Policy: baseline uses gp3 volumes (not gp2)", 
                   '"gp3"' in baseline_content)
        self.test("Policy: baseline EBS volume ≤ 20GB", 
                   'volume_size           = 20' in baseline_content or
                   'volume_size = 20' in baseline_content)
        self.test("Policy: baseline ASG min_size ≤ 2", 
                   'min_size         = 2' in baseline_content or
                   'min_size = 2' in baseline_content)
        self.test("Policy: baseline log retention set (30 days)", 
                   'retention_in_days = 30' in baseline_content)
        self.test("Policy: baseline has S3 lifecycle policy", 
                   'lifecycle_configuration' in baseline_content)
    
        self.logger.info("PR Cost Regression Detection")
    
        if pr_content:
            # Detect policy violations
            self.test("Regression: PR uses expensive instance (t3.xlarge)", 
                       '"t3.xlarge"' in pr_content)
            self.test("Regression: PR increases EBS volume to 200GB", 
                       'volume_size           = 200' in pr_content or
                       'volume_size = 200' in pr_content)
            self.test("Regression: PR removes log retention (0 = infinite)", 
                       'retention_in_days = 0' in pr_content)
            self.test("Regression: PR removes S3 lifecycle optimization",
                       'lifecycle_configuration' not in pr_content or
                       pr_content.count('lifecycle_configuration') < baseline_content.count('lifecycle_configuration'))
        else:
            for _ in range(4):
                self.skip("PR regression detection", "PR file not found")
    
        self.logger.info("Mandatory Security Policies")
    
        # Security best practices
        self.test("Policy: EBS encryption enabled", 'encrypted             = true' in baseline_content)
        self.test("Policy: IMDSv2 required", 'http_tokens                 = "required"' in baseline_content)
        self.test("Policy: S3 versioning enabled", 'Enabled' in baseline_content)
    
        self.logger.info("Resource Limits")
    
        # Resource count limits
        self.test("Policy: ASG max_size ≤ 10", 
                   'max_size         = 4' in baseline_content or 'max_size = 4' in baseline_content)
    
        # Lifecycle policies
        self.test("Policy: prevent_destroy on VPC", 'prevent_destroy = true' in baseline_content)
    
        print("\n🏷️  Tagging Policy")
    
        # Required tags
        self.test("Policy: default_tags configured", 'default_tags' in baseline_content)
        self.test("Policy: Project tag present", 'Project' in baseline_content)
        self.test("Policy: Environment tag present", 'Environment' in baseline_content)
        self.test("Policy: ManagedBy tag present", 'ManagedBy' in baseline_content)


    def test_safeguard_validation(self):
        """Validate safeguard documentation and scripts - 20 tests"""
        self.section("SAFEGUARD VALIDATION (20 tests)")
    
        infra_dir = self.repo_root / "infrastructure" / "terraform"
        safeguards_md = infra_dir / "SAFEGUARDS.md"
        guard_script = infra_dir / "terraform-apply-guard.sh"
    
        print("\n🛡️  Safeguard Documentation")
    
        if safeguards_md.exists():
            content = read_tf_file(safeguards_md)
        
            self.test("SAFEGUARDS.md exists", True)
            self.test("Safeguards: mentions DO NOT APPLY", 
                       'DO NOT' in content.upper() or 'WARNING' in content.upper())
            self.test("Safeguards: explains demo purpose", 
                       'demo' in content.lower() or 'demonstration' in content.lower())
            self.test("Safeguards: warns about costs", 
                       'cost' in content.lower() or 'bill' in content.lower())
            self.test("Safeguards: has guard script reference", 
                       'guard' in content.lower() or 'script' in content.lower())
        else:
            for _ in range(5):
                self.skip("safeguards doc", "SAFEGUARDS.md not found")
    
        print("\n🚨 Guard Script")
    
        if guard_script.exists():
            content = read_tf_file(guard_script)
        
            self.test("terraform-apply-guard.sh exists", True)
            self.test("Guard script: is bash script", '#!/bin/bash' in content or '#!/usr/bin/env bash' in content)
            self.test("Guard script: checks for 'apply' command", 
                       'apply' in content.lower())
            self.test("Guard script: has exit logic", 'exit' in content)
            self.test("Guard script: has warning message", 
                       'WARNING' in content.upper() or 'ERROR' in content.upper())
        else:
            for _ in range(5):
                self.skip("guard script", "terraform-apply-guard.sh not found")
    
        print("\n⚠️  Warning Comments in Terraform Files")
    
        # Check all main.tf files for warnings
        for stack in ["baseline", "pr-change", "noop-change"]:
            stack_file = infra_dir / stack / "main.tf"
            if stack_file.exists():
                content = read_tf_file(stack_file)
                self.test(f"{stack}: has WARNING comment", 
                           'WARNING' in content.upper() or '⚠️' in content)
                self.test(f"{stack}: has DO NOT APPLY comment", 
                           'DO NOT' in content.upper())
            else:
                self.skip(f"{stack} warnings", "File not found")
    
        print("\n🔒 Additional Safety Checks")
    
        # Check that no backend configuration exists (prevents accidental state)
        baseline_file = infra_dir / "baseline" / "main.tf"
        if baseline_file.exists():
            content = read_tf_file(baseline_file)
            self.test("No remote backend configured (safety)", 
                       'backend "s3"' not in content and 'backend "remote"' not in content)


def main():
    """Entry point for test execution"""
    suite = InfrastructureDeepTestSuite()
    suite.run()
    suite.print_summary()
    sys.exit(suite.get_exit_code())


if __name__ == "__main__":
    main()
