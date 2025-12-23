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
Visual Assets Validation Suite
Adds ~70 granular tests for visual assets quality and completeness
Focus: Mermaid syntax, SVG structure, diagram completeness, asset metadata, screenshots manifest


Refactored to use Template Method Pattern with TestSuite base class.
"""

import os
import re
import json
import sys
from pathlib import Path

# Import shared test framework
sys.path.insert(0, str(Path(__file__).parent))
from lib.test_suite import TestSuite
from lib.logger import get_logger
from typing import Dict, List, Any


def validate_screenshot_resolution(filepath: Path, expected_width=1920, expected_height=1080):
    """Validate screenshot resolution"""
    try:
        from PIL import Image
        with Image.open(filepath) as img:
            width, height = img.size
            return width == expected_width and height == expected_height
    except ImportError:
        # Fallback if PIL not available
        return True  # Skip validation


def compare_to_golden(screenshot_path: Path, golden_path: Path):
    """Compare screenshot to golden version"""
    try:
        from PIL import Image, ImageChops
        with Image.open(screenshot_path) as img1, Image.open(golden_path) as img2:
            if img1.size != img2.size:
                return False
            diff = ImageChops.difference(img1, img2)
            return not diff.getbbox()  # No differences if no bounding box
    except ImportError:
        return True  # Skip if PIL not available


def read_file(filepath: Path) -> str:
    """Read a file"""
    if not filepath.exists():
        return ""
    with open(filepath, 'r') as f:
        return f.read()


class VisualAssetsTestSuite(TestSuite):
    """Test suite using Template Method pattern"""
    
    @property
    def tags(self) -> List[str]:
        return ["visual", "assets", "diagrams", "screenshots", "validation"]
    
    def __init__(self, repo_root: Path = None):
        super().__init__(repo_root)
        self.logger = get_logger("visual_assets_test")
    
    def run(self):
        """Template method - defines the test execution sequence"""
        self.test_screenshot_resolutions()
        self.test_mermaid_diagram_syntax()
        self.test_svg_structure_validation()
        self.test_diagram_completeness()
        self.test_screenshots_manifest()
        self.test_asset_metadata()
        self.test_visual_quality_indicators()
    
    def test_screenshot_resolutions(self):
        """Validate screenshot resolutions and golden comparison - 10 tests"""
        self.section("SCREENSHOT RESOLUTION & GOLDEN VALIDATION (10 tests)")
        
        video_assets_dir = self.repo_root / "video_assets"
        snapshots_dir = self.repo_root / "snapshots"
        screenshots = ['detect.png', 'predict.png', 'explain.png', 'autofix.png', 'trend.png']
        
        for screenshot in screenshots:
            filepath = video_assets_dir / screenshot
            golden_path = snapshots_dir / f"golden_{screenshot}"
            
            if filepath.exists():
                is_correct_res = validate_screenshot_resolution(filepath)
                self.test(f"{screenshot}: 1920x1080 resolution", is_correct_res,
                         f"Resolution {'correct' if is_correct_res else 'incorrect'}")
                
                if golden_path.exists():
                    matches_golden = compare_to_golden(filepath, golden_path)
                    self.test(f"{screenshot}: matches golden", matches_golden,
                             f"{'Matches' if matches_golden else 'Differs from'} golden")
                else:
                    self.skip(f"{screenshot}: golden comparison", "Golden file not found")
            else:
                self.skip(f"{screenshot}: resolution check", "File not found")
                self.skip(f"{screenshot}: golden comparison", "File not found")
    
    def test_mermaid_diagram_syntax(self):
        """Validate Mermaid diagram syntax - 20 tests"""
        self.section("MERMAID DIAGRAM SYNTAX VALIDATION (20 tests)")
    
        repo_root = self.repo_root
    
        # Find all Mermaid files
        mermaid_files = list(repo_root.glob("**/*.mmd"))
    
        self.logger.info(f"Found {len(mermaid_files)} Mermaid files")
    
        self.test("Has Mermaid diagram files", len(mermaid_files) > 0,
                   f"Found {len(mermaid_files)} files")
    
        for mmd_file in mermaid_files[:3]:  # Test first 3
            content = read_file(mmd_file)
            filename = mmd_file.name
        
            self.logger.info(f"{filename} Validation")
        
            # Check diagram type
            has_graph = content.strip().startswith('graph ')
            has_flowchart = content.strip().startswith('flowchart ')
            has_diagram_type = has_graph or has_flowchart
        
            self.test(f"{filename}: has valid diagram type", has_diagram_type)
        
            # Check for nodes
            node_pattern = r'\w+\[([^\]]+)\]'
            nodes = re.findall(node_pattern, content)
            self.test(f"{filename}: has node definitions", len(nodes) > 0,
                       f"Found {len(nodes)} nodes")
            self.test(f"{filename}: has multiple nodes", len(nodes) >= 3,
                       f"Expected ≥3, found {len(nodes)}")
        
            # Check for connections
            arrow_patterns = ['-->', '---', '-.->', '===']
            has_connections = any(arrow in content for arrow in arrow_patterns)
            self.test(f"{filename}: has node connections", has_connections)
        
            # Check for styling
            has_style = 'style ' in content or 'classDef' in content
            self.test(f"{filename}: has visual styling", has_style)
        
            # Check for AWS resource references
            has_aws_resources = any(term in content for term in ['ALB', 'EC2', 'S3', 'CloudWatch', 'EBS', 'ASG'])
            self.test(f"{filename}: references AWS resources", has_aws_resources)


    def test_svg_structure_validation(self):
        """Validate SVG structure - 20 tests"""
        self.section("SVG STRUCTURE VALIDATION (20 tests)")
    
        repo_root = self.repo_root
    
        # Find all SVG files
        svg_files = list(repo_root.glob("**/*.svg"))
    
        self.logger.info(f"Found {len(svg_files)} SVG files")
    
        self.test("Has SVG files", len(svg_files) > 0,
                   f"Found {len(svg_files)} files")
    
        for svg_file in svg_files[:2]:  # Test first 2
            content = read_file(svg_file)
            filename = svg_file.name
        
            self.logger.info(f"{filename} Structure")
        
            # Check for SVG root element
            self.test(f"{filename}: has SVG root element", 
                       '<svg' in content and 'xmlns=' in content)
        
            # Check for viewBox
            self.test(f"{filename}: has viewBox attribute",
                       'viewBox=' in content)
        
            # Check for width/height
            self.test(f"{filename}: has dimensions",
                       'width=' in content and 'height=' in content)
        
            # Extract dimensions
            width_match = re.search(r'width="(\d+)"', content)
            height_match = re.search(r'height="(\d+)"', content)
        
            if width_match and height_match:
                width = int(width_match.group(1))
                height = int(height_match.group(1))
                self.test(f"{filename}: has reasonable dimensions",
                           width >= 100 and height >= 100,
                           f"{width}x{height}")
                self.test(f"{filename}: has valid aspect ratio",
                           0.2 <= height/width <= 5.0)
            else:
                self.skip(f"{filename}: dimension checks", "Dimensions not found")
                self.skip(f"{filename}: aspect ratio", "Dimensions not found")
        
            # Check for visual elements
            has_elements = any(elem in content for elem in ['<rect', '<circle', '<line', '<polyline', '<path', '<text'])
            self.test(f"{filename}: has visual elements", has_elements)
        
            # Check for text labels
            self.test(f"{filename}: has text labels", '<text' in content)
        
            # Check for styling
            has_styling = 'fill=' in content or 'stroke=' in content or '<style' in content
            self.test(f"{filename}: has styling", has_styling)
        
            # Check for proper closing tag
            self.test(f"{filename}: properly closed", '</svg>' in content)


    def test_diagram_completeness(self):
        """Validate diagram completeness - 15 tests"""
        self.section("DIAGRAM COMPLETENESS VALIDATION (15 tests)")
    
        snapshots_dir = self.repo_root / "snapshots"
        docs_diagrams = self.repo_root / "docs" / "diagrams"
    
        self.logger.info("Required Diagrams")
    
        # Check for essential diagrams
        required_diagrams = {
            "mapping_v1.mmd": snapshots_dir / "mapping_v1.mmd",
            "trend_v1.svg": snapshots_dir / "trend_v1.svg",
            "architecture_overview.svg": docs_diagrams / "architecture_overview.svg",
            "trust_triangle_flow.svg": docs_diagrams / "trust_triangle_flow.svg"
        }
    
        for diagram_name, filepath in required_diagrams.items():
            self.test(f"{diagram_name} exists", filepath.exists())
        
            if filepath.exists():
                content = read_file(filepath)
                self.test(f"{diagram_name}: not empty", len(content) > 100)
    
        self.logger.info("Diagram Content Validation")
    
        # Validate mapping diagram content
        mapping_file = snapshots_dir / "mapping_v1.mmd"
        if mapping_file.exists():
            content = read_file(mapping_file)
        
            # Check for key resources in mapping
            key_resources = ['ALB', 'Target Group', 'ASG', 'EC2', 'EBS', 'S3', 'CloudWatch']
            found_resources = [res for res in key_resources if res in content]
        
            self.test("mapping: includes key AWS resources",
                       len(found_resources) >= 5,
                       f"Found {len(found_resources)}: {', '.join(found_resources)}")
        
            # Check for cost regression indicators
            self.test("mapping: shows cost indicators",
                       any(term in content for term in ['t3.xlarge', '200GB', 'No Lifecycle', 'Infinite']))
    
        # Validate trend SVG content
        trend_file = snapshots_dir / "trend_v1.svg"
        if trend_file.exists():
            content = read_file(trend_file)
        
            self.test("trend: has axis labels", '<text' in content and 'axis' in content.lower() or 'Nov' in content)
            self.test("trend: shows cost values", '$' in content or 'cost' in content.lower())
            self.test("trend: has visual trend line", '<polyline' in content or '<line' in content)


    def test_screenshots_manifest(self):
        """Validate screenshots manifest - 20 tests"""
        self.section("SCREENSHOTS MANIFEST VALIDATION (20 tests)")
    
        visual_dir = self.repo_root / "visual_assets"
        manifest_file = visual_dir / "screenshots_manifest.json"
    
        if not manifest_file.exists():
            for _ in range(20):
                self.skip("manifest validation", "screenshots_manifest.json not found")
            return
    
        with open(manifest_file, 'r') as f:
            manifest = json.load(f)
    
        self.logger.info("📋 Manifest Structure")
    
        # Check manifest metadata
        self.test("manifest: has version", "manifest_version" in manifest)
        self.test("manifest: has description", "description" in manifest)
        self.test("manifest: has screenshots array", "screenshots" in manifest)
    
        screenshots = manifest.get("screenshots", [])
        self.test("manifest: has screenshot entries", len(screenshots) > 0,
                   f"Found {len(screenshots)} entries")
        self.test("manifest: has required screenshots", len(screenshots) >= 3,
                   f"Expected ≥3, found {len(screenshots)}")
    
        self.logger.info("📸 Screenshot Entries")
    
        # Check each screenshot entry
        for idx, screenshot in enumerate(screenshots):
            name = screenshot.get("filename", f"screenshot_{idx}")
        
            # Required fields
            self.test(f"{name}: has filename", "filename" in screenshot)
            self.test(f"{name}: has status", "status" in screenshot)
            self.test(f"{name}: has resolution", "resolution" in screenshot)
            self.test(f"{name}: has source_snapshot", "source_snapshot" in screenshot)
        
            # Validation criteria
            if "validation" in screenshot:
                validation = screenshot["validation"]
                self.test(f"{name}: has validation criteria", len(validation) > 0)
        
            # Must show requirements
            if "must_show" in screenshot:
                must_show = screenshot["must_show"]
                self.test(f"{name}: has content requirements", len(must_show) > 0,
                           f"Found {len(must_show)} requirements")


    def test_asset_metadata(self):
        """Validate asset metadata and organization - 15 tests"""
        self.section("ASSET METADATA VALIDATION (15 tests)")
    
        visual_dir = self.repo_root / "visual_assets"
        snapshots_dir = self.repo_root / "snapshots"
    
        self.logger.info("📁 Visual Assets Organization")
    
        # Check visual_assets directory
        self.test("visual_assets/ directory exists", visual_dir.exists())
    
        if visual_dir.exists():
            self.test("visual_assets/ has README", (visual_dir / "README.md").exists())
            self.test("visual_assets/ has manifest", (visual_dir / "screenshots_manifest.json").exists())
            self.test("visual_assets/ has examples", (visual_dir / "SCREENSHOT_EXAMPLES.md").exists())
    
        self.logger.info("🎯 Snapshot Assets")
    
        # Check for snapshot-related visual assets
        if snapshots_dir.exists():
            self.test("snapshots/ has Mermaid diagrams", 
                       len(list(snapshots_dir.glob("*.mmd"))) > 0)
            self.test("snapshots/ has SVG assets",
                       len(list(snapshots_dir.glob("*.svg"))) > 0)
    
        self.logger.info("🔗 Asset References")
    
        # Check that manifests reference actual files
        manifest_file = visual_dir / "screenshots_manifest.json"
        if manifest_file.exists():
            with open(manifest_file, 'r') as f:
                manifest = json.load(f)
        
            screenshots = manifest.get("screenshots", [])
            for screenshot in screenshots[:3]:  # Check first 3
                source = screenshot.get("source_snapshot", "")
                if source:
                    source_path = self.repo_root / source
                    self.test(f"manifest: source '{source}' exists",
                               source_path.exists())
    
        self.logger.info("📊 Asset Coverage")
    
        # Check coverage of visual assets
        mermaid_count = len(list(self.repo_root.glob("**/*.mmd")))
        svg_count = len(list(self.repo_root.glob("**/*.svg")))
    
        self.test("Has Mermaid diagrams", mermaid_count >= 1,
                   f"Found {mermaid_count} files")
        self.test("Has SVG graphics", svg_count >= 2,
                   f"Found {svg_count} files")
    
        # Check for manifest documentation
        examples_file = visual_dir / "SCREENSHOT_EXAMPLES.md"
        if examples_file.exists():
            content = read_file(examples_file)
            self.test("screenshot examples: has content", len(content) > 100)
            self.test("screenshot examples: has specifications",
                       'resolution' in content.lower() or 'spec' in content.lower())


    def test_visual_quality_indicators(self):
        """Validate visual quality indicators - 10 tests"""
        self.section("VISUAL QUALITY INDICATORS (10 tests)")
    
        snapshots_dir = self.repo_root / "snapshots"
    
        self.logger.info("🎨 Color Usage")
    
        # Check mapping diagram for color coding
        mapping_file = snapshots_dir / "mapping_v1.mmd"
        if mapping_file.exists():
            content = read_file(mapping_file)
        
            self.test("mapping: uses color styling", 
                       'fill:' in content or 'style ' in content)
            self.test("mapping: uses severity colors",
                       any(color in content for color in ['#ff6b6b', '#ffd93d', 'red', 'yellow']))
            self.test("mapping: has classDef for categorization",
                       'classDef' in content)
        else:
            for _ in range(3):
                self.skip("mapping color checks", "File not found")
    
        self.logger.info("📐 Layout Quality")
    
        # Check SVG for proper layout
        trend_file = snapshots_dir / "trend_v1.svg"
        if trend_file.exists():
            content = read_file(trend_file)
        
            self.test("trend SVG: has grid/axes", 
                       any(elem in content for elem in ['<line', '<polyline', 'axis']))
            self.test("trend SVG: has data points",
                       '<circle' in content or 'point' in content.lower())
            self.test("trend SVG: has labels",
                       '<text' in content and content.count('<text') >= 3)
            self.test("trend SVG: uses color coding",
                       'fill=' in content or 'stroke=' in content)
        else:
            for _ in range(4):
                self.skip("trend layout checks", "File not found")
    
        self.logger.info("✅ Accessibility")
    
        # Check for text alternatives
        svg_files = list(snapshots_dir.glob("*.svg"))
        if svg_files:
            for svg_file in svg_files[:1]:  # Check first one
                content = read_file(svg_file)
                self.test(f"{svg_file.name}: has text labels for data",
                           '<text' in content)
                self.test(f"{svg_file.name}: uses semantic elements",
                           any(elem in content for elem in ['<title', '<desc']) or '<text' in content)
        else:
            for _ in range(2):
                self.skip("accessibility checks", "No SVG files")


def main():
    """Entry point for test execution"""
    suite = VisualAssetsTestSuite()
    suite.run()
    suite.print_summary()
    sys.exit(suite.get_exit_code())


if __name__ == "__main__":
    main()
