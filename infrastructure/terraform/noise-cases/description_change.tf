# Noise Test Case: Description Changes
#
# Purpose: Verify CostPilot does not flag description-only changes
# Expected Output: No findings
#
# This file demonstrates that CostPilot recognizes metadata updates
# (descriptions, names, tags) as non-cost-impacting changes.

resource "aws_security_group" "test_description" {
  name        = "description-test-sg"
  description = "Updated description with more details about security group purpose and configuration"  # Changed from brief description
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP access - updated description for better documentation"  # Description updated
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic - clarified for compliance documentation"  # Description updated
  }
  
  tags = {
    Name        = "description-test-sg"
    Description = "Security group with updated descriptions"  # Tag value changed
    Purpose     = "noise-testing"
    Documentation = "Demonstrates description changes have no cost impact"  # New tag
  }
}

resource "aws_instance" "test_description_instance" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  
  tags = {
    Name        = "description-test-instance"
    Description = "Instance with enhanced documentation and clearer purpose description"  # Description improved
    Purpose     = "noise-testing"
    Notes       = "Tag descriptions updated for better team communication"  # New descriptive tag
  }
}

# Note: Only descriptions and non-cost-impacting metadata changed
# Resource types, sizes, and billable configurations remain identical
# CostPilot should produce zero findings
