#!/usr/bin/env python3
"""
Massive CostPilot Test Case Generator
Generates 250+ realistic terraform plan test cases for optimization detection
"""

import json
import os
from typing import Dict, List, Any

def create_base_terraform_plan() -> Dict[str, Any]:
    """Create base terraform plan structure"""
    return {
        "format_version": "1.2",
        "terraform_version": "1.6.0",
        "resource_changes": []
    }

def generate_instance_test(instance_type: str, name: str, purpose: str, environment: str = "production") -> Dict[str, Any]:
    """Generate an EC2 instance test case"""
    return {
        "address": f"aws_instance.{name}",
        "change": {
            "actions": ["create"],
            "before": None,
            "after": {
                "instance_type": instance_type,
                "ami": "ami-03f9680ef0c07a3d1",
                "tags": {
                    "Name": name,
                    "Purpose": purpose,
                    "Environment": environment
                }
            }
        },
        "mode": "managed",
        "type": "aws_instance",
        "name": name,
        "provider_name": "registry.terraform.io/hashicorp/aws"
    }

def generate_ebs_test(size: int, volume_type: str, name: str, purpose: str) -> Dict[str, Any]:
    """Generate an EBS volume test case"""
    return {
        "address": f"aws_ebs_volume.{name}",
        "change": {
            "actions": ["create"],
            "before": None,
            "after": {
                "size": size,
                "type": volume_type,
                "tags": {
                    "Name": name,
                    "Purpose": purpose,
                    "Environment": "production"
                }
            }
        },
        "mode": "managed",
        "type": "aws_ebs_volume",
        "name": name,
        "provider_name": "registry.terraform.io/hashicorp/aws"
    }

def generate_rds_test(instance_class: str, storage: int, name: str, engine: str) -> Dict[str, Any]:
    """Generate an RDS instance test case"""
    return {
        "address": f"aws_db_instance.{name}",
        "change": {
            "actions": ["create"],
            "before": None,
            "after": {
                "identifier": f"{name}-database",
                "engine": engine,
                "instance_class": instance_class,
                "allocated_storage": storage,
                "max_allocated_storage": 0,
                "storage_type": "gp2",
                "tags": {
                    "Name": f"{name}-db",
                    "Environment": "production"
                }
            }
        },
        "mode": "managed",
        "type": "aws_db_instance",
        "name": name,
        "provider_name": "registry.terraform.io/hashicorp/aws"
    }

def generate_nat_gateway_test(name: str) -> Dict[str, Any]:
    """Generate a NAT Gateway test case"""
    return {
        "address": f"aws_nat_gateway.{name}",
        "change": {
            "actions": ["create"],
            "before": None,
            "after": {
                "allocation_id": "eipalloc-12345",
                "subnet_id": "subnet-12345",
                "tags": {
                    "Name": name,
                    "Purpose": "outbound-traffic",
                    "Environment": "production"
                }
            }
        },
        "mode": "managed",
        "type": "aws_nat_gateway",
        "name": name,
        "provider_name": "registry.terraform.io/hashicorp/aws"
    }

def generate_load_balancer_test(name: str, lb_type: str = "application") -> Dict[str, Any]:
    """Generate a Load Balancer test case"""
    return {
        "address": f"aws_lb.{name}",
        "change": {
            "actions": ["create"],
            "before": None,
            "after": {
                "name": name,
                "internal": False,
                "load_balancer_type": lb_type,
                "subnets": ["subnet-12345", "subnet-67890"],
                "enable_deletion_protection": False,
                "tags": {
                    "Name": name,
                    "Type": lb_type,
                    "Environment": "production"
                }
            }
        },
        "mode": "managed",
        "type": "aws_lb",
        "name": name,
        "provider_name": "registry.terraform.io/hashicorp/aws"
    }

def generate_auto_scaling_group_test(name: str, instance_type: str, min_size: int, max_size: int) -> Dict[str, Any]:
    """Generate an Auto Scaling Group test case"""
    return {
        "address": f"aws_autoscaling_group.{name}",
        "change": {
            "actions": ["create"],
            "before": None,
            "after": {
                "name": name,
                "min_size": min_size,
                "max_size": max_size,
                "desired_capacity": min_size,
                "launch_template": {
                    "id": "lt-12345",
                    "version": "$Latest"
                },
                "vpc_zone_identifier": ["subnet-12345", "subnet-67890"],
                "tags": [{
                    "key": "Name",
                    "value": name,
                    "propagate_at_launch": True
                }, {
                    "key": "InstanceType",
                    "value": instance_type,
                    "propagate_at_launch": True
                }]
            }
        },
        "mode": "managed",
        "type": "aws_autoscaling_group",
        "name": name,
        "provider_name": "registry.terraform.io/hashicorp/aws"
    }

def generate_lambda_test(name: str, memory_size: int, runtime: str, timeout: int) -> Dict[str, Any]:
    """Generate a Lambda function test case"""
    return {
        "address": f"aws_lambda_function.{name}",
        "change": {
            "actions": ["create"],
            "before": None,
            "after": {
                "function_name": name,
                "memory_size": memory_size,
                "runtime": runtime,
                "timeout": timeout,
                "handler": "index.handler",
                "role": "arn:aws:iam::123456789012:role/lambda-role",
                "tags": {
                    "Name": name,
                    "Environment": "production"
                }
            }
        },
        "mode": "managed",
        "type": "aws_lambda_function",
        "name": name,
        "provider_name": "registry.terraform.io/hashicorp/aws"
    }

def generate_cloudfront_test(name: str, price_class: str) -> Dict[str, Any]:
    """Generate a CloudFront distribution test case"""
    return {
        "address": f"aws_cloudfront_distribution.{name}",
        "change": {
            "actions": ["create"],
            "before": None,
            "after": {
                "enabled": True,
                "price_class": price_class,
                "default_cache_behavior": {
                    "target_origin_id": "origin",
                    "viewer_protocol_policy": "allow-all"
                },
                "origins": [{
                    "domain_name": "example.com",
                    "origin_id": "origin"
                }],
                "tags": {
                    "Name": name,
                    "Environment": "production"
                }
            }
        },
        "mode": "managed",
        "type": "aws_cloudfront_distribution",
        "name": name,
        "provider_name": "registry.terraform.io/hashicorp/aws"
    }

def generate_elasticache_test(name: str, node_type: str, num_cache_nodes: int) -> Dict[str, Any]:
    """Generate an ElastiCache cluster test case"""
    return {
        "address": f"aws_elasticache_cluster.{name}",
        "change": {
            "actions": ["create"],
            "before": None,
            "after": {
                "cluster_id": name,
                "engine": "redis",
                "node_type": node_type,
                "num_cache_nodes": num_cache_nodes,
                "port": 6379,
                "tags": {
                    "Name": name,
                    "Environment": "production"
                }
            }
        },
        "mode": "managed",
        "type": "aws_elasticache_cluster",
        "name": name,
        "provider_name": "registry.terraform.io/hashicorp/aws"
    }

def generate_api_gateway_test(name: str, endpoint_type: str) -> Dict[str, Any]:
    """Generate an API Gateway test case"""
    return {
        "address": f"aws_api_gateway_rest_api.{name}",
        "change": {
            "actions": ["create"],
            "before": None,
            "after": {
                "name": name,
                "endpoint_configuration": {
                    "types": [endpoint_type]
                },
                "tags": {
                    "Name": name,
                    "Environment": "production"
                }
            }
        },
        "mode": "managed",
        "type": "aws_api_gateway_rest_api",
        "name": name,
        "provider_name": "registry.terraform.io/hashicorp/aws"
    }

def save_test_case(plan: Dict[str, Any], filepath: str):
    """Save terraform plan to JSON file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(plan, f, indent=2)

def main():
    """Generate massive test suite with 250+ tests"""

    print("Generating expanded massive test suite (250+ tests)...")

    # Instance Rightsizing Tests (80+ tests)
    print("Generating instance rightsizing tests...")

    # Bastion hosts - should be small instances (20 tests)
    bastion_sizes = [
        "m5.large", "c5.large", "r5.large", "m5.xlarge", "t3.medium",
        "m5.2xlarge", "c5.xlarge", "r5.2xlarge", "i3.large", "p3.large",
        "m5.4xlarge", "c5.2xlarge", "r5.4xlarge", "i3.xlarge", "p3.2xlarge",
        "m5.8xlarge", "c5.4xlarge", "r5.8xlarge", "i3.2xlarge", "p3.8xlarge"
    ]
    for idx, size in enumerate(bastion_sizes):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_instance_test(size, f"bastion_{idx+1}", "ssh-access", "production")
        )
        save_test_case(plan, f"optimization_tests/massive_suite/instance_rightsizing/bastion_hosts/bastion_{size.replace('.', '_')}_{idx+1}.json")

    # Web servers - various sizes and types (25 tests)
    web_configs = [
        ("t3.medium", "web-server"), ("m5.large", "web-server"), ("c5.large", "web-server"),
        ("t3.small", "web-server"), ("m5.xlarge", "web-server"), ("r5.large", "web-server"),
        ("m5.2xlarge", "web-server"), ("c5.xlarge", "web-server"), ("r5.2xlarge", "web-server"),
        ("t3.large", "web-server"), ("m5.4xlarge", "web-server"), ("c5.2xlarge", "web-server"),
        ("r5.4xlarge", "web-server"), ("t3.xlarge", "web-server"), ("m5.8xlarge", "web-server"),
        ("c5.4xlarge", "web-server"), ("r5.8xlarge", "web-server"), ("t3.2xlarge", "web-server"),
        ("m5.12xlarge", "web-server"), ("c5.9xlarge", "web-server"), ("r5.12xlarge", "web-server"),
        ("t2.medium", "web-server"), ("m4.large", "web-server"), ("c4.large", "web-server"),
        ("r4.large", "web-server"), ("i3.large", "web-server")
    ]
    for idx, (size, purpose) in enumerate(web_configs):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_instance_test(size, f"web_{idx+1}", purpose, "production")
        )
        save_test_case(plan, f"optimization_tests/massive_suite/instance_rightsizing/web_servers/web_{size.replace('.', '_')}_{idx+1}.json")

    # Databases - various sizes and types (20 tests)
    db_configs = [
        ("c5.large", "database"), ("m5.large", "database"), ("t3.medium", "database"),
        ("r5.large", "database"), ("c5.xlarge", "database"), ("m5.2xlarge", "database"),
        ("c5.2xlarge", "database"), ("t3.large", "database"), ("m5.4xlarge", "database"),
        ("c5.4xlarge", "database"), ("r5.4xlarge", "database"), ("t3.xlarge", "database"),
        ("m5.8xlarge", "database"), ("c5.9xlarge", "database"), ("r5.8xlarge", "database"),
        ("t3.2xlarge", "database"), ("m5.12xlarge", "database"), ("c5.12xlarge", "database"),
        ("r5.12xlarge", "database"), ("db.r5.large", "database")
    ]
    for idx, (size, purpose) in enumerate(db_configs):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_instance_test(size, f"db_{idx+1}", purpose, "production")
        )
        save_test_case(plan, f"optimization_tests/massive_suite/instance_rightsizing/databases/db_{size.replace('.', '_')}_{idx+1}.json")

    # Development instances - should be smaller (10 tests)
    dev_sizes = [
        "m5.large", "c5.large", "r5.large", "m5.xlarge", "t3.large",
        "m5.2xlarge", "c5.xlarge", "r5.2xlarge", "t3.xlarge", "m5.4xlarge"
    ]
    for idx, size in enumerate(dev_sizes):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_instance_test(size, f"dev_{idx+1}", "development", "development")
        )
        save_test_case(plan, f"optimization_tests/massive_suite/instance_rightsizing/development/dev_{size.replace('.', '_')}_{idx+1}.json")

    # Background jobs - various configurations (15 tests)
    job_configs = [
        ("t3.medium", "batch-job"), ("m5.large", "batch-job"), ("c5.large", "batch-job"),
        ("r5.large", "batch-job"), ("t3.small", "batch-job"), ("m5.xlarge", "batch-job"),
        ("c5.xlarge", "batch-job"), ("r5.xlarge", "batch-job"), ("t3.large", "batch-job"),
        ("m5.2xlarge", "batch-job"), ("c5.2xlarge", "batch-job"), ("r5.2xlarge", "batch-job"),
        ("t3.xlarge", "batch-job"), ("m5.4xlarge", "batch-job"), ("c5.4xlarge", "batch-job")
    ]
    for idx, (size, purpose) in enumerate(job_configs):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_instance_test(size, f"job_{idx+1}", purpose, "production")
        )
        save_test_case(plan, f"optimization_tests/massive_suite/instance_rightsizing/background_jobs/job_{size.replace('.', '_')}_{idx+1}.json")

    # Storage Optimization Tests (60+ tests)
    print("Generating storage optimization tests...")

    # EBS volumes - various sizes and types (30 tests)
    ebs_configs = [
        (1000, "gp2", "large_data"), (500, "gp2", "medium_data"), (2000, "gp2", "huge_data"),
        (100, "gp2", "small_data"), (5000, "gp2", "massive_data"), (10000, "gp2", "enormous_data"),
        (50, "gp2", "tiny_data"), (2500, "io1", "io1_medium"), (1000, "io1", "io1_large"),
        (5000, "st1", "st1_large"), (2000, "sc1", "sc1_medium"), (3000, "gp2", "gp2_large"),
        (1500, "io1", "io1_xlarge"), (8000, "gp2", "gp2_huge"), (4000, "st1", "st1_xlarge"),
        (6000, "sc1", "sc1_large"), (12000, "gp2", "gp2_massive"), (250, "gp2", "gp2_small"),
        (7500, "io1", "io1_huge"), (3500, "st1", "st1_medium"), (4500, "sc1", "sc1_xlarge"),
        (9000, "gp2", "gp2_enormous"), (125, "gp2", "gp2_tiny"), (11000, "io1", "io1_massive"),
        (5500, "st1", "st1_huge"), (6500, "sc1", "sc1_enormous"), (13000, "gp2", "gp2_extreme"),
        (175, "gp2", "gp2_mini"), (13500, "io1", "io1_extreme"), (7500, "st1", "st1_extreme")
    ]
    for idx, (size, vol_type, name) in enumerate(ebs_configs):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_ebs_test(size, vol_type, f"ebs_{idx+1}", "application-data")
        )
        save_test_case(plan, f"optimization_tests/massive_suite/storage_optimization/ebs_volumes/ebs_{size}gb_{vol_type}_{idx+1}.json")

    # RDS instances - various storage sizes (30 tests)
    rds_configs = [
        ("db.t3.micro", 1000, "micro_large"), ("db.t3.small", 500, "small_medium"),
        ("db.m5.large", 2000, "large_huge"), ("db.t3.micro", 200, "micro_small"),
        ("db.r5.large", 100, "memory_small"), ("db.t3.large", 50, "large_tiny"),
        ("db.m5.xlarge", 5000, "xlarge_massive"), ("db.r5.2xlarge", 10000, "memory_huge"),
        ("db.t3.medium", 100, "medium_tiny"), ("db.c5.large", 2000, "compute_large"),
        ("db.t3.xlarge", 3000, "xlarge_large"), ("db.m5.2xlarge", 8000, "2xlarge_huge"),
        ("db.r5.4xlarge", 15000, "4xlarge_massive"), ("db.t3.2xlarge", 400, "2xlarge_medium"),
        ("db.c5.xlarge", 6000, "compute_xlarge"), ("db.t2.medium", 800, "t2_large"),
        ("db.m4.large", 3000, "m4_large"), ("db.r4.large", 5000, "r4_large"),
        ("db.c4.large", 2500, "c4_large"), ("db.t3.small", 150, "small_tiny"),
        ("db.m5.4xlarge", 12000, "4xlarge_huge"), ("db.r5.8xlarge", 20000, "8xlarge_extreme"),
        ("db.t3.large", 800, "large_medium"), ("db.c5.2xlarge", 10000, "2xlarge_massive"),
        ("db.t3.xlarge", 1500, "xlarge_medium"), ("db.m5.8xlarge", 18000, "8xlarge_huge"),
        ("db.r5.12xlarge", 25000, "12xlarge_extreme"), ("db.c5.4xlarge", 14000, "4xlarge_large"),
        ("db.t3.2xlarge", 600, "2xlarge_small"), ("db.m5.12xlarge", 22000, "12xlarge_massive")
    ]
    for idx, (instance_class, storage, name) in enumerate(rds_configs):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_rds_test(instance_class, storage, f"rds_{idx+1}", "postgres")
        )
        save_test_case(plan, f"optimization_tests/massive_suite/storage_optimization/rds_instances/rds_{instance_class.replace('.', '_')}_{storage}gb_{idx+1}.json")

    # S3 buckets with various configurations (5 tests)
    s3_configs = [
        ("versioning", "versioned-bucket"),
        ("lifecycle", "lifecycle-bucket"),
        ("encryption", "encrypted-bucket"),
        ("logging", "logging-bucket"),
        ("replication", "replicated-bucket")
    ]
    for idx, (config_type, bucket_name) in enumerate(s3_configs):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append({
            "address": f"aws_s3_bucket.{bucket_name}",
            "change": {
                "actions": ["create"],
                "before": None,
                "after": {
                    "bucket": bucket_name,
                    "tags": {
                        "Name": bucket_name,
                        "Config": config_type,
                        "Environment": "production"
                    }
                }
            },
            "mode": "managed",
            "type": "aws_s3_bucket",
            "name": bucket_name,
            "provider_name": "registry.terraform.io/hashicorp/aws"
        })
        save_test_case(plan, f"optimization_tests/massive_suite/storage_optimization/s3_buckets/s3_{config_type}_{idx+1}.json")

    # EFS file systems (5 tests)
    efs_configs = [
        (100, "small_efs"),
        (1000, "large_efs"),
        (5000, "huge_efs"),
        (50, "tiny_efs"),
        (10000, "massive_efs")
    ]
    for idx, (size, name) in enumerate(efs_configs):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append({
            "address": f"aws_efs_file_system.{name}",
            "change": {
                "actions": ["create"],
                "before": None,
                "after": {
                    "creation_token": f"{name}-token",
                    "tags": {
                        "Name": name,
                        "Size": str(size),
                        "Environment": "production"
                    }
                }
            },
            "mode": "managed",
            "type": "aws_efs_file_system",
            "name": name,
            "provider_name": "registry.terraform.io/hashicorp/aws"
        })
        save_test_case(plan, f"optimization_tests/massive_suite/storage_optimization/efs/efs_{size}gb_{idx+1}.json")

    # Architecture Pattern Tests (50+ tests)
    print("Generating architecture pattern tests...")

    # Microservices - multiple small instances (20 tests)
    for num_instances in [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50, 60, 75]:
        plan = create_base_terraform_plan()
        for i in range(num_instances):
            plan["resource_changes"].append(
                generate_instance_test("t3.micro", f"microservice_{i+1}", f"service-{i+1}", "production")
            )
        save_test_case(plan, f"optimization_tests/massive_suite/architecture_patterns/microservices/{num_instances}_microservices_t3_micro.json")

    # Monolithic applications (10 tests)
    monolithic_sizes = [
        "m5.xlarge", "c5.2xlarge", "r5.xlarge", "m5.2xlarge", "c5.4xlarge",
        "r5.2xlarge", "m5.4xlarge", "c5.9xlarge", "r5.4xlarge", "m5.8xlarge"
    ]
    for idx, size in enumerate(monolithic_sizes):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_instance_test(size, f"monolithic_{idx+1}", "all-services", "production")
        )
        save_test_case(plan, f"optimization_tests/massive_suite/architecture_patterns/monolithic/monolithic_{size.replace('.', '_')}_{idx+1}.json")

    # Development environments (10 tests)
    for num_devs in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        plan = create_base_terraform_plan()
        for i in range(num_devs):
            plan["resource_changes"].append(
                generate_instance_test("m5.large", f"dev_env_{i+1}", "development", "development")
            )
        save_test_case(plan, f"optimization_tests/massive_suite/architecture_patterns/development_envs/{num_devs}_dev_instances_m5_large.json")

    # Staging environments (10 tests)
    for num_staging in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        plan = create_base_terraform_plan()
        for i in range(num_staging):
            plan["resource_changes"].append(
                generate_instance_test("m5.xlarge", f"staging_{i+1}", "staging", "staging")
            )
        save_test_case(plan, f"optimization_tests/massive_suite/architecture_patterns/staging_envs/{num_staging}_staging_instances_m5_xlarge.json")

    # Network Optimization Tests (40+ tests)
    print("Generating network optimization tests...")

    # NAT Gateways (20 tests)
    nat_names = [
        "nat_prod", "nat_staging", "nat_dev", "nat_test", "nat_backup",
        "nat_east", "nat_west", "nat_north", "nat_south", "nat_central",
        "nat_main", "nat_secondary", "nat_primary", "nat_replica", "nat_failover",
        "nat_gateway_1", "nat_gateway_2", "nat_gateway_3", "nat_gateway_4", "nat_gateway_5"
    ]
    for idx, name in enumerate(nat_names):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_nat_gateway_test(f"{name}_{idx+1}")
        )
        save_test_case(plan, f"optimization_tests/massive_suite/network_optimization/nat_gateways/{name}_{idx+1}.json")

    # Load Balancers (10 tests)
    lb_configs = [
        ("app_lb_prod", "application"), ("app_lb_staging", "application"),
        ("app_lb_dev", "application"), ("network_lb_prod", "network"),
        ("network_lb_staging", "network"), ("network_lb_dev", "network"),
        ("classic_lb_prod", "classic"), ("classic_lb_staging", "classic"),
        ("classic_lb_dev", "classic"), ("gateway_lb_prod", "gateway")
    ]
    for idx, (name, lb_type) in enumerate(lb_configs):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_load_balancer_test(f"{name}_{idx+1}", lb_type)
        )
        save_test_case(plan, f"optimization_tests/massive_suite/network_optimization/load_balancers/{name}_{lb_type}_{idx+1}.json")

    # VPC Endpoints (10 tests)
    vpc_endpoint_types = [
        "s3", "dynamodb", "ec2", "rds", "lambda", "sns", "sqs", "kms", "secretsmanager", "cloudformation"
    ]
    for idx, ep_type in enumerate(vpc_endpoint_types):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append({
            "address": f"aws_vpc_endpoint.{ep_type}_endpoint_{idx+1}",
            "change": {
                "actions": ["create"],
                "before": None,
                "after": {
                    "vpc_id": "vpc-12345",
                    "service_name": f"com.amazonaws.us-east-1.{ep_type}",
                    "vpc_endpoint_type": "Gateway",
                    "tags": {
                        "Name": f"{ep_type}-endpoint-{idx+1}",
                        "Purpose": f"{ep_type}-access",
                        "Environment": "production"
                    }
                }
            },
            "mode": "managed",
            "type": "aws_vpc_endpoint",
            "name": f"{ep_type}_endpoint_{idx+1}",
            "provider_name": "registry.terraform.io/hashicorp/aws"
        })
        save_test_case(plan, f"optimization_tests/massive_suite/network_optimization/vpc_endpoints/{ep_type}_endpoint_{idx+1}.json")

    # Security Overhead Tests (30+ tests)
    print("Generating security overhead tests...")

    # WAF configurations (10 tests)
    waf_configs = [
        (50000, "massive_waf"), (5000, "large_waf"), (500, "medium_waf"), (50, "small_waf"),
        (100000, "extreme_waf"), (25000, "xlarge_waf"), (1000, "xlarge_waf"), (25, "tiny_waf"),
        (75000, "huge_waf"), (150, "small_waf")
    ]
    for idx, (limit, name) in enumerate(waf_configs):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append({
            "address": f"aws_wafv2_web_acl.{name}_{idx+1}",
            "change": {
                "actions": ["create"],
                "before": None,
                "after": {
                    "name": f"{name}_{idx+1}",
                    "scope": "REGIONAL",
                    "default_action": {"allow": {}},
                    "rules": [{
                        "name": "rate-limit",
                        "priority": 1,
                        "action": {"block": {}},
                        "statement": {
                            "rate_based_statement": {
                                "limit": limit,
                                "aggregate_key_type": "IP"
                            }
                        },
                        "visibility_config": {
                            "sampled_requests_enabled": True,
                            "cloudwatch_metrics_enabled": True,
                            "metric_name": "rate-limit"
                        }
                    }],
                    "visibility_config": {
                        "sampled_requests_enabled": True,
                        "cloudwatch_metrics_enabled": True,
                        "metric_name": f"{name}_{idx+1}"
                    },
                    "tags": {
                        "Name": f"{name}_{idx+1}",
                        "Purpose": "web-protection",
                        "Environment": "production"
                    }
                }
            },
            "mode": "managed",
            "type": "aws_wafv2_web_acl",
            "name": f"{name}_{idx+1}",
            "provider_name": "registry.terraform.io/hashicorp/aws"
        })
        save_test_case(plan, f"optimization_tests/massive_suite/security_overhead/waf/{name}_{limit}_limit_{idx+1}.json")

    # Security Groups with various rule counts (10 tests)
    sg_rules = [5, 10, 25, 50, 75, 100, 150, 200, 250, 300]
    for idx, num_rules in enumerate(sg_rules):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append({
            "address": f"aws_security_group.complex_sg_{num_rules}_{idx+1}",
            "change": {
                "actions": ["create"],
                "before": None,
                "after": {
                    "name": f"complex-sg-{num_rules}-{idx+1}",
                    "description": f"Security group with {num_rules} rules",
                    "vpc_id": "vpc-12345",
                    "tags": {
                        "Name": f"complex-sg-{num_rules}-{idx+1}",
                        "Rules": str(num_rules),
                        "Environment": "production"
                    }
                }
            },
            "mode": "managed",
            "type": "aws_security_group",
            "name": f"complex_sg_{num_rules}_{idx+1}",
            "provider_name": "registry.terraform.io/hashicorp/aws"
        })
        save_test_case(plan, f"optimization_tests/massive_suite/security_overhead/security_groups/sg_{num_rules}_rules_{idx+1}.json")

    # IAM Roles with various permission levels (10 tests)
    iam_configs = [
        ("admin", "full-admin-role"),
        ("poweruser", "power-user-role"),
        ("developer", "developer-role"),
        ("readonly", "read-only-role"),
        ("billing", "billing-role"),
        ("security", "security-role"),
        ("network", "network-role"),
        ("database", "database-role"),
        ("storage", "storage-role"),
        ("monitoring", "monitoring-role")
    ]
    for idx, (role_type, role_name) in enumerate(iam_configs):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append({
            "address": f"aws_iam_role.{role_name}_{idx+1}",
            "change": {
                "actions": ["create"],
                "before": None,
                "after": {
                    "name": f"{role_name}_{idx+1}",
                    "assume_role_policy": json.dumps({
                        "Version": "2012-10-17",
                        "Statement": [{
                            "Effect": "Allow",
                            "Principal": {"Service": "ec2.amazonaws.com"},
                            "Action": "sts:AssumeRole"
                        }]
                    }),
                    "tags": {
                        "Name": f"{role_name}_{idx+1}",
                        "Type": role_type,
                        "Environment": "production"
                    }
                }
            },
            "mode": "managed",
            "type": "aws_iam_role",
            "name": f"{role_name}_{idx+1}",
            "provider_name": "registry.terraform.io/hashicorp/aws"
        })
        save_test_case(plan, f"optimization_tests/massive_suite/security_overhead/iam_roles/iam_{role_type}_{idx+1}.json")

    # Auto Scaling Groups (20 tests)
    print("Generating auto scaling group tests...")
    asg_configs = [
        ("t3.medium", 1, 3), ("t3.large", 2, 5), ("m5.large", 1, 2), ("m5.xlarge", 3, 8),
        ("c5.large", 2, 6), ("c5.xlarge", 1, 4), ("r5.large", 2, 7), ("r5.xlarge", 1, 3),
        ("t3.small", 5, 15), ("t3.medium", 3, 10), ("m5.large", 1, 5), ("m5.xlarge", 2, 8),
        ("c5.large", 3, 9), ("c5.xlarge", 1, 6), ("r5.large", 2, 10), ("r5.xlarge", 1, 4),
        ("t3.large", 4, 12), ("t3.xlarge", 2, 8), ("m5.2xlarge", 1, 3), ("c5.2xlarge", 2, 6)
    ]
    for idx, (instance_type, min_size, max_size) in enumerate(asg_configs):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_auto_scaling_group_test(f"asg_{idx+1}", instance_type, min_size, max_size)
        )
        save_test_case(plan, f"optimization_tests/massive_suite/architecture_patterns/auto_scaling/asg_{instance_type.replace('.', '_')}_{min_size}_{max_size}_{idx+1}.json")

    # Lambda Functions (40 tests)
    print("Generating Lambda function tests...")
    lambda_configs = [
        (128, "python3.9", 30), (256, "python3.9", 60), (512, "python3.9", 120), (1024, "python3.9", 300),
        (2048, "python3.9", 600), (3008, "python3.9", 900), (128, "nodejs18.x", 30), (256, "nodejs18.x", 60),
        (512, "nodejs18.x", 120), (1024, "nodejs18.x", 300), (128, "java11", 30), (256, "java11", 60),
        (512, "java11", 120), (1024, "java11", 300), (2048, "java11", 600), (3008, "java11", 900),
        (128, "dotnet6", 30), (256, "dotnet6", 60), (512, "dotnet6", 120), (1024, "dotnet6", 300),
        (128, "go1.x", 30), (256, "go1.x", 60), (512, "go1.x", 120), (1024, "go1.x", 300),
        (128, "ruby2.7", 30), (256, "ruby2.7", 60), (512, "ruby2.7", 120), (1024, "ruby2.7", 300),
        (2048, "python3.9", 30), (3008, "nodejs18.x", 60), (128, "python3.9", 900), (256, "java11", 900),
        (512, "dotnet6", 900), (1024, "go1.x", 900), (2048, "ruby2.7", 900), (3008, "python3.9", 900),
        (128, "nodejs18.x", 900), (256, "python3.9", 900), (512, "java11", 900), (1024, "dotnet6", 900)
    ]
    for idx, (memory, runtime, timeout) in enumerate(lambda_configs):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_lambda_test(f"lambda_{idx+1}", memory, runtime, timeout)
        )
        save_test_case(plan, f"optimization_tests/massive_suite/serverless/lambda/lambda_{memory}mb_{runtime.replace('.', '_')}_{timeout}s_{idx+1}.json")

    # CloudFront Distributions (15 tests)
    print("Generating CloudFront distribution tests...")
    cloudfront_configs = [
        "PriceClass_100", "PriceClass_200", "PriceClass_All", "PriceClass_100", "PriceClass_200",
        "PriceClass_All", "PriceClass_100", "PriceClass_200", "PriceClass_All", "PriceClass_100",
        "PriceClass_200", "PriceClass_All", "PriceClass_100", "PriceClass_200", "PriceClass_All"
    ]
    for idx, price_class in enumerate(cloudfront_configs):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_cloudfront_test(f"cloudfront_{idx+1}", price_class)
        )
        save_test_case(plan, f"optimization_tests/massive_suite/cdn/cloudfront/cloudfront_{price_class}_{idx+1}.json")

    # ElastiCache Clusters (20 tests)
    print("Generating ElastiCache tests...")
    elasticache_configs = [
        ("cache.t3.micro", 1), ("cache.t3.small", 1), ("cache.t3.medium", 1), ("cache.m5.large", 1),
        ("cache.m5.xlarge", 1), ("cache.r5.large", 1), ("cache.r5.xlarge", 1), ("cache.c5.large", 1),
        ("cache.c5.xlarge", 1), ("cache.t3.micro", 2), ("cache.t3.small", 2), ("cache.t3.medium", 2),
        ("cache.m5.large", 2), ("cache.m5.xlarge", 2), ("cache.r5.large", 2), ("cache.r5.xlarge", 2),
        ("cache.c5.large", 2), ("cache.c5.xlarge", 2), ("cache.m5.2xlarge", 1), ("cache.r5.2xlarge", 1)
    ]
    for idx, (node_type, num_nodes) in enumerate(elasticache_configs):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_elasticache_test(f"elasticache_{idx+1}", node_type, num_nodes)
        )
        save_test_case(plan, f"optimization_tests/massive_suite/caching/elasticache/elasticache_{node_type.replace('.', '_')}_{num_nodes}nodes_{idx+1}.json")

    # API Gateway (15 tests)
    print("Generating API Gateway tests...")
    api_gateway_configs = [
        "REGIONAL", "EDGE", "PRIVATE", "REGIONAL", "EDGE", "PRIVATE", "REGIONAL", "EDGE", "PRIVATE",
        "REGIONAL", "EDGE", "PRIVATE", "REGIONAL", "EDGE", "PRIVATE"
    ]
    for idx, endpoint_type in enumerate(api_gateway_configs):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_api_gateway_test(f"api_gw_{idx+1}", endpoint_type)
        )
        save_test_case(plan, f"optimization_tests/massive_suite/api/api_gateway/api_gw_{endpoint_type}_{idx+1}.json")

    # Additional Instance Variations (50+ more tests)
    print("Generating additional instance variations...")

    # Multi-region instances (20 tests)
    regions = ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1", "ap-northeast-1"]
    region_instances = ["m5.large", "c5.large", "r5.large", "t3.medium", "m5.xlarge"]
    for region in regions:
        for instance_type in region_instances:
            plan = create_base_terraform_plan()
            plan["resource_changes"].append(
                generate_instance_test(instance_type, f"regional_{region.replace('-', '_')}_{instance_type.replace('.', '_')}",
                                    "regional-workload", "production")
            )
            save_test_case(plan, f"optimization_tests/massive_suite/instance_rightsizing/regional/{region}/{region}_{instance_type.replace('.', '_')}.json")

    # Reserved instance candidates (15 tests)
    reserved_candidates = [
        ("m5.large", "prod_reserved"), ("c5.large", "prod_reserved"), ("r5.large", "prod_reserved"),
        ("m5.xlarge", "prod_reserved"), ("c5.xlarge", "prod_reserved"), ("r5.xlarge", "prod_reserved"),
        ("m5.2xlarge", "prod_reserved"), ("c5.2xlarge", "prod_reserved"), ("r5.2xlarge", "prod_reserved"),
        ("m5.4xlarge", "prod_reserved"), ("c5.4xlarge", "prod_reserved"), ("r5.4xlarge", "prod_reserved"),
        ("m5.8xlarge", "prod_reserved"), ("c5.9xlarge", "prod_reserved"), ("r5.8xlarge", "prod_reserved")
    ]
    for idx, (instance_type, purpose) in enumerate(reserved_candidates):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_instance_test(instance_type, f"reserved_{idx+1}", purpose, "production")
        )
        save_test_case(plan, f"optimization_tests/massive_suite/instance_rightsizing/reserved_instances/reserved_{instance_type.replace('.', '_')}_{idx+1}.json")

    # Spot instance opportunities (15 tests)
    spot_candidates = [
        ("m5.large", "spot_eligible"), ("c5.large", "spot_eligible"), ("r5.large", "spot_eligible"),
        ("m5.xlarge", "spot_eligible"), ("c5.xlarge", "spot_eligible"), ("r5.xlarge", "spot_eligible"),
        ("m5.2xlarge", "spot_eligible"), ("c5.2xlarge", "spot_eligible"), ("r5.2xlarge", "spot_eligible"),
        ("t3.medium", "spot_eligible"), ("t3.large", "spot_eligible"), ("t3.xlarge", "spot_eligible"),
        ("m5.4xlarge", "spot_eligible"), ("c5.4xlarge", "spot_eligible"), ("r5.4xlarge", "spot_eligible")
    ]
    for idx, (instance_type, purpose) in enumerate(spot_candidates):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_instance_test(instance_type, f"spot_{idx+1}", purpose, "production")
        )
        save_test_case(plan, f"optimization_tests/massive_suite/instance_rightsizing/spot_instances/spot_{instance_type.replace('.', '_')}_{idx+1}.json")

    print("Generated massive test suite!")
    print("Run 'find optimization_tests/massive_suite/ -name \"*.json\" | wc -l' to count total tests")
    db_configs = [
        ("c5.large", "database"),
        ("m5.large", "database"),
        ("t3.medium", "database"),
        ("r5.large", "database"),
        ("c5.xlarge", "database"),
    ]
    for i, (size, purpose) in enumerate(db_configs):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_instance_test(size, f"db_{i+1}", purpose, "production")
        )
        save_test_case(plan, f"optimization_tests/massive_suite/instance_rightsizing/databases/db_{size.replace('.', '_')}_{i+1}.json")
    
    # Development instances - should be smaller
    dev_sizes = ["m5.large", "c5.large", "r5.large", "m5.xlarge", "t3.large"]
    for i, size in enumerate(dev_sizes):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_instance_test(size, f"dev_{i+1}", "development", "development")
        )
        save_test_case(plan, f"optimization_tests/massive_suite/instance_rightsizing/development/dev_{size.replace('.', '_')}.json")
    
    # Background jobs - various configurations
    job_configs = [
        ("t3.medium", "batch-job"),
        ("m5.large", "batch-job"),
        ("c5.large", "batch-job"),
        ("r5.large", "batch-job"),
    ]
    for i, (size, purpose) in enumerate(job_configs):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_instance_test(size, f"job_{i+1}", purpose, "production")
        )
        save_test_case(plan, f"optimization_tests/massive_suite/instance_rightsizing/background_jobs/job_{size.replace('.', '_')}_{i+1}.json")
    
    # Storage Optimization Tests
    print("Generating storage optimization tests...")
    
    # EBS volumes - various sizes and types
    ebs_configs = [
        (1000, "gp2", "large_data_volume"),
        (500, "gp2", "medium_data_volume"),
        (2000, "gp2", "huge_data_volume"),
        (100, "gp2", "small_data_volume"),
        (5000, "gp2", "massive_data_volume"),
    ]
    for i, (size, vol_type, name) in enumerate(ebs_configs):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_ebs_test(size, vol_type, f"ebs_{i+1}", "application-data")
        )
        save_test_case(plan, f"optimization_tests/massive_suite/storage_optimization/ebs_volumes/ebs_{size}gb_{vol_type}.json")
    
    # RDS instances - various storage sizes
    rds_configs = [
        ("db.t3.micro", 1000, "micro_large_storage"),
        ("db.t3.small", 500, "small_medium_storage"),
        ("db.m5.large", 2000, "large_huge_storage"),
        ("db.t3.micro", 200, "micro_small_storage"),
        ("db.r5.large", 100, "memory_small_storage"),
    ]
    for i, (instance_class, storage, name) in enumerate(rds_configs):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_rds_test(instance_class, storage, f"rds_{i+1}", "postgres")
        )
        save_test_case(plan, f"optimization_tests/massive_suite/storage_optimization/rds_instances/rds_{instance_class.replace('.', '_')}_{storage}gb.json")
    
    # Architecture Pattern Tests
    print("Generating architecture pattern tests...")
    
    # Microservices - multiple small instances
    for num_instances in [3, 5, 7]:
        plan = create_base_terraform_plan()
        for i in range(num_instances):
            plan["resource_changes"].append(
                generate_instance_test("t3.small", f"microservice_{i+1}", f"service-{i+1}", "production")
            )
        save_test_case(plan, f"optimization_tests/massive_suite/architecture_patterns/microservices/{num_instances}_microservices.json")
    
    # Monolithic applications
    monolithic_sizes = ["m5.xlarge", "c5.2xlarge", "r5.xlarge", "m5.2xlarge"]
    for i, size in enumerate(monolithic_sizes):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_instance_test(size, f"monolithic_{i+1}", "all-services", "production")
        )
        save_test_case(plan, f"optimization_tests/massive_suite/architecture_patterns/monolithic/monolithic_{size.replace('.', '_')}.json")
    
    # Development environments
    for num_devs in [2, 3, 5]:
        plan = create_base_terraform_plan()
        for i in range(num_devs):
            plan["resource_changes"].append(
                generate_instance_test("m5.large", f"dev_env_{i+1}", "development", "development")
            )
        save_test_case(plan, f"optimization_tests/massive_suite/architecture_patterns/development_envs/{num_devs}_dev_instances.json")
    
    # Network Optimization Tests
    print("Generating network optimization tests...")
    
    # NAT Gateways
    for i in range(5):
        plan = create_base_terraform_plan()
        plan["resource_changes"].append(
            generate_nat_gateway_test(f"nat_gw_{i+1}")
        )
        save_test_case(plan, f"optimization_tests/massive_suite/network_optimization/nat_gateways/nat_gateway_{i+1}.json")
    
    print("Generated massive test suite!")
    print("Run 'find optimization_tests/massive_suite/ -name \"*.json\" | wc -l' to count total tests")

if __name__ == "__main__":
    main()
