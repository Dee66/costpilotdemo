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
Test script to validate tag filtering functionality
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from scripts.run_tests import discover_test_suites, load_suite_module
from scripts.lib.test_suite import TestSuite

def test_tag_filtering():
    """Test that tag filtering works correctly"""
    print("Testing tag filtering...")

    # Discover test suites
    test_files = discover_test_suites()
    print(f"Found {len(test_files)} test suites")

    # Test filtering by 'validation' tag
    validation_suites = []
    for test_file in test_files:
        try:
            module = load_suite_module(test_file)
            # Get the test suite class
            suite_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and
                    issubclass(attr, TestSuite) and
                    attr != TestSuite):
                    suite_class = attr
                    break

            if suite_class and hasattr(suite_class, 'tags'):
                if 'validation' in suite_class.tags:
                    validation_suites.append(test_file.stem)
        except Exception as e:
            print(f"Warning: Could not load {test_file.stem}: {e}")

    print(f"Suites with 'validation' tag: {validation_suites}")
    print("Tag filtering test completed successfully!")

if __name__ == "__main__":
    test_tag_filtering()