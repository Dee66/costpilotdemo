# CostPilot Demo Video Script

**Duration:** 3 minutes  
**Resolution:** 1080p  
**Tone:** Enthusiastic, technical, value-focused  
**Target Audience:** DevOps engineers, platform leads, technical decision-makers

---

## 0:00 - 0:10 | Hook & Problem Statement

**[SCREEN: GitHub PR #42 diff showing instance type change]**

**VOICEOVER:**  
"Watch CostPilot catch a **$335 per month** AWS regression in real-time—**before** it hits production."

**[TEXT OVERLAY: $335/month saved]**

---

## 0:10 - 0:30 | The Problem

**[SCREEN: Terraform diff highlighting t3.micro → t3.xlarge]**

**VOICEOVER:**  
"Here's PR #42. A developer changed an EC2 instance type from `t3.micro` to `t3.xlarge` for 'better performance.' Looks innocent, right? Wrong."

**[CURSOR highlights the instance_type line]**

**VOICEOVER:**  
"This single line change increases monthly costs from **$52 to $388**—a **639% jump**."

**[TEXT OVERLAY: +639% cost increase]**

---

## 0:30 - 1:00 | Detection in Action

**[SCREEN: Terminal running `costpilot detect`]**

**VOICEOVER:**  
"CostPilot runs as part of the CI/CD pipeline. It analyzes the Terraform plan and flags **4 cost-impacting changes** in seconds."

**[SCREEN: Terminal output showing 4 findings with severity badges]**

**VOICEOVER:**  
"Notice the severity badges: 🔴 **High** for the instance type escalation. Policy violation detected. Rule ID: `policy:default-ec2-type`."

**[CURSOR highlights the severity and rule_id fields]**

---

## 1:00 - 1:30 | Cost Impact Prediction

**[SCREEN: PR comment showing cost table]**

**VOICEOVER:**  
"CostPilot posts the cost impact directly in the pull request. No more surprise bills."

**[SCREEN: Cost table showing Before: $52.43, After: $387.89, Delta: +$335.54]**

**VOICEOVER:**  
"**Before:** $52 per month. **After:** $388 per month. **Delta:** plus $335. That's **$4,020 wasted annually** if this merges."

**[TEXT OVERLAY: $4,020/year wasted if merged]**

---

## 1:30 - 2:00 | Auto-Fix Suggestions

**[SCREEN: Auto-fix section with HCL patch]**

**VOICEOVER:**  
"Here's where CostPilot shines. It doesn't just detect—it **fixes**."

**[CURSOR clicks 'Copy Patch' button]**

**VOICEOVER:**  
"Copy the auto-generated HCL patch. Paste it into your PR. Done. No manual debugging. No digging through Terraform state."

**[SCREEN: Side-by-side diff showing revert]**

**VOICEOVER:**  
"The patch reverts the instance type to `t3.medium`—saving **$335 per month**."

**[TEXT OVERLAY: $335/month saved with one click]**

---

## 2:00 - 2:30 | Infrastructure Mapping

**[SCREEN: Mermaid diagram showing ALB → Target Group → ASG → EC2]**

**VOICEOVER:**  
"But wait—there's more. CostPilot maps your infrastructure dependencies."

**[CURSOR hovers over nodes, highlighting connections]**

**VOICEOVER:**  
"See how the ALB connects to the target group, which connects to the auto-scaling group, which spawns EC2 instances. One change ripples through your entire stack."

**[SCREEN: Nodes flash red for high-cost resources]**

**VOICEOVER:**  
"Red nodes indicate high-cost resources. Yellow indicates medium. You see the **full blast radius** before merging."

---

## 2:30 - 2:50 | Call to Action

**[SCREEN: GitHub repo landing page - Dee66/costpilotdemo]**

**VOICEOVER:**  
"Ready to stop cost regressions before they hit production?"

**[TEXT OVERLAY: github.com/Dee66/costpilotdemo]**

**VOICEOVER:**  
"Try the interactive demo at **github.com/Dee66/costpilotdemo**. No installation required. See CostPilot analyze PR #42 in your browser."

---

## 2:50 - 3:00 | Closing

**[SCREEN: ROI calculator showing 9.5x ROI]**

**VOICEOVER:**  
"Join teams saving **$28,000 per year** with CostPilot. Shift cost review left. Catch regressions at PR time. Ship with confidence."

**[TEXT OVERLAY: Start Free Trial → github.com/Dee66/costpilotdemo]**

**VOICEOVER:**  
"CostPilot. Cloud cost regressions, caught before merge."

**[FADE OUT]**

---

## Production Notes

### Visual Requirements

1. **Terminal Theme:** Light background, high contrast (Solarized Light or GitHub Light)
2. **Font Size:** Minimum 14pt for code/terminal
3. **Cursor Speed:** Slow, deliberate movements (0.5x speed)
4. **Screen Resolution:** Record at 1920x1080, export at 1080p
5. **Frame Rate:** 30fps minimum

### Audio Requirements

1. **Microphone:** Condenser mic with pop filter
2. **Background Music:** Subtle tech/corporate track at -20dB
3. **Voiceover Pace:** 140-160 words per minute (natural, not rushed)
4. **Audio Mix:** Voice at -6dB, music at -20dB, sound effects at -12dB

### Editing Requirements

1. **Transitions:** Fast cuts (no dissolves), max 0.2s fade for scene changes
2. **Text Overlays:** Bold sans-serif (Roboto or Inter), 48pt minimum
3. **Zoom Effects:** Use sparingly, only for key dollar amounts
4. **Highlights:** Yellow box for emphasis, red underline for warnings

### Recording Tools

**Option 1: Loom (Recommended for speed)**
- Browser-based, no setup required
- Built-in editing and captions
- Export at 1080p

**Option 2: OBS Studio (Recommended for quality)**
- Free, open-source
- More control over layout and sources
- Export at 1080p/30fps

### Script Timing Breakdown

| Section | Duration | Word Count |
|---------|----------|------------|
| Hook | 0:10 | 15 words |
| Problem | 0:20 | 45 words |
| Detection | 0:30 | 50 words |
| Prediction | 0:30 | 45 words |
| Auto-fix | 0:30 | 50 words |
| Mapping | 0:30 | 55 words |
| CTA | 0:20 | 35 words |
| Closing | 0:10 | 20 words |
| **TOTAL** | **3:00** | **315 words** |

**Average Pace:** 105 words per minute (relaxed, conversational)

---

## Rehearsal Checklist

- [ ] Read script aloud 3x for natural delivery
- [ ] Time each section to hit marks exactly
- [ ] Practice cursor movements (no erratic clicking)
- [ ] Test screen recording software
- [ ] Verify audio levels (-6dB voice, no clipping)
- [ ] Close all non-essential applications
- [ ] Disable notifications and alerts
- [ ] Clean up desktop (minimal icons/windows)

---

## Post-Production Checklist

- [ ] Add intro bumper (0:00-0:03, CostPilot logo)
- [ ] Add text overlays at key moments
- [ ] Sync voiceover with screen actions
- [ ] Add background music (subtle, non-distracting)
- [ ] Add captions/subtitles (for accessibility)
- [ ] Create custom thumbnail (use $335/month callout)
- [ ] Export at 1080p/30fps, H.264 codec, AAC audio
- [ ] Test playback on desktop and mobile
- [ ] Upload to YouTube and Vimeo (unlisted)
- [ ] Embed in README after hero section

---

## YouTube Metadata

**Title:** CostPilot Demo: Catch $335/mo AWS Regression in Real-Time

**Description:**
```
Watch CostPilot prevent a $4,020/year cost regression at PR time—before it hits production.

In this 3-minute demo, see how CostPilot:
✅ Detects 4 cost-impacting changes in seconds
✅ Predicts exact cost impact ($52 → $388/month)
✅ Provides auto-fix suggestions with one-click HCL patches
✅ Maps infrastructure dependencies to show blast radius

No more surprise AWS bills. Shift cost review left.

🔗 Try the Interactive Demo: https://dee66.github.io/costpilotdemo/
📘 Read the Case Study: https://github.com/Dee66/costpilotdemo/blob/main/docs/CASE_STUDY.md
💰 Calculate Your ROI: https://github.com/Dee66/costpilotdemo/blob/main/ROI_CALCULATOR.md

#AWS #Terraform #FinOps #DevOps #CloudCost #CostOptimization
```

**Tags:** costpilot, aws, terraform, finops, devops, cloud cost, cost optimization, infrastructure as code, terraform cost, aws bill, cost management

**Thumbnail Text:** "Save $335/month" with screenshot of PR comment

---

## Distribution Checklist

- [ ] Upload to YouTube (public)
- [ ] Upload to Vimeo (unlisted backup)
- [ ] Embed in README.md after hero section
- [ ] Share on Twitter with demo link
- [ ] Share on LinkedIn with case study link
- [ ] Post in r/devops, r/terraform, r/aws subreddits
- [ ] Add to Product Hunt launch (if applicable)
- [ ] Include in email campaign to beta users
