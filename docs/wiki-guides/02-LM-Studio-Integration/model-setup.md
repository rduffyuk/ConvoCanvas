---
date: 2025-09-14
source: Claude Code
category: Wiki-Guide
tags: [lm-studio, local-ai, models, librechat]
status: completed
priority: high
created: 2025-09-14 21:54:00
---

# LM Studio Integration & Model Setup

**Guide 2 of 6** | **Estimated Time:** 20-30 minutes
**Prerequisites:** LibreChat running, LM Studio installed, 16GB+ VRAM

## 🎯 What You'll Accomplish

By the end of this guide, you'll have:
- ✅ LM Studio configured for network access
- ✅ Local AI models loaded and running
- ✅ LibreChat connected to LM Studio
- ✅ Agent endpoints functioning properly

## 📋 Prerequisites Check

Before starting, verify you have:

```bash
# Check LM Studio installation
ls ~/.lmstudio/bin/lms || echo "❌ LM Studio not found"

# Check GPU memory (16GB+ recommended)
nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits

# Check LibreChat is running
curl -f http://localhost:3080 || echo "❌ Start LibreChat first"
```

## 🧠 Model Selection Guide

### Recommended Models by Hardware

**16GB VRAM:**
- `microsoft/Phi-3.5-mini-instruct` (7B) - Fast, efficient
- `microsoft/DialoGPT-medium` (774M) - Lightweight option

**24GB VRAM:**
- `meta-llama/Llama-2-13b-chat-hf` (13B) - Balanced performance
- `mistralai/Mistral-7B-Instruct-v0.3` (7B) - High quality

**32GB+ VRAM:**
- `meta-llama/Llama-2-70b-chat-hf` (70B) - Highest quality
- `mistralai/Mixtral-8x7B-Instruct-v0.1` (47B) - Expert mixture

## 🔧 LM Studio Configuration

### Network Access Setup

Configure LM Studio for Docker access:

```bash
# Create LM Studio config directory
mkdir -p ~/.lmstudio/.internal

# Configure network binding
cat > ~/.lmstudio/.internal/http-server-config.json << 'EOF'
{
  "networkInterface": "0.0.0.0",
  "port": 1234,
  "logLevel": "INFO",
  "enableCors": true,
  "corsOrigin": "*"
}
EOF
```

### Model Installation

Install your chosen models:

```bash
# Launch LM Studio
lms server start

# In LM Studio GUI:
# 1. Go to "Discover" tab
# 2. Search for recommended model
# 3. Click "Download"
# 4. Wait for completion
```

### Server Startup

Start the inference server:

```bash
# Start LM Studio server with network access
lms server start --port 1234 --host 0.0.0.0

# Or use GUI:
# 1. Go to "Local Server" tab
# 2. Select downloaded model
# 3. Click "Start Server"
# 4. Verify "Server Running" status
```

## 🔗 LibreChat Integration

### Environment Configuration

Add LM Studio configuration to LibreChat:

```bash
cd ~/librechat-deployment

# Add LM Studio settings to .env
cat >> .env << 'EOF'

# === LM Studio Integration ===
OPENAI_BASE_URL=http://host.docker.internal:1234/v1
OPENAI_API_KEY=lm-studio

# === Agent Configuration ===
AGENTS_ENDPOINT=true
AGENTS_API_KEY=lm-studio

EOF
```

### LibreChat Configuration

Create/update the LibreChat YAML config:

```bash
cat > config/librechat.yaml << 'EOF'
version: 1.2.8
cache: true

endpoints:
  # Local LM Studio Models
  custom:
    - name: "Local AI - Phi 3.5"
      baseURL: "http://host.docker.internal:1234/v1"
      apiKey: "lm-studio"
      models:
        default: ["phi-3.5-mini"]
        fetch: false
      titleConvo: true
      summarize: true
      titleModel: "phi-3.5-mini"
      summaryModel: "phi-3.5-mini"
      dropParams: ["stop"]

  # Agent Endpoints (requires base AI)
  agents:
    capabilities:
      - "web_search"
      - "execute_code"
      - "file_search"
    model: "phi-3.5-mini"
    baseURL: "http://host.docker.internal:1234/v1"
    apiKey: "lm-studio"

  # OpenAI endpoint pointing to LM Studio
  openAI:
    baseURL: "http://host.docker.internal:1234/v1"
    apiKey: "lm-studio"
    models:
      - "phi-3.5-mini"
    dropParams: ["stop"]
    titleConvo: true
    summarize: true
EOF
```

## 🚀 Service Restart and Testing

Restart LibreChat with new configuration:

```bash
# Restart LibreChat containers
docker-compose down
docker-compose up -d

# Check service status
docker-compose ps

# Check logs for errors
docker-compose logs api | grep -i error
```

## ✅ Verification Tests

Test your LM Studio integration:

```bash
# Test 1: LM Studio API accessibility
curl http://localhost:1234/v1/models | jq '.data[].id'

# Test 2: LibreChat can reach LM Studio
docker exec LibreChat curl -f http://host.docker.internal:1234/v1/models

# Test 3: Test basic chat completion
curl -X POST http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "phi-3.5-mini",
    "messages": [{"role": "user", "content": "Hello!"}],
    "max_tokens": 50
  }'
```

## 🌐 Web Interface Testing

1. **Open LibreChat** at `http://localhost:3080`
2. **Check available endpoints:**
   - "Custom" endpoint with your local models
   - "Agents" endpoint for advanced features
3. **Test basic functionality:**
   - Send simple message to local model ✅
   - Verify response generation ✅
   - Check model switching works ✅

## 🔧 Troubleshooting

### Common Issues

**Issue:** Models not appearing in LibreChat
```bash
# Check LM Studio server status
curl http://localhost:1234/v1/models

# Restart LM Studio server
pkill -f lms
lms server start --port 1234 --host 0.0.0.0
```

**Issue:** Agent endpoints not working
```bash
# Verify OpenAI endpoint configuration
grep -A 5 "openAI:" config/librechat.yaml

# Check Docker networking
docker exec LibreChat ping host.docker.internal
```

**Issue:** Out of VRAM errors
```bash
# Check GPU memory usage
nvidia-smi

# Switch to smaller model in LM Studio
# Recommended: Use quantized models (Q4_K_M)
```

**Issue:** Slow response times
```bash
# Optimize LM Studio settings:
# 1. Enable GPU acceleration
# 2. Adjust context length
# 3. Use appropriate quantization
# 4. Monitor system resources
```

## 📊 Performance Optimization

### LM Studio Settings

Optimize for your hardware:

```json
// In LM Studio GPU settings:
{
  "gpu_layers": -1,          // Use all GPU layers
  "context_length": 4096,    // Adjust based on use case
  "batch_size": 512,         // Balance speed vs memory
  "threads": 8               // Match CPU cores
}
```

### Model Selection Matrix

| VRAM | Recommended Model | Performance | Use Case |
|------|-------------------|-------------|----------|
| 8GB | Phi-3.5-mini Q4_K_M | Fast | General chat |
| 16GB | Llama-2-7B-chat Q4_K_M | Balanced | Most tasks |
| 24GB | Llama-2-13B-chat Q5_K_M | High quality | Complex reasoning |
| 32GB+ | Llama-2-70B-chat Q4_K_M | Highest quality | Professional use |

## 📈 Resource Monitoring

Create monitoring script:

```bash
cat > monitor-ai.sh << 'EOF'
#!/bin/bash
echo "🔍 AI System Monitor"
echo "==================="

echo "📊 GPU Status:"
nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits

echo -e "\n🖥️ LM Studio Process:"
ps aux | grep -v grep | grep lms || echo "Not running"

echo -e "\n🌐 LibreChat Status:"
curl -s http://localhost:3080 > /dev/null && echo "✅ LibreChat accessible" || echo "❌ LibreChat not accessible"

echo -e "\n🤖 Available Models:"
curl -s http://localhost:1234/v1/models | jq -r '.data[].id' 2>/dev/null || echo "❌ LM Studio not accessible"

echo -e "\n🔗 Network Test:"
docker exec -it LibreChat curl -s http://host.docker.internal:1234/v1/models > /dev/null && echo "✅ Docker → LM Studio OK" || echo "❌ Docker → LM Studio failed"
EOF

chmod +x monitor-ai.sh
./monitor-ai.sh
```

## ✅ Completion Checklist

Mark each item when completed:

- [ ] LM Studio installed and configured
- [ ] Network access enabled (0.0.0.0:1234)
- [ ] At least one model downloaded and loaded
- [ ] LibreChat configuration updated
- [ ] Docker containers restarted
- [ ] Local models appear in LibreChat interface
- [ ] Agent endpoints functioning
- [ ] Performance monitoring active
- [ ] Troubleshooting script ready

## ⏭️ Next Steps

Once local AI models are running:

1. **[[03-Web-Search-Integration/serper-api-setup.md]]** - Add web search capabilities
2. Configure multiple models for different tasks
3. Set up model switching automation

## 💾 Model Management

```bash
# List downloaded models
ls ~/.lmstudio/models/

# Check model sizes
du -h ~/.lmstudio/models/*

# Clean up unused models
# Use LM Studio GUI: Models → Manage → Delete unused

# Backup model configurations
cp ~/.lmstudio/.internal/http-server-config.json backup/
```

---

**🎉 Success!** Local AI models are now integrated with LibreChat.

**Estimated completion time:** 20-30 minutes
**Next guide:** Web Search Integration