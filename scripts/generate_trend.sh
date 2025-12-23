#!/bin/bash
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

# Generate Trend Visualization
# Creates deterministic trend history and SVG

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "Generating trend data..."

# Generate trend history JSON (fixed seed for determinism)
cat > "$REPO_ROOT/snapshots/trend_history_v1.json" << 'EOF'
{
  "scenario_version": "v1",
  "trends": [
    {
      "name": "flat_trend",
      "description": "Stable costs, expected behavior",
      "data_points": [
        {"date": "2025-11-01", "cost": 50.00},
        {"date": "2025-11-08", "cost": 51.20},
        {"date": "2025-11-15", "cost": 49.80},
        {"date": "2025-11-22", "cost": 50.50},
        {"date": "2025-11-29", "cost": 50.10}
      ]
    },
    {
      "name": "upward_trend",
      "description": "Gradual increase, requires attention",
      "data_points": [
        {"date": "2025-11-01", "cost": 50.00},
        {"date": "2025-11-08", "cost": 120.00},
        {"date": "2025-11-15", "cost": 245.00},
        {"date": "2025-11-22", "cost": 450.00},
        {"date": "2025-11-29", "cost": 720.00}
      ]
    },
    {
      "name": "slo_breach_trend",
      "description": "Budget threshold exceeded",
      "data_points": [
        {"date": "2025-11-01", "cost": 50.00, "slo": 500.00},
        {"date": "2025-11-08", "cost": 120.00, "slo": 500.00},
        {"date": "2025-11-15", "cost": 245.00, "slo": 500.00},
        {"date": "2025-11-22", "cost": 450.00, "slo": 500.00},
        {"date": "2025-11-29", "cost": 720.00, "slo": 500.00, "breach": true}
      ]
    }
  ]
}
EOF

# Generate deterministic SVG (800x300 as per spec)
cat > "$REPO_ROOT/snapshots/trend_v1.svg" << 'EOF'
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="300" viewBox="0 0 800 300">
  <defs>
    <linearGradient id="costGradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#ff6b6b;stop-opacity:0.8" />
      <stop offset="100%" style="stop-color:#ff6b6b;stop-opacity:0.2" />
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="800" height="300" fill="#f8f9fa"/>
  
  <!-- Grid lines -->
  <line x1="100" y1="50" x2="100" y2="250" stroke="#dee2e6" stroke-width="2"/>
  <line x1="100" y1="250" x2="750" y2="250" stroke="#dee2e6" stroke-width="2"/>
  
  <!-- Trend line (upward) -->
  <polyline points="100,230 250,190 400,140 550,90 700,40" 
            fill="none" stroke="#ff6b6b" stroke-width="3"/>
  
  <!-- Data points -->
  <circle cx="100" cy="230" r="5" fill="#c92a2a"/>
  <circle cx="250" cy="190" r="5" fill="#c92a2a"/>
  <circle cx="400" cy="140" r="5" fill="#c92a2a"/>
  <circle cx="550" cy="90" r="5" fill="#c92a2a"/>
  <circle cx="700" cy="40" r="5" fill="#fa5252"/>
  
  <!-- SLO threshold line -->
  <line x1="100" y1="90" x2="750" y2="90" stroke="#ffd93d" stroke-width="2" stroke-dasharray="5,5"/>
  <text x="760" y="95" font-family="Arial" font-size="12" fill="#495057">SLO</text>
  
  <!-- Labels -->
  <text x="400" y="25" font-family="Arial" font-size="18" font-weight="bold" 
        fill="#212529" text-anchor="middle">Cost Trend: Upward Regression</text>
  
  <!-- Y-axis labels -->
  <text x="85" y="55" font-family="Arial" font-size="12" fill="#495057" text-anchor="end">$750</text>
  <text x="85" y="145" font-family="Arial" font-size="12" fill="#495057" text-anchor="end">$400</text>
  <text x="85" y="255" font-family="Arial" font-size="12" fill="#495057" text-anchor="end">$50</text>
  
  <!-- X-axis labels -->
  <text x="100" y="270" font-family="Arial" font-size="10" fill="#6c757d" text-anchor="middle">Nov 1</text>
  <text x="250" y="270" font-family="Arial" font-size="10" fill="#6c757d" text-anchor="middle">Nov 8</text>
  <text x="400" y="270" font-family="Arial" font-size="10" fill="#6c757d" text-anchor="middle">Nov 15</text>
  <text x="550" y="270" font-family="Arial" font-size="10" fill="#6c757d" text-anchor="middle">Nov 22</text>
  <text x="700" y="270" font-family="Arial" font-size="10" fill="#6c757d" text-anchor="middle">Nov 29</text>
  
  <!-- Status indicator -->
  <rect x="650" y="280" width="15" height="15" fill="#ff6b6b"/>
  <text x="670" y="292" font-family="Arial" font-size="12" fill="#212529">SLO Breach</text>
</svg>
EOF

# Copy to demo directory
cp "$REPO_ROOT/snapshots/trend_history.json" "$REPO_ROOT/.costpilot/demo/"
cp "$REPO_ROOT/snapshots/trend_v1.svg" "$REPO_ROOT/.costpilot/demo/"
cp "$REPO_ROOT/snapshots/trend_history.json" "$REPO_ROOT/costpilot_artifacts/output_trend.json"

echo "✓ Trend visualization generated"
