# Demo Infrastructure for CostPilot CLI
# This Terraform configuration creates resources that will trigger various cost optimization recommendations

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

# EC2 Instance - Will trigger Reserved Instance recommendation
resource "aws_instance" "web_server" {
  ami           = "ami-0c7217cdde317cfec"
  instance_type = "m5.large"

  tags = {
    Name        = "demo-web-server"
    Environment = "production"
    Application = "web-app"
    Team        = "platform"
  }
}

# S3 Bucket without lifecycle policy - Will trigger S3 lifecycle recommendations
resource "aws_s3_bucket" "static_assets" {
  bucket = "demo-static-assets-${random_string.suffix.result}"

  tags = {
    Name        = "demo-static-assets"
    Environment = "production"
    Purpose     = "static-content"
  }
}

resource "aws_s3_bucket_versioning" "static_assets_versioning" {
  bucket = aws_s3_bucket.static_assets.id
  versioning_configuration {
    status = "Enabled"
  }
}

# IAM Role for Lambda function
resource "aws_iam_role" "lambda_role" {
  name = "demo-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "demo-lambda-role"
    Environment = "production"
  }
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Lambda function with potentially suboptimal configuration
resource "aws_lambda_function" "data_processor" {
  function_name = "demo-data-processor"
  runtime       = "python3.9"
  handler       = "lambda_function.lambda_handler"
  memory_size   = 512
  timeout       = 120
  role          = aws_iam_role.lambda_role.arn

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  tags = {
    Name        = "demo-data-processor"
    Environment = "production"
    Application = "data-pipeline"
  }
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  output_path = "${path.module}/lambda_function.zip"

  source {
    content  = "def lambda_handler(event, context):\n    return {'statusCode': 200, 'body': 'Hello World'}"
    filename = "lambda_function.py"
  }
}

# RDS Instance - Will trigger database optimization recommendations
resource "aws_db_instance" "application_db" {
  identifier           = "demo-app-db"
  engine              = "mysql"
  engine_version      = "8.0"
  instance_class      = "db.t3.medium"
  allocated_storage   = 100
  storage_type        = "gp2"
  username           = "admin"
  password           = "password123"
  skip_final_snapshot = true

  tags = {
    Name        = "demo-application-db"
    Environment = "production"
    Application = "web-app"
  }
}

# EBS Volume - Will trigger storage optimization recommendations
resource "aws_ebs_volume" "data_volume" {
  availability_zone = "us-east-1a"
  size             = 200
  type             = "gp2"

  tags = {
    Name        = "demo-data-volume"
    Environment = "production"
    Application = "data-storage"
  }
}

# ElastiCache cluster - Will trigger caching optimization recommendations
resource "aws_elasticache_cluster" "redis_cache" {
  cluster_id      = "demo-redis-cache"
  engine         = "redis"
  node_type      = "cache.t3.medium"
  num_cache_nodes = 1

  tags = {
    Name        = "demo-redis-cache"
    Environment = "production"
    Application = "web-app"
  }
}

# SQS Queue - Will trigger messaging optimization recommendations
resource "aws_sqs_queue" "task_queue" {
  name = "demo-task-queue"

  tags = {
    Name        = "demo-task-queue"
    Environment = "production"
    Application = "async-processing"
  }
}

# Random suffix for unique bucket names
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}