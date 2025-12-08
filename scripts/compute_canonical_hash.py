#!/usr/bin/env python3
"""
Compute canonical hash for CostPilot demo snapshots.
Ensures deterministic, reproducible outputs.
"""

import hashlib
import json
from pathlib import Path


def compute_file_hash(filepath):
    """Compute SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def compute_canonical_hash():
    """Compute canonical hash from all snapshot files."""
    repo_root = Path(__file__).parent.parent
    snapshots_dir = repo_root / 'snapshots'
    
    # Files to include in canonical hash (in order)
    snapshot_files = [
        'plan_before.json',
        'plan_after.json',
        'plan_diff.json',
        'detect_v1.json',
        'predict_v1.json',
        'explain_v1.json',
        'snippet_v1.tf',
        'patch_v1.diff',
        'mapping_v1.mmd',
        'trend_history_v1.json',
        'trend_v1.svg'
    ]
    
    hashes = {}
    combined_hash = hashlib.sha256()
    
    print("Computing canonical hash for CostPilot Demo v1")
    print("=" * 60)
    
    for filename in snapshot_files:
        filepath = snapshots_dir / filename
        if filepath.exists():
            file_hash = compute_file_hash(filepath)
            hashes[filename] = file_hash
            combined_hash.update(file_hash.encode())
            print(f"✓ {filename:30} {file_hash[:16]}...")
        else:
            print(f"✗ {filename:30} MISSING")
            return None
    
    canonical_hash = combined_hash.hexdigest()
    
    print("=" * 60)
    print(f"Canonical Hash: {canonical_hash}")
    print("=" * 60)
    
    # Save hash manifest
    manifest = {
        'version': '1.0.0',
        'scenario_version': 'v1',
        'canonical_hash': canonical_hash,
        'file_hashes': hashes,
        'files_included': snapshot_files
    }
    
    manifest_path = snapshots_dir / 'hash_manifest.json'
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\n✓ Hash manifest saved: {manifest_path}")
    
    return canonical_hash


if __name__ == '__main__':
    canonical_hash = compute_canonical_hash()
    if canonical_hash:
        print(f"\n✅ Canonical hash computed successfully")
        print(f"   Hash: {canonical_hash}")
    else:
        print("\n❌ Failed to compute canonical hash (missing files)")
        exit(1)
