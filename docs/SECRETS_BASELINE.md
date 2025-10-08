# 🔐 Understanding .secrets.baseline

## What is it?

`.secrets.baseline` is a security configuration file used by the **detect-secrets** pre-commit hook to prevent accidentally committing sensitive information (passwords, API keys, tokens) to your repository.

## Quick Summary

**Purpose:** Prevent secret leaks
**How:** Scans code for potential secrets before commit
**Result:** Blocks commits containing new secrets

## How It Works

```
You commit code
    ↓
detect-secrets hook runs
    ↓
Scans for potential secrets (AWS keys, passwords, etc.)
    ↓
Compares findings with .secrets.baseline
    ↓
New secret found? → ❌ Commit BLOCKED
Matches baseline? → ✅ Commit ALLOWED
```

## What Gets Detected

The tool scans for:

- ✅ **AWS Keys** - `AKIAIOSFODNN7EXAMPLE` # pragma: allowlist secret
- ✅ **API Tokens** - `ghp_1234567890abcdef` # pragma: allowlist secret
- ✅ **Private Keys** - `-----BEGIN RSA PRIVATE KEY-----` # pragma: allowlist secret
- ✅ **JWT Tokens** - JSON Web Tokens
- ✅ **Passwords** - In variable names or values
- ✅ **Database URLs** - `postgres://user:pass@host/db` # pragma: allowlist secret
- ✅ **High Entropy Strings** - Random-looking strings
- ✅ **Basic Auth** - `username:password` patterns # pragma: allowlist secret

## File Structure

```json
{
  "version": "1.4.0",
  "plugins_used": [
    {"name": "AWSKeyDetector"},
    {"name": "PrivateKeyDetector"},
    {"name": "Base64HighEntropyString", "limit": 4.5}
  ],
  "results": {},  // Approved exceptions go here
  "generated_at": "2024-01-01T00:00:00Z"
}
```

## Example: What Gets Blocked

### ❌ Would Be Blocked

```python
# Real credentials - BLOCKED!
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" # pragma: allowlist secret
GITHUB_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuv" # pragma: allowlist secret
DATABASE_URL = "postgres://admin:secret123@localhost/prod" # pragma: allowlist secret
API_KEY = "sk-proj-abc123realkey456" # pragma: allowlist secret
```

### ✅ Safe Patterns

```python
# Using environment variables - SAFE
API_KEY = os.getenv("API_KEY")
PASSWORD = os.environ["PASSWORD"]

# Placeholders - SAFE
API_KEY = "YOUR_API_KEY_HERE"
TOKEN = "<your-token>"

# Test mocks (in baseline) - SAFE
MOCK_KEY = "test-key-not-real"  # Added to baseline # pragma: allowlist secret
```

## Common Use Cases

### 1. Test Credentials

```python
# tests/conftest.py
# NOTE: This is a test key, not real
TEST_API_KEY = "test-key-12345"  # Added to baseline # pragma: allowlist secret
```

### 2. Documentation Examples

```python
# docs/examples/auth.py
# Example (not a real key):
AWS_KEY = "AKIAIOSFODNN7EXAMPLE"  # In baseline # pragma: allowlist secret
```

### 3. Demo/Public Keys

```python
# config/demo.py
DEMO_TOKEN = "demo-token-abc123"  # Safe in baseline # pragma: allowlist secret
```

## Managing the Baseline

### Update Baseline

When you add new safe credentials:

```bash
# Scan and update baseline
detect-secrets scan --baseline .secrets.baseline
```

### Audit Baseline

Review what's approved:

```bash
# View entries
cat .secrets.baseline | jq '.results'

# Interactive audit
detect-secrets audit .secrets.baseline
```

### Regenerate Baseline

Start fresh:

```bash
# Regenerate from scratch
detect-secrets scan > .secrets.baseline
```

## Best Practices

### ✅ DO

```python
# Use environment variables
API_KEY = os.getenv("API_KEY")

# Use .env files (gitignored)
from dotenv import load_dotenv
load_dotenv()

# Document test keys clearly
TEST_KEY = "test-abc-123"  # Not a real key
```

### ❌ DON'T

```python
# Never commit real secrets
API_KEY = "sk-real-secret-key"  # BAD! # pragma: allowlist secret

# Don't hardcode passwords
PASSWORD = "myPassword123"  # BAD! # pragma: allowlist secret

# Don't commit .env files
# Add .env to .gitignore!
```

## Workflow Example

```bash
# 1. Add code with test key
echo 'TEST_KEY = "test-123"' > test.py # pragma: allowlist secret

# 2. Try to commit
git add test.py
git commit -m "add test"

# 3. detect-secrets runs automatically
# Output: ❌ Potential secret detected: TEST_KEY

# 4. If it's safe, add to baseline
detect-secrets scan --baseline .secrets.baseline

# 5. Commit again
git add .secrets.baseline test.py
git commit -m "add test with baseline"
# Output: ✅ Commit allowed
```

## Emergency Bypass

**Only use in genuine emergencies:**

```bash
# Skip detect-secrets once
SKIP=detect-secrets git commit -m "emergency fix"

# Or skip all hooks
git commit --no-verify -m "emergency"
```

⚠️ **Warning:** Review and fix immediately after!

## Troubleshooting

### False Positive Won't Clear

```bash
# Regenerate baseline, excluding certain files
detect-secrets scan --baseline .secrets.baseline \
  --exclude-files '.*\.json$'
```

### Too Many False Positives

Adjust sensitivity in `.pre-commit-config.yaml`:

```yaml
- id: detect-secrets
  args: [
    '--baseline', '.secrets.baseline',
    '--base64-limit', '5.0'  # Higher = less strict
  ]
```

### Remove Entry from Baseline

```bash
# Option 1: Edit .secrets.baseline manually
# Remove entry from "results" section

# Option 2: Regenerate
detect-secrets scan > .secrets.baseline
```

## Security Benefits

1. 🛡️ **Prevents leaks** - Catches secrets before they reach GitHub
2. ⚡ **Early detection** - Finds issues locally, not in production
3. 👥 **Team protection** - All team members' commits are checked
4. 📝 **Audit trail** - Baseline documents approved exceptions
5. 🔄 **CI/CD integration** - Same checks locally and in CI

## Integration

This file works with the pre-commit hook in [.pre-commit-config.yaml](../.pre-commit-config.yaml):

```yaml
- repo: https://github.com/Yelp/detect-secrets
  rev: v1.4.0
  hooks:
    - id: detect-secrets
      args: ['--baseline', '.secrets.baseline']
```

## Resources

- [detect-secrets on GitHub](https://github.com/Yelp/detect-secrets)
- [Pre-commit Hooks Guide](PRE_COMMIT_GUIDE.md)
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

---

**Summary:** `.secrets.baseline` is your first line of defense against accidentally committing secrets to version control. It works automatically with pre-commit hooks to keep your repository secure. 🔐
