#!/bin/bash
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
