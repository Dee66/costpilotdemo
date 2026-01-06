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

# Noise Test Case: Comments Only Changes
#
# Purpose: Verify CostPilot does not flag comment-only changes
# Expected Output: No findings
#
# This file demonstrates that CostPilot focuses on actual resource
# changes and ignores documentation/comment updates.

# This is a new comment added in the PR
# Comments should not affect cost analysis
# Adding documentation does not change infrastructure cost

resource "aws_instance" "test_comments" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"  # Default cost-efficient type
  
  # New comment: This instance runs the demo workload
  # Another comment: Configured for low-cost operation
  
  tags = {
    Name        = "comments-test"
    Environment = "demo"
    Purpose     = "noise-testing"  # Comment update should not trigger findings
  }
}

# More comments added for documentation purposes
# These changes should result in zero cost findings
# CostPilot should recognize this as non-cost-impacting noise
