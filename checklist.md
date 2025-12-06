# CostPilot Demo Implementation Checklist

**Version:** 1.0.0  
**Source Spec:** products.yml  
**Last Updated:** 2025-12-06

<div role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="47" style="width:94%; background:#e6eef0; border-radius:8px; padding:6px; box-shadow: inset 0 1px 2px rgba(0,0,0,0.04);">
  <div style="width:47.4%; background:linear-gradient(90deg,#f59e0b,#eab308,#84cc16); color:#fff; padding:10px 12px; text-align:right; border-radius:6px; font-weight:700; transition:width 0.5s ease;">
    <span style="display:inline-block; background:rgba(0,0,0,0.12); padding:4px 8px; border-radius:999px; font-size:0.95em;">47.4% · 72/152</span>
  </div>
</div>

---

## 1. Repository Initialization

### Repo Setup
- [x] create_repo_structure
- [x] initialize_git
- [x] create_main_branch
- [ ] set_branch_protection_rules_for_main

### Initial Directories
- [x] mkdir_infrastructure_terraform_baseline
- [x] mkdir_infrastructure_terraform_pr_change
- [x] mkdir_infrastructure_terraform_noop_change
- [x] mkdir_snapshots
- [x] mkdir_costpilot_demo
- [x] mkdir_costpilot_artifacts
- [x] mkdir_tools
- [x] mkdir_github_workflows

### Required Files
- [x] create_README_md
- [x] create_costpilot_yml
- [x] create_reset_demo_sh
- [x] create_costpilot_ci_yml

---

## 2. Terraform Environments

### Terraform Baseline Stack
- [x] write_main_tf_baseline
- [x] write_variables_tf_baseline
- [x] write_outputs_tf_baseline
- [x] ensure_low_cost_resources
- [x] include_autoscaling_group
- [x] include_alb_target_group_listener
- [x] include_s3_with_lifecycle_enabled
- [x] include_cloudwatch_log_30day_retention
- [x] validate_terraform_format_baseline

### Terraform PR Change Stack
- [x] write_main_tf_pr_change
- [x] add_ec2_instance_upgrade_regression
- [x] disable_s3_lifecycle_regression
- [x] increase_cloudwatch_retention_regression
- [x] increase_ebs_volume_size_regression
- [x] maintain_cross_service_dependencies
- [x] validate_terraform_format_pr_change

### Terraform Noop Change Stack
- [x] write_main_tf_noop
- [x] guarantee_no_semantic_cost_differences
- [x] validate_terraform_format_noop

### Terraform Requirements Validation
- [x] enforce_minimum_version_1_6
- [x] enforce_plan_schema_version_2

---

## 3. Snapshot Generation

### Snapshots Generation
- [ ] generate_plan_before_json
- [ ] generate_plan_after_json
- [ ] generate_plan_diff_json
- [ ] run_costpilot_detect_store_detect_v1_json
- [ ] run_costpilot_predict_store_predict_v1_json
- [ ] run_costpilot_explain_store_explain_v1_json
- [ ] run_costpilot_autofix_snippet_store_snippet_v1_tf
- [ ] run_costpilot_autofix_patch_store_patch_v1_diff
- [ ] generate_mapping_mmd_snapshot
- [ ] generate_trend_history_json
- [ ] generate_trend_svg_snapshot
- [ ] copy_all_snapshots_to_costpilot_demo_directory

### Snapshot Invariants
- [ ] enforce_deterministic_hashes
- [ ] enforce_float_precision_2
- [ ] enforce_stable_whitespace
- [ ] enforce_stable_ordering_rules

---

## 4. Trust Triangle Verification

### Detect Output Must Show
- [ ] resource_classification
- [ ] rule_ids
- [ ] severity_scoring

### Predict Output Must Show
- [ ] heuristic_references
- [ ] low_and_high_ranges
- [ ] cold_start_assumptions

### Explain Output Must Show
- [ ] root_cause
- [ ] regression_type
- [ ] severity_score
- [ ] heuristic_provenance
- [ ] delta_justification

### Validation Tasks
- [ ] verify_detect_output_contains_required_fields
- [ ] verify_predict_output_contains_required_fields
- [ ] verify_explain_output_contains_required_fields

---

## 5. Patch Preview Implementation

### Snippet Scope
- [ ] implement_snippet_generation_ec2_only
- [ ] implement_snippet_generation_s3_only

### Patch Mode
- [ ] generate_patch_diff
- [ ] simulate_patch_application
- [ ] generate_simulation_output_json
- [ ] include_before_and_after_hashes
- [ ] include_patch_id
- [ ] include_rollback_patch

### Patch Scope Limit Rationale
- [x] document_reason_for_scope_limit_in_README

---

## 6. Mapping Engine Demo

### Mapping Demo
- [ ] ensure_cross_service_dependencies_exist
- [ ] run_costpilot_map_mermaid
- [ ] fix_mermaid_layout_seed
- [ ] store_output_mapping_mmd
- [ ] copy_to_snapshots_and_demo

### Mapping Validation
- [ ] ensure_no_cycles
- [ ] ensure_deterministic_node_ordering

---

## 7. Trend Engine Demo

### Variations
- [ ] generate_flat_trend
- [ ] generate_upward_trend
- [ ] generate_slo_breach_trend

### Constraints
- [ ] fixed_layout_seed
- [ ] fixed_svg_dimensions_800_300
- [ ] deterministic_coloring

### Trend Tasks
- [ ] create_trend_history_json
- [ ] create_trend_svg_snapshot
- [ ] validate_trend_is_deterministic

---

## 8. Reset Script Implementation

### Must Implement
- [x] restore_baseline_infrastructure
- [x] regenerate_all_snapshots
- [x] regenerate_mapping
- [x] regenerate_trend_history
- [x] validate_deterministic_hashes
- [x] exit_nonzero_on_drift

### Permissions
- [x] chmod_plus_x_reset_demo_sh

---

## 9. CI Pipeline Implementation

### Tasks
- [x] configure_terraform_init
- [x] run_costpilot_scan
- [x] run_costpilot_diff
- [x] run_costpilot_explain
- [x] enforce_noop_expected_no_findings
- [x] verify_deterministic_output_against_snapshots
- [x] block_on_any_drift

### CI Guardrails
- [x] prevent_updates_to_snapshots
- [x] prevent_updates_to_costpilot_artifacts
- [x] prevent_updates_to_video_assets
- [x] allowlist_infrastructure_terraform_pr_change
- [x] allowlist_README_md
- [x] allowlist_costpilot_yml

---

## 10. Artifact Generation Pipeline

### Artifacts Pipeline
- [ ] generate_output_detect_json
- [ ] generate_output_predict_json
- [ ] generate_output_explain_json
- [ ] generate_output_snippet_tf
- [ ] generate_output_patch_diff
- [ ] generate_output_mapping_mmd
- [ ] generate_output_trend_json
- [ ] ensure_all_artifacts_hash_stable

### Artifact Constraints
- [ ] store_all_artifacts_in_costpilot_artifacts
- [ ] ensure_no_overwrite_drift_over_time

---

## 11. README Implementation

### README Tasks
- [x] write_hero_copy
- [x] add_statement_of_purpose
- [x] add_quickstart_section
- [x] add_pr_walkthrough_section
- [x] add_mapping_example
- [x] add_trend_example
- [x] add_trust_triangle_section
- [x] include_scope_limit_explanation
- [x] include_scenario_versioning_notice

### README Validation
- [x] confirm_clarity
- [x] confirm_asset_paths_correct
- [x] confirm_no_enterprise_features_mentioned
- [x] include_scenario_version_badge

---

## 12. Versioning & Checksum

### Scenario Versioning
- [x] embed_scenario_version_in_snapshots
- [x] embed_scenario_version_in_README

### Canonical Hash Generation
- [ ] compute_canonical_spec_hash
- [ ] insert_hash_into_spec
- [ ] verify_snapshots_match_hash
- [ ] verify_explain_output_matches_hash

---

## 13. Final Review & QA

### QA Tasks
- [ ] run_reset_demo_script_fresh
- [ ] re-run_costpilot_scan_all_modes
- [ ] revalidate_trust_triangle
- [ ] validate_noop_does_not_trigger_findings
- [ ] open_mapping_svg_to_validate_layout
- [ ] validate_consistency_of_hashes
- [ ] run_ci_locally
- [ ] test_repo_on_clean_machine

### Drift Protection
- [ ] enforce_all_outputs_reproducible_on_3_runs
- [ ] commit_final_snapshots
- [ ] tag_v1_demo_release

---

## Summary

**Total Tasks:** 152  
**Completed:** 72  
**Remaining:** 80  
**Progress:** 47.4%

---

*This checklist is auto-generated from `docs/checklist.yml`. Use `python tools/update_progress.py` to update the progress bar.*
