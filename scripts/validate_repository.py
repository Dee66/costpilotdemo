#!/usr/bin/env python3
"""
Validate that all expected files exist and have reasonable sizes.
"""

from pathlib import Path
import json

def validate_repository():
    """Validate repository structure and content."""
    repo_root = Path(__file__).parent.parent
    
    print("CostPilot Demo - Repository Validation")
    print("=" * 60)
    
    checks_passed = 0
    checks_failed = 0
    
    # Check 1: Terraform stacks
    print("\n1. Terraform Stacks")
    for stack in ['baseline', 'pr-change', 'noop-change']:
        stack_dir = repo_root / 'infrastructure' / 'terraform' / stack
        if (stack_dir / 'main.tf').exists():
            print(f"   ✓ {stack}/main.tf exists")
            checks_passed += 1
        else:
            print(f"   ✗ {stack}/main.tf MISSING")
            checks_failed += 1
    
    # Check 2: Snapshots
    print("\n2. Snapshot Files")
    snapshot_files = [
        'plan_before.json', 'plan_after.json', 'plan_diff.json',
        'detect_v1.json', 'predict_v1.json', 'explain_v1.json',
        'snippet_v1.tf', 'patch_v1.diff', 'simulation_output.json',
        'mapping_v1.mmd', 'trend_history_v1.json', 'trend_v1.svg',
        'hash_manifest.json'
    ]
    
    for filename in snapshot_files:
        filepath = repo_root / 'snapshots' / filename
        if filepath.exists():
            size = filepath.stat().st_size
            if size > 100:  # Reasonable minimum size
                print(f"   ✓ {filename:30} ({size:,} bytes)")
                checks_passed += 1
            else:
                print(f"   ⚠ {filename:30} TOO SMALL ({size} bytes)")
                checks_failed += 1
        else:
            print(f"   ✗ {filename:30} MISSING")
            checks_failed += 1
    
    # Check 3: Trust Triangle validation
    print("\n3. Trust Triangle Outputs")
    for output_type in ['detect', 'predict', 'explain']:
        filepath = repo_root / 'snapshots' / f'{output_type}_v1.json'
        if filepath.exists():
            with open(filepath) as f:
                data = json.load(f)
            
            # Check for required keys
            key_map = {
                'detect': 'detection_results',
                'predict': 'prediction_results',
                'explain': 'explanation_results'
            }
            
            if key_map[output_type] in data:
                print(f"   ✓ {output_type}_v1.json has {key_map[output_type]}")
                checks_passed += 1
            else:
                print(f"   ✗ {output_type}_v1.json INVALID STRUCTURE")
                checks_failed += 1
    
    # Check 4: Documentation
    print("\n4. Documentation")
    doc_files = ['README.md', 'CONTRIBUTING.md', 'LICENSE']
    for filename in doc_files:
        filepath = repo_root / filename
        if filepath.exists():
            print(f"   ✓ {filename} exists")
            checks_passed += 1
        else:
            print(f"   ✗ {filename} MISSING")
            checks_failed += 1
    
    # Check 5: Scripts
    print("\n5. Scripts & Tools")
    scripts = [
        'tools/reset_demo.sh',
        'tools/update_progress.py',
        'scripts/compute_canonical_hash.py',
        'scripts/verify_hashes.py',
        'scripts/test_safeguards.sh'
    ]
    
    for script in scripts:
        filepath = repo_root / script
        if filepath.exists():
            print(f"   ✓ {script}")
            checks_passed += 1
        else:
            print(f"   ✗ {script} MISSING")
            checks_failed += 1
    
    # Check 6: CI/CD
    print("\n6. CI/CD Pipeline")
    ci_file = repo_root / '.github' / 'workflows' / 'costpilot-ci.yml'
    if ci_file.exists():
        print(f"   ✓ GitHub Actions workflow exists")
        checks_passed += 1
    else:
        print(f"   ✗ GitHub Actions workflow MISSING")
        checks_failed += 1
    
    # Check 7: Safeguards
    print("\n7. Safeguards")
    safeguards = [
        '.git/hooks/pre-commit',
        'infrastructure/terraform/SAFEGUARDS.md'
    ]
    
    for safeguard in safeguards:
        filepath = repo_root / safeguard
        if filepath.exists():
            print(f"   ✓ {safeguard}")
            checks_passed += 1
        else:
            print(f"   ✗ {safeguard} MISSING")
            checks_failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Validation Results:")
    print(f"  ✓ Passed: {checks_passed}")
    print(f"  ✗ Failed: {checks_failed}")
    print(f"  Total:   {checks_passed + checks_failed}")
    print(f"  Success Rate: {checks_passed / (checks_passed + checks_failed) * 100:.1f}%")
    print("=" * 60)
    
    return checks_failed == 0


if __name__ == '__main__':
    import sys
    success = validate_repository()
    sys.exit(0 if success else 1)
