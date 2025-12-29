# Copyright (c) 2025 CostPilot Demo Team
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# ==================================================
# LINEAGE METADATA
# ==================================================
# source_plan: infrastructure/terraform/pr-change/
# scenario: pr-change
# plan_time: 2025-12-06T16:47:00Z
# seed: demo-v1-stable
# hash: 2ee40eba7073284d
# ==================================================

# CostPilot Autofix Snippets - Scenario v1
# Generated: 2025-12-06T16:47:00Z
# Findings: 4 cost regressions detected
# Autofix Mode: snippet (safe, deterministic)
#
# SCOPE LIMITATION:
# Autofix snippet mode only covers EC2 and S3 optimizations.
# CloudWatch retention and networking changes require broader
# context not available in deterministic snippet mode.
#
# Apply these snippets by copying the relevant sections into
# your Terraform configuration files.


# AUTOFIX #1: EC2 Instance Type Rightsizing

# Finding ID: detect-001
# Resource: aws_launch_template.main
# Regression: t3.micro → t3.xlarge (16x cost increase)
# Recommendation: Downgrade to t3.large (balanced performance/cost)
# Monthly Savings: ~$56.85
#
# BEFORE:
#   instance_type = "t3.xlarge"  # 4 vCPU, 16GB RAM, $0.1664/hr
#
# AFTER (Recommended):
resource "aws_launch_template" "main" {
  name_prefix   = "costpilot-demo-"
  image_id      = data.aws_ami.amazon_linux_2.id
  instance_type = "t3.large"  # 2 vCPU, 8GB RAM, $0.0832/hr
  
  # ... other configuration unchanged ...
  
  block_device_mappings {
    device_name = "/dev/xvda"
    ebs {
      volume_size           = 50  # See Autofix #2
      volume_type           = "gp3"
      delete_on_termination = true
      encrypted             = true
    }
  }
  
  metadata_options {
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }
  
  user_data = base64encode(<<-EOF
    #!/bin/bash
    yum update -y
    yum install -y httpd
    systemctl start httpd
    systemctl enable httpd
    echo "<h1>CostPilot Demo - Baseline</h1>" > /var/www/html/index.html
  EOF
  )
}

# ALTERNATIVE: If t3.large is still too large
# instance_type = "t3.medium"  # 2 vCPU, 4GB RAM, $0.0416/hr
# Monthly cost: 2 instances × 730hr × $0.0416 = $60.74/mo
# Savings vs t3.xlarge: $182.70/mo


# AUTOFIX #2: EBS Volume Rightsizing

# Finding ID: detect-002
# Resource: aws_launch_template.main (block_device_mappings)
# Regression: 20GB → 200GB (10x increase)
# Recommendation: Use 50GB (middle ground)
# Monthly Savings: ~$12.00
#
# BEFORE:
#   volume_size = 200  # $0.08/GB-month × 200GB × 2 = $32/mo
#
# AFTER (Recommended):
resource "aws_launch_template" "main" {
  # ... other configuration ...
  
  block_device_mappings {
    device_name = "/dev/xvda"
    
    ebs {
      volume_size           = 50  # Balanced size for web app
      volume_type           = "gp3"
      delete_on_termination = true
      encrypted             = true
      
      # Optional: Add IOPS and throughput if needed
      # iops       = 3000  # Default, sufficient for most workloads
      # throughput = 125   # MB/s, default
    }
  }
}

# RATIONALE:
# - 20GB may be too small for OS + application + logs
# - 200GB is excessive for stateless web application
# - 50GB provides comfortable headroom for growth
# - Cost: 2 instances × 50GB × $0.08 = $8/mo (vs $32/mo)


# AUTOFIX #3: S3 Lifecycle Policy Restoration

# Finding ID: detect-004
# Resource: aws_s3_bucket.main
# Regression: Lifecycle policy removed
# Recommendation: Restore lifecycle rules for cost optimization
# Monthly Savings: ~$20.00 (grows over time)
#
# BEFORE:
#   (No lifecycle configuration)
#
# AFTER (Recommended):
resource "aws_s3_bucket" "main" {
  bucket        = "costpilot-demo-bucket-${data.aws_caller_identity.current.account_id}"
  force_destroy = false
  
  tags = {
    Name        = "costpilot-demo-bucket"
    Environment = "baseline"
  }
}

resource "aws_s3_bucket_versioning" "main" {
  bucket = aws_s3_bucket.main.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

# RESTORE THIS RESOURCE:
resource "aws_s3_bucket_lifecycle_configuration" "main" {
  bucket = aws_s3_bucket.main.id
  
  rule {
    id     = "transition-old-objects"
    status = "Enabled"
    
    transition {
      days          = 90
      storage_class = "GLACIER_IR"  # Instant Retrieval for frequent access
    }
    
    transition {
      days          = 180
      storage_class = "GLACIER"  # Standard Glacier for archive
    }
    
    expiration {
      days = 365  # Optional: delete after 1 year if appropriate
    }
  }
  
  rule {
    id     = "cleanup-incomplete-uploads"
    status = "Enabled"
    
    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
  
  # Optional: Separate rule for non-current versions
  rule {
    id     = "expire-old-versions"
    status = "Enabled"
    
    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "GLACIER"
    }
    
    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }
}

# COST SAVINGS:
# - Objects >90 days old: S3 Standard ($0.023/GB) → Glacier IR ($0.004/GB) = 83% savings
# - Objects >180 days old: → Glacier ($0.0036/GB) = 84% savings
# - Estimated monthly savings: $20-40 depending on data age distribution


# AUTOFIX #4: CloudWatch Log Retention (Manual Fix Required)

# Finding ID: detect-003
# Resource: aws_cloudwatch_log_group.application
# Regression: 30 days → infinite retention
# Recommendation: Restore 30-day retention
# Monthly Savings: ~$145.00
#
# ⚠️  AUTOFIX NOT AVAILABLE - MANUAL REVIEW REQUIRED
#
# REASON: Log retention policies may affect:
# - Compliance and audit requirements
# - Legal data retention obligations
# - Security investigation capabilities
# - Incident post-mortem analysis
#
# MANUAL FIX:
# 1. Review your organization's log retention policy
# 2. Consult with compliance/security team
# 3. Apply appropriate retention based on requirements:

# For general application logs (recommended):
resource "aws_cloudwatch_log_group" "application" {
  name              = "/aws/costpilot-demo/application"
  retention_in_days = 30  # Restore 30-day retention
  
  tags = {
    Name        = "costpilot-demo-logs"
    Environment = "baseline"
  }
}

# For debug/development logs:
# retention_in_days = 7

# For audit/compliance logs:
# retention_in_days = 90  # or longer based on requirements

# For archived logs (alternative approach):
# retention_in_days = 7
# + Export to S3 with lifecycle to Glacier for long-term storage
# (More cost-effective than CloudWatch for >30 days retention)


# SUMMARY

#
# Autofix Coverage:
#   ✓ EC2 instance type (snippet provided)
#   ✓ EBS volume size (snippet provided)  
#   ✓ S3 lifecycle policy (snippet provided)
#   ✗ CloudWatch retention (manual fix required)
#
# Total Estimated Monthly Savings: $88.85 - $233.85
# - EC2 rightsizing: $56.85 - $182.70
# - EBS rightsizing: $12.00
# - S3 lifecycle: $20.00
# - CloudWatch: $145.00 (requires manual fix)
#
# Annual Savings: $1,066 - $2,806
#
# Next Steps:
# 1. Review and test snippets in non-production environment
# 2. Apply EC2/EBS/S3 fixes (safe, deterministic)
# 3. Consult compliance team for CloudWatch retention policy
# 4. Run terraform plan to verify changes
# 5. Monitor resource utilization after applying fixes
#
# Generated by: CostPilot v1.0.0 (autofix snippet mode)
# Confidence: High (EC2/EBS/S3), Manual review required (CloudWatch)

