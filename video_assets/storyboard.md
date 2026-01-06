# CostPilot Demo Video Storyboard

**Duration:** 3:45  
**Format:** Horizontal (16:9) 1920x1080  
**Style:** Professional technical demonstration

---

## Shot 1: Title Card (0:00 - 0:05)
**Duration:** 5 seconds

**Visual:**
- CostPilot logo (centered)
- Subtitle: "Intelligent Cloud Cost Analysis"
- Background: Subtle gradient (blue to purple)

**Animation:**
- Logo fades in
- Text appears letter-by-letter

**Audio:**
- Upbeat intro music (fade in)

---

## Shot 2: Repository Introduction (0:05 - 0:20)
**Duration:** 15 seconds

**Visual:**
- GitHub repository page (github.com/Dee66/costpilotdemo)
- Pan down showing README structure
- Highlight: "Official Demo Repository"

**Animation:**
- Smooth scroll through repository
- Highlight pulse on key elements

**Audio:**
- VO: "Meet CostPilot - the intelligent cost analysis tool..."
- Background music continues (lower volume)

---

## Shot 3: The Problem - PR Diff (0:20 - 0:45)
**Duration:** 25 seconds

**Visual:**
- Split screen:
  - Left: Terraform code (before)
  - Right: Terraform code (after)
- Highlight: `instance_type = "t3.xlarge"`
- Cost annotation appears: "+$113/month"

**Animation:**
- Diff line highlights in red
- Cost callout zooms in
- Dollar signs animated

**Audio:**
- VO: "Here's a common scenario..."
- Sound effect: Cash register "cha-ching" (subtle)

---

## Shot 4: Trust Triangle Overview (0:45 - 1:00)
**Duration:** 15 seconds

**Visual:**
- Full-screen Trust Triangle diagram
- Three nodes: DETECT, PREDICT, EXPLAIN
- Animated arrows showing flow
- Central ACTION node pulses

**Animation:**
- Triangle builds piece by piece
- Arrows animate in sequence
- Each phase lights up as mentioned

**Audio:**
- VO: "CostPilot uses the Trust Triangle approach..."
- Music swells slightly

---

## Shot 5: DETECT Phase (1:00 - 1:15)
**Duration:** 15 seconds

**Visual:**
- Terminal window (full screen)
- Command: `costpilot detect --pr 42`
- Output shows 4 findings with severity levels
- Red/yellow/green color coding

**Animation:**
- Text types out (simulated)
- Findings appear one by one
- Severity icons pulse

**Audio:**
- VO: "First, DETECT identifies all cost-impacting changes..."
- Typing sound effects (subtle)

---

## Shot 6: PREDICT Phase (1:15 - 1:30)
**Duration:** 15 seconds

**Visual:**
- Terminal window
- Command: `costpilot predict --pr 42`
- Bar chart appears: Baseline vs PR cost
- Numbers animate: $57 → $609

**Animation:**
- Bar chart grows
- Percentage counter animates: 0% → 964%
- Cost difference highlighted

**Audio:**
- VO: "Next, PREDICT calculates the exact monthly cost..."
- Sound effect: Graph "whoosh"

---

## Shot 7: EXPLAIN Phase (1:30 - 1:50)
**Duration:** 20 seconds

**Visual:**
- Terminal window (left 60%)
- Dependency graph (right 40%)
- Shows: instance → ASG → target_group → ALB
- Each node highlights in sequence

**Animation:**
- Graph builds node by node
- Arrows animate showing flow
- Cost number appears at each node

**Audio:**
- VO: "Finally, EXPLAIN shows you WHY costs increased..."
- Sound effect: Connection "ping" for each arrow

---

## Shot 8: Live Demo Montage (1:50 - 2:30)
**Duration:** 40 seconds

**Visual:**
- Quick cuts between:
  1. Baseline infrastructure diagram (5s)
  2. PR change diff side-by-side (5s)
  3. CostPilot detect output (5s)
  4. CostPilot predict with chart (8s)
  5. CostPilot explain with mapping (8s)
  6. Architecture diagram showing impact (9s)

**Animation:**
- Smooth transitions (slide/fade)
- Key numbers zoom in
- Critical changes pulse

**Audio:**
- VO: "Let's see it in action..." (continuous)
- Faster-paced background music

---

## Shot 9: Policy Enforcement (2:30 - 2:50)
**Duration:** 20 seconds

**Visual:**
- Split screen:
  - Left: Policy YAML file
  - Right: Violation detection output
- Highlight: "t3.micro → t3.xlarge VIOLATION"

**Animation:**
- Policy file scrolls to relevant section
- Violation box shakes slightly
- Red "X" appears

**Audio:**
- VO: "CostPilot also supports policy-based governance..."
- Sound effect: Alert beep (subtle)

---

## Shot 10: Noise Resilience (2:50 - 3:10)
**Duration:** 20 seconds

**Visual:**
- 2x2 grid showing 4 noise test cases:
  - Whitespace only
  - Comments only
  - Reordered resources
  - Description changes
- Each shows "✓ No findings"

**Animation:**
- Green checkmarks appear in sequence
- All four pulse together at end

**Audio:**
- VO: "CostPilot is smart about what it flags..."
- Sound effect: Success chime for each checkmark

---

## Shot 11: Key Features Summary (3:10 - 3:30)
**Duration:** 20 seconds

**Visual:**
- Clean slide with bullet points:
  - ✓ Detect cost-impacting changes
  - ✓ Predict monthly impact ($552/month)
  - ✓ Explain root causes
  - ✓ Policy enforcement
  - ✓ Noise resilience (zero false positives)

**Animation:**
- Bullets appear one by one (fade in)
- Icons pulse on appearance

**Audio:**
- VO: "Everything you've seen is reproducible..."
- Music builds to crescendo

---

## Shot 12: Call to Action (3:30 - 3:45)
**Duration:** 15 seconds

**Visual:**
- GitHub repository URL (large, centered)
- QR code (bottom right)
- Social: @costpilot
- CTA: "Try CostPilot Today"

**Animation:**
- URL types out
- QR code fades in
- Social handles bounce in

**Audio:**
- VO: "CostPilot: Catch expensive changes before they hit production."
- Music ends with strong finish

---

## Production Specifications

**Technical Requirements:**
- Resolution: 1920x1080 (Full HD)
- Frame Rate: 30fps
- Aspect Ratio: 16:9
- Format: MP4 (H.264)
- Bitrate: 8-10 Mbps

**Software Tools:**
- Screen Recording: OBS Studio / Camtasia
- Video Editing: DaVinci Resolve / Premiere Pro
- Animation: After Effects (for diagrams)
- Terminal: Asciinema / Terminalizer (for clean recordings)

**Font Standards:**
- Code: JetBrains Mono / Fira Code (14pt)
- UI Text: Inter / SF Pro (readable at 1080p)
- Titles: Inter Bold (24-36pt)

**Color Palette:**
- Success: #10b981 (green)
- Warning: #f59e0b (amber)
- Error: #ef4444 (red)
- Primary: #3b82f6 (blue)
- Background: #1f2937 (dark gray)
- Text: #f9fafb (off-white)

**Audio Mix:**
- Voiceover: -18 LUFS
- Music: -24 LUFS
- Sound Effects: -20 LUFS
- Final Master: -16 LUFS

---

**Total Shots:** 12  
**Total Duration:** 3:45  
**Complexity:** Medium (requires terminal recording + diagram animation)  
**Production Time Estimate:** 8-12 hours
