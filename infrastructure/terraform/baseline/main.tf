# CostPilot Demo - Baseline Infrastructure
# This represents a cost-efficient baseline for comparison
#
# ⚠️  WARNING: DO NOT RUN 'terraform apply' ⚠️
# This is a DEMONSTRATION REPOSITORY for documentation only.
# Running terraform apply will create real AWS resources and incur costs.
# See: infrastructure/terraform/SAFEGUARDS.md

terraform {
  required_version = ">=1.6"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "CostPilot-Demo"
      Environment = "baseline"
      ManagedBy   = "Terraform"
    }
  }
}

# VPC and Networking
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  lifecycle {
    prevent_destroy = true
  }

  tags = {
    Name = "costpilot-demo-vpc"
  }
}

resource "aws_subnet" "public_a" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true

  tags = {
    Name = "costpilot-demo-public-a"
    Type = "public"
  }
}

resource "aws_subnet" "public_b" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "${var.aws_region}b"
  map_public_ip_on_launch = true

  tags = {
    Name = "costpilot-demo-public-b"
    Type = "public"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "costpilot-demo-igw"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "costpilot-demo-public-rt"
  }
}

resource "aws_route_table_association" "public_a" {
  subnet_id      = aws_subnet.public_a.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_b" {
  subnet_id      = aws_subnet.public_b.id
  route_table_id = aws_route_table.public.id
}

# Security Group for ALB
resource "aws_security_group" "alb" {
  name        = "costpilot-demo-alb-sg"
  description = "Security group for Application Load Balancer"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "All outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "costpilot-demo-alb-sg"
  }
}

# Security Group for EC2 Instances
resource "aws_security_group" "ec2" {
  name        = "costpilot-demo-ec2-sg"
  description = "Security group for EC2 instances"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "HTTP from ALB"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    description = "All outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "costpilot-demo-ec2-sg"
  }
}

# Application Load Balancer
resource "aws_lb" "main" {
  name               = "costpilot-demo-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = [aws_subnet.public_a.id, aws_subnet.public_b.id]

  enable_deletion_protection = false

  tags = {
    Name = "costpilot-demo-alb"
  }
}

# Target Group
resource "aws_lb_target_group" "main" {
  name     = "costpilot-demo-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }

  tags = {
    Name = "costpilot-demo-tg"
  }
}

# Listener
resource "aws_lb_listener" "main" {
  load_balancer_arn = aws_lb.main.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.main.arn
  }
}

# Launch Template for EC2 instances
resource "aws_launch_template" "main" {
  name_prefix   = "costpilot-demo-"
  image_id      = data.aws_ami.amazon_linux_2.id
  instance_type = "t3.micro" # Cost-efficient baseline

  vpc_security_group_ids = [aws_security_group.ec2.id]

  user_data = base64encode(<<-EOF
              #!/bin/bash
              yum update -y
              yum install -y httpd
              systemctl start httpd
              systemctl enable httpd
              echo "<h1>CostPilot Demo - Baseline</h1>" > /var/www/html/index.html
              EOF
  )

  block_device_mappings {
    device_name = "/dev/xvda"

    ebs {
      volume_size           = 20 # Baseline: 20GB
      volume_type           = "gp3"
      delete_on_termination = true
      encrypted             = true
    }
  }

  metadata_options {
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }

  tags = {
    Name = "costpilot-demo-lt"
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "main" {
  name                      = "costpilot-demo-asg"
  vpc_zone_identifier       = [aws_subnet.public_a.id, aws_subnet.public_b.id]
  target_group_arns         = [aws_lb_target_group.main.arn]
  health_check_type         = "ELB"
  health_check_grace_period = 300

  min_size         = 2
  max_size         = 4
  desired_capacity = 2

  launch_template {
    id      = aws_launch_template.main.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "costpilot-demo-instance"
    propagate_at_launch = true
  }

  tag {
    key                 = "Environment"
    value               = "baseline"
    propagate_at_launch = true
  }
}

# S3 Bucket with Lifecycle Policy (cost-efficient baseline)
resource "aws_s3_bucket" "main" {
  bucket = "${var.project_name}-demo-bucket-${data.aws_caller_identity.current.account_id}"

  tags = {
    Name        = "costpilot-demo-bucket"
    Environment = "baseline"
  }
}

resource "aws_s3_bucket_versioning" "main" {
  bucket = aws_s3_bucket.main.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "main" {
  bucket = aws_s3_bucket.main.id

  rule {
    id     = "transition-old-versions"
    status = "Enabled"

    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "STANDARD_IA"
    }

    noncurrent_version_transition {
      noncurrent_days = 90
      storage_class   = "GLACIER"
    }

    noncurrent_version_expiration {
      noncurrent_days = 180
    }
  }

  rule {
    id     = "expire-old-objects"
    status = "Enabled"

    expiration {
      days = 365
    }
  }
}

# CloudWatch Log Group with 30-day retention (cost-efficient baseline)
resource "aws_cloudwatch_log_group" "application" {
  name              = "/aws/costpilot-demo/application"
  retention_in_days = 30 # Baseline: 30 days

  tags = {
    Name        = "costpilot-demo-logs"
    Environment = "baseline"
  }
}

# Data sources
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

data "aws_caller_identity" "current" {}


# Mini Real-World Stack (v2.0.0 Enhancement)

# These components demonstrate realistic application patterns:
# REST API → Queue → Background Worker → Analytics Storage

# SQS Queue (for async job processing)
resource "aws_sqs_queue" "jobs" {
  name                       = "costpilot-demo-job-queue"
  delay_seconds              = 0
  max_message_size           = 262144
  message_retention_seconds  = 345600 # 4 days
  receive_wait_time_seconds  = 10
  visibility_timeout_seconds = 300

  tags = {
    Name        = "costpilot-demo-job-queue"
    Environment = "baseline"
    Purpose     = "async-job-processing"
  }
}

# Dead Letter Queue
resource "aws_sqs_queue" "jobs_dlq" {
  name                       = "costpilot-demo-job-queue-dlq"
  message_retention_seconds  = 1209600 # 14 days
  
  tags = {
    Name        = "costpilot-demo-job-queue-dlq"
    Environment = "baseline"
    Purpose     = "dead-letter-queue"
  }
}

# Security Group for Background Worker
resource "aws_security_group" "worker" {
  name        = "costpilot-demo-worker-sg"
  description = "Security group for background worker instances"
  vpc_id      = aws_vpc.main.id

  egress {
    description = "All outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "costpilot-demo-worker-sg"
  }
}

# Launch Template for Background Worker
resource "aws_launch_template" "worker" {
  name_prefix   = "costpilot-demo-worker-"
  image_id      = data.aws_ami.amazon_linux_2.id
  instance_type = "t3.micro" # Cost-efficient for background jobs

  vpc_security_group_ids = [aws_security_group.worker.id]

  user_data = base64encode(<<-EOF
              #!/bin/bash
              yum update -y
              yum install -y aws-cli
              
              # Simulate background worker that processes jobs from SQS
              cat > /home/ec2-user/worker.sh << 'WORKER'
              #!/bin/bash
              while true; do
                echo "$(date) - Processing jobs from queue..."
                # Worker would poll SQS and process jobs here
                sleep 30
              done
              WORKER
              
              chmod +x /home/ec2-user/worker.sh
              nohup /home/ec2-user/worker.sh > /var/log/worker.log 2>&1 &
              EOF
  )

  iam_instance_profile {
    name = aws_iam_instance_profile.worker.name
  }

  block_device_mappings {
    device_name = "/dev/xvda"

    ebs {
      volume_size           = 20
      volume_type           = "gp3"
      delete_on_termination = true
      encrypted             = true
    }
  }

  metadata_options {
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }

  tags = {
    Name = "costpilot-demo-worker-lt"
  }
}

# Auto Scaling Group for Worker
resource "aws_autoscaling_group" "worker" {
  name                = "costpilot-demo-worker-asg"
  vpc_zone_identifier = [aws_subnet.public_a.id, aws_subnet.public_b.id]
  health_check_type   = "EC2"

  min_size         = 1
  max_size         = 2
  desired_capacity = 1

  launch_template {
    id      = aws_launch_template.worker.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "costpilot-demo-worker"
    propagate_at_launch = true
  }

  tag {
    key                 = "Role"
    value               = "background-worker"
    propagate_at_launch = true
  }
}

# IAM Role for Worker (to access SQS)
resource "aws_iam_role" "worker" {
  name = "costpilot-demo-worker-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "costpilot-demo-worker-role"
  }
}

# IAM Policy for SQS Access
resource "aws_iam_role_policy" "worker_sqs" {
  name = "costpilot-demo-worker-sqs-policy"
  role = aws_iam_role.worker.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes",
          "sqs:ChangeMessageVisibility"
        ]
        Resource = aws_sqs_queue.jobs.arn
      },
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject"
        ]
        Resource = "${aws_s3_bucket.analytics.arn}/*"
      }
    ]
  })
}

# IAM Instance Profile
resource "aws_iam_instance_profile" "worker" {
  name = "costpilot-demo-worker-profile"
  role = aws_iam_role.worker.name
}

# Analytics S3 Bucket (for processed job results)
resource "aws_s3_bucket" "analytics" {
  bucket = "${var.project_name}-analytics-${data.aws_caller_identity.current.account_id}"

  tags = {
    Name        = "costpilot-demo-analytics"
    Environment = "baseline"
    Purpose     = "job-results-storage"
  }
}

# Analytics Bucket Lifecycle (cost optimization)
resource "aws_s3_bucket_lifecycle_configuration" "analytics" {
  bucket = aws_s3_bucket.analytics.id

  rule {
    id     = "transition-analytics-data"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }
}

# CloudWatch Log Group for Worker
resource "aws_cloudwatch_log_group" "worker" {
  name              = "/aws/costpilot-demo/worker"
  retention_in_days = 30

  tags = {
    Name        = "costpilot-demo-worker-logs"
    Environment = "baseline"
  }
}

