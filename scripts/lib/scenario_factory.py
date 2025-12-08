#!/usr/bin/env python3
"""
Scenario Factory - Centralized scenario creation
Part of SOLID refactoring: Factory Pattern for scenario management
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Scenario:
    """Represents a test scenario with metadata"""
    
    name: str
    description: str
    terraform_path: Path
    expected_findings: int
    expected_severity: str  # "high", "medium", "low"
    seed: int = 42
    metadata: Dict = field(default_factory=dict)
    
    def __str__(self) -> str:
        return f"Scenario({self.name}, findings={self.expected_findings}, severity={self.expected_severity})"


class ScenarioFactory:
    """Factory for creating test scenarios"""
    
    def __init__(self, repo_root: Path = None):
        self.repo_root = repo_root or Path(__file__).parent.parent.parent
        self._scenarios = {}
        self._register_scenarios()
    
    def _register_scenarios(self):
        """Register all available scenarios"""
        
        # Baseline scenario - before any PR changes
        self._scenarios["baseline"] = Scenario(
            name="baseline",
            description="Baseline infrastructure before PR #42",
            terraform_path=self.repo_root / "terraform" / "baseline",
            expected_findings=0,
            expected_severity="none",
            seed=42,
            metadata={
                "version": "v1",
                "monthly_cost": 52.43,
                "resources": ["aws_launch_template", "aws_autoscaling_group", "aws_lb", "aws_s3_bucket", "aws_cloudwatch_log_group"]
            }
        )
        
        # PR change scenario - PR #42 with cost regressions
        self._scenarios["pr_change"] = Scenario(
            name="pr_change",
            description="PR #42 with 4 cost regressions (instance type change)",
            terraform_path=self.repo_root / "terraform",
            expected_findings=4,
            expected_severity="high",
            seed=42,
            metadata={
                "version": "v1",
                "pr_number": 42,
                "monthly_cost": 387.89,
                "delta": "+$335.54 (+639%)",
                "regression_types": ["instance_type_escalation", "lifecycle_removal", "retention_increase", "volume_size_increase"]
            }
        )
        
        # No-op scenario - no meaningful changes
        self._scenarios["noop"] = Scenario(
            name="noop",
            description="No-op scenario with no infrastructure changes",
            terraform_path=self.repo_root / "terraform" / "baseline",
            expected_findings=0,
            expected_severity="none",
            seed=42,
            metadata={
                "version": "v1",
                "scenario_type": "noop"
            }
        )
        
        # Noise scenarios - changes that shouldn't trigger findings
        self._scenarios["noise_whitespace"] = Scenario(
            name="noise_whitespace",
            description="Whitespace-only changes (should not trigger findings)",
            terraform_path=self.repo_root / "scenarios" / "noise" / "whitespace_only.tf",
            expected_findings=0,
            expected_severity="none",
            seed=42,
            metadata={
                "version": "v1",
                "noise_type": "whitespace",
                "false_positive_test": True
            }
        )
        
        self._scenarios["noise_comments"] = Scenario(
            name="noise_comments",
            description="Comment-only changes (should not trigger findings)",
            terraform_path=self.repo_root / "scenarios" / "noise" / "comments_only.tf",
            expected_findings=0,
            expected_severity="none",
            seed=42,
            metadata={
                "version": "v1",
                "noise_type": "comments",
                "false_positive_test": True
            }
        )
        
        self._scenarios["noise_reorder"] = Scenario(
            name="noise_reorder",
            description="Resource reordering (should not trigger findings)",
            terraform_path=self.repo_root / "scenarios" / "noise" / "reordered_resources.tf",
            expected_findings=0,
            expected_severity="none",
            seed=42,
            metadata={
                "version": "v1",
                "noise_type": "reorder",
                "false_positive_test": True
            }
        )
        
        self._scenarios["noise_description"] = Scenario(
            name="noise_description",
            description="Description field changes (should not trigger findings)",
            terraform_path=self.repo_root / "scenarios" / "noise" / "description_change.tf",
            expected_findings=0,
            expected_severity="none",
            seed=42,
            metadata={
                "version": "v1",
                "noise_type": "description",
                "false_positive_test": False
            }
        )
    
    def create(self, scenario_name: str) -> Scenario:
        """
        Create a scenario by name
        
        Args:
            scenario_name: Name of the scenario to create
            
        Returns:
            Scenario object
            
        Raises:
            ValueError: If scenario name is not recognized
        """
        if scenario_name not in self._scenarios:
            available = ", ".join(self._scenarios.keys())
            raise ValueError(f"Unknown scenario: {scenario_name}. Available: {available}")
        
        return self._scenarios[scenario_name]
    
    def list_available(self) -> List[str]:
        """
        List all available scenario names
        
        Returns:
            List of scenario names
        """
        return list(self._scenarios.keys())
    
    def list_scenarios(self) -> List[Scenario]:
        """
        List all available scenario objects
        
        Returns:
            List of Scenario objects
        """
        return list(self._scenarios.values())
    
    def get_by_type(self, scenario_type: str) -> List[Scenario]:
        """
        Get scenarios by type (baseline, pr_change, noop, noise)
        
        Args:
            scenario_type: Type of scenarios to retrieve
            
        Returns:
            List of matching scenarios
        """
        if scenario_type == "noise":
            return [s for s in self._scenarios.values() if s.name.startswith("noise_")]
        elif scenario_type == "baseline":
            return [s for s in self._scenarios.values() if s.name == "baseline"]
        elif scenario_type == "pr_change":
            return [s for s in self._scenarios.values() if s.name == "pr_change"]
        elif scenario_type == "noop":
            return [s for s in self._scenarios.values() if s.name == "noop"]
        else:
            return []


# Convenience function for quick access
def create_scenario(scenario_name: str, repo_root: Path = None) -> Scenario:
    """
    Create a scenario using the factory
    
    Args:
        scenario_name: Name of the scenario to create
        repo_root: Optional repository root path
        
    Returns:
        Scenario object
    """
    factory = ScenarioFactory(repo_root)
    return factory.create(scenario_name)
