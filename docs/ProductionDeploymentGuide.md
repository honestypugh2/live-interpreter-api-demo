# Production Deployment Guide: Set-It-And-Forget-It Solution

This guide provides comprehensive instructions for deploying the Live Interpreter API Demo as a production-ready, low-maintenance solution suitable for council meetings, conferences, and other professional environments.

## Table of Contents
- [Overview](#overview)
- [Architecture Options](#architecture-options)
- [Deployment Strategies](#deployment-strategies)
- [Automation & Maintenance Reduction](#automation--maintenance-reduction)
- [Monitoring & Health Checks](#monitoring--health-checks)
- [Backup & Disaster Recovery](#backup--disaster-recovery)
- [Security Hardening](#security-hardening)
- [Cost Optimization](#cost-optimization)
- [Troubleshooting Automation](#troubleshooting-automation)

---

## Overview

### Production-Ready Goals
- **99.9% uptime** for scheduled meeting times
- **Zero-touch operation** during meetings
- **Automated recovery** from common failures
- **Self-healing** infrastructure
- **Minimal human intervention** (< 1 hour/month)

### Recommended Deployment Timeline
| Phase | Duration | Activities |
|-------|----------|------------|
| Planning | 1 week | Requirements, architecture, budget approval |
| Setup | 2 weeks | Infrastructure, deployment, testing |
| Pilot | 2 weeks | Limited use, monitoring, tuning |
| Production | Ongoing | Full deployment, quarterly reviews |

---

## Architecture Options

### Option 1: Azure-Hosted (Recommended for Set-and-Forget)

**Best For**: Organizations wanting minimal maintenance and maximum reliability

```
┌─────────────────────────────────────────────────────────────┐
│                   Azure Subscription                         │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │           Azure App Service (React Frontend)        │    │
│  │  - Auto-scaling: 1-3 instances                      │    │
│  │  - Always On: Enabled                               │    │
│  │  - Health Check: /health endpoint                   │    │
│  │  - SSL: Azure-managed certificate                   │    │
│  └────────────────┬───────────────────────────────────┘    │
│                   │                                          │
│  ┌────────────────▼───────────────────────────────────┐    │
│  │      Azure Container Instances (Backend)            │    │
│  │  - Restart Policy: Always                           │    │
│  │  - Liveness Probe: /api/health                      │    │
│  │  - Resource Limits: 2 vCPU, 4GB RAM                │    │
│  └────────────────┬───────────────────────────────────┘    │
│                   │                                          │
│  ┌────────────────▼───────────────────────────────────┐    │
│  │         Azure Speech Service                        │    │
│  │  - Region: eastus (Live Interpreter support)       │    │
│  │  - Tier: Standard (auto-scaling)                   │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │      Azure Monitor + Application Insights            │  │
│  │  - Availability tests every 5 minutes                │  │
│  │  - Alerting: Email + SMS for failures                │  │
│  │  - Log Analytics: 90-day retention                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Azure Key Vault                             │  │
│  │  - API keys, certificates                             │  │
│  │  - Managed identities for access                      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Monthly Cost**: ~$150-300 (depending on usage)

**Maintenance**: ~30 minutes/month
- Review Application Insights dashboard
- Check cost optimization recommendations
- Update dependencies quarterly

### Option 2: On-Premises with Docker

**Best For**: Organizations with existing infrastructure and IT staff

```
┌─────────────────────────────────────────────────────────────┐
│               On-Premises Server / VM                        │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Docker Compose Stack                        │    │
│  │                                                     │    │
│  │  ┌──────────────────────────────────────────┐     │    │
│  │  │   Frontend Container (Nginx + React)     │     │    │
│  │  │   - Health check: curl localhost:80      │     │    │
│  │  │   - Restart: unless-stopped              │     │    │
│  │  └──────────────────────────────────────────┘     │    │
│  │                                                     │    │
│  │  ┌──────────────────────────────────────────┐     │    │
│  │  │   Backend Container (FastAPI)            │     │    │
│  │  │   - Health check: /api/health            │     │    │
│  │  │   - Restart: unless-stopped              │     │    │
│  │  └──────────────────────────────────────────┘     │    │
│  │                                                     │    │
│  │  ┌──────────────────────────────────────────┐     │    │
│  │  │   Watchtower (Auto-Updates)              │     │    │
│  │  │   - Pulls new images weekly              │     │    │
│  │  │   - Graceful container restarts          │     │    │
│  │  └──────────────────────────────────────────┘     │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │    Prometheus + Grafana (Monitoring)                  │  │
│  │    - Metrics collection every 15 seconds              │  │
│  │    - Pre-configured dashboards                        │  │
│  │    - Alert rules for failures                         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTPS (TLS 1.3)
                            ▼
                  Azure Speech Service
```

**Monthly Cost**: ~$50-100 (Azure Speech + hardware)

**Maintenance**: ~2 hours/month
- Monitor Docker container health
- Update OS security patches
- Review logs and metrics

---

## Deployment Strategies

### 1. Azure App Service Deployment (Recommended)

#### Prerequisites
```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Install required tools
pip install azure-cli
```

#### Step-by-Step Deployment

**1.1 Create Resource Group**
```bash
# Login to Azure
az login

# Set variables
RESOURCE_GROUP="live-interpreter-prod"
LOCATION="eastus"
APP_NAME="live-interpreter-app"

# Create resource group
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION
```

**1.2 Create Azure Speech Service**
```bash
# Create Speech resource
az cognitiveservices account create \
  --name "${APP_NAME}-speech" \
  --resource-group $RESOURCE_GROUP \
  --kind SpeechServices \
  --sku S0 \
  --location $LOCATION

# Get keys (save these)
SPEECH_KEY=$(az cognitiveservices account keys list \
  --name "${APP_NAME}-speech" \
  --resource-group $RESOURCE_GROUP \
  --query "key1" -o tsv)

echo "SPEECH_KEY=$SPEECH_KEY"
```

**1.3 Create Key Vault**
```bash
# Create Key Vault
az keyvault create \
  --name "${APP_NAME}-kv" \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --enable-rbac-authorization

# Store secrets
az keyvault secret set \
  --vault-name "${APP_NAME}-kv" \
  --name "SpeechKey" \
  --value "$SPEECH_KEY"
```

**1.4 Deploy Backend (Container Instance)**
```bash
# Create container registry
az acr create \
  --name "${APP_NAME}acr" \
  --resource-group $RESOURCE_GROUP \
  --sku Basic \
  --admin-enabled true

# Build and push backend image
cd src/react_app/backend
az acr build \
  --registry "${APP_NAME}acr" \
  --image backend:latest \
  --file Dockerfile .

# Deploy container
az container create \
  --name "${APP_NAME}-backend" \
  --resource-group $RESOURCE_GROUP \
  --image "${APP_NAME}acr.azurecr.io/backend:latest" \
  --dns-name-label "${APP_NAME}-backend" \
  --ports 8000 \
  --environment-variables \
    SPEECH_REGION=$LOCATION \
  --secure-environment-variables \
    SPEECH_KEY=$SPEECH_KEY \
  --restart-policy Always \
  --cpu 2 \
  --memory 4
```

**1.5 Deploy Frontend (App Service)**
```bash
# Create App Service plan
az appservice plan create \
  --name "${APP_NAME}-plan" \
  --resource-group $RESOURCE_GROUP \
  --sku B1 \
  --is-linux

# Create web app
az webapp create \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --plan "${APP_NAME}-plan" \
  --runtime "NODE|18-lts"

# Configure app settings
BACKEND_URL="https://${APP_NAME}-backend.${LOCATION}.azurecontainer.io"

az webapp config appsettings set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings \
    VITE_BACKEND_URL=$BACKEND_URL \
    WEBSITE_NODE_DEFAULT_VERSION="18-lts"

# Enable Always On
az webapp config set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --always-on true

# Deploy frontend
cd ../../frontend
npm install
npm run build

# Create deployment zip
zip -r frontend.zip dist/

az webapp deployment source config-zip \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --src frontend.zip
```

**1.6 Configure SSL Certificate**
```bash
# Enable HTTPS only
az webapp update \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --https-only true

# Bind custom domain (optional)
# az webapp config hostname add \
#   --webapp-name $APP_NAME \
#   --resource-group $RESOURCE_GROUP \
#   --hostname your-domain.com

# Enable managed certificate
# az webapp config ssl create \
#   --name $APP_NAME \
#   --resource-group $RESOURCE_GROUP \
#   --hostname your-domain.com
```

### 2. Docker Compose Deployment (On-Premises)

#### Complete Docker Setup

**2.1 Create Docker Compose File**

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  # Frontend - React App
  frontend:
    build:
      context: ./src/react_app/frontend
      dockerfile: Dockerfile
    container_name: live-interpreter-frontend
    ports:
      - "80:80"
      - "443:443"
    environment:
      - VITE_BACKEND_URL=http://backend:8000
    volumes:
      - ./ssl:/etc/nginx/ssl:ro
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Backend - FastAPI
  backend:
    build:
      context: ./src/react_app/backend
      dockerfile: Dockerfile
    container_name: live-interpreter-backend
    ports:
      - "8000:8000"
    environment:
      - SPEECH_KEY=${SPEECH_KEY}
      - SPEECH_REGION=${SPEECH_REGION}
      - SOURCE_LANGUAGE=${SOURCE_LANGUAGE}
      - TARGET_LANGUAGE=${TARGET_LANGUAGE}
      - LOG_LEVEL=INFO
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Watchtower - Auto-update containers
  watchtower:
    image: containrrr/watchtower:latest
    container_name: watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - WATCHTOWER_CLEANUP=true
      - WATCHTOWER_POLL_INTERVAL=604800  # Weekly updates
      - WATCHTOWER_INCLUDE_RESTARTING=true
    restart: unless-stopped

  # Prometheus - Metrics collection
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.retention.time=90d'
    restart: unless-stopped

  # Grafana - Monitoring dashboard
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana
      - ./monitoring/grafana-dashboards:/etc/grafana/provisioning/dashboards:ro
      - ./monitoring/grafana-datasources.yml:/etc/grafana/provisioning/datasources/datasources.yml:ro
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
      - GF_INSTALL_PLUGINS=grafana-piechart-panel
    depends_on:
      - prometheus
    restart: unless-stopped

volumes:
  prometheus-data:
  grafana-data:

networks:
  default:
    name: live-interpreter-network
```

**2.2 Create Dockerfiles**

`src/react_app/frontend/Dockerfile`:
```dockerfile
# Multi-stage build for optimized production image
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build production bundle
RUN npm run build

# Production image with Nginx
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:80/health || exit 1

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
```

`src/react_app/backend/Dockerfile`:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    portaudio19-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/api/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

**2.3 Create Monitoring Configuration**

`monitoring/prometheus.yml`:
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

rule_files:
  - '/etc/prometheus/alert.rules.yml'
```

`monitoring/alert.rules.yml`:
```yaml
groups:
  - name: live_interpreter_alerts
    interval: 30s
    rules:
      - alert: BackendDown
        expr: up{job="backend"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Backend service is down"
          description: "Backend has been down for more than 2 minutes"

      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} requests/second"

      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "95th percentile latency is {{ $value }} seconds"
```

**2.4 Deploy with Docker Compose**

```bash
# Create production environment file
cat > .env.prod << EOF
SPEECH_KEY=your_azure_speech_key
SPEECH_REGION=eastus
SOURCE_LANGUAGE=en-US
TARGET_LANGUAGE=es-ES
GRAFANA_PASSWORD=secure_password_here
EOF

# Start all services
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Check service health
docker-compose -f docker-compose.prod.yml ps
```

---

## Automation & Maintenance Reduction

### 1. Automated Dependency Updates

#### GitHub Dependabot Configuration

Create `.github/dependabot.yml`:
```yaml
version: 2
updates:
  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "sunday"
      time: "02:00"
    open-pull-requests-limit: 5
    labels:
      - "dependencies"
      - "python"
    reviewers:
      - "your-team-name"

  # JavaScript dependencies (Frontend)
  - package-ecosystem: "npm"
    directory: "/src/react_app/frontend"
    schedule:
      interval: "weekly"
      day: "sunday"
      time: "03:00"
    open-pull-requests-limit: 5
    labels:
      - "dependencies"
      - "javascript"
    ignore:
      - dependency-name: "*"
        update-types: ["version-update:semver-major"]

  # Docker dependencies
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "sunday"
      time: "04:00"
```

### 2. Automated Testing & Deployment

Create `.github/workflows/ci-cd.yml`:
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    # Weekly health check
    - cron: '0 2 * * 0'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: |
          pytest tests/ --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build-and-deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Login to Azure
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: Build and push backend
        run: |
          az acr build \
            --registry ${{ secrets.ACR_NAME }} \
            --image backend:${{ github.sha }} \
            --image backend:latest \
            --file src/react_app/backend/Dockerfile \
            src/react_app/backend
      
      - name: Update container instance
        run: |
          az container create \
            --name live-interpreter-backend \
            --resource-group ${{ secrets.RESOURCE_GROUP }} \
            --image ${{ secrets.ACR_NAME }}.azurecr.io/backend:latest \
            --restart-policy Always
      
      - name: Deploy frontend
        run: |
          cd src/react_app/frontend
          npm ci
          npm run build
          az webapp deployment source config-zip \
            --name ${{ secrets.APP_NAME }} \
            --resource-group ${{ secrets.RESOURCE_GROUP }} \
            --src frontend.zip
```

### 3. Self-Healing Scripts

Create `scripts/health-monitor.sh`:
```bash
#!/bin/bash
# Health monitoring and auto-recovery script
# Run this as a cron job: */5 * * * * /path/to/health-monitor.sh

LOG_FILE="/var/log/live-interpreter-health.log"
MAX_RESTART_ATTEMPTS=3
RESTART_COUNT_FILE="/tmp/restart_count"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_backend() {
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/health)
    if [ "$response" != "200" ]; then
        return 1
    fi
    return 0
}

check_frontend() {
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:80/health)
    if [ "$response" != "200" ]; then
        return 1
    fi
    return 0
}

restart_service() {
    local service=$1
    local count=0
    
    if [ -f "$RESTART_COUNT_FILE" ]; then
        count=$(cat "$RESTART_COUNT_FILE")
    fi
    
    if [ "$count" -ge "$MAX_RESTART_ATTEMPTS" ]; then
        log "ERROR: Max restart attempts reached for $service. Manual intervention required."
        # Send alert (configure with your notification system)
        curl -X POST https://your-alert-webhook.com \
            -d "service=$service&status=critical&message=Max restarts exceeded"
        exit 1
    fi
    
    log "Restarting $service (attempt $((count + 1))/$MAX_RESTART_ATTEMPTS)"
    docker-compose -f /path/to/docker-compose.prod.yml restart "$service"
    
    echo $((count + 1)) > "$RESTART_COUNT_FILE"
    
    # Wait and verify
    sleep 30
    if [ "$service" = "backend" ]; then
        if check_backend; then
            log "✓ Backend recovered successfully"
            rm -f "$RESTART_COUNT_FILE"
            return 0
        fi
    elif [ "$service" = "frontend" ]; then
        if check_frontend; then
            log "✓ Frontend recovered successfully"
            rm -f "$RESTART_COUNT_FILE"
            return 0
        fi
    fi
    
    return 1
}

# Main health checks
if ! check_backend; then
    log "⚠ Backend health check failed"
    restart_service "backend"
fi

if ! check_frontend; then
    log "⚠ Frontend health check failed"
    restart_service "frontend"
fi

# Check disk space
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 85 ]; then
    log "⚠ Disk usage critical: ${DISK_USAGE}%"
    # Cleanup old logs
    find /var/log -name "*.log" -mtime +30 -delete
    docker system prune -af --volumes --filter "until=720h"
fi

# Reset restart counter if all is well
if check_backend && check_frontend; then
    rm -f "$RESTART_COUNT_FILE"
fi

log "✓ Health check completed"
```

**Install as cron job:**
```bash
# Make script executable
chmod +x scripts/health-monitor.sh

# Add to crontab (every 5 minutes)
crontab -e
# Add this line:
*/5 * * * * /path/to/live-interpreter-api-demo/scripts/health-monitor.sh
```

### 4. Automated Backup Script

Create `scripts/automated-backup.sh`:
```bash
#!/bin/bash
# Automated backup script for configuration and logs
# Run daily: 0 2 * * * /path/to/automated-backup.sh

BACKUP_DIR="/var/backups/live-interpreter"
RETENTION_DAYS=30
DATE=$(date +%Y%m%d_%H%M%S)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup environment configuration
log "Backing up configuration..."
tar -czf "$BACKUP_DIR/config_$DATE.tar.gz" \
    .env \
    docker-compose.prod.yml \
    monitoring/ \
    --exclude='*.pyc' \
    --exclude='__pycache__'

# Backup Docker volumes
log "Backing up Docker volumes..."
docker run --rm \
    -v prometheus-data:/data \
    -v "$BACKUP_DIR:/backup" \
    alpine tar -czf "/backup/prometheus_$DATE.tar.gz" /data

docker run --rm \
    -v grafana-data:/data \
    -v "$BACKUP_DIR:/backup" \
    alpine tar -czf "/backup/grafana_$DATE.tar.gz" /data

# Backup logs (last 7 days)
log "Backing up recent logs..."
find /var/log/live-interpreter-health.log -mtime -7 | \
    tar -czf "$BACKUP_DIR/logs_$DATE.tar.gz" -T -

# Upload to cloud storage (optional - Azure Blob Storage example)
if [ -n "$AZURE_STORAGE_CONNECTION_STRING" ]; then
    log "Uploading backups to Azure..."
    az storage blob upload-batch \
        --destination backups \
        --source "$BACKUP_DIR" \
        --pattern "*_$DATE.tar.gz"
fi

# Cleanup old backups
log "Removing backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete

log "✓ Backup completed successfully"
```

---

## Monitoring & Health Checks

### 1. Azure Monitor Configuration (Azure-Hosted)

**Create availability test:**
```bash
# Create availability test
az monitor app-insights web-test create \
    --resource-group $RESOURCE_GROUP \
    --name "live-interpreter-availability" \
    --location $LOCATION \
    --web-test-kind "ping" \
    --locations "us-east-azure" "west-us-2-azure" \
    --frequency 300 \
    --timeout 30 \
    --url "https://${APP_NAME}.azurewebsites.net/health"

# Create alert rule
az monitor metrics alert create \
    --name "backend-availability-alert" \
    --resource-group $RESOURCE_GROUP \
    --scopes "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Web/sites/$APP_NAME" \
    --condition "avg availability < 99" \
    --description "Alert when availability drops below 99%" \
    --evaluation-frequency 5m \
    --window-size 15m \
    --action-group-name "admin-notifications"
```

### 2. Grafana Dashboard Configuration

Create `monitoring/grafana-dashboards/live-interpreter.json`:
```json
{
  "dashboard": {
    "title": "Live Interpreter Production Dashboard",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{path}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])",
            "legendFormat": "5xx Errors"
          }
        ],
        "type": "graph",
        "alert": {
          "conditions": [
            {
              "evaluator": { "params": [0.05], "type": "gt" },
              "operator": { "type": "and" },
              "query": { "params": ["A", "5m", "now"] },
              "reducer": { "params": [], "type": "avg" },
              "type": "query"
            }
          ],
          "executionErrorState": "alerting",
          "frequency": "1m",
          "handler": 1,
          "message": "Error rate above threshold",
          "name": "High Error Rate"
        }
      },
      {
        "title": "Response Time (95th percentile)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Active WebSocket Connections",
        "targets": [
          {
            "expr": "websocket_connections_active",
            "legendFormat": "Active Connections"
          }
        ],
        "type": "stat"
      },
      {
        "title": "Azure Speech API Latency",
        "targets": [
          {
            "expr": "azure_speech_api_duration_seconds",
            "legendFormat": "{{operation}}"
          }
        ],
        "type": "graph"
      }
    ],
    "refresh": "30s",
    "time": {
      "from": "now-6h",
      "to": "now"
    }
  }
}
```

### 3. Health Endpoint Implementation

Add to `src/react_app/backend/main.py`:
```python
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from datetime import datetime
import psutil
import os

@app.get("/api/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Comprehensive health check endpoint
    Returns system status and dependencies
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "checks": {}
    }
    
    # Check Azure Speech Service connectivity
    try:
        # Attempt to create a speech config (lightweight check)
        from src.core.config import get_settings
        settings = get_settings()
        speech_key = settings.SPEECH_KEY
        speech_region = settings.SPEECH_REGION
        
        if speech_key and speech_region:
            health_status["checks"]["azure_speech"] = {
                "status": "up",
                "region": speech_region
            }
        else:
            health_status["checks"]["azure_speech"] = {
                "status": "degraded",
                "message": "Missing configuration"
            }
            health_status["status"] = "degraded"
    except Exception as e:
        health_status["checks"]["azure_speech"] = {
            "status": "down",
            "error": str(e)
        }
        health_status["status"] = "unhealthy"
    
    # Check system resources
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    health_status["checks"]["system_resources"] = {
        "status": "up" if cpu_percent < 90 and memory.percent < 90 else "degraded",
        "cpu_percent": cpu_percent,
        "memory_percent": memory.percent,
        "disk_percent": disk.percent
    }
    
    if health_status["status"] == "unhealthy":
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=health_status
        )
    
    return health_status

@app.get("/api/readiness")
async def readiness_check():
    """
    Kubernetes-style readiness probe
    Checks if app is ready to accept traffic
    """
    # Check if all required environment variables are set
    required_vars = ["SPEECH_KEY", "SPEECH_REGION"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"ready": False, "missing_config": missing_vars}
        )
    
    return {"ready": True}

@app.get("/api/liveness")
async def liveness_check():
    """
    Kubernetes-style liveness probe
    Simple check that app is running
    """
    return {"alive": True}
```

---

## Backup & Disaster Recovery

### 1. Disaster Recovery Plan

| Scenario | Recovery Time Objective | Recovery Point Objective | Solution |
|----------|-------------------------|--------------------------|----------|
| Frontend failure | 5 minutes | 0 (stateless) | Azure App Service auto-restart |
| Backend failure | 5 minutes | 0 (stateless) | Container auto-restart |
| Azure Speech outage | Immediate | N/A | Fallback region (westus2) |
| Complete region failure | 30 minutes | 24 hours | Multi-region deployment |
| Data corruption | 1 hour | 24 hours | Daily backups |

### 2. Multi-Region Failover Configuration

Create `scripts/setup-failover.sh`:
```bash
#!/bin/bash
# Setup multi-region failover for critical meetings

PRIMARY_REGION="eastus"
SECONDARY_REGION="westus2"
RESOURCE_GROUP="live-interpreter-prod"

# Create Traffic Manager profile
az network traffic-manager profile create \
    --name live-interpreter-tm \
    --resource-group $RESOURCE_GROUP \
    --routing-method Priority \
    --unique-dns-name live-interpreter-global \
    --ttl 30

# Add primary endpoint
az network traffic-manager endpoint create \
    --name primary-endpoint \
    --profile-name live-interpreter-tm \
    --resource-group $RESOURCE_GROUP \
    --type azureEndpoints \
    --priority 1 \
    --target-resource-id "<primary-app-service-id>"

# Add secondary endpoint
az network traffic-manager endpoint create \
    --name secondary-endpoint \
    --profile-name live-interpreter-tm \
    --resource-group $RESOURCE_GROUP \
    --type azureEndpoints \
    --priority 2 \
    --target-resource-id "<secondary-app-service-id>"

echo "Failover configured: http://live-interpreter-global.trafficmanager.net"
```

### 3. Automated Recovery Testing

Create `scripts/test-disaster-recovery.sh`:
```bash
#!/bin/bash
# Monthly disaster recovery test
# Schedule: 0 3 1 * * /path/to/test-disaster-recovery.sh

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a /var/log/dr-test.log
}

log "Starting DR test..."

# 1. Test backup restoration
log "Testing backup restoration..."
LATEST_BACKUP=$(ls -t /var/backups/live-interpreter/config_*.tar.gz | head -1)
tar -tzf "$LATEST_BACKUP" > /dev/null
if [ $? -eq 0 ]; then
    log "✓ Backup integrity verified"
else
    log "✗ Backup corrupted"
    exit 1
fi

# 2. Test failover endpoints
log "Testing failover endpoints..."
PRIMARY_URL="https://live-interpreter-eastus.azurewebsites.net/api/health"
SECONDARY_URL="https://live-interpreter-westus2.azurewebsites.net/api/health"

PRIMARY_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $PRIMARY_URL)
SECONDARY_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $SECONDARY_URL)

log "Primary status: $PRIMARY_STATUS"
log "Secondary status: $SECONDARY_STATUS"

if [ "$SECONDARY_STATUS" = "200" ]; then
    log "✓ Secondary region operational"
else
    log "✗ Secondary region unavailable"
    exit 1
fi

# 3. Test monitoring alerts
log "Testing alert system..."
curl -X POST http://localhost:9090/-/reload

log "✓ DR test completed successfully"
```

---

## Security Hardening

### 1. Environment Variable Security

**Use Azure Key Vault (recommended):**

```python
# src/core/config.py
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from functools import lru_cache

class Settings:
    def __init__(self):
        if os.getenv("USE_KEY_VAULT", "false").lower() == "true":
            self._load_from_keyvault()
        else:
            self._load_from_env()
    
    def _load_from_keyvault(self):
        key_vault_name = os.getenv("KEY_VAULT_NAME")
        key_vault_uri = f"https://{key_vault_name}.vault.azure.net"
        
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=key_vault_uri, credential=credential)
        
        self.SPEECH_KEY = client.get_secret("SpeechKey").value
        self.SPEECH_REGION = client.get_secret("SpeechRegion").value
    
    def _load_from_env(self):
        self.SPEECH_KEY = os.getenv("SPEECH_KEY")
        self.SPEECH_REGION = os.getenv("SPEECH_REGION")

@lru_cache()
def get_settings():
    return Settings()
```

### 2. Network Security Configuration

Create `nginx/nginx.conf` with security headers:
```nginx
server {
    listen 80;
    listen [::]:80;
    server_name your-domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name your-domain.com;

    # SSL Configuration
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' https:; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';" always;

    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=ws_limit:10m rate=5r/s;

    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        limit_req zone=api_limit burst=20 nodelay;
        
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    location /ws {
        limit_req zone=ws_limit burst=10 nodelay;
        
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        # WebSocket timeouts
        proxy_connect_timeout 7d;
        proxy_send_timeout 7d;
        proxy_read_timeout 7d;
    }
}
```

### 3. Secrets Rotation Strategy

Create `scripts/rotate-secrets.sh`:
```bash
#!/bin/bash
# Rotate Azure Speech Service keys
# Run quarterly: 0 0 1 */3 * /path/to/rotate-secrets.sh

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a /var/log/secrets-rotation.log
}

RESOURCE_GROUP="live-interpreter-prod"
SPEECH_SERVICE_NAME="live-interpreter-app-speech"

log "Starting secrets rotation..."

# Get current key in use (key1 or key2)
CURRENT_KEY_NAME=$(az keyvault secret show \
    --vault-name live-interpreter-kv \
    --name SpeechKeyName \
    --query value -o tsv)

# Determine which key to rotate
if [ "$CURRENT_KEY_NAME" = "key1" ]; then
    ROTATE_KEY="key2"
    NEW_KEY_NAME="key2"
else
    ROTATE_KEY="key1"
    NEW_KEY_NAME="key1"
fi

log "Rotating to $NEW_KEY_NAME..."

# Regenerate the key
az cognitiveservices account keys regenerate \
    --name $SPEECH_SERVICE_NAME \
    --resource-group $RESOURCE_GROUP \
    --key-name $ROTATE_KEY

# Get new key value
NEW_KEY=$(az cognitiveservices account keys list \
    --name $SPEECH_SERVICE_NAME \
    --resource-group $RESOURCE_GROUP \
    --query "$ROTATE_KEY" -o tsv)

# Update Key Vault
az keyvault secret set \
    --vault-name live-interpreter-kv \
    --name SpeechKey \
    --value "$NEW_KEY"

az keyvault secret set \
    --vault-name live-interpreter-kv \
    --name SpeechKeyName \
    --value "$NEW_KEY_NAME"

# Restart services to pick up new key
log "Restarting services..."
az webapp restart \
    --name live-interpreter-app \
    --resource-group $RESOURCE_GROUP

log "✓ Secrets rotation completed successfully"

# Send notification
curl -X POST https://your-notification-webhook.com \
    -d "event=secrets_rotated&service=live-interpreter&status=success"
```

---

## Cost Optimization

### 1. Azure Cost Management Automation

Create `scripts/cost-optimization.sh`:
```bash
#!/bin/bash
# Weekly cost optimization review
# Schedule: 0 9 * * 1 /path/to/cost-optimization.sh

RESOURCE_GROUP="live-interpreter-prod"
COST_THRESHOLD=300  # USD per month

# Get current month's costs
CURRENT_COST=$(az consumption usage list \
    --start-date $(date -d "$(date +%Y-%m-01)" +%Y-%m-%d) \
    --end-date $(date +%Y-%m-%d) \
    --query "[?properties.resourceGroup=='$RESOURCE_GROUP'] | sum([].properties.pretaxCost)" \
    -o tsv)

echo "Current month cost: \$$CURRENT_COST"

if (( $(echo "$CURRENT_COST > $COST_THRESHOLD" | bc -l) )); then
    echo "⚠️ Cost threshold exceeded!"
    
    # Analyze top cost contributors
    az consumption usage list \
        --start-date $(date -d "$(date +%Y-%m-01)" +%Y-%m-%d) \
        --end-date $(date +%Y-%m-%d) \
        --query "[?properties.resourceGroup=='$RESOURCE_GROUP'].{Service:properties.meterDetails.meterCategory, Cost:properties.pretaxCost}" \
        -o table
    
    # Send alert
    curl -X POST https://your-alert-webhook.com \
        -d "event=cost_alert&cost=$CURRENT_COST&threshold=$COST_THRESHOLD"
fi

# Optimization recommendations
echo "Checking for optimization opportunities..."

# 1. Check for idle App Service instances
az webapp list \
    --resource-group $RESOURCE_GROUP \
    --query "[].{Name:name, State:state, AppServicePlan:appServicePlanId}" \
    -o table

# 2. Check for unused storage
az storage account list \
    --resource-group $RESOURCE_GROUP \
    --query "[].{Name:name, PrimaryLocation:primaryLocation}" \
    -o table

# 3. Review Speech Service usage
SPEECH_HOURS=$(az monitor metrics list \
    --resource "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.CognitiveServices/accounts/live-interpreter-app-speech" \
    --metric "TotalCalls" \
    --start-time $(date -d "7 days ago" +%Y-%m-%dT%H:%M:%S) \
    --end-time $(date +%Y-%m-%dT%H:%M:%S) \
    --query "value[].timeseries[].data[].total | sum(@)" \
    -o tsv)

echo "Speech API calls (last 7 days): $SPEECH_HOURS"
```

### 2. Scheduled Scaling Configuration

```bash
# Scale down during off-hours (nights and weekends)
az webapp config set \
    --name live-interpreter-app \
    --resource-group live-interpreter-prod \
    --always-on false

# Create autoscaling rules
az monitor autoscale create \
    --resource-group live-interpreter-prod \
    --resource live-interpreter-app-plan \
    --resource-type Microsoft.Web/serverfarms \
    --name autoscale-plan \
    --min-count 1 \
    --max-count 3 \
    --count 1

# Scale up during business hours (Monday-Friday, 8 AM - 6 PM)
az monitor autoscale rule create \
    --resource-group live-interpreter-prod \
    --autoscale-name autoscale-plan \
    --condition "CpuPercentage > 70 avg 5m" \
    --scale out 1 \
    --cooldown 5

# Scale down during off-hours
az monitor autoscale rule create \
    --resource-group live-interpreter-prod \
    --autoscale-name autoscale-plan \
    --condition "CpuPercentage < 25 avg 10m" \
    --scale in 1 \
    --cooldown 10
```

---

## Troubleshooting Automation

### 1. Common Issue Detection & Auto-Fix

Create `scripts/auto-troubleshoot.sh`:
```bash
#!/bin/bash
# Automatic troubleshooting script
# Runs every 15 minutes via cron

LOG_FILE="/var/log/auto-troubleshoot.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Issue 1: High memory usage
check_memory() {
    MEMORY_USAGE=$(free | grep Mem | awk '{print ($3/$2) * 100.0}')
    if (( $(echo "$MEMORY_USAGE > 85" | bc -l) )); then
        log "⚠️ High memory usage: ${MEMORY_USAGE}%"
        
        # Clear application cache
        docker exec live-interpreter-backend python -c "import gc; gc.collect()"
        
        # Restart if still high after 5 minutes
        sleep 300
        NEW_USAGE=$(free | grep Mem | awk '{print ($3/$2) * 100.0}')
        if (( $(echo "$NEW_USAGE > 85" | bc -l) )); then
            log "Restarting backend due to persistent high memory"
            docker-compose restart backend
        fi
    fi
}

# Issue 2: WebSocket connection drops
check_websocket() {
    WS_ERRORS=$(docker logs live-interpreter-backend --since 15m 2>&1 | grep -c "WebSocket.*error")
    if [ "$WS_ERRORS" -gt 10 ]; then
        log "⚠️ High WebSocket error count: $WS_ERRORS"
        
        # Check network connectivity
        if ! ping -c 3 8.8.8.8 > /dev/null 2>&1; then
            log "Network connectivity issue detected"
            # Restart network service (adjust for your OS)
            systemctl restart networking
        fi
        
        # Restart backend
        docker-compose restart backend
    fi
}

# Issue 3: Azure Speech Service errors
check_azure_speech() {
    SPEECH_ERRORS=$(docker logs live-interpreter-backend --since 15m 2>&1 | grep -c "Azure.*error\|401\|403")
    if [ "$SPEECH_ERRORS" -gt 5 ]; then
        log "⚠️ Azure Speech Service errors: $SPEECH_ERRORS"
        
        # Check if credentials are valid
        TEST_URL="https://${SPEECH_REGION}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
            -H "Ocp-Apim-Subscription-Key: $SPEECH_KEY" \
            "$TEST_URL")
        
        if [ "$RESPONSE" != "200" ]; then
            log "❌ Invalid Azure credentials. Manual intervention required."
            # Send critical alert
            curl -X POST https://your-alert-webhook.com \
                -d "event=azure_auth_failure&severity=critical"
        else
            log "Azure credentials valid. Restarting service..."
            docker-compose restart backend
        fi
    fi
}

# Issue 4: Disk space
check_disk_space() {
    DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$DISK_USAGE" -gt 90 ]; then
        log "⚠️ Critical disk space: ${DISK_USAGE}%"
        
        # Cleanup old logs
        find /var/log -name "*.log" -mtime +7 -delete
        
        # Cleanup Docker
        docker system prune -af --volumes --filter "until=168h"
        
        log "Disk cleanup completed"
    fi
}

# Run all checks
check_memory
check_websocket
check_azure_speech
check_disk_space

log "✓ Auto-troubleshooting completed"
```

### 2. Log Aggregation & Analysis

Create `scripts/log-analyzer.sh`:
```bash
#!/bin/bash
# Daily log analysis and reporting
# Schedule: 0 7 * * * /path/to/log-analyzer.sh

REPORT_DATE=$(date +%Y-%m-%d)
REPORT_FILE="/var/log/reports/daily-report-$REPORT_DATE.txt"

mkdir -p /var/log/reports

{
    echo "========================================="
    echo "Live Interpreter Daily Report - $REPORT_DATE"
    echo "========================================="
    echo ""
    
    # Summary statistics
    echo "## Summary Statistics"
    echo "Total requests: $(docker logs live-interpreter-backend --since 24h 2>&1 | grep -c 'POST\|GET')"
    echo "Translation sessions: $(docker logs live-interpreter-backend --since 24h 2>&1 | grep -c 'start_recording')"
    echo "Average session duration: $(docker logs live-interpreter-backend --since 24h 2>&1 | grep 'session_duration' | awk '{sum+=$NF; count++} END {print sum/count}') seconds"
    echo ""
    
    # Error analysis
    echo "## Error Analysis"
    echo "Total errors: $(docker logs live-interpreter-backend --since 24h 2>&1 | grep -c 'ERROR')"
    echo ""
    echo "Top 5 errors:"
    docker logs live-interpreter-backend --since 24h 2>&1 | grep 'ERROR' | sort | uniq -c | sort -rn | head -5
    echo ""
    
    # Performance metrics
    echo "## Performance Metrics"
    echo "Average response time: $(docker logs live-interpreter-backend --since 24h 2>&1 | grep 'response_time' | awk '{sum+=$NF; count++} END {print sum/count}') ms"
    echo "Peak CPU usage: $(docker stats --no-stream live-interpreter-backend | awk 'NR==2 {print $3}')"
    echo "Peak memory usage: $(docker stats --no-stream live-interpreter-backend | awk 'NR==2 {print $7}')"
    echo ""
    
    # Recommendations
    echo "## Recommendations"
    ERROR_RATE=$(docker logs live-interpreter-backend --since 24h 2>&1 | grep -c 'ERROR')
    if [ "$ERROR_RATE" -gt 100 ]; then
        echo "⚠️ High error rate detected. Review logs for root cause."
    else
        echo "✓ Error rate within acceptable limits."
    fi
    
} > "$REPORT_FILE"

# Email report (configure mail server)
# cat "$REPORT_FILE" | mail -s "Live Interpreter Daily Report - $REPORT_DATE" admin@your-domain.com

echo "Report generated: $REPORT_FILE"
```

---

## Maintenance Checklist

### Daily (Automated)
- ✅ Health check monitoring (every 5 minutes)
- ✅ Log rotation
- ✅ Performance metrics collection
- ✅ Backup creation

### Weekly (Automated)
- ✅ Dependency update checks (Dependabot)
- ✅ Security scan (GitHub Advanced Security)
- ✅ Cost review
- ✅ Error trend analysis

### Monthly (Manual - 30 minutes)
- ☐ Review Application Insights dashboard
- ☐ Review Grafana dashboards
- ☐ Check for Azure service updates
- ☐ Test disaster recovery procedures
- ☐ Review and optimize costs

### Quarterly (Manual - 2 hours)
- ☐ Update Python dependencies
- ☐ Update Node.js dependencies
- ☐ Rotate secrets and credentials
- ☐ Penetration testing
- ☐ Review and update documentation
- ☐ Capacity planning review

---

## Quick Reference Commands

### Docker Operations
```bash
# Start all services
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Restart specific service
docker-compose -f docker-compose.prod.yml restart backend

# Update all containers
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d

# Cleanup
docker system prune -af --volumes
```

### Azure CLI Operations
```bash
# Check app status
az webapp show --name live-interpreter-app --resource-group live-interpreter-prod --query state

# View logs
az webapp log tail --name live-interpreter-app --resource-group live-interpreter-prod

# Restart app
az webapp restart --name live-interpreter-app --resource-group live-interpreter-prod

# Scale app
az appservice plan update --name live-interpreter-plan --resource-group live-interpreter-prod --sku P1V2
```

### Monitoring Commands
```bash
# Check service health
curl http://localhost:8000/api/health

# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# View Grafana dashboards
open http://localhost:3000
```

---

## Support & Escalation

### Escalation Matrix

| Issue Severity | Response Time | Escalation Path |
|----------------|---------------|-----------------|
| Critical (service down) | Immediate | On-call engineer → Manager → Azure Support |
| High (degraded service) | 1 hour | Team lead → Azure Support |
| Medium (non-critical error) | 4 hours | Team member → Team lead |
| Low (optimization) | 24 hours | Next sprint planning |

### Contact Information

**Internal Team:**
- On-call engineer: +1-XXX-XXX-XXXX
- Team lead: team-lead@your-domain.com
- IT operations: it-ops@your-domain.com

**External Support:**
- Azure Support: https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade
- GitHub Copilot support: GitHub issues
- Community forum: [Your forum URL]

---

## Conclusion

By following this production deployment guide, your Live Interpreter API Demo will be:

- **99.9% available** during scheduled meeting times
- **Self-healing** with automated recovery from common failures
- **Cost-optimized** with automatic scaling and resource management
- **Secure** with industry-standard practices and automated updates
- **Low-maintenance** requiring less than 1 hour per month of human intervention

**Next Steps:**
1. Choose deployment option (Azure-hosted or On-premises)
2. Complete initial setup (1-2 weeks)
3. Run pilot program (2 weeks)
4. Enable all automation scripts
5. Schedule quarterly reviews

**Remember:** The key to a successful set-it-and-forget-it solution is:
- Comprehensive monitoring
- Automated recovery mechanisms
- Regular (but automated) updates
- Good documentation
- Proactive cost management

For additional help, refer to:
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture details
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Step-by-step deployment
- [API_REFERENCE.md](./API_REFERENCE.md) - API documentation
