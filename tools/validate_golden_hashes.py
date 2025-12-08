#!/usr/bin/env python3
"""
Validate golden output hashes against the manifest.
Used in CI and local development to detect drift.
"""

import json
import hashlib
import sys
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def calculate_hash(file_path):
    """Calculate SHA256 hash of a file (first 16 chars)."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()[:16]

def main():
    """Validate all golden outputs against manifest."""
    repo_root = Path(__file__).parent.parent
    manifest_path = repo_root / "snapshots" / "golden_outputs_manifest.json"
    
    print("=" * 60)
    print("Golden Output Hash Validation")
    print("=" * 60)
    print()
    
    # Load manifest
    if not manifest_path.exists():
        print(f"{Colors.RED}❌ ERROR: golden_outputs_manifest.json not found{Colors.NC}")
        sys.exit(1)
    
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    golden_outputs = manifest['golden_outputs']
    
    # Validate each golden output
    drift_detected = False
    validated_count = 0
    
    for output_name, output_info in golden_outputs.items():
        file_path = repo_root / output_info['file']
        expected_hash = output_info['hash']
        
        if not file_path.exists():
            print(f"{Colors.YELLOW}⚠️  SKIP: {output_name} - File not found: {file_path}{Colors.NC}")
            continue
        
        actual_hash = calculate_hash(file_path)
        
        if actual_hash == expected_hash:
            print(f"{Colors.GREEN}✅ PASS: {output_name}{Colors.NC}")
            print(f"   File: {output_info['file']}")
            print(f"   Hash: {actual_hash}")
            validated_count += 1
        else:
            print(f"{Colors.RED}❌ DRIFT: {output_name}{Colors.NC}")
            print(f"   File: {output_info['file']}")
            print(f"   Expected: {expected_hash}")
            print(f"   Actual:   {actual_hash}")
            print(f"   {Colors.YELLOW}See: docs/DRIFT_MANAGEMENT.md{Colors.NC}")
            drift_detected = True
        
        print()
    
    # Summary
    print("=" * 60)
    if drift_detected:
        print(f"{Colors.RED}❌ DRIFT DETECTED{Colors.NC}")
        print()
        print("Remediation steps:")
        print("  1. Review docs/DRIFT_MANAGEMENT.md")
        print("  2. Run: ./tools/reset_demo.sh")
        print("  3. Re-run this validation")
        print()
        print("For intentional changes:")
        print("  1. Document reason")
        print("  2. Update golden_outputs_manifest.json")
        print("  3. Get team sign-off")
        print("=" * 60)
        sys.exit(1)
    else:
        print(f"{Colors.GREEN}✅ ALL GOLDEN OUTPUTS VALIDATED{Colors.NC}")
        print()
        print(f"Validated: {validated_count}/{len(golden_outputs)} files")
        print("No drift detected - outputs match golden versions")
        print("=" * 60)
        sys.exit(0)

if __name__ == "__main__":
    main()
