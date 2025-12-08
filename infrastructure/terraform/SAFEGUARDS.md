# Terraform Safeguards - DO NOT APPLY

## 🚨 CRITICAL WARNING 🚨

**This is a DEMONSTRATION REPOSITORY only.**

**DO NOT run `terraform apply` under any circumstances.**

These Terraform configurations are for:
- Documentation purposes
- Generating plan files for CostPilot analysis
- CI/CD pipeline demonstrations
- Cost analysis examples

## What You CAN Do (Safe)

```bash
terraform init      # Download providers locally
terraform validate  # Check syntax
terraform fmt       # Format code
terraform plan      # Generate execution plans
terraform show      # Display plans
```

## What You MUST NOT Do (Costs Money)

```bash
terraform apply     # ❌ NEVER RUN THIS
terraform destroy   # ❌ NOT NEEDED (nothing to destroy)
```

## Safety Measures Implemented

1. **Backend Configuration**: Commented out to prevent state management
2. **Lifecycle Prevent Destroy**: Added to critical resources
3. **Pre-commit Hook**: Blocks `terraform apply` commands
4. **CI/CD Check**: Pipeline fails if apply detected
5. **Documentation**: Clear warnings throughout

## If You Need a Live Demo

Instead of applying this Terraform:
1. Use the generated plan files in `snapshots/`
2. Run CostPilot CLI against plan JSONs
3. Review the walkthrough documentation
4. Watch the demo video (when available)

## Emergency: If Applied By Accident

```bash
# This will cost money, but less than leaving resources running
terraform destroy -auto-approve

# Then verify everything is gone
aws ec2 describe-instances --filters "Name=tag:Project,Values=costpilot-demo"
aws elbv2 describe-load-balancers --names costpilot-demo-alb
aws s3 ls | grep costpilot-demo
```

## Questions?

See: `docs/README.md` for safe demo alternatives.
