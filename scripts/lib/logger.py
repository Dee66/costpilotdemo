#!/usr/bin/env python3
"""
CostPilot Logger - Structured Logging for Test Framework
Professional logging with configurable levels and multiple output formats
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any


class CostPilotLogger:
    """Professional logger for CostPilot test framework"""

    def __init__(self, name: str = "costpilot", level: str = "INFO", log_file: Optional[Path] = None):
        self.name = name
        self.level = getattr(logging, level.upper(), logging.INFO)
        self.log_file = log_file

        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)

        # Remove existing handlers
        self.logger.handlers.clear()

        # Console handler with colored output
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.level)
        console_formatter = CostPilotFormatter(color=True)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # File handler (JSON format) if specified
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(self.level)
            file_formatter = CostPilotFormatter(json_format=True)
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

    def info(self, message: str, **kwargs):
        """Log info message"""
        self.logger.info(message, extra=kwargs)

    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.logger.debug(message, extra=kwargs)

    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.logger.warning(message, extra=kwargs)

    def error(self, message: str, **kwargs):
        """Log error message"""
        self.logger.error(message, extra=kwargs)

    def test_passed(self, test_name: str, **kwargs):
        """Log test passed"""
        self.logger.info(f"✓ {test_name}", extra={"test_status": "passed", **kwargs})

    def test_failed(self, test_name: str, reason: str = "", **kwargs):
        """Log test failed"""
        self.logger.error(f"✗ {test_name}" + (f" - {reason}" if reason else ""),
                         extra={"test_status": "failed", "reason": reason, **kwargs})


class CostPilotFormatter(logging.Formatter):
    """Custom formatter for CostPilot logs"""

    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'RESET': '\033[0m'      # Reset
    }

    def __init__(self, color: bool = False, json_format: bool = False):
        super().__init__()
        self.color = color
        self.json_format = json_format

        if json_format:
            self.format = self._format_json
        else:
            self.format = self._format_text

    def _format_text(self, record: logging.LogRecord) -> str:
        """Format as colored text"""
        timestamp = datetime.fromtimestamp(record.created).strftime('%H:%M:%S')
        level = record.levelname

        if self.color and level in self.COLORS:
            colored_level = f"{self.COLORS[level]}{level}{self.COLORS['RESET']}"
        else:
            colored_level = level

        message = f"[{timestamp}] {colored_level}: {record.getMessage()}"

        # Add extra fields if present
        if hasattr(record, '__dict__') and record.__dict__:
            extras = {k: v for k, v in record.__dict__.items()
                     if k not in ['name', 'msg', 'args', 'levelname', 'levelno',
                                'pathname', 'filename', 'module', 'exc_info',
                                'exc_text', 'stack_info', 'lineno', 'funcName',
                                'created', 'msecs', 'relativeCreated', 'thread',
                                'threadName', 'processName', 'process', 'message']}
            if extras:
                message += f" {extras}"

        return message

    def _format_json(self, record: logging.LogRecord) -> str:
        """Format as JSON"""
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage()
        }

        # Add extra fields
        if hasattr(record, '__dict__') and record.__dict__:
            extras = {k: v for k, v in record.__dict__.items()
                     if k not in ['name', 'msg', 'args', 'levelname', 'levelno',
                                'pathname', 'filename', 'module', 'exc_info',
                                'exc_text', 'stack_info', 'lineno', 'funcName',
                                'created', 'msecs', 'relativeCreated', 'thread',
                                'threadName', 'processName', 'process', 'message']}
            log_entry.update(extras)

        return json.dumps(log_entry)


# Global logger instance
_default_logger = None

def get_logger(name: str = "costpilot", level: str = "INFO", log_file: Optional[Path] = None) -> CostPilotLogger:
    """Get or create a CostPilot logger instance"""
    global _default_logger
    if _default_logger is None or _default_logger.name != name:
        _default_logger = CostPilotLogger(name, level, log_file)
    return _default_logger