# Marketing Review & Quality Gates Checklist

**Version:** 2.0.0  
**Purpose:** Pre-release quality assurance for CostPilot demo repository  
**Last Updated:** 2025-12-06

---

## 📋 Overview

This checklist ensures all marketing assets, documentation, and demo outputs meet quality standards before public release. All items must be verified and signed off before launching v2.0.0.

---

## ✅ Output Consistency Review

### Golden Outputs Validation

- [ ] **All snapshots match spec v2.0.0**
  - `detect_v1.json` consistent with expected findings
  - `predict_v1.json` shows correct cost ranges
  - `explain_v1.json` includes proper heuristic provenance
  - `snippet_v1.tf` provides valid auto-fix code
  - `patch_v1.diff` applies cleanly

- [ ] **Hash validation passes**
  ```bash
  python3 tools/validate_golden_hashes.py
  # Expected: ✅ ALL GOLDEN OUTPUTS VALIDATED (9/9)
  ```

- [ ] **Lineage metadata complete**
  - All snapshots include `source_plan`, `scenario`, `plan_time`, `seed`
  - Hash chains valid (`hash_before` → `hash_after`)

- [ ] **No placeholder or fake data**
  - All costs based on actual AWS pricing (as of freeze date)
  - No "TODO", "TBD", or "PLACEHOLDER" strings
  - All resource names consistent (no test-123, foo-bar, etc.)

**Sign-Off:**  
_Name:_ ____________  _Date:_ ______  _Role:_ Engineering Lead

---

## 📸 Screenshot Quality Review

### Resolution & Theme Standards

- [ ] **All screenshots at 1920x1080**
  ```bash
  for f in visual_assets/*.png; do 
    file "$f" | grep -q "1920 x 1080" || echo "❌ $f wrong resolution"
  done
  ```

- [ ] **All screenshots use light theme**
  - Terminal background: light (not dark)
  - Syntax highlighting appropriate for light theme
  - No inverted or high-contrast themes

- [ ] **Version tags visible**
  - CostPilot version shown (v1.0.0)
  - Scenario version shown (v1)
  - PR context shown (PR #42)

### Screenshot Content Validation

- [ ] **detect_output_screenshot.png**
  - Shows all 4 findings from `detect_v1.json`
  - Rule IDs visible
  - Severity colors correct (high=red, medium=yellow)
  - Resource addresses match spec

- [ ] **explain_mode_screenshot.png**
  - Root cause analysis visible
  - Heuristic provenance shown
  - Severity justification included
  - Matches `explain_v1.json` content

- [ ] **mapping_graph.png**
  - Graph centered, not clipped
  - All node labels readable
  - Cross-service dependencies clear
  - Matches `snapshots/mapping_v1.mmd` (if exists)

- [ ] **trend_graph.png**
  - Axes visible and labeled
  - Legend readable
  - Baseline and PR lines distinguishable
  - SLO threshold marked if applicable

- [ ] **pr_comment_cost_diff.png**
  - Dollar amounts match `predict_v1.json`
  - Percentage calculations correct
  - Formatting appropriate for GitHub PR comment

**Sign-Off:**  
_Name:_ ____________  _Date:_ ______  _Role:_ Design/UX Lead

---

## 💬 PR Comment Readability

### Desktop (1080p) Verification

- [ ] **comment_detect.txt readable at 1920x1080**
  - Tables fit within viewport
  - No horizontal scrolling required
  - Font size legible (minimum 11pt)

- [ ] **comment_predict.txt readable at 1920x1080**
  - Cost tables formatted correctly
  - Numbers aligned properly
  - Calculations visible and verifiable

- [ ] **comment_explain.txt readable at 1920x1080**
  - Root cause analysis flows logically
  - Code blocks don't overflow
  - Links and references clickable

- [ ] **comment_autofix.txt readable at 1920x1080**
  - Code snippets properly formatted
  - Diff syntax highlighting (+ / -) clear
  - Instructions actionable

### Mobile Verification

- [ ] **All comments tested on mobile** (375px width minimum)
  - Tables stack vertically if needed
  - No text cutoff or overflow
  - Tap targets appropriately sized
  - Code blocks scrollable but not critical info hidden

- [ ] **Markdown rendering tested on GitHub**
  - Headers render correctly
  - Lists and numbering correct
  - Code fences syntax-highlighted
  - Emoji render consistently

**Sign-Off:**  
_Name:_ ____________  _Date:_ ______  _Role:_ Product Manager

---

## 📊 Diagram Quality Review

### SVG Rendering Tests

- [ ] **trust_triangle_flow.svg renders on GitHub**
  - Opens in browser without errors
  - All text legible
  - Colors display correctly
  - Arrows and flow clear

- [ ] **architecture_overview.svg renders on GitHub**
  - All components visible
  - Labels readable
  - Legend clear
  - Layout not clipped

### Mermaid Diagrams (if applicable)

- [ ] **Mermaid diagrams render without errors**
  - Syntax valid (test on mermaid.live)
  - Layout seed fixed for determinism
  - Node labels don't overlap
  - Graph direction appropriate (TD, LR, etc.)

### Responsiveness

- [ ] **SVGs responsive at 1080p**
  - Scale appropriately
  - Text remains legible when scaled
  - No pixelation or artifacts

- [ ] **SVGs accessible**
  - Alt text or title elements present
  - Color contrast meets WCAG AA standards
  - Works without JavaScript

**Sign-Off:**  
_Name:_ ____________  _Date:_ ______  _Role:_ Technical Writer

---

## 📝 JSON Output Formatting

### Consistency Checks

- [ ] **All JSON outputs use 2-space indentation**
  ```bash
  jq --indent 2 '.' snapshots/detect_v1.json > /tmp/test.json
  diff snapshots/detect_v1.json /tmp/test.json
  # Should show no differences
  ```

- [ ] **Arrays and objects properly formatted**
  - Opening brackets on same line
  - Closing brackets on new line
  - Trailing commas removed

- [ ] **Numbers formatted consistently**
  - Float precision: 2 decimal places
  - No scientific notation (e.g., 1e-5)
  - Currency values: $XX.XX format

- [ ] **Timestamps use ISO 8601 format**
  - Format: `2025-12-06T16:47:00Z`
  - UTC timezone (Z suffix)
  - No milliseconds unless required

**Sign-Off:**  
_Name:_ ____________  _Date:_ ______  _Role:_ QA Engineer

---

## 📖 README Narrative Alignment

### Content Accuracy

- [ ] **README matches actual repo behavior**
  - Quick start steps work as documented
  - File paths correct
  - Command examples execute successfully
  - No broken links

- [ ] **Code snippets in README are copy-pastable**
  - Bash commands tested
  - Terraform examples valid
  - Python scripts run without errors

- [ ] **Screenshots referenced in README exist**
  - All `![image](path)` links resolve
  - Image descriptions accurate
  - Captions match content

### Narrative Flow

- [ ] **Story flows logically**
  - Hero → Why → What → How
  - Example PR #42 used consistently
  - Trust Triangle explained clearly
  - Auto-fix suggestions compelling

- [ ] **Technical accuracy**
  - AWS pricing accurate (as of freeze date)
  - Terraform syntax valid
  - Cost calculations correct
  - Policy examples realistic

- [ ] **Tone appropriate for target audience**
  - Technical enough for engineers
  - Accessible for managers
  - Clear for first-time users
  - Professional for enterprise

**Sign-Off:**  
_Name:_ ____________  _Date:_ ______  _Role:_ Content Lead

---

## 🎥 Video Assets (if applicable)

### Quality Standards

- [ ] **Resolution: 1920x1080 or higher**
- [ ] **Frame rate: 30fps minimum**
- [ ] **Audio clear and audible**
- [ ] **Subtitles/captions available**
- [ ] **No background noise or distractions**

### Content Standards

- [ ] **Demo follows documented scenario**
- [ ] **Matches golden outputs exactly**
- [ ] **Transitions smooth and professional**
- [ ] **Branding consistent with CostPilot**
- [ ] **Length appropriate (5-10 minutes recommended)**

**Sign-Off:**  
_Name:_ ____________  _Date:_ ______  _Role:_ Video Producer

---

## 🔍 Drift Detection

### File Drift Checks

- [ ] **No drift in protected directories**
  ```bash
  git diff origin/main...HEAD -- snapshots/ costpilot_artifacts/ visual_assets/
  # Expected: No output (or only approved changes)
  ```

- [ ] **Manifest hashes match files**
  ```bash
  python3 tools/validate_golden_hashes.py
  # Expected: ✅ ALL GOLDEN OUTPUTS VALIDATED
  ```

### Semantic Drift Checks

- [ ] **Severity scores consistent**
  - High severity findings still high
  - Medium severity findings still medium
  - No unexplained severity changes

- [ ] **Regression classifications unchanged**
  - Cost increases still flagged
  - Policy violations still detected
  - Cross-service dependencies still mapped

**Sign-Off:**  
_Name:_ ____________  _Date:_ ______  _Role:_ DevOps Lead

---

## 🚀 Final Pre-Release Checklist

### Repository Health

- [ ] **CI/CD passing**
  - All GitHub Actions workflows green
  - Integrity tests pass
  - Drift detection clean
  - No failing jobs

- [ ] **Documentation complete**
  - README up to date
  - DRIFT_MANAGEMENT.md finalized
  - GOLDEN_VERSION_SIGNOFF.md template ready
  - API docs current

- [ ] **No sensitive data committed**
  - No AWS credentials
  - No API keys
  - No internal URLs/IPs
  - No personal information

### Marketing Readiness

- [ ] **Blog post drafted** (if applicable)
- [ ] **Social media assets prepared**
- [ ] **Launch announcement ready**
- [ ] **Demo video uploaded** (if applicable)
- [ ] **Press kit available**
- [ ] **Interactive demo link added to all marketing materials**
  - README includes demo link (https://dee66.github.io/costpilotdemo/)
  - Case study references demo
  - ROI calculator links to demo
  - Social proof section mentions demo

### Legal & Compliance

- [ ] **License file present** (MIT)
- [ ] **No copyright violations**
- [ ] **Third-party attributions correct**
- [ ] **Privacy policy compliant** (if collecting data)

**Final Sign-Off:**  
_Name:_ ____________  _Date:_ ______  _Role:_ Release Manager

---

## 📅 Release Timeline

| Milestone | Date | Owner | Status |
|-----------|------|-------|--------|
| Marketing review complete | ________ | ________ | ⬜ Pending |
| Design review complete | ________ | ________ | ⬜ Pending |
| Engineering review complete | ________ | ________ | ⬜ Pending |
| Final sign-off | ________ | ________ | ⬜ Pending |
| Release to production | ________ | ________ | ⬜ Pending |

---

## 🐛 Issues & Blockers

| Issue | Priority | Owner | Resolution | Date Resolved |
|-------|----------|-------|------------|---------------|
| _Example: Screenshot resolution incorrect_ | High | Design | Re-captured | 2025-12-06 |
| | | | | |
| | | | | |

---

## 📋 Post-Release Verification

After release, verify:

- [ ] **Public repository accessible**
- [ ] **README renders correctly on GitHub**
- [ ] **Screenshots display properly**
- [ ] **Links work (including badges)**
- [ ] **CI badges show correct status**
- [ ] **Star/fork counts visible**
- [ ] **Issues/PRs enabled** (if desired)

---

**Document Version:** 1.0.0  
**Created:** 2025-12-06  
**Last Review:** __________  
**Next Review Due:** __________

---

_This checklist is part of the CostPilot v2.0.0 release process. All sign-offs must be completed before public launch._
