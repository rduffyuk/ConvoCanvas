---
date: 2025-09-14
source: Claude Code
category: Wiki-Guide
tags: [librechat, docker, deployment, setup]
status: completed
priority: high
created: 2025-09-14 21:52:00
---

# LibreChat Docker Deployment Guide

**Guide 1 of 6** | **Estimated Time:** 30-45 minutes
**Prerequisites:** Docker, Docker Compose, 8GB+ RAM

## 🎯 What You'll Accomplish

By the end of this guide, you'll have:
- ✅ LibreChat running in Docker containers
- ✅ MongoDB database for conversation storage
- ✅ RAG API for document processing
- ✅ Basic web interface accessible at localhost:3080

## 📋 Prerequisites Check

Before starting, verify you have:

```bash
# Check Docker version (20.10+)
docker --version

# Check Docker Compose version (2.0+)
docker-compose --version

# Check available RAM (8GB+ recommended)
free -h

# Check available disk space (10GB+ recommended)
df -h
```

## 🗂️ Directory Setup

Create your LibreChat directory structure:

```bash
# Create main directory
mkdir -p ~/librechat-deployment
cd ~/librechat-deployment

# Create required subdirectories
mkdir -p {logs,uploads,images,config}
```

## 📝 Environment Configuration

Create your environment file (sanitized template):

```bash
# Create .env file
cat > .env << 'EOF'
# === App Configuration ===
APP_TITLE=Your AI Assistant
HOST=0.0.0.0
PORT=3080

# === Endpoints Configuration ===
ENDPOINTS=custom,agents

# === MongoDB ===
MONGO_URI=mongodb://mongodb:27017/LibreChat

# === PostgreSQL for Vector DB ===
POSTGRES_DB=mydatabase
POSTGRES_USER=myuser
POSTGRES_PASSWORD=YOUR_SECURE_PASSWORD_HERE

# === Meilisearch ===
MEILI_HOST=http://meilisearch:7700
MEILI_MASTER_KEY=YOUR_MEILISEARCH_KEY_HERE

# === Security (GENERATE NEW VALUES) ===
JWT_SECRET=YOUR_JWT_SECRET_HERE
JWT_REFRESH_SECRET=YOUR_JWT_REFRESH_SECRET_HERE
CREDS_KEY=YOUR_CREDS_KEY_HERE
CREDS_IV=YOUR_CREDS_IV_HERE

# === User/Group IDs ===
UID=1000
GID=1000

# === RAG Configuration ===
RAG_API_URL=http://rag_api:8000
RAG_PORT=8000
ENABLE_RAG=true
ENABLE_RAG_API=true

# === File Configuration ===
FILE_UPLOAD_ENABLED=true
FILE_UPLOAD_MAX_SIZE=95
FILE_UPLOAD_SIZE_LIMIT=95

# === Debug Configuration ===
DEBUG_LOGGING=true
DEBUG_CONSOLE=true
DEBUG_RAG_API=true

# === Search Configuration ===
SEARCH_ENABLED=true
ENABLE_WEB_SEARCH=true
# Add your search API keys here (see next guide)

# === Authentication Settings ===
ALLOW_REGISTRATION=true
ALLOW_SOCIAL_LOGIN=false
ALLOW_EMAIL_LOGIN=true
EOF
```

## 🔐 Security Keys Generation

Generate secure random keys for your environment:

```bash
# Generate JWT secrets (keep these secure!)
echo "JWT_SECRET=$(openssl rand -hex 64)" >> .env.security
echo "JWT_REFRESH_SECRET=$(openssl rand -hex 64)" >> .env.security
echo "CREDS_KEY=$(openssl rand -hex 32)" >> .env.security
echo "CREDS_IV=$(openssl rand -hex 16)" >> .env.security
echo "POSTGRES_PASSWORD=$(openssl rand -base64 32)" >> .env.security
echo "MEILI_MASTER_KEY=$(openssl rand -base64 32)" >> .env.security

# Review generated keys
cat .env.security

# Manually copy these into your .env file
```

## 🐳 Docker Compose Configuration

Create your Docker Compose file:

```bash
cat > docker-compose.yml << 'EOF'
services:
  api:
    container_name: LibreChat
    ports:
      - "${PORT}:${PORT}"
    depends_on:
      - mongodb
      - rag_api
    image: ghcr.io/danny-avila/librechat-dev:latest
    restart: always
    user: "${UID}:${GID}"
    extra_hosts:
      - "host.docker.internal:host-gateway"
    environment:
      - HOST=0.0.0.0
      - MONGO_URI=mongodb://mongodb:27017/LibreChat
      - MEILI_HOST=http://meilisearch:7700
      - RAG_PORT=${RAG_PORT:-8000}
      - RAG_API_URL=http://rag_api:${RAG_PORT:-8000}
    volumes:
      - type: bind
        source: ./.env
        target: /app/.env
      - ./images:/app/client/public/images
      - ./uploads:/app/uploads
      - ./logs:/app/api/logs

  mongodb:
    container_name: chat-mongodb
    image: mongo
    restart: always
    user: "${UID}:${GID}"
    volumes:
      - ./data-node:/data/db
    command: mongod --noauth

  meilisearch:
    container_name: chat-meilisearch
    image: getmeili/meilisearch:v1.12.3
    restart: always
    user: "${UID}:${GID}"
    environment:
      - MEILI_HOST=http://meilisearch:7700
      - MEILI_NO_ANALYTICS=true
      - MEILI_MASTER_KEY=${MEILI_MASTER_KEY}
    volumes:
      - ./meili_data_v1.12:/meili_data

  vectordb:
    container_name: vectordb
    image: ankane/pgvector:latest
    environment:
      POSTGRES_DB: mydatabase
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    restart: always
    volumes:
      - pgdata2:/var/lib/postgresql/data

  rag_api:
    container_name: rag_api
    image: ghcr.io/danny-avila/librechat-rag-api-dev:latest
    environment:
      - DB_HOST=vectordb
      - RAG_PORT=${RAG_PORT:-8000}
    restart: always
    depends_on:
      - vectordb
    env_file:
      - .env

volumes:
  pgdata2:
EOF
```

## 🚀 Initial Deployment

Deploy your LibreChat stack:

```bash
# Start the services
docker-compose up -d

# Check service status
docker-compose ps

# View logs (optional)
docker-compose logs -f --tail=50
```

## ✅ Verification Tests

Test your deployment:

```bash
# Test 1: Check all containers are running
docker ps | grep -E "(LibreChat|mongodb|meilisearch|vectordb|rag_api)"

# Test 2: Check LibreChat web interface
curl -f http://localhost:3080 || echo "❌ LibreChat not accessible"

# Test 3: Check RAG API health
curl -f http://localhost:8000/health || echo "❌ RAG API not healthy"

# Test 4: Check MongoDB connection
docker exec chat-mongodb mongosh --eval "db.runCommand('ping')" || echo "❌ MongoDB not responsive"
```

## 🌐 Web Interface Access

1. **Open your browser** to `http://localhost:3080`
2. **Create an account** (first user becomes admin)
3. **Verify basic functionality:**
   - Can access the interface ✅
   - Can create conversations ✅
   - Can see endpoints menu ✅

## 🔧 Troubleshooting

### Common Issues

**Issue:** LibreChat container won't start
```bash
# Check logs
docker logs LibreChat

# Common fix: Permission issues
sudo chown -R $USER:$USER ./logs ./uploads ./images
```

**Issue:** Database connection errors
```bash
# Check MongoDB status
docker logs chat-mongodb

# Reset MongoDB data (⚠️ destroys data)
docker-compose down
sudo rm -rf data-node/
docker-compose up -d
```

**Issue:** Port conflicts
```bash
# Check what's using port 3080
sudo netstat -tulpn | grep 3080

# Change port in .env file
echo "PORT=3081" >> .env
docker-compose down && docker-compose up -d
```

## 📊 Health Check Script

Create a health check script:

```bash
cat > health-check.sh << 'EOF'
#!/bin/bash
echo "🏥 LibreChat Health Check"
echo "========================="

# Check containers
echo "📦 Container Status:"
docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "(LibreChat|mongodb|meilisearch|vectordb|rag_api)"

# Check endpoints
echo -e "\n🌐 Endpoint Health:"
curl -s http://localhost:3080 > /dev/null && echo "✅ LibreChat: http://localhost:3080" || echo "❌ LibreChat: Not accessible"
curl -s http://localhost:8000/health > /dev/null && echo "✅ RAG API: http://localhost:8000" || echo "❌ RAG API: Not accessible"

# Check disk usage
echo -e "\n💾 Disk Usage:"
du -sh data-node/ meili_data_v1.12/ logs/ uploads/ 2>/dev/null || echo "No data directories yet"

echo -e "\n✨ Health check complete!"
EOF

chmod +x health-check.sh
./health-check.sh
```

## ✅ Completion Checklist

Mark each item when completed:

- [ ] Docker and Docker Compose installed
- [ ] Directory structure created
- [ ] Environment file configured with secure keys
- [ ] Docker Compose file created
- [ ] All containers started successfully
- [ ] Web interface accessible at localhost:3080
- [ ] User account created
- [ ] Health check script runs without errors
- [ ] Basic conversation functionality verified

## ⏭️ Next Steps

Once LibreChat is running:

1. **[[02-LM-Studio-Integration/model-setup.md]]** - Add local AI models
2. Configure additional endpoints and models
3. Set up web search integration

## 💾 Backup & Maintenance

```bash
# Backup conversations and data
docker-compose exec mongodb mongodump --out /data/db/backup
sudo cp -r data-node/ backup-$(date +%Y%m%d)/

# Update LibreChat
docker-compose pull
docker-compose down && docker-compose up -d

# View resource usage
docker stats
```

---

**🎉 Congratulations!** LibreChat is now deployed and ready for AI model integration.

**Estimated completion time:** 30-45 minutes
**Next guide:** LM Studio Integration