# Video Assets

This directory contains video assets for CostPilot launch materials and demonstrations.

## 🎬 Directory Structure

```
video_assets/
├── screenshots/          # Product screenshots for marketing
├── screen-recordings/    # Demo walkthroughs and tutorials
├── launch-video/         # Launch video assets and clips
└── social-media/         # Social media clips and thumbnails
```

## 🔒 CI Protection

This directory is **protected by CI guardrails**:
- ❌ Direct modifications blocked in pull requests
- ✅ Changes only allowed through dedicated video asset PRs
- ✅ All assets version-controlled for reproducibility

## 📸 Screenshot Guidelines

All screenshots must originate from this demo repository:
- Use deterministic outputs from `snapshots/`
- Capture from PR #42 walkthrough (`docs/walkthrough.md`)
- Ensure scenario version `v1` is visible
- Follow brand guidelines for consistency

## 🎥 Video Recording Guidelines

### Demo Walkthroughs
1. Start with clean repository state (run `./tools/reset_demo.sh`)
2. Follow PR #42 scenario exactly as documented
3. Show Trust Triangle in action (Detect → Predict → Explain)
4. Demonstrate patch preview and auto-fix capabilities
5. Highlight deterministic outputs and hash validation

### Launch Video
- Duration: 60-90 seconds
- Focus on value proposition: prevent cost regressions before merge
- Show real cost impact ($450-720/month regression detected)
- Emphasize speed (<1 second analysis) and accuracy

## 📋 Asset Inventory

### Screenshots (Planned)
- [ ] PR #42 diff view with CostPilot bot comment
- [ ] Detect output with 4 findings highlighted
- [ ] Predict output showing $450-720 monthly delta
- [ ] Explain output with root cause analysis
- [ ] Dependency mapping diagram (Mermaid rendered)
- [ ] Cost trend graph showing SLO breach
- [ ] Patch preview with before/after comparison
- [ ] CI pipeline success with all checks passing

### Screen Recordings (Planned)
- [ ] Complete PR workflow (3-5 minutes)
- [ ] Trust Triangle deep dive (2-3 minutes)
- [ ] Patch preview and auto-fix demo (1-2 minutes)
- [ ] Reset script demonstration (1 minute)

### Launch Video (Planned)
- [ ] Hero video (60-90 seconds)
- [ ] Feature highlights (30 seconds each):
  - Detection capabilities
  - Prediction accuracy
  - Explanation clarity
  - Auto-fix suggestions

## 🎨 Branding Guidelines

- **Primary Color**: #2196F3 (blue - matches cost trend line)
- **Accent Colors**:
  - High severity: #ff6b6b (red)
  - Medium severity: #ffd93d (yellow)
  - Low severity: #6bcf7f (green)
- **Font**: System default (sans-serif)
- **Logo**: CostPilot wordmark with navigation icon

## 📦 Asset Formats

### Screenshots
- Format: PNG (lossless)
- Resolution: 1920x1080 minimum
- DPI: 144+ for retina displays
- Color space: sRGB

### Videos
- Format: MP4 (H.264)
- Resolution: 1920x1080
- Frame rate: 30 fps
- Bitrate: 5-8 Mbps
- Audio: AAC 192 kbps (if narration included)

## 🔄 Version Control

All assets versioned with scenario:
- `screenshot_detect_v1.png`
- `video_walkthrough_v1.mp4`
- `launch_hero_v1.mp4`

## 🚫 What NOT to Include

- Real customer data or account IDs
- Non-demo infrastructure screenshots
- Unedited raw footage (must be polished)
- Assets from non-canonical sources

## 📚 Related Documentation

- [Main README](../README.md) - Demo overview
- [PR #42 Walkthrough](../docs/walkthrough.md) - Script for video content
- [products.yml](../docs/products.yml) - Full specification
- [snapshots/](../snapshots/) - Canonical outputs for screenshots

---

**Last Updated:** 2025-12-06  
**Scenario Version:** v1  
**Status:** Directory structure created, assets pending
