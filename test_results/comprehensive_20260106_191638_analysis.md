# CostPilot Comprehensive Test Analysis
**Run ID:** comprehensive_20260106_191638
**Date:** Tue 06 Jan 2026 19:17:07 SAST
**CostPilot Version:** costpilot 1.0.0 (Free)

## Executive Summary
- **Total Tests:** 1012
- **Optimizations Detected:** 831
- **Detection Rate:** 82.11%
- **Total Potential Savings:** $ 181125/month

## Performance by Category

- **api:** 15 tests, 15 optimizations detected
- **architecture_patterns:** 90 tests, 42 optimizations detected
- **caching:** 60 tests, 51 optimizations detected
- **cdn:** 15 tests, 15 optimizations detected
- **instance_rightsizing:** 387 tests, 376 optimizations detected
- **network_optimization:** 105 tests, 80 optimizations detected
- **security_overhead:** 99 tests, 60 optimizations detected
- **serverless:** 70 tests, 32 optimizations detected
- **storage_optimization:** 171 tests, 160 optimizations detected

## Top Failure Categories

- **serverless/lambda:** 38 failed tests
- **architecture_patterns/auto_scaling:** 20 failed tests
- **security_overhead/security_groups:** 15 failed tests
- **network_optimization/vpc_endpoints:** 15 failed tests
- **architecture_patterns/staging_envs:** 15 failed tests
- **security_overhead/waf:** 14 failed tests
- **architecture_patterns/development_envs:** 13 failed tests
- **storage_optimization/ebs_volumes:** 11 failed tests
- **instance_rightsizing/development:** 11 failed tests
- **security_overhead/iam_roles:** 10 failed tests

## Most Common Failure Patterns

- **lambda:** 40 failed tests
- **dev:** 28 failed tests
- **staging:** 18 failed tests
- **ebs:** 10 failed tests
- **elasticache:** 9 failed tests
- **s3:** 2 failed tests
- **rds:** 2 failed tests
- **db:** 2 failed tests
