#!/usr/bin/env python3
"""
Verify that snapshot hashes match the canonical hash.
"""

import json
import sys
from pathlib import Path

def verify_hashes():
    """Verify snapshot hashes match manifest."""
    repo_root = Path(__file__).parent.parent
    manifest_path = repo_root / 'snapshots' / 'hash_manifest.json'
    
    if not manifest_path.exists():
        print("❌ Hash manifest not found. Run compute_canonical_hash.py first.")
        return False
    
    with open(manifest_path) as f:
        manifest = json.load(f)
    
    print("Verifying snapshot hashes against manifest...")
    print("=" * 60)
    
    # Import the hash computation function
    sys.path.insert(0, str(repo_root / 'scripts'))
    from compute_canonical_hash import compute_file_hash
    
    snapshots_dir = repo_root / 'snapshots'
    all_match = True
    
    for filename, expected_hash in manifest['file_hashes'].items():
        filepath = snapshots_dir / filename
        if not filepath.exists():
            print(f"✗ {filename:30} MISSING")
            all_match = False
            continue
        
        actual_hash = compute_file_hash(filepath)
        if actual_hash == expected_hash:
            print(f"✓ {filename:30} {actual_hash[:16]}...")
        else:
            print(f"✗ {filename:30} HASH MISMATCH")
            print(f"  Expected: {expected_hash}")
            print(f"  Actual:   {actual_hash}")
            all_match = False
    
    print("=" * 60)
    
    if all_match:
        print("✅ All snapshots match canonical hash")
        print(f"   Canonical: {manifest['canonical_hash']}")
        return True
    else:
        print("❌ Hash verification failed - snapshots have drifted")
        return False


if __name__ == '__main__':
    success = verify_hashes()
    sys.exit(0 if success else 1)
