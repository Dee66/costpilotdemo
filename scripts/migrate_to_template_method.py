#!/usr/bin/env python3
"""
Automated migration script to convert test files to Template Method pattern.
Migrates TestRunner-based files to use TestSuite base class.
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple

def migrate_test_file(filepath: Path) -> Tuple[int, int, bool]:
    """
    Migrate a test file to Template Method pattern.
    Returns: (lines_before, lines_after, success)
    """
    print(f"\n{'='*80}")
    print(f"Migrating: {filepath.name}")
    print(f"{'='*80}")
    
    # Read original file
    with open(filepath, 'r') as f:
        original_lines = f.readlines()
    
    lines_before = len(original_lines)
    content = ''.join(original_lines)
    
    # Step 1: Update docstring to mention Template Method pattern
    content = re.sub(
        r'("""[^"]*?""")',
        lambda m: m.group(1).rstrip('"""') + '\n\nRefactored to use Template Method Pattern with TestSuite base class.\n"""',
        content,
        count=1
    )
    
    # Step 2: Remove color code definitions
    content = re.sub(
        r"# Color codes\nGREEN = '[^']+'\nRED = '[^']+'\nYELLOW = '[^']+'\nBLUE = '[^']+'\nRESET = '[^']+'\n\n",
        '',
        content
    )
    
    # Step 3: Remove TestRunner class (approximately lines 20-48)
    content = re.sub(
        r'class TestRunner:.*?def section\(self, name: str\):.*?\n        print\(f"{BLUE}\{\'=\'\*80\}{RESET}"\)\n\n',
        '',
        content,
        flags=re.DOTALL
    )
    
    # Step 4: Add import for TestSuite
    import_section = """import sys
from pathlib import Path"""
    
    new_import_section = """import sys
from pathlib import Path

# Import shared test framework
sys.path.insert(0, str(Path(__file__).parent))
from lib.test_suite import TestSuite"""
    
    content = content.replace(import_section, new_import_section)
    
    # Step 5: Find all test function names
    test_functions = re.findall(r'def (test_\w+)\(runner: TestRunner\):', content)
    print(f"Found {len(test_functions)} test functions: {', '.join(test_functions)}")
    
    # Step 6: Create class with run() method
    if test_functions:
        # Determine class name from filename
        class_name = filepath.stem.replace('test_', '').title().replace('_', '') + 'TestSuite'
        
        # Find where first test function starts
        first_func_match = re.search(r'def ' + test_functions[0] + r'\(runner: TestRunner\):', content)
        if first_func_match:
            insertion_point = first_func_match.start()
            
            # Create class header and run() method
            run_method_calls = '\n        '.join(f'self.{func}()' for func in test_functions)
            class_header = f'''class {class_name}(TestSuite):
    """Test suite using Template Method pattern"""
    
    def run(self):
        """Template method - defines the test execution sequence"""
        {run_method_calls}
    
    '''
            
            # Insert class definition
            content = content[:insertion_point] + class_header + content[insertion_point:]
    
    # Step 7: Convert test functions to methods
    # Replace all "def test_" with "    def test_"
    content = re.sub(r'^def test_', r'    def test_', content, flags=re.MULTILINE)
    
    # Replace function signatures
    content = re.sub(r'\(runner: TestRunner\):', r'(self):', content)
    
    # Step 8: Replace all runner. with self.
    content = re.sub(r'runner\.', r'self.', content)
    
    # Step 9: Indent all method bodies (add 4 spaces to lines within methods)
    lines = content.split('\n')
    output_lines = []
    in_method = False
    
    for i, line in enumerate(lines):
        # Check if this is a method definition
        if re.match(r'    def test_\w+\(self\):', line):
            in_method = True
            output_lines.append(line)
        # Check if we hit another def or class at root level
        elif re.match(r'^(def |class )', line):
            in_method = False
            output_lines.append(line)
        # If we're in a method, add 4 spaces to non-empty lines
        elif in_method and line.strip() and not line.startswith('    def '):
            output_lines.append('    ' + line)
        else:
            output_lines.append(line)
    
    content = '\n'.join(output_lines)
    
    # Step 10: Replace main() function
    main_pattern = r'def main\(\):.*?sys\.exit\(0 if self\.failed == 0 else 1\)'
    main_replacement = f'''def main():
    """Entry point for test execution"""
    suite = {class_name}()
    suite.run()
    suite.print_summary()
    sys.exit(suite.get_exit_code())'''
    
    content = re.sub(main_pattern, main_replacement, content, flags=re.DOTALL)
    
    # Write migrated file
    with open(filepath, 'w') as f:
        f.write(content)
    
    lines_after = len(content.split('\n'))
    reduction = lines_before - lines_after
    
    print(f"✓ Migration complete: {lines_before} → {lines_after} lines ({reduction} eliminated, {reduction/lines_before*100:.1f}%)")
    
    return lines_before, lines_after, True


def main():
    """Migrate all test files that haven't been migrated yet"""
    repo_root = Path(__file__).parent.parent
    scripts_dir = repo_root / "scripts"
    
    # Files to migrate (excluding test_golden_deep.py which is already done)
    files_to_migrate = [
        "test_infrastructure_deep.py",
        "test_pr_comments.py",
        "test_documentation_deep.py",
        "test_visual_assets.py",
        "test_hash_lineage.py",
        "test_cicd_deep.py",
        "test_regressions.py",
    ]
    
    total_before = 0
    total_after = 0
    successes = 0
    
    print(f"\n{'='*80}")
    print(f"TEMPLATE METHOD MIGRATION - BATCH PROCESSING")
    print(f"{'='*80}")
    print(f"Files to migrate: {len(files_to_migrate)}")
    
    for filename in files_to_migrate:
        filepath = scripts_dir / filename
        if not filepath.exists():
            print(f"⚠ Skipping {filename} - file not found")
            continue
        
        try:
            before, after, success = migrate_test_file(filepath)
            total_before += before
            total_after += after
            if success:
                successes += 1
        except Exception as e:
            print(f"✗ Error migrating {filename}: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print(f"\n{'='*80}")
    print(f"MIGRATION SUMMARY")
    print(f"{'='*80}")
    print(f"Files migrated: {successes}/{len(files_to_migrate)}")
    print(f"Total lines before: {total_before}")
    print(f"Total lines after: {total_after}")
    print(f"Lines eliminated: {total_before - total_after} ({(total_before - total_after)/total_before*100:.1f}%)")
    
    if successes == len(files_to_migrate):
        print(f"\n✓ All files migrated successfully!")
        return 0
    else:
        print(f"\n⚠ Some files failed to migrate")
        return 1


if __name__ == "__main__":
    sys.exit(main())
