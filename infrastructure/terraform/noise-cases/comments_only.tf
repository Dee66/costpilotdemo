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
