# LibreChat + ConvoCanvas Integration Guide

**Transform your AI conversations into organized, persistent knowledge**

## 🎯 What This Integration Provides

- **Local AI Models**: Run AI entirely on your hardware (LM Studio + LibreChat)
- **Perplexity-Style Search**: Real-time web search with citations
- **Automatic Organization**: Conversations auto-archived to Obsidian
- **Persistent Context**: Maintain project context across multiple sessions
- **Knowledge Management**: Searchable history with smart tagging

## 🏗️ Architecture Overview

```
User → LibreChat → LM Studio (Local AI)
  ↓        ↓         ↓
Web Search → Response → Auto Documentation
  ↓                    ↓
Obsidian Vault ← ConvoCanvas Processing
```

## 📋 Quick Setup Checklist

### **Prerequisites**
- [ ] Docker and Docker Compose installed
- [ ] 16GB+ RAM (32GB recommended)
- [ ] RTX 4080+ or equivalent GPU (16GB+ VRAM)
- [ ] LM Studio downloaded and installed

### **Step 1: Clone and Setup**
```bash
# Clone ConvoCanvas repository
git clone https://github.com/rduffyuk/ConvoCanvas.git
cd ConvoCanvas

# Copy integration files
cp -r integrations/librechat/* ~/librechat-deployment/
```

### **Step 2: Configure LM Studio**
```bash
# Enable network access for Docker
mkdir -p ~/.lmstudio/.internal
cat > ~/.lmstudio/.internal/http-server-config.json << 'EOF'
{
  "networkInterface": "0.0.0.0",
  "port": 1234
}
EOF
```

### **Step 3: Environment Setup**
```bash
# Copy environment template
cp templates/librechat/env.template .env

# Generate secure keys
echo "JWT_SECRET=$(openssl rand -hex 64)" >> .env
echo "JWT_REFRESH_SECRET=$(openssl rand -hex 64)" >> .env
echo "CREDS_KEY=$(openssl rand -hex 32)" >> .env
echo "CREDS_IV=$(openssl rand -hex 16)" >> .env

# Add your Serper API key for web search
read -p "Enter Serper API key: " SERPER_KEY
sed -i "s/YOUR_SERPER_API_KEY_HERE/$SERPER_KEY/" .env
```

### **Step 4: LibreChat Configuration**
```bash
# Copy configuration template
cp templates/librechat/librechat.template.yaml config/librechat.yaml

# Edit with your preferred model names
nano config/librechat.yaml
```

### **Step 5: Deploy Stack**
```bash
# Start all services
docker-compose -f docker-compose-complete.yml up -d

# Verify services are running
docker-compose ps
```

## 🔍 Verification Tests

### **Test 1: Basic AI Functionality**
1. Open http://localhost:3080
2. Create account (first user becomes admin)
3. Select "Local AI + Search" endpoint
4. Send test message → Should get response from local model

### **Test 2: Web Search Integration**
1. Select "Agents" endpoint
2. Click search button or ask "search for docker networking"
3. Verify search results with citations appear

### **Test 3: File Access**
1. Ask AI to "analyze my project files"
2. Verify AI can access mounted directories
3. Test file content summarization

## 🤖 Automation Setup

### **Install ConvoCanvas Scripts**
```bash
# Copy automation scripts
cp -r automation/obsidian-organizer/* /path/to/your/scripts/

# Make executable
chmod +x /path/to/your/scripts/*.sh

# Setup cron job for daily organization
crontab -e
# Add: 0 2 * * * /path/to/your/scripts/obsidian-universal-organizer.sh
```

### **Configure Obsidian Integration**
1. Mount your Obsidian vault to LibreChat (read-only)
2. Configure output directory for processed conversations
3. Run universal tagger for existing files

## 📊 Expected Results

### **After Setup**
- ✅ Local AI models responding in LibreChat
- ✅ Web search working with citations
- ✅ File access functional
- ✅ Conversations being auto-archived
- ✅ Smart tagging and organization active

### **Daily Workflow**
1. **Morning**: Review auto-generated summaries
2. **Work**: Use LibreChat with full context retention
3. **Evening**: Automation organizes and tags new conversations

## 🔧 Customization Options

### **Model Selection**
- Edit `config/librechat.yaml` to change models
- Adjust LM Studio settings for performance
- Configure multiple models for different tasks

### **Organization Patterns**
- Modify automation scripts for your folder structure
- Customize tagging patterns in Python scripts
- Adjust date-based organization preferences

### **Search Configuration**
- Fine-tune Serper API settings
- Adjust citation formatting
- Configure result limits and filtering

## 🐛 Troubleshooting

### **Common Issues**

**LibreChat can't reach LM Studio**
```bash
# Verify LM Studio network config
curl http://localhost:1234/v1/models

# Check Docker networking
docker exec LibreChat curl http://host.docker.internal:1234/v1/models
```

**Search not working**
```bash
# Test Serper API key
curl -X POST "https://google.serper.dev/search" \
  -H "X-API-KEY: YOUR_KEY" \
  -d '{"q": "test"}'
```

**File access denied**
```bash
# Fix permissions
sudo chown -R $USER:$USER ./uploads ./logs
chmod -R 755 ./uploads ./logs
```

## 📈 Performance Optimization

### **Hardware Recommendations**
- **Minimum**: 16GB RAM, RTX 4070, 500GB storage
- **Recommended**: 32GB RAM, RTX 4080+, 1TB+ NVMe
- **Optimal**: 64GB RAM, RTX 4090, 2TB+ NVMe

### **Model Selection Guide**
| VRAM | Recommended Model | Performance |
|------|-------------------|-------------|
| 8GB  | Phi-3.5-mini Q4_K_M | Fast |
| 16GB | Llama-2-7B-chat Q4_K_M | Balanced |
| 24GB | Llama-2-13B-chat Q5_K_M | High |
| 32GB+ | Llama-2-70B-chat Q4_K_M | Highest |

## 📚 Additional Resources

- **Complete Setup Guides**: See `/docs/wiki-guides/`
- **Automation Scripts**: See `/automation/obsidian-organizer/`
- **Configuration Templates**: See `/templates/`
- **Real-World Examples**: See `/examples/`

---

**Result**: A complete AI automation system that maintains context, organizes knowledge, and works entirely offline for sensitive tasks.**