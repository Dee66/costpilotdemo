#!/usr/bin/env python3
"""
Test Result Model - Represents a single test outcome
Part of SOLID refactoring: Single Responsibility Principle
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class TestResult:
    """Represents the outcome of a single test"""
    
    name: str
    passed: bool
    reason: str = ""
    details: Optional[dict] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def __str__(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        reason_str = f": {self.reason}" if self.reason else ""
        return f"[{status}] {self.name}{reason_str}"
