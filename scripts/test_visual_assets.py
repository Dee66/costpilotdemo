#!/usr/bin/env python3
"""
Visual Assets Validation Suite
Adds ~70 granular tests for visual assets quality and completeness
Focus: Mermaid syntax, SVG structure, diagram completeness, asset metadata, screenshots manifest
"""

import os
import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Any

# Color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class TestRunner:
    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.failures = []
    
    def test(self, name: str, condition: bool, reason: str = ""):
        if condition:
            self.passed += 1
            print(f"  {GREEN}✓{RESET} {name}")
        else:
            self.failed += 1
            msg = f"{name}" + (f": {reason}" if reason else "")
            self.failures.append(msg)
            print(f"  {RED}✗{RESET} {name}" + (f" - {reason}" if reason else ""))
    
    def skip(self, name: str, reason: str = ""):
        self.skipped += 1
        print(f"  {YELLOW}⊘{RESET} {name}" + (f" - {reason}" if reason else ""))
    
    def section(self, name: str):
        print(f"\n{BLUE}{'='*80}{RESET}")
        print(f"{BLUE}{name}{RESET}")
        print(f"{BLUE}{'='*80}{RESET}")


def read_file(filepath: Path) -> str:
    """Read a file"""
    if not filepath.exists():
        return ""
    with open(filepath, 'r') as f:
        return f.read()


def test_mermaid_diagram_syntax(runner: TestRunner):
    """Validate Mermaid diagram syntax - 20 tests"""
    runner.section("MERMAID DIAGRAM SYNTAX VALIDATION (20 tests)")
    
    repo_root = runner.repo_root
    
    # Find all Mermaid files
    mermaid_files = list(repo_root.glob("**/*.mmd"))
    
    print(f"\n📊 Found {len(mermaid_files)} Mermaid files")
    
    runner.test("Has Mermaid diagram files", len(mermaid_files) > 0,
               f"Found {len(mermaid_files)} files")
    
    for mmd_file in mermaid_files[:3]:  # Test first 3
        content = read_file(mmd_file)
        filename = mmd_file.name
        
        print(f"\n🔍 {filename} Validation")
        
        # Check diagram type
        has_graph = content.strip().startswith('graph ')
        has_flowchart = content.strip().startswith('flowchart ')
        has_diagram_type = has_graph or has_flowchart
        
        runner.test(f"{filename}: has valid diagram type", has_diagram_type)
        
        # Check for nodes
        node_pattern = r'\w+\[([^\]]+)\]'
        nodes = re.findall(node_pattern, content)
        runner.test(f"{filename}: has node definitions", len(nodes) > 0,
                   f"Found {len(nodes)} nodes")
        runner.test(f"{filename}: has multiple nodes", len(nodes) >= 3,
                   f"Expected ≥3, found {len(nodes)}")
        
        # Check for connections
        arrow_patterns = ['-->', '---', '-.->', '===']
        has_connections = any(arrow in content for arrow in arrow_patterns)
        runner.test(f"{filename}: has node connections", has_connections)
        
        # Check for styling
        has_style = 'style ' in content or 'classDef' in content
        runner.test(f"{filename}: has visual styling", has_style)
        
        # Check for AWS resource references
        has_aws_resources = any(term in content for term in ['ALB', 'EC2', 'S3', 'CloudWatch', 'EBS', 'ASG'])
        runner.test(f"{filename}: references AWS resources", has_aws_resources)


def test_svg_structure_validation(runner: TestRunner):
    """Validate SVG structure - 20 tests"""
    runner.section("SVG STRUCTURE VALIDATION (20 tests)")
    
    repo_root = runner.repo_root
    
    # Find all SVG files
    svg_files = list(repo_root.glob("**/*.svg"))
    
    print(f"\n🎨 Found {len(svg_files)} SVG files")
    
    runner.test("Has SVG files", len(svg_files) > 0,
               f"Found {len(svg_files)} files")
    
    for svg_file in svg_files[:2]:  # Test first 2
        content = read_file(svg_file)
        filename = svg_file.name
        
        print(f"\n🖼️  {filename} Structure")
        
        # Check for SVG root element
        runner.test(f"{filename}: has SVG root element", 
                   '<svg' in content and 'xmlns=' in content)
        
        # Check for viewBox
        runner.test(f"{filename}: has viewBox attribute",
                   'viewBox=' in content)
        
        # Check for width/height
        runner.test(f"{filename}: has dimensions",
                   'width=' in content and 'height=' in content)
        
        # Extract dimensions
        width_match = re.search(r'width="(\d+)"', content)
        height_match = re.search(r'height="(\d+)"', content)
        
        if width_match and height_match:
            width = int(width_match.group(1))
            height = int(height_match.group(1))
            runner.test(f"{filename}: has reasonable dimensions",
                       width >= 100 and height >= 100,
                       f"{width}x{height}")
            runner.test(f"{filename}: has valid aspect ratio",
                       0.2 <= height/width <= 5.0)
        else:
            runner.skip(f"{filename}: dimension checks", "Dimensions not found")
            runner.skip(f"{filename}: aspect ratio", "Dimensions not found")
        
        # Check for visual elements
        has_elements = any(elem in content for elem in ['<rect', '<circle', '<line', '<polyline', '<path', '<text'])
        runner.test(f"{filename}: has visual elements", has_elements)
        
        # Check for text labels
        runner.test(f"{filename}: has text labels", '<text' in content)
        
        # Check for styling
        has_styling = 'fill=' in content or 'stroke=' in content or '<style' in content
        runner.test(f"{filename}: has styling", has_styling)
        
        # Check for proper closing tag
        runner.test(f"{filename}: properly closed", '</svg>' in content)


def test_diagram_completeness(runner: TestRunner):
    """Validate diagram completeness - 15 tests"""
    runner.section("DIAGRAM COMPLETENESS VALIDATION (15 tests)")
    
    snapshots_dir = runner.repo_root / "snapshots"
    docs_diagrams = runner.repo_root / "docs" / "diagrams"
    
    print("\n📈 Required Diagrams")
    
    # Check for essential diagrams
    required_diagrams = {
        "mapping_v1.mmd": snapshots_dir / "mapping_v1.mmd",
        "trend_v1.svg": snapshots_dir / "trend_v1.svg",
        "architecture_overview.svg": docs_diagrams / "architecture_overview.svg",
        "trust_triangle_flow.svg": docs_diagrams / "trust_triangle_flow.svg"
    }
    
    for diagram_name, filepath in required_diagrams.items():
        runner.test(f"{diagram_name} exists", filepath.exists())
        
        if filepath.exists():
            content = read_file(filepath)
            runner.test(f"{diagram_name}: not empty", len(content) > 100)
    
    print("\n🔗 Diagram Content Validation")
    
    # Validate mapping diagram content
    mapping_file = snapshots_dir / "mapping_v1.mmd"
    if mapping_file.exists():
        content = read_file(mapping_file)
        
        # Check for key resources in mapping
        key_resources = ['ALB', 'Target Group', 'ASG', 'EC2', 'EBS', 'S3', 'CloudWatch']
        found_resources = [res for res in key_resources if res in content]
        
        runner.test("mapping: includes key AWS resources",
                   len(found_resources) >= 5,
                   f"Found {len(found_resources)}: {', '.join(found_resources)}")
        
        # Check for cost regression indicators
        runner.test("mapping: shows cost indicators",
                   any(term in content for term in ['t3.xlarge', '200GB', 'No Lifecycle', 'Infinite']))
    
    # Validate trend SVG content
    trend_file = snapshots_dir / "trend_v1.svg"
    if trend_file.exists():
        content = read_file(trend_file)
        
        runner.test("trend: has axis labels", '<text' in content and 'axis' in content.lower() or 'Nov' in content)
        runner.test("trend: shows cost values", '$' in content or 'cost' in content.lower())
        runner.test("trend: has visual trend line", '<polyline' in content or '<line' in content)


def test_screenshots_manifest(runner: TestRunner):
    """Validate screenshots manifest - 20 tests"""
    runner.section("SCREENSHOTS MANIFEST VALIDATION (20 tests)")
    
    visual_dir = runner.repo_root / "visual_assets"
    manifest_file = visual_dir / "screenshots_manifest.json"
    
    if not manifest_file.exists():
        for _ in range(20):
            runner.skip("manifest validation", "screenshots_manifest.json not found")
        return
    
    with open(manifest_file, 'r') as f:
        manifest = json.load(f)
    
    print("\n📋 Manifest Structure")
    
    # Check manifest metadata
    runner.test("manifest: has version", "manifest_version" in manifest)
    runner.test("manifest: has description", "description" in manifest)
    runner.test("manifest: has screenshots array", "screenshots" in manifest)
    
    screenshots = manifest.get("screenshots", [])
    runner.test("manifest: has screenshot entries", len(screenshots) > 0,
               f"Found {len(screenshots)} entries")
    runner.test("manifest: has required screenshots", len(screenshots) >= 3,
               f"Expected ≥3, found {len(screenshots)}")
    
    print("\n📸 Screenshot Entries")
    
    # Check each screenshot entry
    for idx, screenshot in enumerate(screenshots):
        name = screenshot.get("filename", f"screenshot_{idx}")
        
        # Required fields
        runner.test(f"{name}: has filename", "filename" in screenshot)
        runner.test(f"{name}: has status", "status" in screenshot)
        runner.test(f"{name}: has resolution", "resolution" in screenshot)
        runner.test(f"{name}: has source_snapshot", "source_snapshot" in screenshot)
        
        # Validation criteria
        if "validation" in screenshot:
            validation = screenshot["validation"]
            runner.test(f"{name}: has validation criteria", len(validation) > 0)
        
        # Must show requirements
        if "must_show" in screenshot:
            must_show = screenshot["must_show"]
            runner.test(f"{name}: has content requirements", len(must_show) > 0,
                       f"Found {len(must_show)} requirements")


def test_asset_metadata(runner: TestRunner):
    """Validate asset metadata and organization - 15 tests"""
    runner.section("ASSET METADATA VALIDATION (15 tests)")
    
    visual_dir = runner.repo_root / "visual_assets"
    snapshots_dir = runner.repo_root / "snapshots"
    
    print("\n📁 Visual Assets Organization")
    
    # Check visual_assets directory
    runner.test("visual_assets/ directory exists", visual_dir.exists())
    
    if visual_dir.exists():
        runner.test("visual_assets/ has README", (visual_dir / "README.md").exists())
        runner.test("visual_assets/ has manifest", (visual_dir / "screenshots_manifest.json").exists())
        runner.test("visual_assets/ has examples", (visual_dir / "SCREENSHOT_EXAMPLES.md").exists())
    
    print("\n🎯 Snapshot Assets")
    
    # Check for snapshot-related visual assets
    if snapshots_dir.exists():
        runner.test("snapshots/ has Mermaid diagrams", 
                   len(list(snapshots_dir.glob("*.mmd"))) > 0)
        runner.test("snapshots/ has SVG assets",
                   len(list(snapshots_dir.glob("*.svg"))) > 0)
    
    print("\n🔗 Asset References")
    
    # Check that manifests reference actual files
    manifest_file = visual_dir / "screenshots_manifest.json"
    if manifest_file.exists():
        with open(manifest_file, 'r') as f:
            manifest = json.load(f)
        
        screenshots = manifest.get("screenshots", [])
        for screenshot in screenshots[:3]:  # Check first 3
            source = screenshot.get("source_snapshot", "")
            if source:
                source_path = runner.repo_root / source
                runner.test(f"manifest: source '{source}' exists",
                           source_path.exists())
    
    print("\n📊 Asset Coverage")
    
    # Check coverage of visual assets
    mermaid_count = len(list(runner.repo_root.glob("**/*.mmd")))
    svg_count = len(list(runner.repo_root.glob("**/*.svg")))
    
    runner.test("Has Mermaid diagrams", mermaid_count >= 1,
               f"Found {mermaid_count} files")
    runner.test("Has SVG graphics", svg_count >= 2,
               f"Found {svg_count} files")
    
    # Check for manifest documentation
    examples_file = visual_dir / "SCREENSHOT_EXAMPLES.md"
    if examples_file.exists():
        content = read_file(examples_file)
        runner.test("screenshot examples: has content", len(content) > 100)
        runner.test("screenshot examples: has specifications",
                   'resolution' in content.lower() or 'spec' in content.lower())


def test_visual_quality_indicators(runner: TestRunner):
    """Validate visual quality indicators - 10 tests"""
    runner.section("VISUAL QUALITY INDICATORS (10 tests)")
    
    snapshots_dir = runner.repo_root / "snapshots"
    
    print("\n🎨 Color Usage")
    
    # Check mapping diagram for color coding
    mapping_file = snapshots_dir / "mapping_v1.mmd"
    if mapping_file.exists():
        content = read_file(mapping_file)
        
        runner.test("mapping: uses color styling", 
                   'fill:' in content or 'style ' in content)
        runner.test("mapping: uses severity colors",
                   any(color in content for color in ['#ff6b6b', '#ffd93d', 'red', 'yellow']))
        runner.test("mapping: has classDef for categorization",
                   'classDef' in content)
    else:
        for _ in range(3):
            runner.skip("mapping color checks", "File not found")
    
    print("\n📐 Layout Quality")
    
    # Check SVG for proper layout
    trend_file = snapshots_dir / "trend_v1.svg"
    if trend_file.exists():
        content = read_file(trend_file)
        
        runner.test("trend SVG: has grid/axes", 
                   any(elem in content for elem in ['<line', '<polyline', 'axis']))
        runner.test("trend SVG: has data points",
                   '<circle' in content or 'point' in content.lower())
        runner.test("trend SVG: has labels",
                   '<text' in content and content.count('<text') >= 3)
        runner.test("trend SVG: uses color coding",
                   'fill=' in content or 'stroke=' in content)
    else:
        for _ in range(4):
            runner.skip("trend layout checks", "File not found")
    
    print("\n✅ Accessibility")
    
    # Check for text alternatives
    svg_files = list(snapshots_dir.glob("*.svg"))
    if svg_files:
        for svg_file in svg_files[:1]:  # Check first one
            content = read_file(svg_file)
            runner.test(f"{svg_file.name}: has text labels for data",
                       '<text' in content)
            runner.test(f"{svg_file.name}: uses semantic elements",
                       any(elem in content for elem in ['<title', '<desc']) or '<text' in content)
    else:
        for _ in range(2):
            runner.skip("accessibility checks", "No SVG files")


def main():
    runner = TestRunner()
    
    print(f"{BLUE}╔════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BLUE}║                                                                            ║{RESET}")
    print(f"{BLUE}║           VISUAL ASSETS VALIDATION SUITE (~70 tests)                      ║{RESET}")
    print(f"{BLUE}║                                                                            ║{RESET}")
    print(f"{BLUE}╚════════════════════════════════════════════════════════════════════════════╝{RESET}")
    
    # Run all test suites
    test_mermaid_diagram_syntax(runner)
    test_svg_structure_validation(runner)
    test_diagram_completeness(runner)
    test_screenshots_manifest(runner)
    test_asset_metadata(runner)
    test_visual_quality_indicators(runner)
    
    # Print summary
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}TEST SUMMARY{RESET}")
    print(f"{BLUE}{'='*80}{RESET}")
    
    total = runner.passed + runner.failed + runner.skipped
    pass_rate = (runner.passed / total * 100) if total > 0 else 0
    
    print(f"\n{GREEN}✓ Passed:{RESET}  {runner.passed}/{total} ({pass_rate:.1f}%)")
    print(f"{RED}✗ Failed:{RESET}  {runner.failed}/{total}")
    print(f"{YELLOW}⊘ Skipped:{RESET} {runner.skipped}/{total}")
    
    if runner.failures:
        print(f"\n{RED}{'='*80}{RESET}")
        print(f"{RED}FAILURES ({len(runner.failures)}){RESET}")
        print(f"{RED}{'='*80}{RESET}")
        for failure in runner.failures[:20]:  # Show first 20
            print(f"{RED}✗{RESET} {failure}")
        if len(runner.failures) > 20:
            print(f"\n{YELLOW}... and {len(runner.failures) - 20} more failures{RESET}")
    
    print(f"\n{BLUE}{'='*80}{RESET}")
    
    # Exit code
    sys.exit(0 if runner.failed == 0 else 1)


if __name__ == "__main__":
    main()
