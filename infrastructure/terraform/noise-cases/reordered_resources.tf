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
