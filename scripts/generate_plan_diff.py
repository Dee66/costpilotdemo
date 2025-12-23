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
Generate a diff between baseline and pr-change Terraform plans.
Extracts key cost-related differences for CostPilot analysis.
"""

import json
import sys
from pathlib import Path

def extract_resource_changes(plan_data):
    """Extract resource changes from a Terraform plan."""
    changes = {}
    
    if not plan_data or 'resource_changes' not in plan_data:
        return changes
    
    for resource in plan_data.get('resource_changes', []):
        address = resource.get('address', '')
        change = resource.get('change', {})
        
        if change.get('actions') in [['create'], ['update'], ['delete']]:
            changes[address] = {
                'actions': change.get('actions'),
                'before': change.get('before'),
                'after': change.get('after')
            }
    
    return changes

def compare_plans(before_path, after_path):
    """Compare two Terraform plans and generate a diff."""
    with open(before_path) as f:
        before = json.load(f)
    
    with open(after_path) as f:
        after = json.load(f)
    
    before_changes = extract_resource_changes(before)
    after_changes = extract_resource_changes(after)
    
    diff = {
        'format_version': '1.0',
        'plan_comparison': {
            'baseline_resources': len(before_changes),
            'pr_change_resources': len(after_changes),
            'changes_detected': []
        }
    }
    
    # Find differences in resource configurations
    for address in after_changes:
        if address in before_changes:
            # Resource exists in both, check for modifications
            before_config = before_changes[address].get('after', {})
            after_config = after_changes[address].get('after', {})
            
            changes = []
            
            # Check instance type changes
            if before_config.get('instance_type') != after_config.get('instance_type'):
                changes.append({
                    'attribute': 'instance_type',
                    'before': before_config.get('instance_type'),
                    'after': after_config.get('instance_type'),
                    'cost_impact': 'high'
                })
            
            # Check EBS volume size changes
            before_ebs = {}
            after_ebs = {}
            
            if before_config.get('block_device_mappings'):
                bdm = before_config['block_device_mappings']
                if isinstance(bdm, list) and len(bdm) > 0 and isinstance(bdm[0], dict):
                    before_ebs = bdm[0].get('ebs', {}) if isinstance(bdm[0].get('ebs'), dict) else {}
            
            if after_config.get('block_device_mappings'):
                bdm = after_config['block_device_mappings']
                if isinstance(bdm, list) and len(bdm) > 0 and isinstance(bdm[0], dict):
                    after_ebs = bdm[0].get('ebs', {}) if isinstance(bdm[0].get('ebs'), dict) else {}
            
            if (isinstance(before_ebs, dict) and isinstance(after_ebs, dict) and 
                before_ebs.get('volume_size') != after_ebs.get('volume_size')):
                changes.append({
                    'attribute': 'ebs_volume_size',
                    'before': before_ebs.get('volume_size'),
                    'after': after_ebs.get('volume_size'),
                    'cost_impact': 'medium'
                })
            
            # Check CloudWatch retention
            if before_config.get('retention_in_days') != after_config.get('retention_in_days'):
                changes.append({
                    'attribute': 'log_retention_days',
                    'before': before_config.get('retention_in_days'),
                    'after': after_config.get('retention_in_days'),
                    'cost_impact': 'medium'
                })
            
            if changes:
                diff['plan_comparison']['changes_detected'].append({
                    'resource': address,
                    'changes': changes
                })
    
    # Check for lifecycle rule changes in S3
    for address in after_changes:
        if 's3_bucket_lifecycle' in address:
            # Check if lifecycle rule exists in before but not in after
            lifecycle_before = any('s3_bucket_lifecycle' in a for a in before_changes)
            lifecycle_after = any('s3_bucket_lifecycle' in a for a in after_changes)
            
            if lifecycle_before != lifecycle_after:
                diff['plan_comparison']['changes_detected'].append({
                    'resource': address,
                    'changes': [{
                        'attribute': 's3_lifecycle_configuration',
                        'before': 'enabled' if lifecycle_before else 'disabled',
                        'after': 'enabled' if lifecycle_after else 'disabled',
                        'cost_impact': 'high'
                    }]
                })
    
    return diff

def main():
    repo_root = Path(__file__).parent.parent
    before_path = repo_root / 'snapshots' / 'plan_before.json'
    after_path = repo_root / 'snapshots' / 'plan_after.json'
    output_path = repo_root / 'snapshots' / 'plan_diff.json'
    
    if not before_path.exists():
        print(f"Error: {before_path} not found", file=sys.stderr)
        sys.exit(1)
    
    if not after_path.exists():
        print(f"Error: {after_path} not found", file=sys.stderr)
        sys.exit(1)
    
    diff = compare_plans(before_path, after_path)
    
    with open(output_path, 'w') as f:
        json.dump(diff, f, indent=2)
    
    print(f"Generated plan diff: {output_path}")
    print(f"Changes detected: {len(diff['plan_comparison']['changes_detected'])}")

if __name__ == '__main__':
    main()
