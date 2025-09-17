# Unleash Feature Flag Integration Guide

## 🎯 Why Unleash?

Unleash is an open-source feature management platform perfect for ConvoCanvas:
- **Free tier**: 2 environments, unlimited flags
- **Self-hosted option**: Keep control of your data
- **Python SDK**: First-class support
- **10k+ GitHub stars**: Trusted by community

## 📦 Installation Options

### Option 1: Docker (Recommended for Development)
```bash
# Clone Unleash
git clone https://github.com/Unleash/unleash.git
cd unleash

# Start with Docker Compose
docker compose up -d

# Access at http://localhost:4242
# Default admin: admin/unleash4all
```

### Option 2: Unleash Cloud (Free Tier)
1. Sign up at https://www.getunleash.io
2. Create project
3. Get API tokens

## 🔧 Python Integration

### Install SDK
```bash
pip install UnleashClient
```

### Basic Setup
```python
from UnleashClient import UnleashClient

# Initialize client
client = UnleashClient(
    url="http://localhost:4242/api",
    app_name="convocanvas",
    environment="development",
    custom_headers={'Authorization': 'your-api-token'}
)

# Start client
client.initialize_client()

# Check feature
if client.is_enabled("gpu_acceleration"):
    # Use GPU features
    pass
```

### Integration with ConvoCanvas

```python
# backend/app/core/unleash_flags.py
from UnleashClient import UnleashClient
import os

class UnleashFeatureFlags:
    def __init__(self):
        self.client = UnleashClient(
            url=os.getenv("UNLEASH_URL", "http://localhost:4242/api"),
            app_name="convocanvas",
            environment=os.getenv("ENVIRONMENT", "development"),
            custom_headers={'Authorization': os.getenv("UNLEASH_API_TOKEN", "")}
        )
        self.client.initialize_client()

    def is_enabled(self, feature: str, context: dict = None) -> bool:
        """Check if feature is enabled"""
        return self.client.is_enabled(feature, context)

    def get_variant(self, feature: str) -> dict:
        """Get feature variant for A/B testing"""
        return self.client.get_variant(feature)
```

## 🚀 ConvoCanvas Feature Flags

### Proposed Flags Structure
```yaml
# GPU Features
gpu_acceleration:
  description: "Enable GPU processing for high-end cards"
  type: release
  strategies:
    - name: userWithId
      parameters:
        userIds: "beta-testers"
    - name: gradualRolloutRandom
      parameters:
        percentage: 10

# Enhanced Analysis
enhanced_analysis:
  description: "NLP-powered content extraction"
  type: experiment
  strategies:
    - name: default
      parameters:
        enabled: true

# Local AI
local_ai_integration:
  description: "LM Studio and Ollama support"
  type: permission
  strategies:
    - name: userWithId
      parameters:
        userIds: "power-users"
```

## 📊 Benefits for ConvoCanvas

1. **Gradual Rollout**: Test GPU features with specific users
2. **Kill Switch**: Disable problematic features instantly
3. **A/B Testing**: Compare analysis algorithms
4. **User Targeting**: Enable features for beta testers
5. **No Redeploy**: Change flags without pushing code

## 🔄 Migration Path

### Phase 1: Current (Simple Flags)
```python
# Current implementation in feature_flags.py
if os.getenv("ENABLE_GPU", "false") == "true":
    # Use GPU
```

### Phase 2: Unleash Integration
```python
# Future with Unleash
if unleash.is_enabled("gpu_acceleration", {"userId": user_id}):
    # Use GPU
```

## 📈 Dashboard Features

Unleash provides:
- Real-time feature status
- Usage metrics
- Rollout history
- User segments
- A/B test results

## 🔐 Security Considerations

1. **API Tokens**: Store in environment variables
2. **Network**: Use HTTPS in production
3. **Self-host**: For sensitive deployments
4. **Audit Log**: Track all flag changes

## 📝 Environment Variables

Add to `.env`:
```bash
# Unleash Configuration
UNLEASH_URL=http://localhost:4242/api
UNLEASH_API_TOKEN=*:development.your-token-here
UNLEASH_ENVIRONMENT=development
```

## 🎯 Next Steps

1. **Local Testing**: Set up Unleash locally with Docker
2. **Create Flags**: Define ConvoCanvas feature flags
3. **Update Code**: Replace env vars with Unleash checks
4. **Monitor**: Use dashboard to track feature usage

## 🔗 Resources

- [Unleash Docs](https://docs.getunleash.io/)
- [Python SDK Guide](https://docs.getunleash.io/feature-flag-tutorials/python)
- [Best Practices](https://docs.getunleash.io/topics/best-practices)
- [GitHub Repo](https://github.com/Unleash/unleash)