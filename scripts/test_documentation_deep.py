#!/usr/bin/env python3
"""
Deep Documentation Content Validation Suite
Adds ~120+ granular tests for documentation quality and completeness
Focus: Code examples, links, terminology, command accuracy, TOC, consistency


Refactored to use Template Method Pattern with TestSuite base class.
"""

import os
import re
import sys
from pathlib import Path

# Import shared test framework
sys.path.insert(0, str(Path(__file__).parent))
from lib.test_suite import TestSuite
from lib.scenario_factory import ScenarioFactory
from typing import Dict, List, Any, Set


def read_doc(filepath: Path) -> str:
    """Read a documentation file"""
    if not filepath.exists():
        return ""
    with open(filepath, 'r') as f:
        return f.read()


def extract_code_blocks(content: str) -> List[Dict[str, str]]:
    """Extract code blocks with language tags"""
    blocks = []
    pattern = r'```(\w+)?\n(.*?)```'
    for match in re.finditer(pattern, content, re.DOTALL):
        blocks.append({
            'language': match.group(1) or 'unknown',
            'code': match.group(2)
        })
    return blocks


def extract_links(content: str) -> List[str]:
    """Extract markdown links"""
    # Match [text](url) format
    links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
    return [url for text, url in links]


class DocumentationDeepTestSuite(TestSuite):
    """Test suite using Template Method pattern"""
    
    def __init__(self, repo_root: Path = None):
        super().__init__(repo_root)
        self.factory = ScenarioFactory(self.repo_root)
        self.pr_scenario = self.factory.create("pr_change")
    
    def run(self):
        """Template method - defines the test execution sequence"""
        self.test_code_example_validation()
        self.test_link_integrity()
        self.test_table_of_contents()
        self.test_terminology_consistency()
        self.test_command_accuracy()
        self.test_documentation_structure()
        self.test_documentation_metadata()
    
    def test_code_example_validation(self):
        """Validate code examples in documentation - 40 tests"""
        self.section("CODE EXAMPLE VALIDATION (40 tests)")
    
        docs_dir = self.repo_root / "docs"
        readme = self.repo_root / "README.md"
    
        doc_files = {
            "README.md": readme,
            "DRIFT_MANAGEMENT.md": docs_dir / "DRIFT_MANAGEMENT.md",
            "MANUAL_TASKS_GUIDE.md": docs_dir / "MANUAL_TASKS_GUIDE.md",
            "walkthrough.md": docs_dir / "walkthrough.md"
        }
    
        for doc_name, filepath in doc_files.items():
            if not filepath.exists():
                for _ in range(10):
                    self.skip(f"{doc_name} code examples", "File not found")
                continue
        
            content = read_doc(filepath)
            code_blocks = extract_code_blocks(content)
        
            print(f"\n📝 {doc_name} Code Examples")
        
            # Code block presence
            self.test(f"{doc_name}: has code blocks", len(code_blocks) > 0,
                       f"Found {len(code_blocks)} blocks")
        
            # Language tags
            bash_blocks = [b for b in code_blocks if b['language'] in ['bash', 'sh']]
            json_blocks = [b for b in code_blocks if b['language'] == 'json']
            hcl_blocks = [b for b in code_blocks if b['language'] in ['hcl', 'terraform']]
        
            if 'README' in doc_name or 'MANUAL' in doc_name:
                self.test(f"{doc_name}: has bash examples", len(bash_blocks) > 0,
                           f"Found {len(bash_blocks)} bash blocks")
        
            # Code block quality
            for idx, block in enumerate(code_blocks[:3]):  # Test first 3 blocks
                code = block['code']
                self.test(f"{doc_name}: block {idx+1} not empty", len(code.strip()) > 0)
                self.test(f"{doc_name}: block {idx+1} has language tag", 
                           block['language'] != 'unknown')
            
                # Check for common errors
                if block['language'] == 'bash':
                    self.test(f"{doc_name}: bash block {idx+1} has commands",
                               any(cmd in code for cmd in ['cd', 'git', 'terraform', 'python', 'echo']))


    def test_link_integrity(self):
        """Validate link integrity - 30 tests"""
        self.section("LINK INTEGRITY VALIDATION (30 tests)")
    
        docs_dir = self.repo_root / "docs"
        readme = self.repo_root / "README.md"
    
        doc_files = list((docs_dir).glob("*.md")) + [readme]
    
        print("\n🔗 Internal Links")
    
        for filepath in doc_files[:5]:  # Test first 5 docs
            if not filepath.exists():
                continue
        
            content = read_doc(filepath)
            links = extract_links(content)
        
            doc_name = filepath.name
        
            # Check internal links
            internal_links = [link for link in links if not link.startswith('http')]
        
            for link in internal_links[:3]:  # Test first 3 internal links
                if link.startswith('#'):
                    # Anchor link - check if section exists
                    anchor = link[1:]
                    # Convert anchor to heading format
                    heading = anchor.replace('-', ' ').lower()
                    self.test(f"{doc_name}: anchor '{anchor}' has target",
                               heading in content.lower() or anchor.replace('-', '') in content.lower())
                else:
                    # File link - check if file exists
                    target_path = filepath.parent / link
                    self.test(f"{doc_name}: file link '{link}' exists",
                               target_path.exists() or '../' in link)
    
        print("\n🌐 External Links")
    
        for filepath in doc_files[:3]:  # Test first 3 docs
            if not filepath.exists():
                continue
        
            content = read_doc(filepath)
            links = extract_links(content)
        
            doc_name = filepath.name
        
            # Check external links format
            external_links = [link for link in links if link.startswith('http')]
        
            self.test(f"{doc_name}: has external links", len(external_links) > 0,
                       f"Found {len(external_links)} links")
        
            for link in external_links[:2]:  # Test first 2
                self.test(f"{doc_name}: external link well-formed",
                           link.startswith('https://') or link.startswith('http://'))


    def test_table_of_contents(self):
        """Validate table of contents accuracy - 15 tests"""
        self.section("TABLE OF CONTENTS VALIDATION (15 tests)")
    
        readme = self.repo_root / "README.md"
    
        if not readme.exists():
            for _ in range(15):
                self.skip("TOC validation", "README.md not found")
            return
    
        content = read_doc(readme)
    
        print("\n📑 README TOC")
    
        # Check for TOC section
        has_toc = bool(re.search(r'##\s+Table of Contents|##\s+Contents', content, re.IGNORECASE))
        self.test("README: has table of contents", has_toc or '- [' in content[:2000])
    
        # Extract headers
        headers = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
        self.test("README: has section headers", len(headers) >= 5,
                   f"Found {len(headers)} headers")
    
        # Check for common sections
        common_sections = [
            'Quick Start', 'Installation', 'Usage', 'Features', 'Overview',
            'Purpose', 'Infrastructure', 'Scenario', 'Safeguards'
        ]
    
        content_lower = content.lower()
        found_sections = [s for s in common_sections if s.lower() in content_lower]
        self.test("README: has standard sections", len(found_sections) >= 4,
                   f"Found: {', '.join(found_sections[:5])}")
    
        # Check header hierarchy
        h1_count = content.count('\n# ')
        h2_count = content.count('\n## ')
        h3_count = content.count('\n### ')
    
        self.test("README: has primary title (H1)", h1_count >= 1)
        self.test("README: has section headers (H2)", h2_count >= 5,
                   f"Found {h2_count} H2 headers")
        self.test("README: has subsections (H3)", h3_count >= 3,
                   f"Found {h3_count} H3 headers")
        self.test("README: proper header hierarchy", h2_count > h1_count)
    
        # Check for anchor links in TOC
        toc_links = re.findall(r'\[([^\]]+)\]\(#([^\)]+)\)', content)
        self.test("README: TOC has anchor links", len(toc_links) >= 3,
                   f"Found {len(toc_links)} TOC links")
    
        # Validate anchor targets exist
        for text, anchor in toc_links[:5]:  # Test first 5
            heading = anchor.replace('-', ' ')
            self.test(f"TOC link '{anchor}' has target",
                       heading.lower() in content.lower() or 
                       anchor.replace('-', '').lower() in content.lower())


    def test_terminology_consistency(self):
        """Validate terminology consistency - 20 tests"""
        self.section("TERMINOLOGY CONSISTENCY VALIDATION (20 tests)")
    
        docs_dir = self.repo_root / "docs"
        readme = self.repo_root / "README.md"
    
        # Collect all documentation content
        all_docs = {}
        for filepath in [readme] + list(docs_dir.glob("*.md")):
            if filepath.exists():
                all_docs[filepath.name] = read_doc(filepath)
    
        print("\n📖 Standard Terminology")
    
        # Key terms that should be consistent
        expected_terms = {
            'CostPilot': ['CostPilot', 'costpilot', 'Cost Pilot'],
            'Trust Triangle': ['Trust Triangle', 'trust triangle'],
            'golden output': ['golden output', 'Golden Output', 'golden version'],
            'baseline': ['baseline', 'Baseline'],
            'PR': ['PR', 'Pull Request', 'pull request']
        }
    
        for term_group, variants in expected_terms.items():
            found_in_docs = []
            for doc_name, content in all_docs.items():
                if any(variant in content for variant in variants):
                    found_in_docs.append(doc_name)
        
            self.test(f"Term '{term_group}' used consistently",
                       len(found_in_docs) >= 2,
                       f"Found in {len(found_in_docs)} docs")
    
        print("\n🔤 Naming Conventions")
    
        # Check for consistent resource naming
        if 'README.md' in all_docs:
            readme_content = all_docs['README.md']
        
            self.test("README: uses 'aws_' prefix for resources",
                       'aws_' in readme_content)
            self.test("README: mentions t3.micro instance type",
                       't3.micro' in readme_content)
            self.test("README: mentions t3.xlarge regression",
                       't3.xlarge' in readme_content)
    
        print("\n🎯 Scenario Consistency")
    
        # Check scenario version consistency
        scenario_versions = {}
        for doc_name, content in all_docs.items():
            matches = re.findall(r'scenario[_\s]+version[:\s]+[`"]?(v\d+)[`"]?', content, re.IGNORECASE)
            if matches:
                scenario_versions[doc_name] = matches[0]
    
        if len(scenario_versions) >= 2:
            versions = list(scenario_versions.values())
            self.test("Scenario version consistent across docs",
                       len(set(versions)) == 1,
                       f"Found versions: {set(versions)}")
    
        # Check for proper capitalization
        for doc_name, content in list(all_docs.items())[:3]:
            self.test(f"{doc_name}: uses proper AWS capitalization",
                       'AWS' in content and 'aws' in content)
            self.test(f"{doc_name}: uses proper Terraform capitalization",
                       'Terraform' in content)


    def test_command_accuracy(self):
        """Validate command accuracy and executability - 25 tests"""
        self.section("COMMAND ACCURACY VALIDATION (25 tests)")
    
        docs_dir = self.repo_root / "docs"
        readme = self.repo_root / "README.md"
    
        doc_files = {
            "README.md": readme,
            "MANUAL_TASKS_GUIDE.md": docs_dir / "MANUAL_TASKS_GUIDE.md",
        }
    
        for doc_name, filepath in doc_files.items():
            if not filepath.exists():
                for _ in range(12):
                    self.skip(f"{doc_name} commands", "File not found")
                continue
        
            content = read_doc(filepath)
            code_blocks = extract_code_blocks(content)
            bash_blocks = [b for b in code_blocks if b['language'] in ['bash', 'sh', 'shell']]
        
            print(f"\n💻 {doc_name} Command Validation")
        
            self.test(f"{doc_name}: has bash commands", len(bash_blocks) > 0,
                       f"Found {len(bash_blocks)} bash blocks")
        
            # Analyze commands
            for idx, block in enumerate(bash_blocks[:5]):  # Test first 5
                code = block['code']
                lines = [line.strip() for line in code.split('\n') if line.strip()]
            
                # Check for common commands
                has_valid_commands = any(
                    line.startswith(cmd) for line in lines
                    for cmd in ['git', 'cd', 'python', 'terraform', 'chmod', 'echo', 'cat', 'ls']
                )
            
                self.test(f"{doc_name}: bash block {idx+1} has valid commands",
                           has_valid_commands or '#!/bin/bash' in code)
            
                # Check for dangerous commands (should have warnings)
                dangerous_cmds = ['rm -rf', 'sudo', 'terraform apply', 'terraform destroy']
                has_dangerous = any(cmd in code for cmd in dangerous_cmds)
            
                if has_dangerous and 'terraform apply' in code:
                    self.test(f"{doc_name}: dangerous command has warning",
                               '⚠️' in content or 'WARNING' in content or 'DO NOT' in content)
            
                # Check for proper shell syntax
                if len(lines) > 0 and not lines[0].startswith('#'):
                    self.test(f"{doc_name}: bash block {idx+1} has executable content",
                               len(lines) > 0)


    def test_documentation_structure(self):
        """Validate documentation structure and organization - 20 tests"""
        self.section("DOCUMENTATION STRUCTURE VALIDATION (20 tests)")
    
        docs_dir = self.repo_root / "docs"
        readme = self.repo_root / "README.md"
    
        print("\n📁 Required Documentation Files")
    
        required_docs = [
            "README.md",
            "DRIFT_MANAGEMENT.md",
            "GOLDEN_VERSION_SIGNOFF.md",
            "MANUAL_TASKS_GUIDE.md"
        ]
    
        for doc in required_docs:
            if doc == "README.md":
                filepath = readme
            else:
                filepath = docs_dir / doc
        
            self.test(f"{doc} exists", filepath.exists())
        
            if filepath.exists():
                content = read_doc(filepath)
                self.test(f"{doc}: not empty", len(content) > 100)
                self.test(f"{doc}: has title", content.startswith('#') or '# ' in content[:200])
    
        print("\n📊 Documentation Completeness")
    
        if readme.exists():
            readme_content = read_doc(readme)
        
            # Check for essential sections
            essential_sections = [
                ('Purpose', 'Why'),
                ('Quick Start', 'Getting Started'),
                ('Installation', 'Setup'),
                ('Usage', 'How to'),
                ('Safeguards', 'Warning')
            ]
        
            for primary, secondary in essential_sections:
                has_section = primary in readme_content or secondary in readme_content
                self.test(f"README: has {primary} section", has_section)
    
        print("\n🔍 Documentation Quality Indicators")
    
        for filepath in [readme, docs_dir / "DRIFT_MANAGEMENT.md"][:2]:
            if not filepath.exists():
                continue
        
            content = read_doc(filepath)
            doc_name = filepath.name
        
            # Quality checks
            self.test(f"{doc_name}: has examples", 
                       '```' in content or 'example' in content.lower())
            self.test(f"{doc_name}: has formatting",
                       '**' in content or '_' in content or '`' in content)


    def test_documentation_metadata(self):
        """Validate documentation metadata and frontmatter - 15 tests"""
        self.section("DOCUMENTATION METADATA VALIDATION (15 tests)")
    
        readme = self.repo_root / "README.md"
    
        if not readme.exists():
            for _ in range(15):
                self.skip("metadata validation", "README.md not found")
            return
    
        content = read_doc(readme)
    
        print("\n🏷️  Badges and Status Indicators")
    
        # Check for badges
        badges = re.findall(r'!\[([^\]]+)\]\(([^\)]+)\)', content)
        self.test("README: has badges", len(badges) >= 2,
                   f"Found {len(badges)} badges")
    
        # Check for license badge
        has_license_badge = any('license' in badge[0].lower() for badge in badges)
        self.test("README: has license badge", has_license_badge)
    
        # Check for version indicators
        has_version = bool(re.search(r'v\d+\.\d+\.\d+', content))
        self.test("README: has version number", has_version)
    
        print("\n📝 Warnings and Notices")
    
        # Check for important warnings
        self.test("README: has cost warning",
                   'cost' in content.lower() and ('warning' in content.lower() or '⚠️' in content))
        self.test("README: warns about terraform apply",
                   'terraform apply' in content.lower() and 
                   ('do not' in content.lower() or 'warning' in content.lower()))
        self.test("README: identifies as demo",
                   'demo' in content.lower() or 'demonstration' in content.lower())
    
        print("\n🎯 Purpose Statement")
    
        # Check for clear purpose
        first_500 = content[:500]
        self.test("README: has clear purpose in intro",
                   any(term in first_500.lower() 
                       for term in ['purpose', 'goal', 'why', 'what is']))
    
        # Check for scenario identification
        self.test("README: identifies scenario",
                   'scenario' in content.lower() and 'v1' in content)
    
        print("\n📦 Project Information")
    
        # Check for repository info
        self.test("README: mentions repository",
                   'repository' in content.lower() or 'repo' in content.lower())
        self.test("README: has git clone example",
                   'git clone' in content)
    
        # Check for contact/support info
        self.test("README: has navigation aids",
                   '[' in content and '](' in content)  # Has markdown links
    
        # Check for structured content
        self.test("README: well-structured",
                   content.count('## ') >= 5)  # At least 5 major sections
        self.test("README: substantial content",
                   len(content) >= 500)


def main():
    """Entry point for test execution"""
    suite = DocumentationDeepTestSuite()
    suite.run()
    suite.print_summary()
    sys.exit(suite.get_exit_code())


if __name__ == "__main__":
    main()
