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
CostPilotDemo Startup Script

Starts the interactive web demo for CostPilot, including:
- Web UI with cost regression visualization
- ROI calculator
- Interactive findings display

Usage:
    python scripts/start_demo.py [--port PORT] [--no-browser]

Options:
    --port PORT    Port to run the server on (default: 8000)
    --no-browser   Don't automatically open browser
    --help         Show this help message
"""

import argparse
import json
import os
import subprocess
import sys
import time
import webbrowser
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading


class DemoHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Custom HTTP request handler with CORS support for demo"""

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def log_message(self, format, *args):
        # Suppress default HTTP server logs for cleaner output
        pass


def validate_demo_components():
    """Validate that all demo components are present and functional"""
    print("🔍 Validating CostPilotDemo components...")

    issues = []

    # Check required files
    required_files = [
        'index.html',
        'demo/index.html',
        'docs/ROI_CALCULATOR.md',
        'costpilot',
        'snapshots/detect_v1.json',
        'snapshots/predict_v1.json',
        'snapshots/explain_v1.json'
    ]

    for file_path in required_files:
        if not os.path.exists(file_path):
            issues.append(f"❌ Missing required file: {file_path}")
        else:
            print(f"✅ Found: {file_path}")

    # Validate JSON files
    json_files = ['snapshots/detect_v1.json', 'snapshots/predict_v1.json', 'snapshots/explain_v1.json']
    for json_file in json_files:
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r') as f:
                    json.load(f)
                print(f"✅ Valid JSON: {json_file}")
            except json.JSONDecodeError as e:
                issues.append(f"❌ Invalid JSON in {json_file}: {e}")

    # Check CLI binary
    cli_path = './costpilot'
    if os.path.exists(cli_path):
        try:
            result = subprocess.run([cli_path, '--help'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✅ CLI binary functional")
            else:
                issues.append("❌ CLI binary not functional")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            issues.append("❌ CLI binary not executable")
    else:
        issues.append("❌ CLI binary not found")

    if issues:
        print("\n❌ Demo validation failed:")
        for issue in issues:
            print(f"  {issue}")
        return False

    print("\n✅ All demo components validated successfully!")
    return True


def start_server(port=8000):
    """Start the HTTP server"""
    try:
        server_address = ('', port)
        httpd = HTTPServer(server_address, DemoHTTPRequestHandler)
        print(f"🚀 Starting CostPilotDemo server on http://localhost:{port}")
        print("📁 Serving from: " + os.getcwd())

        # Start server in a separate thread
        server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        server_thread.start()

        return httpd, server_thread
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {port} is already in use. Try a different port with --port option.")
        else:
            print(f"❌ Failed to start server: {e}")
        sys.exit(1)


def open_browser(port=8000, delay=2):
    """Open the demo in the default web browser"""
    url = f"http://localhost:{port}"
    print(f"🌐 Opening {url} in your default browser...")

    def _open_browser():
        time.sleep(delay)  # Wait for server to be ready
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print(f"   Please manually open: {url}")

    browser_thread = threading.Thread(target=_open_browser, daemon=True)
    browser_thread.start()


def show_demo_info(port=8000):
    """Display information about the demo"""
    print("\n" + "="*60)
    print("🎯 COSTPILOT DEMO IS RUNNING!")
    print("="*60)
    print(f"📍 Main Demo:      http://localhost:{port}/")
    print(f"🎮 Interactive:     http://localhost:{port}/demo/")
    print(f"💰 ROI Calculator:  http://localhost:{port}/docs/ROI_CALCULATOR.md")
    print()
    print("✨ Features:")
    print("  • Interactive cost regression detection")
    print("  • Real-time findings visualization")
    print("  • ROI calculator with customizable parameters")
    print("  • Working CLI binary for infrastructure scanning")
    print()
    print("🛑 Press Ctrl+C to stop the demo server")
    print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description="Start the CostPilotDemo web application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=8000,
        help='Port to run the server on (default: 8000)'
    )
    parser.add_argument(
        '--no-browser', '-n',
        action='store_true',
        help="Don't automatically open browser"
    )
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate components, don\'t start server'
    )

    args = parser.parse_args()

    # Change to the project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)

    print("🏗️  CostPilotDemo Startup Script")
    print(f"📂 Working directory: {os.getcwd()}")

    # Validate components
    if not validate_demo_components():
        print("\n❌ Demo validation failed. Please fix the issues above and try again.")
        sys.exit(1)

    if args.validate_only:
        print("\n✅ Validation complete. All components are ready.")
        return

    # Start the server
    httpd, server_thread = start_server(args.port)

    # Show demo information
    show_demo_info(args.port)

    # Open browser (unless disabled)
    if not args.no_browser:
        open_browser(args.port)

    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down CostPilotDemo server...")
        httpd.shutdown()
        print("✅ Server stopped. Goodbye!")


if __name__ == "__main__":
    main()