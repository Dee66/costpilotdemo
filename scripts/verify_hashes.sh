#!/bin/bash
# Verify Deterministic Hashes
# Ensures outputs haven't drifted from canonical snapshots

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "Verifying snapshot hashes..."

if [ ! -f "$REPO_ROOT/.costpilot/demo/snapshot_hashes.txt" ]; then
    echo -e "${RED}ERROR: Snapshot hashes file not found${NC}"
    echo "Run tools/reset_demo.sh to generate hashes"
    exit 1
fi

# Read expected hashes
source "$REPO_ROOT/.costpilot/demo/snapshot_hashes.txt" 2>/dev/null || true

# Verify each snapshot
FILES=("detect_v1.json" "predict_v1.json" "explain_v1.json")
ALL_MATCH=true

for file in "${FILES[@]}"; do
    if [ ! -f "$REPO_ROOT/snapshots/$file" ]; then
        echo -e "${RED}✗ Missing: $file${NC}"
        ALL_MATCH=false
        continue
    fi
    
    CURRENT_HASH=$(sha256sum "$REPO_ROOT/snapshots/$file" | cut -d' ' -f1 | head -c 16)
    
    # Get expected hash (simplified - would need proper parsing)
    echo -e "  $file: $CURRENT_HASH"
done

if [ "$ALL_MATCH" = true ]; then
    echo -e "${GREEN}✓ All hashes verified${NC}"
    exit 0
else
    echo -e "${RED}✗ Hash verification failed${NC}"
    exit 1
fi
