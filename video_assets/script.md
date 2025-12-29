# CostPilot Demo Video Script

**Duration:** 3-4 minutes  
**Target Audience:** DevOps engineers, platform teams, cloud cost optimization professionals  
**Tone:** Professional, technical, clear demonstration of capabilities

---

## Opening (0:00 - 0:20)

**[Visual: CostPilot logo + demo repository]**

**Voiceover:**
> "Meet CostPilot - the intelligent cost analysis tool that helps you catch expensive infrastructure changes before they hit production. This is the official demonstration repository, showing exactly how CostPilot works in a real-world scenario."

---

## Scene 1: The Problem (0:20 - 0:45)

**[Visual: PR diff showing terraform changes]**

**Voiceover:**
> "Here's a common scenario: Your team submits a PR that changes an EC2 instance type from t3.micro to t3.xlarge. Seems reasonable for a performance upgrade, right?"

**[Visual: Highlight the instance_type change in code]**

> "But this single line change will increase your monthly AWS bill by over $110 per month - or $1,300 per year - just for one resource."

---

## Scene 2: The Trust Triangle (0:45 - 1:30)

**[Visual: Trust Triangle diagram animating: Detect → Predict → Explain]**

**Voiceover:**
> "CostPilot uses the Trust Triangle approach to give you complete visibility:"

**[Highlight DETECT phase]**
> "First, DETECT identifies all cost-impacting changes. Not just the obvious ones - CostPilot catches subtle regressions like disabled lifecycle policies or infinite log retention."

**[Highlight PREDICT phase]**
> "Next, PREDICT calculates the exact monthly cost increase. In this PR, we see the total impact: $552 per month - a 964% increase from our baseline."

**[Highlight EXPLAIN phase]**
> "Finally, EXPLAIN shows you WHY costs increased. CostPilot traces the impact through your infrastructure - from the instance change through the autoscaling group to the load balancer."

---

## Scene 3: Real Demo (1:30 - 2:30)

**[Visual: Terminal showing CostPilot commands]**

**Voiceover:**
> "Let's see it in action. Starting with our baseline infrastructure:"

**[Show: costpilot detect command output]**
```
$ costpilot detect --pr 42

✓ Detected 4 cost-impacting changes
  - EC2 instance type upgrade (HIGH)
  - S3 lifecycle disabled (MEDIUM)
  - CloudWatch retention infinite (MEDIUM)
  - EBS volume increased (LOW)
```

**[Show: costpilot predict command output]**
```
$ costpilot predict --pr 42

Monthly Cost Impact: +$552/month
Baseline: $57/month → PR: $609/month
Increase: +964%
```

**[Show: costpilot explain command output with mapping]**
```
$ costpilot explain --pr 42

Root Cause: EC2 instance type change
Cost Propagation Path:
  aws_launch_template.main
    → aws_autoscaling_group.main (2-4 instances)
      → aws_lb_target_group.main
        → aws_lb.main
Impact: $476.70/month (87% of total increase)
```

---

## Scene 4: Policy Enforcement (2:30 - 3:00)

**[Visual: Policy file and baseline configuration]**

**Voiceover:**
> "CostPilot also supports policy-based governance. Our demo includes a default EC2 type policy that flags any deviation from t3.micro."

**[Show: Policy violation detection]**
```yaml
# policies/default_ec2_type.yml
spec:
  resource_type: aws_instance
  rules:
    - enforce-instance-type
      condition: resource.instance_type != "t3.micro"
      action: flag
```

> "This helps teams maintain cost-efficient defaults while still allowing exceptions when properly justified."

---

## Scene 5: Noise Resilience (3:00 - 3:20)

**[Visual: Noise test cases]**

**Voiceover:**
> "CostPilot is smart about what it flags. Whitespace changes, comment updates, and resource reordering produce zero findings - because they have zero cost impact."

**[Show: 4 noise test results, all showing "No findings"]**

> "This means fewer false positives and more trust in the alerts you do receive."

---

## Closing (3:20 - 3:45)

**[Visual: GitHub repository, documentation links]**

**Voiceover:**
> "Everything you've seen is reproducible from the official CostPilot demo repository. The infrastructure code, golden outputs, and test cases are all available at github.com/Dee66/costpilotdemo."

**[Show: Key features list]**
- Detect cost-impacting changes
- Predict monthly impact
- Explain root causes
- Policy enforcement
- Noise resilience

> "CostPilot: Catch expensive changes before they hit production."

**[End card: Logo + Repository URL]**

---

## Production Notes

**Key Points to Emphasize:**
- Real, reproducible demo (not marketing fluff)
- Trust Triangle methodology
- Concrete numbers ($552/month, 964% increase)
- Smart detection (no false positives)
- Policy governance

**Visual Requirements:**
- Clear terminal output (readable at 1080p)
- Animated Trust Triangle diagram
- Side-by-side baseline vs PR comparison
- Clean, professional code highlighting
- GitHub repository prominently displayed

**Call to Action:**
- Visit demo repository
- Try CostPilot on your infrastructure
- Star the repository
- Report issues or contribute

---

**Total Runtime:** ~3:45  
**Format:** Screen recording + voiceover  
**Resolution:** 1920x1080  
**Frame Rate:** 30fps
