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
Unit Tests for ScenarioFactory
Validates scenario creation, registration, and metadata
"""

import sys
from pathlib import Path

# Import shared test framework
sys.path.insert(0, str(Path(__file__).parent))
from lib.test_suite import TestSuite
from lib.scenario_factory import ScenarioFactory, create_scenario, Scenario


class ScenarioFactoryTestSuite(TestSuite):
    """Test suite for ScenarioFactory"""
    
    @property
    def tags(self):
        return ["factory", "scenarios", "validation"]
    
    def run(self):
        """Template method - defines the test execution sequence"""
        self.test_factory_initialization()
        self.test_create_baseline_scenario()
        self.test_create_pr_change_scenario()
        self.test_create_noop_scenario()
        self.test_create_noise_scenarios()
        self.test_list_available_scenarios()
        self.test_invalid_scenario_name()
        self.test_scenario_metadata()
        self.test_get_by_type()
        self.test_convenience_function()
    
    def test_factory_initialization(self):
        """Test factory initialization - 3 tests"""
        self.section("FACTORY INITIALIZATION (3 tests)")
        
        factory = ScenarioFactory()
        
        self.test("factory_initializes", factory is not None)
        self.test("factory_has_repo_root", factory.repo_root is not None)
        self.test("factory_has_scenarios", len(factory._scenarios) > 0)
    
    def test_create_baseline_scenario(self):
        """Test baseline scenario creation - 8 tests"""
        self.section("BASELINE SCENARIO CREATION (8 tests)")
        
        factory = ScenarioFactory()
        scenario = factory.create("baseline")
        
        self.test("scenario_created", scenario is not None)
        self.test("scenario_is_scenario_type", isinstance(scenario, Scenario))
        self.test("scenario_has_name", scenario.name == "baseline")
        self.test("scenario_has_description", len(scenario.description) > 0)
        self.test("scenario_has_terraform_path", scenario.terraform_path is not None)
        self.test("scenario_expected_findings_zero", scenario.expected_findings == 0)
        self.test("scenario_expected_severity_none", scenario.expected_severity == "none")
        self.test("scenario_has_metadata", isinstance(scenario.metadata, dict))
    
    def test_create_pr_change_scenario(self):
        """Test PR change scenario creation - 10 tests"""
        self.section("PR CHANGE SCENARIO CREATION (10 tests)")
        
        factory = ScenarioFactory()
        scenario = factory.create("pr_change")
        
        self.test("scenario_created", scenario is not None)
        self.test("scenario_name_pr_change", scenario.name == "pr_change")
        self.test("scenario_expected_findings_four", scenario.expected_findings == 4)
        self.test("scenario_expected_severity_high", scenario.expected_severity == "high")
        self.test("scenario_has_pr_number", "pr_number" in scenario.metadata)
        self.test("scenario_pr_number_is_42", scenario.metadata.get("pr_number") == 42)
        self.test("scenario_has_monthly_cost", "monthly_cost" in scenario.metadata)
        self.test("scenario_has_delta", "delta" in scenario.metadata)
        self.test("scenario_has_regression_types", "regression_types" in scenario.metadata)
        self.test("scenario_regression_types_is_list", isinstance(scenario.metadata.get("regression_types"), list))
    
    def test_create_noop_scenario(self):
        """Test no-op scenario creation - 6 tests"""
        self.section("NO-OP SCENARIO CREATION (6 tests)")
        
        factory = ScenarioFactory()
        scenario = factory.create("noop")
        
        self.test("scenario_created", scenario is not None)
        self.test("scenario_name_noop", scenario.name == "noop")
        self.test("scenario_expected_findings_zero", scenario.expected_findings == 0)
        self.test("scenario_expected_severity_none", scenario.expected_severity == "none")
        self.test("scenario_has_scenario_type", "scenario_type" in scenario.metadata)
        self.test("scenario_type_is_noop", scenario.metadata.get("scenario_type") == "noop")
    
    def test_create_noise_scenarios(self):
        """Test noise scenario creation - 16 tests"""
        self.section("NOISE SCENARIOS CREATION (16 tests)")
        
        factory = ScenarioFactory()
        noise_types = ["noise_whitespace", "noise_comments", "noise_reorder", "noise_description"]
        
        for noise_type in noise_types:
            scenario = factory.create(noise_type)
            
            self.test(f"{noise_type}_created", scenario is not None)
            self.test(f"{noise_type}_expected_findings_zero", scenario.expected_findings == 0)
            self.test(f"{noise_type}_has_noise_type", "noise_type" in scenario.metadata)
            self.test(f"{noise_type}_has_false_positive_test", "false_positive_test" in scenario.metadata)
    
    def test_list_available_scenarios(self):
        """Test listing available scenarios - 6 tests"""
        self.section("LIST AVAILABLE SCENARIOS (6 tests)")
        
        factory = ScenarioFactory()
        available = factory.list_available()
        
        self.test("list_returns_list", isinstance(available, list))
        self.test("list_not_empty", len(available) > 0)
        self.test("list_contains_baseline", "baseline" in available)
        self.test("list_contains_pr_change", "pr_change" in available)
        self.test("list_contains_noop", "noop" in available)
        self.test("list_contains_noise_scenarios", any(s.startswith("noise_") for s in available))
    
    def test_invalid_scenario_name(self):
        """Test invalid scenario name handling - 3 tests"""
        self.section("INVALID SCENARIO NAME (3 tests)")
        
        factory = ScenarioFactory()
        
        try:
            scenario = factory.create("invalid_scenario_name")
            self.test("invalid_scenario_raises_error", False, "Should have raised ValueError")
        except ValueError as e:
            self.test("invalid_scenario_raises_valueerror", True)
            self.test("error_message_contains_unknown", "Unknown scenario" in str(e))
            self.test("error_message_contains_available", "Available" in str(e))
    
    def test_scenario_metadata(self):
        """Test scenario metadata completeness - 10 tests"""
        self.section("SCENARIO METADATA COMPLETENESS (10 tests)")
        
        factory = ScenarioFactory()
        
        # Baseline metadata
        baseline = factory.create("baseline")
        self.test("baseline_has_version", "version" in baseline.metadata)
        self.test("baseline_has_monthly_cost", "monthly_cost" in baseline.metadata)
        self.test("baseline_has_resources", "resources" in baseline.metadata)
        
        # PR change metadata
        pr_change = factory.create("pr_change")
        self.test("pr_change_has_version", "version" in pr_change.metadata)
        self.test("pr_change_has_pr_number", "pr_number" in pr_change.metadata)
        self.test("pr_change_has_delta", "delta" in pr_change.metadata)
        
        # Noise metadata
        noise = factory.create("noise_whitespace")
        self.test("noise_has_version", "version" in noise.metadata)
        self.test("noise_has_noise_type", "noise_type" in noise.metadata)
        self.test("noise_has_false_positive_test", "false_positive_test" in noise.metadata)
        self.test("noise_whitespace_false_positive_true", noise.metadata.get("false_positive_test") == True)
    
    def test_get_by_type(self):
        """Test getting scenarios by type - 8 tests"""
        self.section("GET SCENARIOS BY TYPE (8 tests)")
        
        factory = ScenarioFactory()
        
        # Get noise scenarios
        noise_scenarios = factory.get_by_type("noise")
        self.test("noise_scenarios_is_list", isinstance(noise_scenarios, list))
        self.test("noise_scenarios_not_empty", len(noise_scenarios) > 0)
        self.test("all_noise_scenarios_start_with_noise", 
                  all(s.name.startswith("noise_") for s in noise_scenarios))
        
        # Get baseline scenarios
        baseline_scenarios = factory.get_by_type("baseline")
        self.test("baseline_scenarios_is_list", isinstance(baseline_scenarios, list))
        self.test("baseline_scenarios_has_one", len(baseline_scenarios) == 1)
        
        # Get pr_change scenarios
        pr_change_scenarios = factory.get_by_type("pr_change")
        self.test("pr_change_scenarios_is_list", isinstance(pr_change_scenarios, list))
        self.test("pr_change_scenarios_has_one", len(pr_change_scenarios) == 1)
        
        # Get noop scenarios
        noop_scenarios = factory.get_by_type("noop")
        self.test("noop_scenarios_is_list", isinstance(noop_scenarios, list))
    
    def test_convenience_function(self):
        """Test convenience function - 3 tests"""
        self.section("CONVENIENCE FUNCTION (3 tests)")
        
        scenario = create_scenario("baseline")
        
        self.test("convenience_function_returns_scenario", scenario is not None)
        self.test("convenience_function_returns_correct_scenario", scenario.name == "baseline")
        self.test("convenience_function_scenario_is_scenario_type", isinstance(scenario, Scenario))


def main():
    """Run the test suite"""
    suite = ScenarioFactoryTestSuite()
    suite.run()
    suite.print_summary()
    return suite.get_exit_code()


if __name__ == "__main__":
    exit(main())
