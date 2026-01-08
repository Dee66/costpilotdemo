#!/usr/bin/env python3
# test_framework/scripts/generators/generate_massive_tests.py

import json
import os
import random
from pathlib import Path

class TestGenerator:
    def __init__(self, base_dir="optimization_tests/massive_suite"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def generate_container_tests(self, count=800):
        """Generate ECS Fargate optimization test cases"""
        container_dir = self.base_dir / "containers"
        container_dir.mkdir(exist_ok=True)

        cpu_options = [512, 1024, 2048, 4096, 8192]
        memory_options = [1024, 2048, 4096, 8192, 16384, 32768]

        for i in range(count):
            cpu = random.choice(cpu_options)
            memory = random.choice(memory_options)

            # Create oversized scenario
            if cpu >= 2048 or memory >= 8192:
                test_case = self._create_ecs_test_case(cpu, memory, f"oversized_{i}")
                with open(container_dir / f"ecs_oversized_{i}.json", 'w', encoding='utf-8') as f:
                    f.write(json.dumps(test_case, indent=2))

    def generate_instance_rightsizing_tests(self, count=1200):
        """Generate EC2 instance rightsizing test cases"""
        instance_dir = self.base_dir / "instance_rightsizing"
        instance_dir.mkdir(exist_ok=True)

        instance_types = [
            "t3.micro", "t3.small", "t3.medium",
            "m5.large", "m5.xlarge", "m5.2xlarge", "m5.4xlarge",
            "c5.large", "c5.xlarge", "c5.2xlarge",
            "r5.large", "r5.xlarge", "r5.2xlarge"
        ]

        for i in range(count):
            instance_type = random.choice(instance_types)
            test_case = self._create_ec2_test_case(instance_type, f"rightsizing_{i}")
            with open(instance_dir / f"ec2_{instance_type.replace('.', '_')}_{i}.json", 'w', encoding='utf-8') as f:
                f.write(json.dumps(test_case, indent=2))

    def _create_ecs_test_case(self, cpu, memory, scenario):
        return {
            "format_version": "1.2",
            "terraform_version": "1.6.0",
            "resource_changes": [{
                "address": f"aws_ecs_task_definition.{scenario}",
                "change": {
                    "actions": ["create"],
                    "after": {
                        "family": f"{scenario}-task",
                        "cpu": str(cpu),
                        "memory": str(memory),
                        "requires_compatibilities": ["FARGATE"],
                        "container_definitions": json.dumps([{
                            "name": "app",
                            "image": "nginx",
                            "cpu": 256,
                            "memory": 512
                        }])
                    }
                },
                "mode": "managed",
                "type": "aws_ecs_task_definition",
                "name": scenario
            }]
        }

    def _create_ec2_test_case(self, instance_type, scenario):
        return {
            "format_version": "1.2",
            "terraform_version": "1.6.0",
            "resource_changes": [{
                "address": f"aws_instance.{scenario}",
                "change": {
                    "actions": ["create"],
                    "after": {
                        "instance_type": instance_type,
                        "ami": "ami-12345678",
                        "tags": {
                            "Name": scenario,
                            "Environment": "test"
                        }
                    }
                },
                "mode": "managed",
                "type": "aws_instance",
                "name": scenario
            }]
        }

if __name__ == "__main__":
    generator = TestGenerator()
    print("Generating massive test suite...")

    generator.generate_container_tests(800)
    generator.generate_instance_rightsizing_tests(1200)

    print("✅ Test generation completed!")