# Contributing to CostPilot Demo

This repository is the **canonical demonstration environment** for CostPilot. All changes must maintain deterministic, reproducible outputs.

## 🔒 Protected Files

The following files are **protected by CI** and should NOT be modified directly:

- `snapshots/*` - Canonical cost analysis outputs
- `costpilot_artifacts/*` - CI/CD pipeline outputs  
- `video_assets/*` - Launch and marketing assets

To update these files, use `./tools/reset_demo.sh`.

## ✅ Allowed Changes

You may modify:

- `infrastructure/terraform/pr-change/*` - PR regression scenarios
- `README.md` - Documentation updates
- `costpilot.yml` - Configuration adjustments
- `scripts/*` - Helper scripts
- `tools/*` - Automation tools

## 🔄 Workflow

1. Fork the repository
2. Create a feature branch
3. Make changes following deterministic constraints
4. Run validation: `./scripts/validate_mapping.sh && ./scripts/validate_trend.sh`
5. Submit PR

## 📏 Requirements

- Terraform >= 1.6
- Python 3.x
- Bash shell
- Git

## 🔐 Deterministic Constraints

All outputs must be:

- **Hash-stable**: Same inputs → same outputs
- **Float precision**: Fixed to 2 decimal places
- **Whitespace normalized**: Consistent formatting
- **Ordering enforced**: Predictable sequence

## 🧪 Testing

Before submitting:

```bash
# Validate mapping
./scripts/validate_mapping.sh

# Validate trend  
./scripts/validate_trend.sh

# Verify hashes
./scripts/verify_hashes.sh

# Update progress
python3 tools/update_progress.py
```

## 📝 Commit Messages

Follow conventional commits:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `chore:` - Maintenance tasks
- `test:` - Test additions

## 🎯 Scenario Version

Current: **v1**

Any breaking changes require new scenario version.

## 📞 Questions?

See [README.md](./README.md) or [docs/walkthrough.md](./docs/walkthrough.md).
