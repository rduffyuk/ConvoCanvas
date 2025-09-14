---
date: 2025-09-14
source: Claude Code
category: Wiki-Guide
tags: [serper-api, web-search, perplexity, librechat]
status: completed
priority: high
created: 2025-09-14 21:55:00
---

# Web Search Integration with Serper API

**Guide 3 of 6** | **Estimated Time:** 15-20 minutes
**Prerequisites:** LibreChat with LM Studio running, Serper API account

## 🎯 What You'll Accomplish

By the end of this guide, you'll have:
- ✅ Serper API configured for web search
- ✅ Perplexity-style search interface in LibreChat
- ✅ Real-time search results with citations
- ✅ Agent endpoints with web search capabilities

## 📋 Prerequisites Check

Before starting, verify you have:

```bash
# Check LibreChat and LM Studio are running
curl -f http://localhost:3080 && curl -f http://localhost:1234/v1/models
echo $? # Should return 0 if both accessible

# Check agent endpoints are configured
docker logs LibreChat 2>&1 | grep -i "agents endpoint" || echo "⚠️ Configure agents first"
```

## 🔑 Serper API Setup

### Account Creation

1. **Visit Serper.dev**
   - Go to https://serper.dev
   - Click "Sign Up" / "Get Started"
   - Create account with email

2. **API Key Generation**
   - Navigate to Dashboard
   - Click "API Keys" section
   - Generate new API key
   - Copy key securely (format: `abc123...xyz789`)

3. **Pricing Overview**
   - **Free Tier:** 2,500 requests/month
   - **Paid Plans:** Starting at $5/month
   - **Rate Limits:** 100 requests/minute

### Environment Configuration

Add Serper API key to LibreChat:

```bash
cd ~/librechat-deployment

# Add Serper configuration to .env
cat >> .env << 'EOF'

# === Web Search Configuration ===
SERPER_API_KEY=YOUR_SERPER_API_KEY_HERE
SEARCH_ENABLED=true
ENABLE_WEB_SEARCH=true

# === Search Provider Settings ===
GOOGLE_SEARCH_API_KEY=USE_SERPER_INSTEAD
GOOGLE_CSE_ID=USE_SERPER_INSTEAD

EOF

# Replace placeholder with actual key
read -p "Enter your Serper API key: " SERPER_KEY
sed -i "s/YOUR_SERPER_API_KEY_HERE/$SERPER_KEY/" .env
```

## ⚙️ LibreChat Search Configuration

### Enhanced YAML Configuration

Update LibreChat configuration for search:

```bash
cat > config/librechat.yaml << 'EOF'
version: 1.2.8
cache: true

endpoints:
  # Local LM Studio Models with Search
  custom:
    - name: "Local AI + Search"
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
      # Enable search for this endpoint
      tools: true
      search: true

  # Agent Endpoints with Full Capabilities
  agents:
    capabilities:
      - "web_search"      # Enable web search
      - "execute_code"    # Code execution
      - "file_search"     # Local file search
    model: "phi-3.5-mini"
    baseURL: "http://host.docker.internal:1234/v1"
    apiKey: "lm-studio"
    # Search configuration
    tools: true
    search: true

  # OpenAI endpoint for agents
  openAI:
    baseURL: "http://host.docker.internal:1234/v1"
    apiKey: "lm-studio"
    models:
      - "phi-3.5-mini"
    dropParams: ["stop"]
    titleConvo: true
    summarize: true

# Global search settings
search:
  provider: "serper"
  api_key: "${SERPER_API_KEY}"
  # Search result configuration
  num_results: 10
  safe_search: "moderate"
  country: "us"
  language: "en"
  # Citation formatting
  include_citations: true
  citation_style: "numbered"
EOF
```

## 🚀 Service Configuration and Restart

Apply the new search configuration:

```bash
# Restart LibreChat with search capabilities
docker-compose down
docker-compose up -d

# Verify containers started successfully
docker-compose ps

# Check for search-related logs
docker-compose logs api | grep -i -E "(search|serper|web)" | head -10
```

## ✅ Search Functionality Testing

### API-Level Testing

Test Serper API directly:

```bash
# Test Serper API access
SERPER_KEY=$(grep SERPER_API_KEY .env | cut -d'=' -f2)
curl -X POST "https://google.serper.dev/search" \
  -H "X-API-KEY: $SERPER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "artificial intelligence 2024"}' | jq '.organic[0:3]'
```

### LibreChat Interface Testing

1. **Access LibreChat** at `http://localhost:3080`

2. **Test Web Search Button:**
   - Navigate to "Agents" endpoint
   - Look for 🔍 search icon/button
   - Click search button and enter query
   - Verify search results appear with citations

3. **Test Natural Search Queries:**
   - Type: "search for latest AI news"
   - Type: "find information about docker networking"
   - Verify automatic search triggering

## 🎨 Perplexity-Style Interface

### Search Result Formatting

The configuration provides Perplexity-like features:

- **Numbered Citations**: `[1] [2] [3]` in responses
- **Source Links**: Direct links to original content
- **Search Snippets**: Relevant text excerpts
- **Real-time Results**: Current web information

### Example Search Response Format

```
Based on my search, here's what I found about Docker networking:

Docker provides several networking options for containers [1]. The default bridge network allows containers to communicate with each other [2]. For production deployments, custom networks offer better isolation and security [3].

**Sources:**
[1] Docker Official Documentation - Container Networking
[2] Docker Network Bridge Tutorial
[3] Production Docker Networking Best Practices
```

## 🔧 Advanced Configuration

### Search Optimization Settings

Fine-tune search behavior:

```bash
# Add advanced search settings to .env
cat >> .env << 'EOF'

# === Advanced Search Settings ===
SEARCH_MAX_RESULTS=15
SEARCH_TIMEOUT=10000
SEARCH_CONCURRENT_REQUESTS=3
SEARCH_CACHE_TTL=3600

# === Citation Configuration ===
CITATION_MAX_LENGTH=200
CITATION_INCLUDE_DOMAIN=true
CITATION_NUMBERED_FORMAT=true

EOF
```

### Custom Search Prompts

Optimize search integration with custom prompts:

```yaml
# Add to librechat.yaml under search section
search:
  provider: "serper"
  api_key: "${SERPER_API_KEY}"
  # Custom search prompts
  search_prompt: |
    When searching for information, prioritize:
    1. Recent and authoritative sources
    2. Technical documentation when relevant
    3. Multiple perspectives on the topic

  citation_prompt: |
    Format citations as:
    [1] Source Title - Domain.com
    Include relevant snippets with proper attribution.
```

## 📊 Search Performance Monitoring

Create search monitoring script:

```bash
cat > monitor-search.sh << 'EOF'
#!/bin/bash
echo "🔍 Search System Monitor"
echo "======================="

# Check Serper API quota
SERPER_KEY=$(grep SERPER_API_KEY ~/librechat-deployment/.env | cut -d'=' -f2)
echo "📈 API Status:"
curl -s -X POST "https://google.serper.dev/search" \
  -H "X-API-KEY: $SERPER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "test"}' > /dev/null && echo "✅ Serper API accessible" || echo "❌ Serper API error"

echo -e "\n🌐 LibreChat Search:"
docker logs LibreChat 2>&1 | grep -i "search enabled" | tail -1 || echo "⚠️ Search status unclear"

echo -e "\n🔄 Recent Search Activity:"
docker logs LibreChat 2>&1 | grep -i "web.search" | tail -3

echo -e "\n📊 Search Configuration:"
grep -E "(SEARCH|SERPER)" ~/librechat-deployment/.env | head -5
EOF

chmod +x monitor-search.sh
./monitor-search.sh
```

## 🔧 Troubleshooting

### Common Issues

**Issue:** Search button not appearing
```bash
# Check agents endpoint configuration
grep -A 10 "agents:" config/librechat.yaml

# Verify capabilities include web_search
grep -A 5 "capabilities:" config/librechat.yaml
```

**Issue:** "Search failed" errors
```bash
# Test API key validity
SERPER_KEY=$(grep SERPER_API_KEY .env | cut -d'=' -f2)
curl -X POST "https://google.serper.dev/search" \
  -H "X-API-KEY: $SERPER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "test"}'

# Check LibreChat logs for search errors
docker logs LibreChat | grep -i -A 3 -B 3 "search.*error"
```

**Issue:** Citations not appearing
```bash
# Verify citation settings
grep -A 5 "citation" config/librechat.yaml .env

# Check search response format in logs
docker logs LibreChat | grep -A 5 "search.*response"
```

**Issue:** API quota exceeded
```bash
# Monitor API usage
echo "Current time: $(date)"
echo "Check Serper dashboard for usage stats"
echo "Consider upgrading plan if hitting limits frequently"
```

## 🎯 Search Use Cases

### Technical Searches
- "Search for Docker Swarm best practices 2024"
- "Find Kubernetes troubleshooting guides"
- "Look up Python async/await performance tips"

### Current Information
- "Search for latest cybersecurity vulnerabilities"
- "Find recent AI model releases"
- "Current cloud pricing comparisons"

### Research and Analysis
- "Search for network automation case studies"
- "Find DevOps transformation success stories"
- "Research container security frameworks"

## ✅ Completion Checklist

Mark each item when completed:

- [ ] Serper API account created
- [ ] API key generated and secured
- [ ] LibreChat environment configured
- [ ] YAML configuration updated with search settings
- [ ] Services restarted successfully
- [ ] Search button appears in interface
- [ ] Test searches return results with citations
- [ ] Natural language search queries work
- [ ] Performance monitoring active

## ⏭️ Next Steps

Once web search is working:

1. **[[04-Obsidian-Organization/vault-setup.md]]** - Set up knowledge management
2. Configure search result caching for performance
3. Set up search analytics and monitoring

## 📈 Search Analytics

Track search usage and optimize:

```bash
# Search usage analysis script
cat > analyze-search.sh << 'EOF'
#!/bin/bash
echo "📈 Search Analytics Report"
echo "========================="

LOGFILE="/tmp/librechat-search.log"
docker logs LibreChat 2>&1 | grep -i "web.search" > $LOGFILE

echo "🔍 Total Searches Today: $(grep "$(date +%Y-%m-%d)" $LOGFILE | wc -l)"
echo "📊 Most Common Search Terms:"
grep -o '"q":"[^"]*"' $LOGFILE | cut -d'"' -f4 | sort | uniq -c | sort -rn | head -5

echo -e "\n⚡ Search Performance:"
grep -o "search.*took [0-9]*ms" $LOGFILE | tail -5

rm $LOGFILE
EOF

chmod +x analyze-search.sh
```

---

**🎉 Success!** Perplexity-style web search is now integrated with LibreChat.

**Estimated completion time:** 15-20 minutes
**Next guide:** Obsidian Organization