#!/bin/bash
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

# Generate Mapping Diagram
# Creates Mermaid diagram showing cross-service dependencies

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "Generating mapping diagram..."

# Generate Mermaid mapping with fixed layout seed
cat > "$REPO_ROOT/snapshots/mapping_v1.mmd" << 'EOF'
graph TD
    ALB[Application Load Balancer]
    TG[Target Group]
    ASG[Auto Scaling Group]
    EC2[EC2 Instances - t3.xlarge]
    EBS[EBS Volumes - 200GB]
    S3[S3 Bucket - No Lifecycle]
    CW[CloudWatch Logs - Infinite]
    
    ALB --> TG
    TG --> ASG
    ASG --> EC2
    EC2 --> EBS
    EC2 --> CW
    ASG --> S3
    
    style EC2 fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style EBS fill:#ffd93d,stroke:#f59f00,color:#000
    style S3 fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style CW fill:#ffd93d,stroke:#f59f00,color:#000
    
    classDef highCost fill:#ff6b6b,stroke:#c92a2a,color:#fff
    classDef mediumCost fill:#ffd93d,stroke:#f59f00,color:#000
EOF

# Copy to demo directory
cp "$REPO_ROOT/snapshots/mapping_v1.mmd" "$REPO_ROOT/.costpilot/demo/"
cp "$REPO_ROOT/snapshots/mapping_v1.mmd" "$REPO_ROOT/costpilot_artifacts/output_mapping.mmd"

echo "✓ Mapping diagram generated"
