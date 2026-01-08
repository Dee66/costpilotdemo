# CostPilot Comprehensive Test Analysis
**Run ID:** comprehensive_20260106_182017
**Date:** Tue 06 Jan 2026 18:20:35 SAST
**CostPilot Version:** costpilot 1.0.0 (Free)

## Executive Summary
- **Total Tests:** 536
- **Optimizations Detected:** 117
- **Detection Rate:** 21.82%
- **Total Potential Savings:** $ 14700/month

## Performance by Category

- **api:** 15 tests, 0 optimizations detected
- **architecture_patterns:** 90 tests, 10 optimizations detected
- **caching:** 20 tests, 0 optimizations detected
- **cdn:** 15 tests, 0 optimizations detected
- **instance_rightsizing:** 171 tests, 63 optimizations detected
- **network_optimization:** 55 tests, 0 optimizations detected
- **security_overhead:** 39 tests, 0 optimizations detected
- **serverless:** 40 tests, 16 optimizations detected
- **storage_optimization:** 91 tests, 28 optimizations detected

## Top Failure Categories

- **storage_optimization/rds_instances:** 40 failed tests
- **network_optimization/nat_gateways:** 30 failed tests
- **architecture_patterns/microservices:** 28 failed tests
- **instance_rightsizing/regional:** 25 failed tests
- **serverless/lambda:** 24 failed tests
- **instance_rightsizing/bastion_hosts:** 20 failed tests
- **caching/elasticache:** 20 failed tests
- **architecture_patterns/auto_scaling:** 20 failed tests
- **instance_rightsizing/web_servers:** 16 failed tests
- **security_overhead/security_groups:** 15 failed tests

## Most Common Failure Patterns

- **db:** 53 failed tests
- **rds:** 37 failed tests
- **dev:** 31 failed tests
- **nat:** 30 failed tests
- **microservice:** 28 failed tests
- **lambda:** 26 failed tests
- **staging:** 20 failed tests
- **elasticache:** 20 failed tests
- **bastion:** 20 failed tests
- **web:** 16 failed tests
