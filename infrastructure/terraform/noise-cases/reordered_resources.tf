# Noise Test Case: Reordered Resources
#
# Purpose: Verify CostPilot does not flag resource reordering
# Expected Output: No findings
#
# This file demonstrates that CostPilot recognizes resource reordering
# as a refactoring operation with zero cost impact.

# Resources defined in different order but functionally identical
# Order changed from: instance -> bucket -> security_group
# To: security_group -> bucket -> instance

resource "aws_security_group" "test_reorder_sg" {
  name        = "reorder-test-sg"
  description = "Security group for reorder test"
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name    = "reorder-test-sg"
    Purpose = "noise-testing"
  }
}

resource "aws_s3_bucket" "test_reorder_bucket" {
  bucket = "costpilot-demo-reorder-test"
  
  tags = {
    Name    = "reorder-test-bucket"
    Purpose = "noise-testing"
  }
}

resource "aws_instance" "test_reorder_instance" {
  ami             = "ami-0c55b159cbfafe1f0"
  instance_type   = "t3.micro"
  security_groups = [aws_security_group.test_reorder_sg.name]
  
  tags = {
    Name    = "reorder-test-instance"
    Purpose = "noise-testing"
  }
}

# Note: Resource order changed but dependencies and cost remain identical
# CostPilot should produce zero findings for this refactoring
