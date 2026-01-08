#!/bin/bash
# Comprehensive CostPilot Optimization Testing Script

set -e

# Configuration
TEST_DIR="../optimization_tests"
RESULTS_DIR="../test_results"
COSTPILOT_CMD="../costpilot"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_FILE="${RESULTS_DIR}/optimization_test_report_${TIMESTAMP}.json"

# Categories to test (in priority order)
CATEGORIES=(
    "instance_rightsizing"
    "storage_optimization"
    "architecture_patterns"
    "ri_savings_plans"
    "network_costs"
    "database_optimization"
    "container_orchestration"
    "monitoring_logging"
    "security_overhead"
    "time_based_patterns"
)

# Expected optimizations for each test case
declare -A EXPECTED_OPTIMIZATIONS
EXPECTED_OPTIMIZATIONS["burstable_overprovision"]="rightsizing t3.large to smaller instance"
EXPECTED_OPTIMIZATIONS["wrong_instance_family"]="switch from c5 to storage-optimized instance"
EXPECTED_OPTIMIZATIONS["graviton_migration"]="migrate from x86 to Graviton instance"
EXPECTED_OPTIMIZATIONS["ebs_gp3_overprovision"]="reduce EBS IOPS and throughput"
EXPECTED_OPTIMIZATIONS["s3_versioning_no_lifecycle"]="add lifecycle rules for versioned objects"
EXPECTED_OPTIMIZATIONS["rds_storage_overprovision"]="reduce RDS storage allocation"
EXPECTED_OPTIMIZATIONS["microservices_consolidation"]="consolidate multiple small instances"
EXPECTED_OPTIMIZATIONS["event_driven_vs_always_on"]="migrate to Lambda or event-driven architecture"
EXPECTED_OPTIMIZATIONS["spot_instance_candidates"]="use spot instances for fault-tolerant workloads"

# Initialize results
init_results() {
    cat > "$REPORT_FILE" << EOF
{
  "test_run": {
    "timestamp": "$TIMESTAMP",
    "costpilot_version": "v1.0.0",
    "total_tests": 0,
    "categories_tested": ${#CATEGORIES[@]}
  },
  "results": {
