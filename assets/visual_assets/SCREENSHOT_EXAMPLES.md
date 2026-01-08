# Screenshot Examples & Format Guide

This document provides detailed specifications for the 5 required screenshots in the CostPilot Demo repository.

---

## Screenshot Requirements Summary

| Screenshot | Source | Resolution | Theme | Max Size | Status |
|------------|--------|------------|-------|----------|--------|
| detect_output_screenshot.png | detect_v1.json | 1920x1080 | Light | 2MB | Pending |
| explain_mode_screenshot.png | explain_v1.json | 1920x1080 | Light | 2MB | Pending |
| mapping_graph.png | mapping_v1.mmd | 1920x1080 | Light | 2MB | Pending |
| trend_graph.png | trend_history_v1.json | 1920x1080 | Light | 2MB | Pending |
| pr_comment_cost_diff.png | comment_predict.txt | 1920x1080 | Light | 2MB | Pending |

---

## Example 1: detect_output_screenshot.png

### Expected Content

The screenshot should show terminal output displaying the detect_v1.json findings in a readable format:

```
┌──────────────────────────────────────────────────────────────────┐
│ CostPilot Detect - PR #42 Analysis                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ 📊 FINDINGS SUMMARY                                              │
│   Total Findings: 4                                              │
│   High Severity: 2                                               │
│   Medium Severity: 2                                             │
│                                                                  │
│ ⚠️  HIGH SEVERITY FINDINGS                                       │
│                                                                  │
│ 1. EC2 Instance Type Upgrade                                     │
│    Resource: aws_launch_template.main                            │
│    Change: t3.micro → t3.xlarge                                  │
│    Cost Impact: +$227.96/month                                   │
│    Rule: instance_type_upgrade                                   │
│                                                                  │
│ 2. S3 Lifecycle Disabled                                         │
│    Resource: aws_s3_bucket.data                                  │
│    Change: lifecycle_rule removed                                │
│    Cost Impact: +$82.80/month (at month 12)                      │
│    Rule: s3_lifecycle_disabled                                   │
│                                                                  │
│ 📉 MEDIUM SEVERITY FINDINGS                                      │
│                                                                  │
│ 3. EBS Volume Size Increase                                      │
│    Resource: aws_launch_template.main                            │
│    Change: 20GB → 200GB                                          │
│    Cost Impact: +$18.00/month                                    │
│    Rule: ebs_volume_increase                                     │
│                                                                  │
│ 4. CloudWatch Infinite Retention                                 │
│    Resource: aws_cloudwatch_log_group.app                        │
│    Change: 30 days → infinite                                    │
│    Cost Impact: +$90.00/month (at month 12)                      │
│    Rule: cloudwatch_retention_infinite                           │
│                                                                  │
│ 🚨 POLICY VIOLATION DETECTED                                     │
│    Policy: production_instance_types                             │
│    Violation: t3.xlarge not in allowlist [t3.micro, t3.small]   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Capture Guidelines
- Use `cat snapshots/detect_v1.json | jq '.' | less` for clean output
- Ensure color-coding visible (red for high, yellow for medium)
- Version tag should be visible in header or footer
- Include timestamp from metadata

---

## Example 2: explain_mode_screenshot.png

### Expected Content

Terminal showing the explain output with root cause analysis:

```
┌──────────────────────────────────────────────────────────────────┐
│ CostPilot Explain - Root Cause Analysis                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ 🔍 FINDING 1: EC2 Instance Type Upgrade                          │
│                                                                  │
│ Root Cause:                                                      │
│   Instance type changed from t3.micro (2 vCPU, 1GB) to          │
│   t3.xlarge (4 vCPU, 16GB) in launch template configuration.    │
│                                                                  │
│ Heuristic Provenance:                                            │
│   • Heuristic: ec2_instance_pricing_v2                           │
│   • Confidence: 0.95                                             │
│   • Data Source: AWS EC2 pricing API                             │
│   • Last Updated: 2025-12-01                                     │
│                                                                  │
│ Severity Score: 8.5/10                                           │
│   • Cost Impact: High (+$227.96/month)                           │
│   • Resource Criticality: High (compute layer)                   │
│   • Reversibility: Easy                                          │
│                                                                  │
│ Delta Justification:                                             │
│   Baseline: t3.micro @ $0.0104/hour × 730 hours = $7.59/month   │
│   PR Change: t3.xlarge @ $0.1664/hour × 730 hours = $121.47/mo  │
│   Increase: $235.55/month (+3,004%)                              │
│                                                                  │
│ Cross-Service Impact:                                            │
│   ALB → Target Group → ASG → EC2 (CHANGED) → EBS                │
│   • EBS volumes scale with instance count                        │
│   • CloudWatch logs increase with instance activity              │
│   • Network transfer may increase with larger instances          │
│                                                                  │
│ 💡 Remediation Options:                                          │
│   1. Revert to t3.micro (saves $227.96/month)                    │
│   2. Use t3.small as middle ground (saves $114/month)            │
│   3. Document business justification for xlarge                  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Capture Guidelines
- Show complete explanation for at least 1-2 findings
- Include heuristic provenance section
- Display severity score breakdown
- Show cross-service dependency graph if available

---

## Example 3: mapping_graph.png

### Expected Visual

Mermaid diagram rendered showing resource dependencies:

```
                    ┌────────────────────┐
                    │  Application LB    │
                    │   (aws_lb.main)    │
                    └──────────┬─────────┘
                               │
                    ┌──────────▼─────────┐
                    │   Target Group     │
                    │ (aws_lb_target...) │
                    └──────────┬─────────┘
                               │
                    ┌──────────▼─────────┐
                    │ Auto Scaling Group │
                    │  (aws_autoscal...) │
                    └──────────┬─────────┘
                               │
            ┌──────────────────┼──────────────────┐
            │                  │                  │
    ┌───────▼────────┐  ┌──────▼──────┐  ┌───────▼────────┐
    │ EC2 Instances  │  │ CloudWatch  │  │   S3 Bucket    │
    │  t3.xlarge ⚠️  │  │  Logs ⚠️    │  │  No Lifecycle  │
    │                │  │             │  │      ⚠️        │
    └───────┬────────┘  └─────────────┘  └────────────────┘
            │
    ┌───────▼────────┐
    │  EBS Volumes   │
    │   200GB ⚠️     │
    └────────────────┘

Legend:
  ⚠️  = Cost regression detected
  Green nodes = Efficient
  Red nodes = High cost impact
  Yellow nodes = Medium cost impact
```

### Capture Guidelines
- Use Mermaid Live Editor or VS Code extension
- Ensure all nodes visible
- Color-coding should match: red (high), yellow (medium), green (ok)
- Save at high quality (PNG format)
- Verify all edges/arrows render correctly

---

## Example 4: trend_graph.png

### Expected Visual

Line graph showing cost trend over time:

```
Monthly Cost Trend - PR #42 vs Baseline

$400 ┤                                         ╭──── PR Change
     │                                    ╭────╯     ($387.89)
$350 ┤                               ╭────╯
     │                          ╭────╯
$300 ┤                     ╭────╯
     │                ╭────╯
$250 ┤           ╭────╯
     │      ╭────╯
$200 ┤ ╭────╯
     │╭╯
$150 ┤╯
     │
$100 ┤
     │
$50  ┼────────────────────────────────────────── Baseline ($52.43)
     │
$0   └┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬──
      M1   M2   M3   M4   M5   M6   M7   M8   M9  M10  M11  M12

Key Metrics:
• Baseline: $52.43/month (flat)
• PR Change Month 1: $245.43/month (+368%)
• PR Change Month 12: $387.89/month (+639%) ← includes time-bombs
• SLO Threshold: $500/month (77.6% utilized)

Time-Bomb Analysis:
• S3 storage grows: +$82.80/month by M12 (no lifecycle)
• CloudWatch logs: +$90/month by M12 (infinite retention)
```

### Capture Guidelines
- Can be created in Excel, Google Sheets, or using ASCII art
- Show baseline as flat line
- Show PR change as increasing (due to time-bombs)
- Include key metrics callout
- Highlight SLO threshold
- Save at 1920x1080

---

## Example 5: pr_comment_cost_diff.png

### Expected Content

GitHub PR comment formatted markdown showing cost breakdown:

```
## 💰 CostPilot Prediction - PR #42

### Monthly Cost Impact

| Resource | Baseline | PR Change | Δ | Impact |
|----------|----------|-----------|---|--------|
| **EC2 Instances** | $7.59 | $235.55 | **+$227.96** | 🔴 High |
| **EBS Volumes** | $2.00 | $20.00 | +$18.00 | 🟡 Medium |
| **S3 Storage** | $0.00 | $0.00* | +$82.80* | 🟡 Time-bomb |
| **CloudWatch Logs** | $0.00 | $0.00* | +$90.00* | 🟡 Time-bomb |
| **ALB** | $16.20 | $16.20 | $0.00 | ✅ OK |
| **Total** | **$52.43** | **$387.89*** | **+$335.46** | 🔴 +639% |

\* Includes projected cost at month 12 due to accumulation

### ⚠️ Policy Violations

- **production_instance_types**: t3.xlarge not in allowlist

### 🚨 SLO Impact

- Budget: $500/month
- Projected: $387.89/month
- **Utilization: 77.6%** ⚠️ Approaching threshold

### 💡 Quick Wins

1. **Revert to t3.micro** → Save $227.96/month
2. **Restore S3 lifecycle** → Prevent $82.80/month growth
3. **Set CloudWatch retention to 90 days** → Prevent $90/month growth

**Combined savings: ~$400/month**

---
*Generated by CostPilot v1.0.0 | Scenario: PR #42*
```

### Capture Guidelines
- Render in GitHub-style markdown viewer
- Ensure table formatting is correct
- Color indicators should be visible (🔴🟡✅)
- Include header and footer
- Show at actual GitHub width (~800px main content)

---

## File Specifications

### All Screenshots Must Meet:

1. **Resolution:** Exactly 1920x1080 pixels
2. **Format:** PNG with transparency support
3. **Color Depth:** 24-bit RGB or 32-bit RGBA
4. **Compression:** Optimized, max 2MB per file
5. **Theme:** Light theme (white/light gray background)
6. **Font:** Monospace for code, sans-serif for text
7. **DPI:** 96 DPI minimum (standard screen)

### Naming Convention:
- Lowercase with underscores
- Descriptive suffix: `_screenshot.png` or `_graph.png`
- Match manifest entries exactly

### Storage:
- Location: `visual_assets/`
- Version controlled: Yes (committed to repo)
- Manifest: Update `screenshots_manifest.json` after capture

---

## Validation Checklist

After capturing each screenshot:

- [ ] Verify resolution: `identify -format "%wx%h" filename.png`
- [ ] Check file size: `ls -lh filename.png` (should be < 2MB)
- [ ] Validate content matches source (detect_v1.json, etc.)
- [ ] Ensure text is readable at 100% zoom
- [ ] Confirm theme is light (not dark mode)
- [ ] Update manifest status to "captured"
- [ ] Add commit with appropriate message

---

## Tips for High-Quality Screenshots

1. **Clean Terminal:**
   - Close unnecessary tabs/panes
   - Clear scrollback buffer
   - Set appropriate font size (14-16pt)

2. **Optimal Lighting:**
   - Use light theme for better contrast
   - Ensure syntax highlighting is visible
   - Avoid cursor blinking in frame

3. **Composition:**
   - Center important content
   - Leave some whitespace at edges
   - Include relevant context (header/footer)

4. **Consistency:**
   - Use same terminal theme for all shots
   - Maintain consistent font across screenshots
   - Use same window decorations

---

**Last Updated:** 2025-12-06  
**Status:** Ready for capture  
**Estimated Time:** 30-45 minutes for all 5 screenshots
