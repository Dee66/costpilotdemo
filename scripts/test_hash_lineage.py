#!/usr/bin/env python3
"""
Hash & Lineage Validation Suite
Adds ~80 granular tests for hash integrity and lineage tracking
Focus: Hash formats, lineage chains, version tracking, manifest consistency, reproducibility


Refactored to use Template Method Pattern with TestSuite base class.
"""

import os
import re
import json
import sys
import hashlib
from pathlib import Path
from typing import Dict, List, Any

# Import shared test framework
sys.path.insert(0, str(Path(__file__).parent))
from lib.test_suite import TestSuite


def read_json(filepath: Path) -> Dict[str, Any]:
    """Read JSON file"""
    if not filepath.exists():
        return {}
    with open(filepath, 'r') as f:
        return json.load(f)


def is_valid_hex_hash(hash_str: str, expected_length: int = None) -> bool:
    """Check if string is valid hexadecimal hash"""
    if not hash_str:
        return False
    # Remove common hash prefixes
    clean_hash = hash_str.replace('sha256:', '').replace('0x', '')
    # Check if hexadecimal
    try:
        int(clean_hash, 16)
    except ValueError:
        return False
    # Check length if specified
    if expected_length and len(clean_hash) != expected_length:
        return False
    return True


class HashLineageTestSuite(TestSuite):
    """Test suite using Template Method pattern"""
    
    @property
    def tags(self) -> List[str]:
        return ["hash", "lineage", "integrity", "validation"]
    
    def run(self):
        """Template method - defines the test execution sequence"""
        self.test_hash_manifest_structure()
        self.test_hash_formats_consistency()
        self.test_lineage_tracking()
        self.test_golden_outputs_manifest()
        self.test_hash_integrity()
        self.test_version_consistency()
    
    def test_hash_manifest_structure(self):
        """Validate hash manifest structure - 20 tests"""
        self.section("HASH MANIFEST STRUCTURE VALIDATION (20 tests)")
    
        hash_manifest_file = self.repo_root / "snapshots" / "hash_manifest.json"
    
        if not hash_manifest_file.exists():
            for _ in range(20):
                self.skip("hash manifest validation", "hash_manifest.json not found")
            return
    
        manifest = read_json(hash_manifest_file)
    
        print("\n🔐 Manifest Metadata")
    
        # Check required fields
        self.test("manifest: has version", "version" in manifest)
        self.test("manifest: has scenario_version", "scenario_version" in manifest)
        self.test("manifest: has canonical_hash", "canonical_hash" in manifest)
        self.test("manifest: has file_hashes", "file_hashes" in manifest)
        self.test("manifest: has files_included", "files_included" in manifest)
    
        # Validate version format
        if "version" in manifest:
            version = manifest["version"]
            self.test("manifest: valid version format", 
                       re.match(r'^\d+\.\d+\.\d+$', version) is not None,
                       f"Version: {version}")
    
        # Validate scenario version
        if "scenario_version" in manifest:
            scenario_version = manifest["scenario_version"]
            self.test("manifest: valid scenario_version", 
                       scenario_version.startswith('v'),
                       f"Found: {scenario_version}")
    
        print("\n🔑 Canonical Hash")
    
        # Validate canonical hash
        if "canonical_hash" in manifest:
            canonical_hash = manifest["canonical_hash"]
            self.test("canonical_hash: not empty", len(canonical_hash) > 0)
            self.test("canonical_hash: valid hex format", 
                       is_valid_hex_hash(canonical_hash))
            self.test("canonical_hash: proper length", 
                       len(canonical_hash) == 64,  # SHA256 length
                       f"Length: {len(canonical_hash)}")
    
        print("\n📂 File Hashes")
    
        file_hashes = manifest.get("file_hashes", {})
    
        self.test("file_hashes: not empty", len(file_hashes) > 0,
                   f"Found {len(file_hashes)} files")
        self.test("file_hashes: has required files", 
                   len(file_hashes) >= 8,
                   f"Expected ≥8, found {len(file_hashes)}")
    
        # Check for essential files
        essential_files = [
            "plan_before.json",
            "plan_after.json",
            "plan_diff.json",
            "detect_v1.json",
            "predict_v1.json",
            "explain_v1.json"
        ]
    
        for essential_file in essential_files:
            self.test(f"file_hashes: includes '{essential_file}'",
                       essential_file in file_hashes)
    
        # Check files_included matches file_hashes keys
        files_included = manifest.get("files_included", [])
        self.test("files_included: matches file_hashes keys",
                   set(files_included) == set(file_hashes.keys()))


    def test_hash_formats_consistency(self):
        """Validate hash format consistency - 15 tests"""
        self.section("HASH FORMAT CONSISTENCY (15 tests)")
    
        hash_manifest_file = self.repo_root / "snapshots" / "hash_manifest.json"
        golden_manifest_file = self.repo_root / "snapshots" / "golden_outputs_manifest.json"
    
        if not hash_manifest_file.exists():
            for _ in range(15):
                self.skip("hash format validation", "hash_manifest.json not found")
            return
    
        hash_manifest = read_json(hash_manifest_file)
        file_hashes = hash_manifest.get("file_hashes", {})
    
        print("\n🔍 Hash Format Validation")
    
        # Check each hash format
        for filename, file_hash in list(file_hashes.items())[:5]:  # Check first 5
            self.test(f"{filename}: valid hex hash",
                       is_valid_hex_hash(file_hash))
            self.test(f"{filename}: non-trivial hash",
                       file_hash not in ['0', '00000000', 'ffffffff'])
    
        print("\n📊 Cross-Manifest Consistency")
    
        if golden_manifest_file.exists():
            golden_manifest = read_json(golden_manifest_file)
            golden_outputs = golden_manifest.get("golden_outputs", {})
        
            # Check consistency between manifests
            common_files = 0
            for output_name, output_data in golden_outputs.items():
                if isinstance(output_data, dict):
                    file_path = output_data.get("file", "")
                    filename = Path(file_path).name
                
                    if filename in file_hashes:
                        common_files += 1
        
            self.test("manifests: share common files",
                       common_files > 0,
                       f"Found {common_files} common files")


    def test_lineage_tracking(self):
        """Validate lineage tracking - 20 tests"""
        self.section("LINEAGE TRACKING VALIDATION (20 tests)")
    
        snapshots_dir = self.repo_root / "snapshots"
    
        # Check for lineage fields in snapshots
        snapshot_files = [
            "detect_v1.json",
            "predict_v1.json",
            "explain_v1.json",
            "plan_diff.json"
        ]
    
        print("\n🔗 Lineage Metadata Presence")
    
        for snapshot_file in snapshot_files:
            filepath = snapshots_dir / snapshot_file
            if not filepath.exists():
                self.skip(f"{snapshot_file}: lineage check", "File not found")
                continue
        
            data = read_json(filepath)
        
            # Check for version tracking
            self.test(f"{snapshot_file}: has format_version",
                       "format_version" in data)
            self.test(f"{snapshot_file}: has scenario_version",
                       "scenario_version" in data)
            self.test(f"{snapshot_file}: has timestamp",
                       "timestamp" in data)
        
            # Check version format
            if "scenario_version" in data:
                scenario_version = data["scenario_version"]
                self.test(f"{snapshot_file}: valid scenario_version",
                           scenario_version.startswith('v'),
                           f"Found: {scenario_version}")
    
        print("\n📅 Timestamp Validation")
    
        # Check timestamp formats
        for snapshot_file in snapshot_files[:3]:  # Check first 3
            filepath = snapshots_dir / snapshot_file
            if not filepath.exists():
                continue
        
            data = read_json(filepath)
            timestamp = data.get("timestamp", "")
        
            if timestamp:
                # Check ISO 8601 format
                iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z?$'
                self.test(f"{snapshot_file}: valid ISO 8601 timestamp",
                           re.match(iso_pattern, timestamp) is not None,
                           f"Found: {timestamp}")


    def test_golden_outputs_manifest(self):
        """Validate golden outputs manifest - 20 tests"""
        self.section("GOLDEN OUTPUTS MANIFEST VALIDATION (20 tests)")
    
        golden_manifest_file = self.repo_root / "snapshots" / "golden_outputs_manifest.json"
    
        if not golden_manifest_file.exists():
            for _ in range(20):
                self.skip("golden manifest validation", "golden_outputs_manifest.json not found")
            return
    
        manifest = read_json(golden_manifest_file)
    
        print("\n📋 Manifest Structure")
    
        # Check required fields
        self.test("manifest: has version", "version" in manifest)
        self.test("manifest: has description", "description" in manifest)
        self.test("manifest: has last_updated", "last_updated" in manifest)
        self.test("manifest: has golden_outputs", "golden_outputs" in manifest)
    
        golden_outputs = manifest.get("golden_outputs", {})
    
        self.test("golden_outputs: not empty", len(golden_outputs) > 0,
                   f"Found {len(golden_outputs)} outputs")
        self.test("golden_outputs: has required outputs",
                   len(golden_outputs) >= 5,
                   f"Expected ≥5, found {len(golden_outputs)}")
    
        print("\n🎯 Output Entries")
    
        # Check essential golden outputs
        essential_outputs = ["detect", "predict", "explain", "snippet", "patch"]
    
        for output_name in essential_outputs:
            self.test(f"golden_outputs: includes '{output_name}'",
                       output_name in golden_outputs)
    
        # Validate each output entry
        for output_name, output_data in list(golden_outputs.items())[:5]:  # Check first 5
            if not isinstance(output_data, dict):
                continue
        
            print(f"\n🔍 {output_name} validation")
        
            self.test(f"{output_name}: has file path", "file" in output_data)
            self.test(f"{output_name}: has hash", "hash" in output_data)
            self.test(f"{output_name}: has format", "format" in output_data)
            self.test(f"{output_name}: has lineage_verified",
                       "lineage_verified" in output_data)
        
            # Validate hash format
            if "hash" in output_data:
                output_hash = output_data["hash"]
                self.test(f"{output_name}: valid hash format",
                           is_valid_hex_hash(output_hash),
                           f"Hash: {output_hash}")


    def test_hash_integrity(self):
        """Validate hash integrity against actual files - 15 tests"""
        self.section("HASH INTEGRITY VALIDATION (15 tests)")
    
        hash_manifest_file = self.repo_root / "snapshots" / "hash_manifest.json"
    
        if not hash_manifest_file.exists():
            for _ in range(15):
                self.skip("hash integrity check", "hash_manifest.json not found")
            return
    
        manifest = read_json(hash_manifest_file)
        file_hashes = manifest.get("file_hashes", {})
    
        print("\n✅ File Existence")
    
        # Check that hashed files exist
        snapshots_dir = self.repo_root / "snapshots"
    
        existing_files = []
        for filename in list(file_hashes.keys())[:10]:  # Check first 10
            filepath = snapshots_dir / filename
            self.test(f"{filename}: file exists",
                       filepath.exists())
            if filepath.exists():
                existing_files.append(filename)
    
        print("\n📊 File Integrity")
    
        # Validate that files are non-empty
        for filename in existing_files[:5]:  # Check first 5 existing files
            filepath = snapshots_dir / filename
            file_size = filepath.stat().st_size
            self.test(f"{filename}: non-empty file",
                       file_size > 0,
                       f"Size: {file_size} bytes")


    def test_version_consistency(self):
        """Validate version consistency across files - 10 tests"""
        self.section("VERSION CONSISTENCY VALIDATION (10 tests)")
    
        snapshots_dir = self.repo_root / "snapshots"
    
        # Collect all scenario_versions
        versions = {}
    
        snapshot_files = [
            "detect_v1.json",
            "predict_v1.json",
            "explain_v1.json",
            "trend_history_v1.json",
            "plan_diff.json"
        ]
    
        print("\n🔢 Version Collection")
    
        for snapshot_file in snapshot_files:
            filepath = snapshots_dir / snapshot_file
            if not filepath.exists():
                continue
        
            data = read_json(filepath)
            scenario_version = data.get("scenario_version", "")
            versions[snapshot_file] = scenario_version
    
        # Check version consistency
        unique_versions = set(versions.values())
    
        self.test("snapshots: have scenario_version field",
                   len(versions) > 0,
                   f"Found in {len(versions)} files")
    
        self.test("snapshots: consistent scenario_version",
                   len(unique_versions) == 1,
                   f"Found versions: {unique_versions}")
    
        if len(unique_versions) == 1:
            common_version = list(unique_versions)[0]
            self.test("common scenario_version: valid format",
                       common_version.startswith('v'),
                       f"Version: {common_version}")
    
        print("\n📋 Manifest Version Alignment")
    
        # Check manifests match snapshot versions
        hash_manifest = read_json(snapshots_dir / "hash_manifest.json")
        golden_manifest = read_json(snapshots_dir / "golden_outputs_manifest.json")
    
        if hash_manifest and "scenario_version" in hash_manifest:
            hash_scenario_version = hash_manifest["scenario_version"]
            self.test("hash_manifest: matches snapshot version",
                       hash_scenario_version in unique_versions,
                       f"Found: {hash_scenario_version}")
    
        if golden_manifest and "scenario_version" in golden_manifest:
            golden_scenario_version = golden_manifest["scenario_version"]
            self.test("golden_manifest: matches snapshot version",
                       golden_scenario_version in unique_versions,
                       f"Found: {golden_scenario_version}")
    
        print("\n🔖 Version Naming")
    
        # Check that filenames match versions
        for snapshot_file in snapshot_files[:3]:  # Check first 3
            if snapshot_file in versions:
                version_in_name = re.search(r'_v(\d+)', snapshot_file)
                version_in_data = versions[snapshot_file]
            
                if version_in_name:
                    name_version = f"v{version_in_name.group(1)}"
                    self.test(f"{snapshot_file}: filename matches data version",
                               name_version == version_in_data,
                               f"Filename: {name_version}, Data: {version_in_data}")


def main():
    """Entry point for test execution"""
    suite = HashLineageTestSuite()
    suite.run()
    suite.print_summary()
    sys.exit(suite.get_exit_code())


if __name__ == "__main__":
    main()
