# Spec v2.0.0 Analysis & Gap Assessment

**Date:** 2025-12-06  
**Current Progress:** 150/152 tasks (98.7% of v1.0.0 spec)  
**New Spec:** product.yml v2.0.0 (585 lines)

---

## Executive Summary

The v2.0.0 spec introduces **significant expansions** to the demo repository requirements. Based on my analysis, there are approximately **80-100 NEW tasks** across 8 new major areas, plus enhancements to existing sections.

### Critical Findings:

1. **New Directory Structure Required** ⚠️
   - 4 new top-level directories
   - 13+ new files/subdirectories
   - Will require filesystem changes

2. **Major New Features Required**
   - Policy & governance demo (NEW)
   - Noise/false-positive testing (NEW)
   - Marketing assets (screenshots, diagrams, PR comments) (NEW)
   - Enhanced baseline infrastructure (mini real-world stack)

3. **Backward Compatibility**
   - Most v1 work is preserved
   - Enhancements are mostly additive
   - Some files need renaming (trend_history.json → trend_history_v1.json)

---

## New Directory Structure Requirements

### NEW Directories & Files:

```
NEW: policies/
     └── default_ec2_type.yml                    # NEW

NEW: infrastructure/terraform/noise-cases/
     ├── whitespace_only.tf                      # NEW
     ├── comments_only.tf                        # NEW
     ├── reordered_resources.tf                  # NEW
     └── description_change.tf                   # NEW

NEW: pr_comments/
     ├── comment_detect.txt                      # NEW
     ├── comment_predict.txt                     # NEW
     ├── comment_explain.txt                     # NEW
     └── comment_autofix.txt                     # NEW

NEW: diagram/
     ├── trust_triangle_flow.svg                 # NEW
     └── architecture_overview.svg               # NEW

NEW: video_assets/
     ├── script.md                               # NEW
     ├── storyboard.md                           # NEW
     └── shot_list.md                            # NEW

MODIFIED: .costpilot/
          ├── demo/ (existing)
          └── baselines.json                     # NEW

RENAMED: snapshots/trend_history.json → trend_history_v1.json
```

**Total New Directories:** 4  
**Total New Files:** 18  
**Total Renamed Files:** 1

---

## Section-by-Section Analysis

### Section 0: PURPOSE & DEMO CONTRACT (NEW)

**Conceptual Section** - Defines principles, not implementation tasks.

**Key Concepts:**
- `purpose_binding`: This repo = ground truth
- `demo_contract`: Freeze rules, no changes after v1 without version bump
- Marketing claims must map 1:1 to demo outputs

**Tasks:** None (documentation/governance only)

---

### Section 3: DIRECTORY STRUCTURE (EXPANDED)

**Status:** Partially complete (13 of 19 directories exist)

**NEW Tasks:**
- [ ] Create `policies/` directory
- [ ] Create `policies/default_ec2_type.yml`
- [ ] Create `infrastructure/terraform/noise-cases/` directory
- [ ] Create 4 noise test case files
- [ ] Create `pr_comments/` directory
- [ ] Create 4 PR comment text files
- [ ] Create `diagram/` directory
- [ ] Create 2 diagram SVG files
- [ ] Create `video_assets/` directory
- [ ] Create 3 video asset markdown files
- [ ] Create `.costpilot/baselines.json`
- [ ] Rename `trend_history.json` → `trend_history_v1.json`

**Estimated Tasks:** 18

---

### Section 5: INFRASTRUCTURE SCENARIOS (ENHANCED)

**Status:** Baseline needs expansion

**Current Baseline Stack:**
- ✅ ec2_t3_micro_autoscaling_group
- ✅ alb + target_group + listener
- ✅ s3_bucket_with_lifecycle_enabled
- ✅ cloudwatch_logs_with_30_day_retention

**NEW Baseline Requirements (mini_real_world_stack):**
- [ ] rest_api_service (EC2 or Fargate-backed)
- [ ] background_worker (queue consumer)
- [ ] queue_or_topic (SQS-like pattern)
- [ ] analytics_s3_bucket (with lifecycle)

**NEW PR Regression Requirements:**
- [ ] alb_access_logs_to_expensive_bucket
- [ ] cloudwatch_metric_stream_enabled
- [ ] api_service → queue → worker → s3_analytics_bucket dependencies

**NEW Noise Test Cases:**
- [ ] whitespace_only.tf (no findings expected)
- [ ] comments_only.tf (no findings expected)
- [ ] reordered_resources.tf (no findings expected)
- [ ] description_change.tf (no findings expected)

**Estimated Tasks:** 11

---

### Section 6: POLICY & BASELINE DEMO (NEW)

**Status:** Not implemented

**NEW Requirements:**

**Policy Demo:**
- [ ] Create `costpilot.yml` configuration file
- [ ] Create `policies/default_ec2_type.yml` policy
- [ ] Policy must flag EC2 instance type regression (t3.micro → t3.xlarge)
- [ ] Policy violation message must appear in detect output
- [ ] Test policy enforcement in CI

**Baseline Usage:**
- [ ] Create `.costpilot/baselines.json`
- [ ] Record baseline monthly cost for core stack
- [ ] Demonstrate PR comparison against baseline
- [ ] Baseline-aware SLO breach example in trend demo

**Estimated Tasks:** 8

---

### Section 7: TRUST TRIANGLE VALIDATION (ENHANCED)

**Status:** Mostly complete, needs minor additions

**NEW Requirements:**
- [ ] Add `regression_type` to detect output (if not present)
- [ ] Add `baseline_comparison_if_available` to predict output
- [ ] Add `reference_to_policy_or_baseline_when_relevant` to explain output

**Estimated Tasks:** 3

---

### Section 8: DETERMINISTIC CONSTRAINTS (ENHANCED)

**Status:** Mostly complete, needs additions

**NEW Requirements:**
- [ ] Ensure `mermaid_layout_seed_fixed` (may already be done)
- [ ] Verify `snapshots_cross_platform_identical`
- [ ] Add snapshot lineage metadata to all snapshots:
  - [ ] source_plan
  - [ ] scenario (baseline, pr-change, noop, noise-case)
  - [ ] plan_time
  - [ ] seed
  - [ ] hash_before
  - [ ] hash_after

**Estimated Tasks:** 8 (1 per snapshot file + validation)

---

### Section 9: DEMO OUTPUT REQUIREMENTS (ENHANCED)

**Status:** Files exist, needs golden output formalization

**NEW Concepts:**
- [ ] Formalize golden outputs concept in documentation
- [ ] Create golden_outputs manifest
- [ ] Update canonical_spec_hash in products.yml (TBD_AFTER_FREEZE)
- [ ] Document golden version policy

**Estimated Tasks:** 4

---

### Section 13: DRIFT DEFINITION & HANDLING (NEW)

**Status:** Not documented

**NEW Requirements:**
- [ ] Document drift_definition in README or separate doc
- [ ] Define file_drift, semantic_drift, structural_drift
- [ ] Document actions_on_drift policy
- [ ] Update CI to fail on drift with clear messaging

**Estimated Tasks:** 4

---

### Section 14: CI GUARDRAILS & INTEGRITY TESTS (ENHANCED)

**Status:** Basic CI exists, needs 8 new integrity tests

**NEW Integrity Tests:**
- [ ] detect_diff_against_baseline
- [ ] predict_range_validation
- [ ] explain_provenance_validation
- [ ] mapping_cycle_detection_test
- [ ] trend_continuity_test
- [ ] golden_output_hash_validation
- [ ] policy_violation_message_present_for_pr_stack
- [ ] noop_and_noise_cases_are_clean

**CI Guardrails Updates:**
- [ ] Add noise-cases/* to allowlist
- [ ] Add policies/* to allowlist
- [ ] Add noise_cases_produce_no_findings check

**Estimated Tasks:** 11

---

### Section 16: README REQUIREMENTS (ENHANCED)

**Status:** README exists, needs restructuring

**NEW Requirements:**
- [ ] Add `short_for_auditors_section` ("How to reproduce all outputs exactly")
- [ ] Restructure README to match `readme_structure` order:
  - hero_section
  - why_costpilot_exists
  - what_this_repo_is
  - quickstart
  - infrastructure_scenario_overview
  - example_PR_flow
  - trust_triangle
  - mapping_demo
  - trend_demo
  - autofix_examples
  - deterministic_guarantees
  - faq
  - final_cta
- [ ] Follow `readme_narrative_flow` exactly
- [ ] Add governance_and_policy_section
- [ ] Add reproducibility_and_audit_section

**Estimated Tasks:** 6

---

### Section 17: VISUAL & SCREENSHOT REQUIREMENTS (NEW)

**Status:** Not implemented

**NEW Requirements:**

**Screenshots Manifest:**
- [ ] detect_output_screenshot.png (1920x1080, light theme)
- [ ] explain_mode_screenshot.png
- [ ] mapping_graph.png
- [ ] trend_graph.png
- [ ] pr_comment_cost_diff.png

**Screenshot Invariants:**
- [ ] All screenshots must be 1920x1080
- [ ] Use light theme
- [ ] Show CostPilot version and scenario_version
- [ ] Use deterministic colors
- [ ] Always show PR #42 context

**Estimated Tasks:** 10 (5 screenshots + 5 validation tasks)

---

### Section 19: PR COMMENT ASSETS (NEW)

**Status:** Not implemented

**NEW Requirements:**
- [ ] Create `pr_comments/comment_detect.txt`
- [ ] Create `pr_comments/comment_predict.txt`
- [ ] Create `pr_comments/comment_explain.txt`
- [ ] Create `pr_comments/comment_autofix.txt`
- [ ] All comments must reference PR #42
- [ ] All comments must show dollar impact
- [ ] All comments must show severity
- [ ] All comments must suggest fixes

**Estimated Tasks:** 8

---

### Section 20: DIAGRAMS & RENDERING TESTS (NEW)

**Status:** Not implemented

**NEW Requirements:**
- [ ] Create `diagram/trust_triangle_flow.svg`
  - Must map Detect → Predict → Explain → Action
- [ ] Create `diagram/architecture_overview.svg`
  - Must reflect baseline + PR regression stack
- [ ] Test Mermaid rendering on GitHub
- [ ] Test SVG responsiveness to 1080p

**Estimated Tasks:** 4

---

### Section 21: NOISE & FALSE-POSITIVE TESTING (NEW)

**Status:** Not implemented

**NEW Requirements:**

**Test Cases:**
- [ ] Create `noise-cases/whitespace_only.tf`
- [ ] Create `noise-cases/comments_only.tf`
- [ ] Create `noise-cases/reordered_resources.tf`
- [ ] Create `noise-cases/description_change.tf`

**Testing:**
- [ ] Run CostPilot on each noise case
- [ ] Verify no_findings for all 4 cases
- [ ] Add noise tests to CI pipeline
- [ ] Document noise resilience in README

**Estimated Tasks:** 8

---

### Section 23: MARKETING REVIEW CHECKLIST (NEW)

**Status:** Not implemented

**NEW Requirements:**
- [ ] Create marketing review checklist document
- [ ] Validate outputs consistent with CostPilot v1
- [ ] Verify no placeholder/fake data
- [ ] Verify PR comments readable at 1080p and mobile
- [ ] Verify trend graph visually legible
- [ ] Verify mapping graph centered and readable
- [ ] Verify JSON outputs formatted correctly
- [ ] Verify screenshots match golden outputs
- [ ] Verify README narrative aligns with behavior

**Estimated Tasks:** 9

---

## Task Summary

### By Category:

| Category | Tasks | Complexity |
|----------|-------|------------|
| Directory Structure | 18 | Low |
| Infrastructure Enhancement | 11 | Medium |
| Policy & Baseline Demo | 8 | Medium |
| Trust Triangle Updates | 3 | Low |
| Snapshot Lineage | 8 | Low |
| Golden Outputs | 4 | Low |
| Drift Documentation | 4 | Low |
| CI Integrity Tests | 11 | Medium |
| README Restructure | 6 | Medium |
| Screenshots | 10 | High |
| PR Comments | 8 | Low |
| Diagrams | 4 | Medium |
| Noise Testing | 8 | Medium |
| Marketing Review | 9 | Low |
| **TOTAL** | **112** | **Mixed** |

### By Priority:

**P0 - Critical (Breaking Changes):**
- Directory structure changes (18 tasks)
- File renames (1 task)
- Baseline stack enhancement (4 tasks)

**P1 - High (Core Features):**
- Policy & baseline demo (8 tasks)
- Noise testing (8 tasks)
- CI integrity tests (11 tasks)

**P2 - Medium (Quality & Polish):**
- Trust Triangle updates (3 tasks)
- Snapshot lineage (8 tasks)
- README restructure (6 tasks)
- PR comments (8 tasks)

**P3 - Low (Marketing Assets):**
- Screenshots (10 tasks)
- Diagrams (4 tasks)
- Marketing review (9 tasks)

---

## Recommended Approach

### Option 1: Add New Section to Checklist ✅ RECOMMENDED

**Pros:**
- Preserves v1 completion (150/152)
- Clear separation of v1 vs v2 work
- Easy to track incremental progress
- Maintains historical context

**Structure:**
```markdown
## 13. Final Review & QA (v1)
[existing 150/152 tasks]

---

## 14. Spec v2.0.0 Enhancements (NEW)

### 14.1 Directory Structure Updates
- [ ] Create policies/ directory
- [ ] Create noise-cases/ directory
...

### 14.2 Infrastructure Enhancements
...

### 14.3 Policy & Baseline Demo
...

[etc.]
```

### Option 2: Integrate into Existing Sections

**Pros:**
- Single unified view
- Logical grouping by feature area

**Cons:**
- Loses v1 completion milestone
- Harder to see what's new
- More complex to update progress

---

## Checklist Update Recommendation

I recommend **Option 1**: Add a new section titled **"Spec v2.0.0 Enhancements"** with subsections:

```markdown
## 14. Spec v2.0.0 Enhancements

### 14.1 Directory Structure & File Organization (18 tasks)
### 14.2 Infrastructure Enhancements (11 tasks)
### 14.3 Policy & Baseline Demo (8 tasks)
### 14.4 Trust Triangle Enhancements (3 tasks)
### 14.5 Snapshot Lineage & Golden Outputs (12 tasks)
### 14.6 Drift Management (4 tasks)
### 14.7 CI Integrity Tests (11 tasks)
### 14.8 README Restructure (6 tasks)
### 14.9 Visual Assets (10 tasks)
### 14.10 PR Comment Assets (8 tasks)
### 14.11 Diagrams (4 tasks)
### 14.12 Noise Testing (8 tasks)
### 14.13 Marketing Review (9 tasks)
```

**New Progress Bar:**
- Current: 150/152 (98.7%) [v1.0.0 spec]
- With v2: 150/264 (56.8%) [combined v1 + v2]
- Or separate: v1: 150/152 (98.7%), v2: 0/112 (0%)

---

## Critical Decisions Needed

### 1. Directory Structure Changes

**Question:** Should we create all new directories now, or phase them in?

**Impact:** 
- 4 new top-level directories
- 18+ new files
- 1 file rename

**Recommendation:** Wait for your decision - this is structural.

### 2. Infrastructure Scope

**Question:** Do we enhance the baseline stack with "mini real-world" components, or keep it minimal?

**Impact:**
- Current baseline: 4 resources (simple)
- v2 baseline: 8+ resources (more realistic but more complex)

**Trade-off:** Realism vs. simplicity and maintenance burden.

### 3. Marketing Assets Priority

**Question:** Are screenshots, diagrams, and PR comments immediate priorities, or can they wait?

**Impact:**
- 27 tasks total
- Require manual work (screenshots)
- Time-intensive

**Recommendation:** Defer to P3 (after core functionality).

---

## Next Steps

**Immediate:**
1. **Decision:** Confirm checklist structure approach (Option 1 recommended)
2. **Decision:** Confirm if we should create new directories now
3. **Decision:** Prioritize v2 tasks (all, subset, or phased)

**Then:**
1. Update `checklist.md` with chosen structure
2. Create new directories (if approved)
3. Begin highest-priority v2 tasks

---

## Compatibility Assessment

**Good News:**
- ✅ All v1 work is preserved
- ✅ No v1 features removed
- ✅ Mostly additive changes
- ✅ Backward compatible

**Concerns:**
- ⚠️ File rename required (trend_history.json)
- ⚠️ Directory structure changes required
- ⚠️ Baseline stack enhancement may alter existing cost calculations
- ⚠️ Golden outputs concept may require hash recalculation

---

**End of Analysis**

**Summary:** The v2.0.0 spec introduces ~112 new tasks across 13 major areas. Most changes are additive and compatible with v1 work. The largest impacts are directory structure changes (18 tasks) and marketing assets (27 tasks). I recommend adding a new section to the checklist to preserve v1 milestone while clearly tracking v2 progress.

**Recommendation:** Proceed with Option 1 (new checklist section), get approval for directory changes, then prioritize core features (P0-P1) before marketing assets (P3).
