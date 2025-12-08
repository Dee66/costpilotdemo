"""
Result Exporter - Multi-format test result output
Abstract base class and concrete exporters for JSON, HTML, Markdown, JUnit XML
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import json
from datetime import datetime
from pathlib import Path


class ResultExporter(ABC):
    """
    Abstract base class for result exporters
    Implements Template Method pattern for consistent export workflow
    """
    
    @abstractmethod
    def export(self, results: List[Dict[str, Any]], output_path: str = None) -> str:
        """
        Export test results to specified format
        
        Args:
            results: List of test suite result dictionaries
            output_path: Optional file path to write output
            
        Returns:
            Formatted output string
        """
        pass
    
    def _calculate_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate summary statistics from results"""
        return {
            "total_suites": len(results),
            "passed_suites": sum(1 for r in results if r["status"] == "success"),
            "failed_suites": sum(1 for r in results if r["status"] == "failed"),
            "error_suites": sum(1 for r in results if r["status"] == "error"),
            "total_tests": sum(r.get("total", 0) for r in results),
            "passed_tests": sum(r.get("passed", 0) for r in results),
            "failed_tests": sum(r.get("failed", 0) for r in results),
            "timestamp": datetime.now().isoformat()
        }


class JSONExporter(ResultExporter):
    """Export results as JSON"""
    
    def export(self, results: List[Dict[str, Any]], output_path: str = None) -> str:
        """
        Export results as JSON format
        Schema: {name, status, passed, failed, reason[]}
        """
        summary = self._calculate_summary(results)
        
        # Build structured output
        output = {
            "summary": summary,
            "suites": [
                {
                    "name": r.get("name", "unknown"),
                    "status": r["status"],
                    "passed": r.get("passed", 0),
                    "failed": r.get("failed", 0),
                    "total": r.get("total", 0),
                    "pass_rate": r.get("pass_rate", 0.0),
                    "reason": [r.get("error", "")] if r["status"] == "error" else []
                }
                for r in results
            ]
        }
        
        json_str = json.dumps(output, indent=2)
        
        if output_path:
            Path(output_path).write_text(json_str)
        
        return json_str


class HTMLExporter(ResultExporter):
    """Export results as HTML with color coding and expandable details"""
    
    def export(self, results: List[Dict[str, Any]], output_path: str = None) -> str:
        """
        Export results as HTML format
        Features: color-coded pass/fail, expandable details, time series graphs (placeholder)
        """
        summary = self._calculate_summary(results)
        
        html_parts = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            "<meta charset='UTF-8'>",
            "<title>CostPilot Test Results</title>",
            self._generate_styles(),
            "</head>",
            "<body>",
            "<div class='container'>",
            "<h1>🧪 CostPilot Test Results</h1>",
            self._generate_summary_section(summary),
            self._generate_suites_section(results),
            "</div>",
            self._generate_scripts(),
            "</body>",
            "</html>"
        ]
        
        html_str = "\n".join(html_parts)
        
        if output_path:
            Path(output_path).write_text(html_str)
        
        return html_str
    
    def _generate_styles(self) -> str:
        """Generate CSS styles"""
        return """
<style>
body { 
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif; 
    margin: 0; 
    padding: 20px; 
    background: #f5f5f5;
}
.container { 
    max-width: 1200px; 
    margin: 0 auto; 
    background: white; 
    padding: 30px; 
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
h1 { 
    color: #333; 
    border-bottom: 3px solid #4caf50; 
    padding-bottom: 10px; 
}
.summary { 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    color: white; 
    padding: 20px; 
    margin: 20px 0; 
    border-radius: 8px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
}
.summary .stat { 
    text-align: center; 
}
.summary .stat .label { 
    font-size: 0.9em; 
    opacity: 0.9; 
    margin-bottom: 5px;
}
.summary .stat .value { 
    font-size: 2em; 
    font-weight: bold; 
}
.suite { 
    border: 1px solid #ddd; 
    margin: 15px 0; 
    border-radius: 8px; 
    overflow: hidden;
    transition: box-shadow 0.3s ease;
}
.suite:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.suite-header { 
    padding: 15px; 
    cursor: pointer; 
    display: flex; 
    justify-content: space-between; 
    align-items: center;
    transition: background 0.2s ease;
}
.suite-header:hover {
    background: #f8f8f8;
}
.suite.success .suite-header { 
    background: #e8f5e9; 
    border-left: 5px solid #4caf50; 
}
.suite.failed .suite-header { 
    background: #ffebee; 
    border-left: 5px solid #f44336; 
}
.suite.error .suite-header { 
    background: #fff3e0; 
    border-left: 5px solid #ff9800; 
}
.suite-title { 
    font-size: 1.2em; 
    font-weight: 600; 
    display: flex;
    align-items: center;
    gap: 10px;
}
.suite-stats { 
    display: flex; 
    gap: 20px; 
    font-size: 0.9em;
}
.suite-details { 
    padding: 15px; 
    background: #fafafa; 
    display: none;
}
.suite-details.expanded { 
    display: block; 
}
.pass { color: #4caf50; font-weight: bold; }
.fail { color: #f44336; font-weight: bold; }
.error { color: #ff9800; font-weight: bold; }
.status-badge {
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 0.85em;
    font-weight: 600;
    text-transform: uppercase;
}
.status-badge.success {
    background: #4caf50;
    color: white;
}
.status-badge.failed {
    background: #f44336;
    color: white;
}
.status-badge.error {
    background: #ff9800;
    color: white;
}
.expand-icon {
    transition: transform 0.3s ease;
}
.expand-icon.expanded {
    transform: rotate(180deg);
}
</style>
"""
    
    def _generate_summary_section(self, summary: Dict[str, Any]) -> str:
        """Generate summary statistics section"""
        pass_rate = 0
        if summary["total_tests"] > 0:
            pass_rate = (summary["passed_tests"] / summary["total_tests"]) * 100
        
        return f"""
<div class='summary'>
    <div class='stat'>
        <div class='label'>Total Suites</div>
        <div class='value'>{summary['total_suites']}</div>
    </div>
    <div class='stat'>
        <div class='label'>Passed Suites</div>
        <div class='value'>{summary['passed_suites']}</div>
    </div>
    <div class='stat'>
        <div class='label'>Total Tests</div>
        <div class='value'>{summary['total_tests']}</div>
    </div>
    <div class='stat'>
        <div class='label'>Pass Rate</div>
        <div class='value'>{pass_rate:.1f}%</div>
    </div>
</div>
<p style='color: #666; font-size: 0.9em;'>Generated: {summary['timestamp']}</p>
"""
    
    def _generate_suites_section(self, results: List[Dict[str, Any]]) -> str:
        """Generate test suites section"""
        suites_html = ["<div class='suites'>"]
        
        for i, result in enumerate(results):
            status = result["status"]
            name = result.get("name", "unknown")
            passed = result.get("passed", 0)
            failed = result.get("failed", 0)
            total = result.get("total", 0)
            
            icon = "✅" if status == "success" else ("❌" if status == "failed" else "⚠️")
            
            suites_html.append(f"""
<div class='suite {status}'>
    <div class='suite-header' onclick='toggleDetails({i})'>
        <div class='suite-title'>
            <span>{icon}</span>
            <span>{name}</span>
            <span class='status-badge {status}'>{status}</span>
        </div>
        <div class='suite-stats'>
            <span class='pass'>{passed} passed</span>
            <span class='fail'>{failed} failed</span>
            <span>📊 {total} total</span>
            <span class='expand-icon' id='icon-{i}'>▼</span>
        </div>
    </div>
    <div class='suite-details' id='details-{i}'>
        <p><strong>Status:</strong> {status}</p>
        <p><strong>Tests Run:</strong> {total}</p>
        <p><strong>Pass Rate:</strong> {result.get('pass_rate', 0):.1f}%</p>
        {self._generate_error_section(result) if status == 'error' else ''}
    </div>
</div>
""")
        
        suites_html.append("</div>")
        return "\n".join(suites_html)
    
    def _generate_error_section(self, result: Dict[str, Any]) -> str:
        """Generate error details section"""
        error = result.get("error", "Unknown error")
        return f"<div style='background: #ffebee; padding: 10px; border-radius: 4px; margin-top: 10px;'><strong>Error:</strong> {error}</div>"
    
    def _generate_scripts(self) -> str:
        """Generate JavaScript for interactivity"""
        return """
<script>
function toggleDetails(index) {
    const details = document.getElementById('details-' + index);
    const icon = document.getElementById('icon-' + index);
    details.classList.toggle('expanded');
    icon.classList.toggle('expanded');
}
</script>
"""


class MarkdownExporter(ResultExporter):
    """Export results as Markdown with checkboxes"""
    
    def export(self, results: List[Dict[str, Any]], output_path: str = None) -> str:
        """
        Export results as Markdown format
        Features: checkboxes for pass/fail, links to relevant files
        """
        summary = self._calculate_summary(results)
        
        lines = [
            "# 🧪 CostPilot Test Results",
            "",
            f"**Generated:** {summary['timestamp']}",
            "",
            "## 📊 Summary",
            "",
            f"- **Total Suites:** {summary['total_suites']}",
            f"- **Passed Suites:** {summary['passed_suites']} ✅",
            f"- **Failed Suites:** {summary['failed_suites']} ❌",
            f"- **Error Suites:** {summary['error_suites']} ⚠️",
            "",
            f"- **Total Tests:** {summary['total_tests']}",
            f"- **Passed Tests:** {summary['passed_tests']} ✅",
            f"- **Failed Tests:** {summary['failed_tests']} ❌",
            "",
        ]
        
        if summary['total_tests'] > 0:
            pass_rate = (summary['passed_tests'] / summary['total_tests']) * 100
            lines.append(f"**Pass Rate:** {pass_rate:.1f}%")
        
        lines.extend([
            "",
            "## 📋 Test Suites",
            ""
        ])
        
        for result in results:
            status = result["status"]
            name = result.get("name", "unknown")
            passed = result.get("passed", 0)
            failed = result.get("failed", 0)
            total = result.get("total", 0)
            
            checkbox = "[x]" if status == "success" else "[ ]"
            icon = "✅" if status == "success" else ("❌" if status == "failed" else "⚠️")
            
            lines.extend([
                f"### {icon} {name}",
                "",
                f"- {checkbox} **Status:** {status}",
                f"- **Tests:** {passed}/{total} passed ({result.get('pass_rate', 0):.1f}%)",
                ""
            ])
            
            if status == "error":
                lines.extend([
                    "**Error:**",
                    f"```",
                    result.get("error", "Unknown error"),
                    f"```",
                    ""
                ])
            
            # Add link to test file (if in scripts directory)
            lines.append(f"[View Source](../scripts/{name}.py)")
            lines.append("")
        
        markdown_str = "\n".join(lines)
        
        if output_path:
            Path(output_path).write_text(markdown_str)
        
        return markdown_str


class JUnitXMLExporter(ResultExporter):
    """Export results as JUnit XML for CI/CD integration"""
    
    def export(self, results: List[Dict[str, Any]], output_path: str = None) -> str:
        """
        Export results as JUnit XML format
        Features: test suite elements, test case elements, valid XML schema
        """
        summary = self._calculate_summary(results)
        
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<testsuites tests="{summary["total_tests"]}" '
            f'failures="{summary["failed_tests"]}" '
            f'errors="{summary["error_suites"]}" '
            f'time="0" '
            f'name="CostPilot Test Suites" '
            f'timestamp="{summary["timestamp"]}">'
        ]
        
        for result in results:
            name = result.get("name", "unknown")
            total = result.get("total", 0)
            passed = result.get("passed", 0)
            failed = result.get("failed", 0)
            status = result["status"]
            
            lines.append(f'  <testsuite name="{name}" tests="{total}" failures="{failed}" errors="0" time="0">')
            
            # Add test cases (we don't have individual test details, so create summary)
            if status == "success":
                lines.append(f'    <testcase name="{name}_suite" classname="{name}" time="0"/>')
            elif status == "failed":
                lines.append(f'    <testcase name="{name}_suite" classname="{name}" time="0">')
                lines.append(f'      <failure message="{failed} tests failed"/>')
                lines.append(f'    </testcase>')
            elif status == "error":
                error_msg = result.get("error", "Unknown error").replace('"', '&quot;')
                lines.append(f'    <testcase name="{name}_suite" classname="{name}" time="0">')
                lines.append(f'      <error message="{error_msg}"/>')
                lines.append(f'    </testcase>')
            
            lines.append('  </testsuite>')
        
        lines.append('</testsuites>')
        
        xml_str = "\n".join(lines)
        
        if output_path:
            Path(output_path).write_text(xml_str)
        
        return xml_str


def create_exporter(format_type: str) -> ResultExporter:
    """
    Factory function to create exporters
    
    Args:
        format_type: One of 'json', 'html', 'markdown', 'junit'
        
    Returns:
        ResultExporter instance
    """
    exporters = {
        "json": JSONExporter,
        "html": HTMLExporter,
        "markdown": MarkdownExporter,
        "junit": JUnitXMLExporter
    }
    
    if format_type not in exporters:
        raise ValueError(f"Unknown format: {format_type}. Supported: {list(exporters.keys())}")
    
    return exporters[format_type]()
