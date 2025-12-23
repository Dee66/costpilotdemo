#!/usr/bin/env python3
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

"""
Add lineage metadata to CostPilot Demo snapshots.
This script adds required lineage fields to all snapshot files.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path

# Repository root
REPO_ROOT = Path(__file__).parent.parent
SNAPSHOTS_DIR = REPO_ROOT / "snapshots"

def calculate_hash(file_path):
    """Calculate SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()[:16]  # First 16 chars

def add_lineage_to_json(file_path, scenario, source_plan=None):
    """Add lineage metadata to a JSON snapshot file."""
    print(f"Processing: {file_path.name}")
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Calculate hash before modification
    hash_before = calculate_hash(file_path)
    
    # Create lineage metadata
    lineage = {
        "source_plan": source_plan or f"infrastructure/terraform/{scenario}/",
        "scenario": scenario,
        "plan_time": "2025-12-06T16:47:00Z",
        "seed": "demo-v1-stable",
        "hash_before": hash_before,
        "hash_after": None  # Will be calculated after writing
    }
    
    # Add lineage to the appropriate location based on file structure
    if 'lineage' not in data:
        if 'format_version' in data and 'terraform_version' in data:
            # Terraform plan file - add at root level
            data['lineage'] = lineage
        elif 'format_version' in data and 'scenario_version' in data:
            # CostPilot output file (detect/predict/explain)
            data['lineage'] = lineage
        elif 'scenario_version' in data:
            # Simple format (diff, trend)
            data['lineage'] = lineage
        else:
            # Default: add at root
            data['lineage'] = lineage
    
    # Write back with formatting
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    # Calculate hash after modification
    hash_after = calculate_hash(file_path)
    
    # Update the hash_after field
    with open(file_path, 'r') as f:
        data = json.load(f)
    data['lineage']['hash_after'] = hash_after
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"  ✅ Added lineage (scenario: {scenario}, hash: {hash_after})")
    return hash_after

def add_lineage_to_text(file_path, scenario, extension='.tf'):
    """Add lineage metadata as comment header to text files."""
    print(f"Processing: {file_path.name}")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Calculate hash
    file_hash = calculate_hash(file_path)
    
    # Create comment header based on file type
    if extension in ['.tf', '.hcl']:
        comment_start = "# "
    elif extension in ['.diff', '.patch']:
        comment_start = "# "
    elif extension in ['.mmd']:
        comment_start = "%% "
    else:
        comment_start = "# "
    
    # Check if lineage already exists
    if 'LINEAGE METADATA' in content:
        print(f"  ⏭️  Lineage already present, skipping")
        return
    
    # Create lineage header
    lineage_header = f"""{comment_start}==================================================
{comment_start}LINEAGE METADATA
{comment_start}==================================================
{comment_start}source_plan: infrastructure/terraform/{scenario}/
{comment_start}scenario: {scenario}
{comment_start}plan_time: 2025-12-06T16:47:00Z
{comment_start}seed: demo-v1-stable
{comment_start}hash: {file_hash}
{comment_start}==================================================

"""
    
    # Prepend lineage header
    new_content = lineage_header + content
    
    with open(file_path, 'w') as f:
        f.write(new_content)
    
    print(f"  ✅ Added lineage comment header (scenario: {scenario}, hash: {file_hash})")

def main():
    """Add lineage metadata to all snapshot files."""
    print("=" * 60)
    print("Adding Lineage Metadata to CostPilot Demo Snapshots")
    print("=" * 60)
    print()
    
    # JSON snapshots with lineage
    json_snapshots = [
        ("plan_before.json", "baseline"),
        ("plan_after.json", "pr-change"),
        ("plan_diff.json", "pr-change"),
        ("detect_v1.json", "pr-change"),
        ("predict_v1.json", "pr-change"),
        ("explain_v1.json", "pr-change"),
        ("trend_history_v1.json", "pr-change"),
    ]
    
    print("📄 Processing JSON snapshots...")
    print()
    for filename, scenario in json_snapshots:
        file_path = SNAPSHOTS_DIR / filename
        if file_path.exists():
            add_lineage_to_json(file_path, scenario)
        else:
            print(f"  ⚠️  File not found: {filename}")
    
    print()
    print("📝 Processing text/code snapshots...")
    print()
    
    # Text/code snapshots with comment headers
    text_snapshots = [
        ("snippet_v1.tf", "pr-change", ".tf"),
        ("patch_v1.diff", "pr-change", ".diff"),
    ]
    
    for filename, scenario, ext in text_snapshots:
        file_path = SNAPSHOTS_DIR / filename
        if file_path.exists():
            add_lineage_to_text(file_path, scenario, ext)
        else:
            print(f"  ⚠️  File not found: {filename}")
    
    print()
    print("=" * 60)
    print("✅ Lineage metadata addition complete!")
    print("=" * 60)
    print()
    print("Summary:")
    print(f"  - JSON snapshots: {len(json_snapshots)} files processed")
    print(f"  - Text snapshots: {len(text_snapshots)} files processed")
    print()
    print("All snapshot files now include lineage metadata for")
    print("traceability, reproducibility, and drift detection.")

if __name__ == "__main__":
    main()
