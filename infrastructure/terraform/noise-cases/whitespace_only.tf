# Noise Test Case: Whitespace Only Changes
#
# Purpose: Verify CostPilot does not flag whitespace-only changes
# Expected Output: No findings
#
# This file demonstrates noise resilience - CostPilot should recognize
# that whitespace changes have zero cost impact and produce no alerts.

resource "aws_instance" "test_whitespace" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"


  tags = {
    Name        = "whitespace-test"
    Environment = "demo"
    Purpose     = "noise-testing"
  }




}


# Trailing whitespace and blank lines should not trigger findings
