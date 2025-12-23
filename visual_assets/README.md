# Visual Assets Directory

This directory contains screenshots and visual assets for the CostPilot demo repository.

## Screenshot Requirements

All screenshots must meet the following standards:

- **Resolution**: 1920x1080
- **Theme**: Light mode
- **Font**: Default system font
- **Version Tag**: Must show CostPilot version
- **Scenario Tag**: Must show "v1" or current version
- **Context**: All screenshots reference PR #42

## Required Screenshots

### 1. `detect_output_screenshot.png`
- **Content**: CostPilot detect output showing findings from PR #42
- **Must Show**:
  - Resource classifications
  - Rule IDs and severity scores
  - Regression types
  - Cross-service dependencies

### 2. `explain_mode_screenshot.png`
- **Content**: CostPilot explain output with root cause analysis
- **Must Show**:
  - Root cause explanation
  - Heuristic provenance
  - Severity justification
  - Delta breakdown

### 3. `mapping_graph.png`
- **Content**: Mermaid diagram showing cross-service dependencies
- **Must Show**:
  - ALB → Target Group → ASG → EC2 flow
  - CloudWatch → Log Groups → Metric Streams
  - Clear labels and readable at 1080p

### 4. `trend_graph.png`
- **Content**: Cost trend visualization
- **Must Show**:
  - Baseline cost ($52.43)
  - PR change cost ($387.89)
  - SLO threshold ($500)
  - Historical trajectory
  - Clear axes and legend

### 5. `pr_comment_cost_diff.png`
- **Content**: PR comment showing cost comparison
- **Must Show**:
  - Before/after costs
  - Dollar delta
  - Percentage increase
  - Severity indicators
  - Suggested actions

## Screenshot Validation

Before committing screenshots:

1. **Verify resolution**: `file <screenshot>.png | grep 1920x1080`
2. **Check file size**: Should be < 500KB for web performance
3. **Validate against golden outputs**: Screenshots must match `snapshots/` content
4. **Test rendering**: View at 1080p and verify legibility

## Screenshot Manifest

The file `screenshots_manifest.json` tracks all screenshots with metadata:

```json
{
  "version": "1.0.0",
  "screenshots": [
    {
      "filename": "detect_output_screenshot.png",
      "resolution": "1920x1080",
      "theme": "light",
      "source": "snapshots/detect_v1.json",
      "captured_date": "2025-12-06",
      "pr_context": "PR #42"
    }
  ]
}
```

## Capture Process

### Using Real CostPilot Output (Recommended)

```bash
# 1. Run CostPilot on pr-change scenario
costpilot detect --plan infrastructure/terraform/pr-change/tfplan.json

# 2. Capture terminal output (full-screen, light theme)
# Use a screenshot tool at 1920x1080 resolution

# 3. Validate against golden output
diff <(costpilot detect --plan ...) snapshots/detect_v1.json
```

### Using Golden Outputs (Alternative)

```bash
# Display golden output in terminal
cat snapshots/detect_v1.json | jq '.'

# Capture terminal window at 1920x1080
# Ensure version tag and context are visible
```

## CI Integration

Screenshots are validated in CI:

- File existence checks
- Resolution validation (via `file` command)
- Manifest consistency checks
- Cross-reference with golden outputs

See `.github/workflows/costpilot-ci.yml` for validation steps.

## Deterministic Colors

All screenshots must use deterministic color schemes:

- **High Severity**: Red (#DC2626)
- **Medium Severity**: Yellow (#FBBF24)
- **Low Severity**: Blue (#3B82F6)
- **Success**: Green (#10B981)
- **Info**: Gray (#6B7280)

## Notes for Marketing Team

- Screenshots are frozen as "golden visuals" once approved
- Any change requires version bump and team sign-off
- Use these screenshots for blog posts, documentation, and launch materials
- Always reference the correct version tag (v1, v2, etc.)

---

## Terminal Image Generator

This directory includes tools for generating professional terminal screenshots for promotional materials.

### Files

- `terminal_commands.txt` - Sample terminal commands showing CostPilot usage
- `terminal_commands.png` - Generated terminal screenshot image (1920x1080)
- `TERMINAL_CONFIG.md` - Configuration guide for manual terminal screenshots

### Generate Terminal Image

```bash
# From repository root
python3 scripts/generate_terminal_image.py visual_assets/terminal_commands.txt visual_assets/terminal_commands.png
```

### Custom Terminal Image

1. Create a text file with your terminal commands
2. Run the generator script:

```bash
python3 scripts/generate_terminal_image.py path/to/your/commands.txt path/to/output.png
```

### Terminal Commands Content

The `terminal_commands.txt` file contains typical AWS Terraform workflow commands integrated with CostPilot:

1. **terraform init** - Initialize Terraform
2. **terraform plan** - Create execution plan  
3. **costpilot scan** - Analyze costs in the plan
4. **costpilot diff** - Compare against baseline
5. **costpilot explain** - Get detailed cost breakdown
6. **costpilot predict** - Predict future costs
7. **terraform apply** - Apply changes
8. **costpilot trend** - Monitor cost trends
9. **costpilot autofix** - Generate optimization suggestions
10. **costpilot audit** - Audit cost changes

---

**Last Updated**: 2025-12-06  
**Version**: 1.0.0
