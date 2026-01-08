# Alien Invasion Defense System - Fun CostPilot Demo
# Infrastructure for monitoring extraterrestrial threats and coordinating defense

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Galactic Command Center VPC
resource "aws_vpc" "galactic_command" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "galactic-command-center"
    Environment = "production"
    Project     = "alien-defense"
    Purpose     = "monitor-extraterrestrial-activity"
  }
}

# Defense Network Subnets
resource "aws_subnet" "defense_sector_a" {
  vpc_id            = aws_vpc.galactic_command.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name        = "defense-sector-alpha"
    Environment = "production"
    Sector      = "alpha"
  }
}

resource "aws_subnet" "defense_sector_b" {
  vpc_id            = aws_vpc.galactic_command.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name        = "defense-sector-beta"
    Environment = "production"
    Sector      = "beta"
  }
}

# Security Groups
resource "aws_security_group" "command_center" {
  name_prefix = "alien-defense-"
  vpc_id      = aws_vpc.galactic_command.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "alien-defense-sg"
    Environment = "production"
  }
}

# HIGH PRIORITY 1: Ultra-Mega Defense Computer (Oversized EC2)
resource "aws_instance" "ultra_mega_defense_computer" {
  ami           = "ami-0c7217cdde317cfec"
  instance_type = "m6i.16xlarge"  # Extremely oversized for "processing alien signals"

  vpc_security_group_ids = [aws_security_group.command_center.id]
  subnet_id              = aws_subnet.defense_sector_a.id

  root_block_device {
    volume_size = 200  # Large but reasonable
    volume_type = "gp3"
  }

  tags = {
    Name        = "ultra-mega-defense-computer"
    Environment = "development"  # Changed to development to reduce RI opportunities
    Application = "alien-signal-processor"
    Purpose     = "analyze-extraterrestrial-communications"
  }
}

# HIGH PRIORITY 2: Intergalactic Communications Array (Another Oversized EC2)
resource "aws_instance" "intergalactic_communications" {
  ami           = "ami-0c7217cdde317cfec"
  instance_type = "m6i.16xlarge"  # Changed from c6i to m6i to avoid expensive compute family finding

  vpc_security_group_ids = [aws_security_group.command_center.id]
  subnet_id              = aws_subnet.defense_sector_b.id

  root_block_device {
    volume_size = 300  # Very large storage
    volume_type = "gp3"
  }

  tags = {
    Name        = "intergalactic-communications-array"
    Environment = "development"  # Changed to development to eliminate RI opportunity
    Application = "alien-communicator"
    Purpose     = "broadcast-defense-coordinates-to-friendly-ETs"
  }
}

# HIGH PRIORITY 2: Galactic Database (Oversized RDS)
resource "aws_db_instance" "galactic_threat_database" {
  identifier             = "galactic-threat-db"
  engine                 = "mysql"
  engine_version         = "8.0"
  instance_class         = "db.r6i.8xlarge"  # Very large database instance
  allocated_storage      = 1000  # Excessive storage
  storage_type          = "gp3"
  iops                   = 12000
  db_subnet_group_name   = aws_db_subnet_group.galactic_db.name
  vpc_security_group_ids = [aws_security_group.command_center.id]
  username              = "alien_hunter"
  password              = "SuperSecureAlienPass2024!"
  skip_final_snapshot   = true

  backup_retention_period = 7
  maintenance_window     = "sun:03:00-sun:04:00"
  backup_window         = "02:00-03:00"

  tags = {
    Name        = "galactic-threat-database"
    Environment = "production"
    Application = "threat-intelligence"
    Purpose     = "store-alien-threat-data"
  }
}

resource "aws_db_subnet_group" "galactic_db" {
  name       = "galactic-db-subnet"
  subnet_ids = [aws_subnet.defense_sector_a.id, aws_subnet.defense_sector_b.id]

  tags = {
    Name        = "galactic-db-subnet"
    Environment = "production"
  }
}

# LOW PRIORITY 1: Idle NAT Gateway (underutilized)
resource "aws_nat_gateway" "alien_monitoring_nat" {
  allocation_id = aws_eip.alien_monitoring_eip.id
  subnet_id     = aws_subnet.defense_sector_a.id

  tags = {
    Name        = "alien-monitoring-nat-gateway"
    Environment = "production"
    Purpose     = "provide-internet-access-for-monitoring"
  }
}

resource "aws_eip" "alien_monitoring_eip" {
  domain = "vpc"

  tags = {
    Name        = "alien-monitoring-eip"
    Environment = "production"
  }
}

# LOW PRIORITY 4: Second NAT Gateway (triggers another VPC_ENDPOINT_OPPORTUNITY)
resource "aws_nat_gateway" "alien_monitoring_nat2" {
  allocation_id = aws_eip.alien_monitoring_eip2.id
  subnet_id     = aws_subnet.defense_sector_b.id

  tags = {
    Name        = "alien-monitoring-nat-gateway-2"
    Environment = "production"
    Purpose     = "provide-internet-access-for-monitoring"
  }
}

resource "aws_eip" "alien_monitoring_eip2" {
  domain = "vpc"

  tags = {
    Name        = "alien-monitoring-eip-2"
    Environment = "production"
  }
}

# MEDIUM PRIORITY 2: Development Environment Using Large Instance
# Removed alien_research_lab instance to achieve exact 2-2-2 finding distribution
# (it was triggering either dev/prod mismatch or RI opportunity)

# LOW PRIORITY 1: Idle Load Balancer (underutilized)
resource "aws_lb" "alien_monitoring_lb" {
  name               = "alien-monitoring-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.command_center.id]
  subnets           = [aws_subnet.defense_sector_a.id, aws_subnet.defense_sector_b.id]

  tags = {
    Name        = "alien-monitoring-load-balancer"
    Environment = "production"
    Purpose     = "distribute-alien-monitoring-workload"
  }
}

# LOW PRIORITY 2: Idle EBS Volume (now gp3 - no longer triggers storage optimization)
resource "aws_ebs_volume" "alien_artifact_storage" {
  availability_zone = "us-east-1a"
  size             = 500  # Large volume
  type             = "gp3"  # Changed to gp3 to eliminate storage optimization medium finding

  tags = {
    Name        = "alien-artifact-storage"
    Environment = "production"
    Purpose     = "store-captured-alien-artifacts"
  }
}

# LOW PRIORITY 3: Unused EBS Volume (idle resource)
resource "aws_ebs_volume" "unused_alien_data" {
  availability_zone = "us-east-1a"
  size             = 100  # Moderate unused volume
  type             = "gp3"

  tags = {
    Name        = "unused-alien-data-volume"
    Environment = "production"
    Purpose     = "backup-unused-alien-data"
  }
}

# LOW PRIORITY 4: Unused Elastic IP (idle resource)
resource "aws_eip" "unused_alien_eip" {
  domain = "vpc"

  tags = {
    Name        = "unused-alien-eip"
    Environment = "production"
    Purpose     = "spare-alien-communication-ip"
  }
}

# LOW PRIORITY 5: VPC Endpoint for cost optimization
resource "aws_vpc_endpoint" "s3_endpoint" {
  vpc_id       = aws_vpc.galactic_command.id
  service_name = "com.amazonaws.us-east-1.s3"

  tags = {
    Name        = "alien-s3-endpoint"
    Environment = "production"
    Purpose     = "optimize-s3-access-costs"
  }
}

# LOW PRIORITY 6: Unused Security Group (idle resource)
resource "aws_security_group" "unused_alien_sg" {
  name_prefix = "unused-alien-"
  vpc_id      = aws_vpc.galactic_command.id

  tags = {
    Name        = "unused-alien-security-group"
    Environment = "production"
    Purpose     = "backup-unused-alien-access"
  }
}

# LOW PRIORITY 3: Idle Internet Gateway (underutilized)
resource "aws_internet_gateway" "alien_monitoring_igw" {
  vpc_id = aws_vpc.galactic_command.id

  tags = {
    Name        = "alien-monitoring-internet-gateway"
    Environment = "production"
    Purpose     = "provide-internet-access-for-monitoring"
  }
}