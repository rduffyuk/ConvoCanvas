# 🔒 Private Repository Setup Guide

## Two-Repo Strategy for ConvoCanvas

### 🌍 Public Repo: `convocanvas`
**Purpose**: Portfolio, sharing, community
- Clean, documented code
- Example configurations
- No sensitive data
- Good for social media sharing

### 🔐 Private Repo: `convocanvas-private`
**Purpose**: Personal use, sensitive configs
- API keys and tokens
- Work-specific customizations
- Experimental features
- Internal documentation

## Setup Instructions

### 1. Create Private Repo
```bash
# Create new private repo on GitHub
gh repo create convocanvas-private --private --clone

# Or create locally and push
git init convocanvas-private
cd convocanvas-private
git remote add origin git@github.com:rduffyuk/convocanvas-private.git
```

### 2. Link Public and Private
```bash
# In private repo, add public as upstream
cd convocanvas-private
git remote add public https://github.com/rduffyuk/convocanvas.git

# Pull public changes
git pull public main

# Your remotes:
# - origin: private repo (push sensitive)
# - public: public repo (pull updates)
```

### 3. File Structure
```
convocanvas-private/
├── .env                    # Real secrets (never commit)
├── .env.private           # Private configs (can commit)
├── configs/               # Private configurations
│   ├── api-keys.json
│   └── work-specific.yaml
├── experiments/           # Personal experiments
├── docs-internal/         # Private documentation
└── scripts-private/       # Custom automation
```

### 4. Sync Strategy

#### Pull from public:
```bash
# Get latest public changes
git pull public main

# Resolve conflicts keeping private changes
git checkout --ours .env
git checkout --ours configs/
```

#### Push to public (selective):
```bash
# Cherry-pick safe commits
git cherry-pick <commit-hash>

# Or create patch
git format-patch -1 <commit>
# Apply in public repo
git am < patch-file
```

### 5. Git Workflow

```bash
# Daily workflow
cd convocanvas          # Public work
git add -A
git commit -m "feat: shareable feature"
git push origin main

cd ../convocanvas-private  # Private work
git add configs/
git commit -m "config: update API keys"
git push origin main
```

## Security Checklist

### Before Public Commit:
- [ ] No API keys or tokens
- [ ] No internal URLs
- [ ] No work-specific details
- [ ] No customer/client data
- [ ] .gitignore properly configured

### Private Repo Only:
- [ ] .env with real values
- [ ] Production configs
- [ ] Internal documentation
- [ ] Work experiments
- [ ] Customer-specific code

## .gitignore for Both

```gitignore
# Always ignore
.env
.env.local
*.key
*.pem
*.cert

# Private repo can commit these
.env.private
configs/private/
docs-internal/
```

## Quick Commands

```bash
# Check what's being committed
git status
git diff --staged

# Verify no secrets
git grep -E "api_key|secret|token|password"

# Safe commit to public
git add -A
git commit -m "feat: public feature"
git push origin main

# Private commit
cd ../convocanvas-private
git add .
git commit -m "private: internal update"
git push origin main
```