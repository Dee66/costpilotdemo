# CostPilot Demo Infrastructure

This directory contains a demo Terraform configuration that creates infrastructure designed to showcase CostPilot CLI's cost optimization detection capabilities.

## Files

- `demo_infrastructure.tf` - Terraform configuration with resources that trigger various cost optimization recommendations
- `demo_plan.json` - Pre-generated Terraform plan in JSON format (ready for CostPilot scanning)
- `generate_lambda_tests.sh` - Script for generating additional test scenarios

## Demo Resources

The demo infrastructure includes:

1. **EC2 Instance** (`m5.large`) - Triggers Reserved Instance recommendations
2. **S3 Bucket** with versioning - Triggers lifecycle policy recommendations
3. **Lambda Function** (512MB, 120s timeout) - Triggers memory optimization recommendations
4. **RDS MySQL Instance** (`db.t3.medium`, 100GB gp2) - Triggers storage optimization recommendations
5. **EBS Volume** (200GB gp2) - Triggers gp2 to gp3 migration recommendations
6. **ElastiCache Redis** (single node) - Triggers redundancy recommendations
7. **SQS Queue** - Triggers messaging optimization recommendations

## Running the Demo

### Option 1: Use Pre-generated Plan (Recommended for Demos)

```bash
./costpilot scan demo_plan.json
```

This will show 7 optimization opportunities across 11 resources with an estimated monthly cost of $150.00.

### Option 2: Generate Fresh Plan

```bash
terraform init
terraform plan -out=tfplan
terraform show -json tfplan > fresh_demo_plan.json
./costpilot scan fresh_demo_plan.json
```

## Expected Results

CostPilot will detect the following optimization opportunities:

- **Medium Priority (4):**
  - EBS gp2 to gp3 migration ($4/month savings)
  - RDS gp2 to gp3 storage migration ($2/month savings)
  - Reserved Instance opportunity for EC2 ($60/month savings)
  - S3 lifecycle policy recommendations

- **Low Priority (3):**
  - ElastiCache redundancy recommendation
  - Additional S3 lifecycle review
  - Lambda memory optimization

**Total: 7 optimization opportunities**

## Screenshot Recommendations

For best demo screenshots, capture:

1. The initial scan output showing all recommendations
2. Individual recommendation details (use `--verbose` flag if available)
3. The summary section showing total potential savings

## Customization

To modify the demo infrastructure:

1. Edit `demo_infrastructure.tf`
2. Run `terraform plan -out=tfplan && terraform show -json tfplan > demo_plan.json`
3. Test with `./costpilot scan demo_plan.json`

This demo configuration provides a realistic infrastructure scenario that demonstrates CostPilot's ability to detect multiple types of cost optimization opportunities across different AWS services.