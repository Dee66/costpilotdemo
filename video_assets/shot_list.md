# CostPilot Demo Video - Shot List

**Project:** CostPilot Demo Video  
**Duration:** 3:45  
**Format:** 1920x1080, 30fps, 16:9

---

## Pre-Production Checklist

- [ ] Install screen recording software (OBS Studio)
- [ ] Install terminal recording tool (Asciinema)
- [ ] Set up demo repository locally
- [ ] Prepare terminal theme (dark, high contrast)
- [ ] Test font sizes for readability (14pt minimum)
- [ ] Create animated diagrams (Trust Triangle, Architecture)
- [ ] Record voiceover script (dry run)
- [ ] Prepare background music (royalty-free)
- [ ] Set up project in video editor

---

## Shot List by Scene

### OPENING SEQUENCE

**Shot 001: Title Card**
- **Type:** Motion Graphics
- **Duration:** 0:05
- **Content:** CostPilot logo + tagline
- **Status:** [ ] Not Started | [ ] In Progress | [ ] Complete
- **Notes:** Use brand colors, clean fade-in

---

**Shot 002: Repository Landing**
- **Type:** Screen Recording
- **Duration:** 0:15
- **Content:** GitHub repository page, README scroll
- **Camera:** Screen capture (Chrome browser)
- **Status:** [ ] Not Started | [ ] In Progress | [ ] Complete
- **Technical:**
  - URL: github.com/Dee66/costpilotdemo
  - Browser: Chrome (clean profile, no extensions visible)
  - Zoom: 125% (for readability)
  - Scroll speed: Slow, smooth

---

### THE PROBLEM

**Shot 003: PR Diff - Full View**
- **Type:** Screen Recording
- **Duration:** 0:10
- **Content:** Full PR diff on GitHub
- **Status:** [ ] Not Started | [ ] In Progress | [ ] Complete
- **Technical:**
  - Show PR #42
  - Files changed tab
  - Highlight terraform/pr-change/main.tf

---

**Shot 004: PR Diff - Close-up**
- **Type:** Screen Recording (zoomed)
- **Duration:** 0:15
- **Content:** Instance type change line
- **Status:** [ ] Not Started | [ ] In Progress | [ ] Complete
- **Technical:**
  - Zoom: 150%
  - Highlight: `instance_type = "t3.xlarge"`
  - Overlay: Cost annotation (+$113/month)

---

### TRUST TRIANGLE

**Shot 005: Trust Triangle Diagram - Full**
- **Type:** Motion Graphics
- **Duration:** 0:15
- **Content:** Animated Trust Triangle
- **Status:** [ ] Not Started | [ ] In Progress | [ ] Complete
- **Source File:** docs/diagrams/trust_triangle_flow.svg
- **Animation:**
  - Build triangle nodes one by one
  - Animate arrows in sequence
  - Pulse ACTION node

---

**Shot 006: DETECT Node Focus**
- **Type:** Motion Graphics
- **Duration:** 0:05
- **Content:** Zoom into DETECT node
- **Status:** [ ] Not Started | [ ] In Progress | [ ] Complete

---

**Shot 007: PREDICT Node Focus**
- **Type:** Motion Graphics
- **Duration:** 0:05
- **Content:** Zoom into PREDICT node
- **Status:** [ ] Not Started | [ ] In Progress | [ ] Complete

---

**Shot 008: EXPLAIN Node Focus**
- **Type:** Motion Graphics
- **Duration:** 0:05
- **Content:** Zoom into EXPLAIN node
- **Status:** [ ] Not Started | [ ] In Progress | [ ] Complete

---

### LIVE DEMO

**Shot 009: Terminal - Setup**
- **Type:** Terminal Recording
- **Duration:** 0:05
- **Content:** `cd costpilotdemo` and `ls -la`
- **Status:** [ ] Not Started | [ ] In Progress | [ ] Complete
- **Terminal Settings:**
  - Theme: Dark (background: #1f2937)
  - Font: JetBrains Mono 14pt
  - Prompt: Simple (no fancy prompts)
  - Window: Full screen, no decorations

---

**Shot 010: Terminal - Detect Command**
- **Type:** Terminal Recording
- **Duration:** 0:15
- **Content:** `costpilot detect --pr 42` with output
- **Status:** [ ] Not Started | [ ] In Progress | [ ] Complete
- **Technical:**
  - Type slowly (readable)
  - Let output appear line by line
  - Pause 2s on final output

---

**Shot 011: Terminal - Predict Command**
- **Type:** Terminal Recording
- **Duration:** 0:15
- **Content:** `costpilot predict --pr 42` with chart
- **Status:** [ ] Not Started | [ ] In Progress | [ ] Complete
- **Technical:**
  - Show cost comparison table
  - Animate bar chart (if possible)
  - Highlight $552/month number

---

**Shot 012: Terminal - Explain Command**
- **Type:** Terminal Recording
- **Duration:** 0:20
- **Content:** `costpilot explain --pr 42` with mapping
- **Status:** [ ] Not Started | [ ] In Progress | [ ] Complete
- **Technical:**
  - Show dependency tree
  - Highlight propagation path
  - Display cost impact per node

---

**Shot 013: Architecture Diagram - Baseline**
- **Type:** Static Image (with highlights)
- **Duration:** 0:09
- **Content:** Baseline stack architecture
- **Status:** [ ] Not Started | [ ] In Progress | [ ] Complete
- **Source:** docs/diagrams/architecture_overview.svg (left side)
- **Animation:** Pulse green components

---

**Shot 014: Architecture Diagram - PR Regression**
- **Type:** Static Image (with highlights)
- **Duration:** 0:09
- **Content:** PR regression stack
- **Status:** [ ] Not Started | [ ] In Progress | [ ] Complete
- **Source:** docs/diagrams/architecture_overview.svg (right side)
- **Animation:** Pulse red components

---

### POLICY ENFORCEMENT

**Shot 015: Policy File - Editor View**
- **Type:** Screen Recording (VS Code)
- **Duration:** 0:10
- **Content:** policies/default_ec2_type.yml open in editor
- **Status:** [ ] Not Started | [ ] In Progress | [ ] Complete
- **Technical:**
  - Editor: VS Code with dark theme
  - Font: 16pt (readable)
  - Scroll to `rules` section

---

**Shot 016: Policy Violation Output**
- **Type:** Terminal Recording
- **Duration:** 0:10
- **Content:** Policy violation detection in detect output
- **Status:** [ ] Not Started | [ ] In Progress | [ ] Complete
- **Technical:**
  - Highlight policy_violation_detected flag
  - Show violation message

---

### NOISE RESILIENCE

**Shot 017: Noise Test Cases - Grid View**
- **Type:** Motion Graphics (2x2 grid)
- **Duration:** 0:20
- **Content:** 4 test cases with "No findings" results
- **Status:** [ ] Not Started | [ ] In Progress | [ ] Complete
- **Layout:**
  - Top-left: whitespace_only.tf
  - Top-right: comments_only.tf
  - Bottom-left: reordered_resources.tf
  - Bottom-right: description_change.tf
- **Animation:** Green checkmarks appear in sequence

---

### CLOSING

**Shot 018: Key Features Slide**
- **Type:** Motion Graphics
- **Duration:** 0:20
- **Content:** Bullet list of features
- **Status:** [ ] Not Started | [ ] In Progress | [ ] Complete
- **Animation:** Fade in one by one

---

**Shot 019: Call to Action**
- **Type:** Motion Graphics
- **Duration:** 0:15
- **Content:** Repository URL + QR code
- **Status:** [ ] Not Started | [ ] In Progress | [ ] Complete
- **Elements:**
  - Large text: github.com/Dee66/costpilotdemo
  - QR code (bottom right)
  - CTA: "Try CostPilot Today"

---

## Post-Production Checklist

- [ ] Import all shots into editor
- [ ] Arrange shots per storyboard timing
- [ ] Add transitions (fade/slide, 0.5s duration)
- [ ] Color correction (match terminal theme across shots)
- [ ] Add voiceover track (sync to visuals)
- [ ] Add background music (royalty-free)
- [ ] Add sound effects (subtle)
- [ ] Create lower-thirds for key points
- [ ] Add captions/subtitles (optional)
- [ ] Export test render (check quality)
- [ ] Final export (1920x1080, 30fps, H.264)
- [ ] Upload to hosting (YouTube, Vimeo)
- [ ] Create thumbnail (1280x720)

---

## Assets Required

**Motion Graphics:**
- [ ] CostPilot logo (high-res PNG/SVG)
- [ ] Trust Triangle diagram (SVG)
- [ ] Architecture diagram (SVG)
- [ ] Title cards (After Effects templates)

**Screen Recordings:**
- [ ] GitHub repository scroll
- [ ] PR diff views (2 shots)
- [ ] VS Code with policy file
- [ ] Terminal sessions (5 shots)

**Audio:**
- [ ] Voiceover recording (WAV, 48kHz)
- [ ] Background music (royalty-free)
- [ ] Sound effects library

**Fonts:**
- [ ] JetBrains Mono (code/terminal)
- [ ] Inter (UI/titles)

---

**Total Shots:** 19  
**Estimated Recording Time:** 4-6 hours  
**Estimated Editing Time:** 4-6 hours  
**Total Production Time:** 8-12 hours

---

## Notes

- Keep terminal recordings clean (no typos)
- Ensure all text is readable at 1080p (minimum 14pt)
- Use consistent color theme across all shots
- Test video on different screens before final export
- Consider creating both 16:9 (YouTube) and 1:1 (social media) versions
