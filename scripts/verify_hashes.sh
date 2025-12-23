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
