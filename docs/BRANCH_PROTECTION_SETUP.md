# Branch Protection Setup Guide

This guide explains how to configure GitHub branch protection rules for the `main` branch to ensure the demo repository remains stable and drift-free.

## Why Branch Protection?

Branch protection rules prevent accidental modifications to:
- Snapshot files (`snapshots/*`)
- Artifacts (`costpilot_artifacts/*`)
- Video assets (`video_assets/*`)
- Critical documentation

## Setup Options

### Option 1: GitHub Web UI (Recommended)

1. **Navigate to Repository Settings**
   - Go to: https://github.com/Dee66/costpilotdemo/settings/branches

2. **Add Branch Protection Rule**
   - Click "Add rule" or "Add branch protection rule"
   - Branch name pattern: `main`

3. **Configure Protection Settings**

   ✅ **Required checks:**
   - ☑ Require a pull request before merging
   - ☑ Require status checks to pass before merging
     - Select: `terraform-validate`
     - Select: `costpilot-detect`
     - Select: `costpilot-predict`
     - Select: `costpilot-explain`
     - Select: `verify-snapshots`
     - Select: `verify-hashes`
   - ☑ Require conversation resolution before merging

   ✅ **Additional protections:**
   - ☑ Do not allow bypassing the above settings
   - ☑ Restrict who can push to matching branches
   - ☑ Require linear history
   - ☑ Include administrators (optional, for maximum safety)

4. **Save Changes**
   - Click "Create" or "Save changes"

### Option 2: GitHub CLI

If you have GitHub CLI installed (`gh`):

```bash
gh api repos/Dee66/costpilotdemo/branches/main/protection \
  --method PUT \
  --field required_pull_request_reviews[required_approving_review_count]=1 \
  --field required_status_checks[strict]=true \
  --field required_status_checks[contexts][]=terraform-validate \
  --field required_status_checks[contexts][]=costpilot-detect \
  --field required_status_checks[contexts][]=costpilot-predict \
  --field required_status_checks[contexts][]=costpilot-explain \
  --field required_status_checks[contexts][]=verify-snapshots \
  --field required_status_checks[contexts][]=verify-hashes \
  --field enforce_admins=true \
  --field required_linear_history=true \
  --field allow_force_pushes=false \
  --field allow_deletions=false
```

### Option 3: GitHub API (Script)

Save this script as `tools/setup_branch_protection.sh`:

```bash
#!/bin/bash
set -euo pipefail

REPO_OWNER="Dee66"
REPO_NAME="costpilotdemo"
BRANCH="main"

# Requires GITHUB_TOKEN environment variable
if [ -z "${GITHUB_TOKEN:-}" ]; then
  echo "Error: GITHUB_TOKEN environment variable not set"
  echo "Create a token at: https://github.com/settings/tokens"
  echo "Required scopes: repo"
  exit 1
fi

curl -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/branches/$BRANCH/protection" \
  -d '{
    "required_status_checks": {
      "strict": true,
      "contexts": [
        "terraform-validate",
        "costpilot-detect",
        "costpilot-predict",
        "costpilot-explain",
        "verify-snapshots",
        "verify-hashes"
      ]
    },
    "enforce_admins": true,
    "required_pull_request_reviews": {
      "required_approving_review_count": 1,
      "dismiss_stale_reviews": true
    },
    "restrictions": null,
    "required_linear_history": true,
    "allow_force_pushes": false,
    "allow_deletions": false
  }'

echo "✅ Branch protection configured for $BRANCH"
```

Then run:
```bash
export GITHUB_TOKEN="your_github_token_here"
bash tools/setup_branch_protection.sh
```

## Verification

After configuring, verify the protection is active:

```bash
# Using GitHub CLI
gh api repos/Dee66/costpilotdemo/branches/main/protection

# Or visit:
# https://github.com/Dee66/costpilotdemo/settings/branches
```

You should see:
- ✅ "Protected" label on the main branch
- ✅ Required status checks listed
- ✅ PR reviews required
- ✅ Force push disabled

## Protected Paths (via CI)

The CI pipeline (`.github/workflows/costpilot-ci.yml`) enforces additional file-level protections:

```yaml
# Blocks updates to:
- snapshots/**
- costpilot_artifacts/**
- video_assets/**

# Allows changes to:
- infrastructure/terraform/pr-change/**
- README.md
- costpilot.yml
```

## Testing Protection

To verify protection is working:

1. Create a test branch:
   ```bash
   git checkout -b test/branch-protection
   ```

2. Make a change to a protected file:
   ```bash
   echo "test" >> snapshots/detect_v1.json
   git add snapshots/detect_v1.json
   git commit -m "Test: attempt to modify snapshot"
   git push origin test/branch-protection
   ```

3. Open a PR to `main`

4. Expected result:
   - ❌ CI check `verify-snapshots` should FAIL
   - ❌ PR cannot be merged
   - ✅ Protection working correctly

5. Clean up:
   ```bash
   git checkout main
   git branch -D test/branch-protection
   git push origin --delete test/branch-protection
   ```

## Troubleshooting

### "Status checks not found"
The CI workflow must run at least once before status checks can be required. Push a commit or manually trigger the workflow.

### "Not authorized to configure protection"
You need admin access to the repository. Contact the repository owner or use a personal access token with `repo` scope.

### "Linear history conflicts"
If you have existing merge commits, you may need to disable this option or rebase existing branches.

## Related Documentation

- [GitHub Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub API - Branch Protection](https://docs.github.com/en/rest/branches/branch-protection)
- [CI Workflow](../.github/workflows/costpilot-ci.yml)
- [Safeguards Documentation](../SAFEGUARDS.md)

## Notes

- Branch protection is a **repository-level** setting
- Changes are immediate and affect all future PRs
- Existing PRs may need to be re-opened to pick up new rules
- Consider enabling "Include administrators" for maximum safety (prevents even repo admins from bypassing rules)

---

**Status:** Ready to configure  
**Priority:** Medium (safeguard feature, not blocking for demo functionality)  
**Required Access:** Repository admin or GitHub token with `repo` scope
