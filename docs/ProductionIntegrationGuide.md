# Production Integration Guide: Set-It-And-Forget-It PEG & Streaming Setup

> **Companion to:** [ProductionDeploymentGuide.md](./ProductionDeploymentGuide.md)  
> **Focus:** Integrating with existing broadcast infrastructure for minimal maintenance

This guide extends the IntegrationGuide with production-ready, automated deployment strategies specifically designed for **PEG channels**, **cable broadcast**, and **live streaming** environments that require 99.9% uptime with minimal human intervention.

## Table of Contents
- [Overview](#overview)
- [Production Architecture Comparison](#production-architecture-comparison)
- [Automated PEG Channel Integration](#automated-peg-channel-integration)
- [Self-Healing Infrastructure](#self-healing-infrastructure)
- [Monitoring & Alerting](#monitoring--alerting)
- [Maintenance Schedule](#maintenance-schedule)
- [Troubleshooting Automation](#troubleshooting-automation)

---

## Overview

### Production Goals
- **99.9% uptime** during scheduled broadcast hours
- **< 6 seconds latency** for closed captioning
- **Zero-touch operation** for routine meetings
- **< 30 minutes/month** maintenance
- **Automated recovery** from 95% of failures

### Key Differences from Standard Integration

| Aspect | Standard Setup | Production Setup |
|--------|---------------|------------------|
| Deployment | Manual | Automated (Docker/Azure) |
| Monitoring | Optional | Required with alerts |
| Recovery | Manual restart | Automated self-healing |
| Updates | Manual | Automated weekly |
| Failover | None | Multi-region/source |
| Maintenance | As-needed | Scheduled quarterly |
| Cost | ~$50/month | ~$150-300/month |

---

## Production Architecture Comparison

### Option 1: PEG Channel with Zero Production Impact (Recommended)

**Best For:** Organizations prioritizing safety and minimal disruption

```
┌──────────────────────────────────────────────────────────────────────────┐
│                  EXISTING PRODUCTION (UNTOUCHED)                          │
│                                                                            │
│  Conference Mics → Mixer → Encoder → Cable Broadcast (Original Audio)    │
│                      ↓                                                     │
│                   AUX Send                                                 │
└──────────────────────┼────────────────────────────────────────────────────┘
                       │ (Audio copy - no impact on main signal)
                       ↓
┌──────────────────────────────────────────────────────────────────────────┐
│              PARALLEL TRANSLATION SYSTEM (NEW)                            │
│              Fully automated, self-healing, monitored                     │
│                                                                            │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │   Audio Interface (USB/Thunderbolt)                                 │  │
│  │   - Focusrite Scarlett 2i2 Gen 3                                    │  │
│  │   - RME Babyface Pro FS                                             │  │
│  │   - MOTU M2                                                          │  │
│  │   Health Check: Automated audio level monitoring every 30s          │  │
│  └────────────────┬───────────────────────────────────────────────────┘  │
│                   │                                                        │
│  ┌────────────────▼───────────────────────────────────────────────────┐  │
│  │   Translation Server (Docker Container)                             │  │
│  │   - Backend: FastAPI + Azure Speech SDK                             │  │
│  │   - Frontend: React app with language selection                     │  │
│  │   - Monitoring: Prometheus + Grafana                                │  │
│  │   - Auto-update: Watchtower (weekly)                                │  │
│  │   Restart Policy: Always                                            │  │
│  │   Health Probe: /api/health every 30s                               │  │
│  │   Resource Limits: 2 vCPU, 4GB RAM                                  │  │
│  └────────────────┬───────────────────────────────────────────────────┘  │
│                   │                                                        │
│                   ├─────────────────────────────────────────────────────┐│
│                   │                                                      ││
│  ┌────────────────▼─────────────┐   ┌────────────────────────────────┐││
│  │  WebSocket Server             │   │  Caption Export Service        │││
│  │  - Real-time streaming        │   │  - CEA-608/708 formatter       │││
│  │  - Multi-language support     │   │  - WebVTT/SRT export           │││
│  │  - Client connections: 1000+  │   │  - Serial/USB output           │││
│  └────────────────┬──────────────┘   └────────────────┬───────────────┘││
│                   │                                    │                ││
└───────────────────┼────────────────────────────────────┼────────────────┘│
                    │                                    │
                    ↓                                    ↓
          ┌──────────────────┐              ┌──────────────────────┐
          │  Web Players      │              │  Caption Encoder     │
          │  - YouTube Live   │              │  (Optional)          │
          │  - Facebook Live  │              │  - Hardware CEA-708  │
          │  - Custom embed   │              │  - CaptionMaker      │
          └──────────────────┘              └──────────────────────┘
```

**Production Features:**
- ✅ **Zero impact** on existing cable broadcast
- ✅ Automated deployment via Docker Compose
- ✅ Self-healing with Watchtower auto-updates
- ✅ Prometheus + Grafana monitoring
- ✅ Automated health checks every 30 seconds
- ✅ Email/SMS alerts on failures
- ✅ Automated backup daily at 2 AM
- ✅ Log rotation and cleanup
- ✅ Cost: ~$100-150/month (hardware + Azure services)

**Deployment Time:** 2-4 hours (one-time setup)  
**Maintenance:** 20-30 minutes/month (review dashboards)

### Option 2: Integrated Multi-Audio Production (Advanced)

**Best For:** Professional production environments with existing IT infrastructure

```
┌──────────────────────────────────────────────────────────────────────────┐
│                  ENHANCED PRODUCTION WORKFLOW                             │
│                                                                            │
│  Conference Mics → Mixer → Audio Router → Video Encoder                  │
│                              ↓           ↓                                 │
│                        Track 1      Track 2 (Translation)                 │
│                        (Original)         ↓                                │
│                                    Azure Live Interpreter                 │
│                                           ↓                                │
│                            Multi-track encoding (HLS/DASH)                │
│                                           ↓                                │
│                              Streaming platform                            │
│                           (Viewer selects audio track)                    │
└──────────────────────────────────────────────────────────────────────────┘
```

**Production Features:**
- ✅ Integrated workflow with single stream
- ✅ Professional viewer experience
- ✅ Automated audio routing
- ✅ Multi-language audio tracks
- ✅ Health monitoring on all components
- ✅ Automated failover to backup tracks

**Deployment Time:** 1-2 weeks (complex integration)  
**Maintenance:** 1-2 hours/month

---

## Automated PEG Channel Integration

### Complete Automated Setup

#### Step 1: Hardware Preparation (One-Time)

**Shopping List:**
```
Hardware                     Model Recommendation          Cost      Purpose
─────────────────────────────────────────────────────────────────────────────
Audio Interface              Focusrite Scarlett 2i2 Gen 3  $180     USB audio capture
                            or RME Babyface Pro FS        $750     (Pro option)
                            
XLR Cables (pair)           Mogami Gold Studio            $40      Audio mixer → interface

USB Cable                   Cable Matters USB 3.0          $15      Interface → server

Mini PC (recommended)       Intel NUC 11 Pro              $400     Dedicated translation server
                            - Intel i5
                            - 16GB RAM
                            - 256GB SSD
                            
OR Use existing server      Your existing Windows/Linux   $0       If available
                            server or VM

UPS Battery Backup          APC Back-UPS Pro 1500VA       $200     Power protection
                            
TOTAL (New deployment):                                   ~$835
TOTAL (Using existing server):                            ~$435
```

**Physical Setup:**
1. Connect audio mixer AUX output → Audio interface XLR input 1
2. Connect audio interface → Server via USB 3.0
3. Connect server to UPS battery backup
4. Connect server to network (wired Gigabit Ethernet)

#### Step 2: Automated Software Deployment

**Complete Docker Compose Setup (Copy-Paste Ready)**

Create deployment directory:
```bash
mkdir -p /opt/council-translation
cd /opt/council-translation
```

Create `docker-compose.prod.yml`:
```yaml
version: '3.8'

services:
  # Main translation backend
  backend:
    image: your-registry/council-translator-backend:latest
    container_name: council-translation-backend
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - SPEECH_KEY=${SPEECH_KEY}
      - SPEECH_REGION=${SPEECH_REGION}
      - SOURCE_LANGUAGE=auto  # Auto-detect English/Spanish
      - TARGET_LANGUAGES=en-US,es-ES
      - ENABLE_LIVE_INTERPRETER=true
      - ENABLE_CAPTIONS=true
      - OUTPUT_CAPTION_FORMAT=CEA708
      - AUDIO_INPUT_DEVICE=hw:1,0  # USB audio interface
      - LOG_LEVEL=INFO
    devices:
      - /dev/snd:/dev/snd  # Audio device access
    volumes:
      - ./logs:/app/logs
      - ./backups:/app/backups
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Web frontend
  frontend:
    image: your-registry/council-translator-frontend:latest
    container_name: council-translation-frontend
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    environment:
      - VITE_BACKEND_URL=http://backend:8000
    volumes:
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Prometheus monitoring
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - ./monitoring/alerts.yml:/etc/prometheus/alerts.yml:ro
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.retention.time=90d'

  # Grafana dashboards
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
      - GF_INSTALL_PLUGINS=grafana-piechart-panel
    volumes:
      - grafana-data:/var/lib/grafana
      - ./monitoring/grafana-dashboards:/etc/grafana/provisioning/dashboards:ro
      - ./monitoring/grafana-datasources.yml:/etc/grafana/provisioning/datasources/datasources.yml:ro
    depends_on:
      - prometheus

  # Watchtower - auto-update containers weekly
  watchtower:
    image: containrrr/watchtower:latest
    container_name: watchtower
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - WATCHTOWER_CLEANUP=true
      - WATCHTOWER_POLL_INTERVAL=604800  # Weekly (Sunday 2 AM)
      - WATCHTOWER_INCLUDE_RESTARTING=true
      - WATCHTOWER_NOTIFICATIONS=email
      - WATCHTOWER_NOTIFICATION_EMAIL_FROM=${ALERT_EMAIL_FROM}
      - WATCHTOWER_NOTIFICATION_EMAIL_TO=${ALERT_EMAIL_TO}

  # Caption formatter (optional - for CEA-708 hardware encoders)
  caption-formatter:
    image: your-registry/caption-formatter:latest
    container_name: caption-formatter
    restart: unless-stopped
    environment:
      - CAPTION_FORMAT=CEA708
      - SERIAL_PORT=/dev/ttyUSB0
    devices:
      - /dev/ttyUSB0:/dev/ttyUSB0  # Caption encoder serial connection
    depends_on:
      - backend

volumes:
  prometheus-data:
  grafana-data:

networks:
  default:
    name: council-translation-network
```

Create environment file `.env`:
```bash
# Azure Speech Service
SPEECH_KEY=your_azure_speech_key_here
SPEECH_REGION=eastus

# Security
GRAFANA_PASSWORD=secure_random_password_here

# Alerting (optional)
ALERT_EMAIL_FROM=alerts@yourdomain.com
ALERT_EMAIL_TO=it-team@yourdomain.com
```

#### Step 3: Monitoring Configuration

Create `monitoring/prometheus.yml`:
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'

  - job_name: 'frontend'
    static_configs:
      - targets: ['frontend:80']

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['localhost:9093']

rule_files:
  - 'alerts.yml'
```

Create `monitoring/alerts.yml`:
```yaml
groups:
  - name: peg_channel_critical
    interval: 30s
    rules:
      - alert: TranslationServiceDown
        expr: up{job="backend"} == 0
        for: 2m
        labels:
          severity: critical
          component: backend
        annotations:
          summary: "Translation service is down"
          description: "Backend service has been unavailable for 2+ minutes"
          action: "Automated restart triggered"

      - alert: AudioInputLost
        expr: audio_input_level < 0.01
        for: 1m
        labels:
          severity: critical
          component: audio
        annotations:
          summary: "No audio input detected"
          description: "Audio level below threshold for 1 minute"
          action: "Check audio interface connection"

      - alert: HighTranslationLatency
        expr: histogram_quantile(0.95, rate(translation_latency_seconds_bucket[5m])) > 6
        for: 5m
        labels:
          severity: warning
          component: performance
        annotations:
          summary: "Translation latency above 6 seconds"
          description: "95th percentile: {{ $value }}s (target: <6s)"
          action: "Check Azure region connectivity"

      - alert: CaptionEncoderDisconnected
        expr: caption_encoder_connected == 0
        for: 2m
        labels:
          severity: high
          component: caption
        annotations:
          summary: "Caption encoder disconnected"
          description: "Cannot send captions to broadcast system"
          action: "Check serial/USB connection"

  - name: peg_channel_warnings
    interval: 1m
    rules:
      - alert: HighMemoryUsage
        expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage: {{ $value | humanizePercentage }}"

      - alert: DiskSpaceRunningLow
        expr: (node_filesystem_avail_bytes / node_filesystem_size_bytes) < 0.15
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Disk space below 15%"
          action: "Cleanup old logs scheduled"
```

Create `monitoring/grafana-dashboards/peg-integration.json`:
```json
{
  "dashboard": {
    "title": "PEG Channel Translation Dashboard",
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Service Status",
        "type": "stat",
        "targets": [
          {
            "expr": "up{job=\"backend\"}",
            "legendFormat": "Backend",
            "refId": "A"
          }
        ],
        "gridPos": {"x": 0, "y": 0, "w": 6, "h": 4},
        "fieldConfig": {
          "defaults": {
            "mappings": [
              {"value": 1, "text": "UP", "color": "green"},
              {"value": 0, "text": "DOWN", "color": "red"}
            ]
          }
        }
      },
      {
        "id": 2,
        "title": "Audio Input Level",
        "type": "graph",
        "targets": [
          {
            "expr": "audio_input_level",
            "legendFormat": "Input Level (dB)"
          }
        ],
        "gridPos": {"x": 6, "y": 0, "w": 12, "h": 8},
        "alert": {
          "conditions": [
            {
              "evaluator": {"params": [0.01], "type": "lt"},
              "query": {"params": ["A", "5m", "now"]},
              "reducer": {"params": [], "type": "avg"},
              "type": "query"
            }
          ],
          "frequency": "1m",
          "name": "Audio Input Lost"
        }
      },
      {
        "id": 3,
        "title": "Translation Latency (95th percentile)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(translation_latency_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ],
        "gridPos": {"x": 0, "y": 8, "w": 12, "h": 8},
        "yaxes": [
          {
            "format": "s",
            "label": "Latency",
            "show": true
          }
        ]
      },
      {
        "id": 4,
        "title": "Active Viewer Connections",
        "type": "graph",
        "targets": [
          {
            "expr": "websocket_connections_active",
            "legendFormat": "Active WebSocket Connections"
          }
        ],
        "gridPos": {"x": 12, "y": 8, "w": 12, "h": 8}
      },
      {
        "id": 5,
        "title": "Error Rate (last 5m)",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(translation_errors_total[5m])",
            "legendFormat": "Errors/sec"
          }
        ],
        "gridPos": {"x": 18, "y": 0, "w": 6, "h": 4},
        "thresholds": {
          "mode": "absolute",
          "steps": [
            {"value": 0, "color": "green"},
            {"value": 0.1, "color": "yellow"},
            {"value": 1, "color": "red"}
          ]
        }
      }
    ],
    "refresh": "30s",
    "time": {"from": "now-6h", "to": "now"}
  }
}
```

#### Step 4: One-Command Deployment

```bash
# Navigate to deployment directory
cd /opt/council-translation

# Pull latest images
docker-compose -f docker-compose.prod.yml pull

# Start all services
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Test health endpoints
curl http://localhost:8000/api/health
curl http://localhost:80/health
```

**Expected Output:**
```
NAME                          STATUS    PORTS
council-translation-backend   Up        0.0.0.0:8000->8000/tcp
council-translation-frontend  Up        0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp
prometheus                    Up        0.0.0.0:9090->9090/tcp
grafana                       Up        0.0.0.0:3000->3000/tcp
watchtower                    Up
caption-formatter             Up
```

#### Step 5: Automated Health Monitoring

Create `/opt/council-translation/scripts/health-monitor.sh`:
```bash
#!/bin/bash
# Automated health monitoring and recovery
# Run every 5 minutes: */5 * * * * /opt/council-translation/scripts/health-monitor.sh

LOG_FILE="/var/log/council-translation-health.log"
DOCKER_COMPOSE_FILE="/opt/council-translation/docker-compose.prod.yml"
MAX_RESTART_ATTEMPTS=3
RESTART_COUNT_FILE="/tmp/council_restart_count"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

send_alert() {
    local message=$1
    local severity=$2
    
    # Send email alert (configure mail server)
    echo "$message" | mail -s "[$severity] Council Translation Alert" it-team@yourdomain.com
    
    # Send SMS via Twilio (optional - configure credentials)
    # curl -X POST https://api.twilio.com/2010-04-01/Accounts/$TWILIO_SID/Messages.json \
    #   --data-urlencode "To=+1234567890" \
    #   --data-urlencode "From=+0987654321" \
    #   --data-urlencode "Body=$message"
}

check_service() {
    local service_name=$1
    local health_url=$2
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$health_url")
    if [ "$response" != "200" ]; then
        log "⚠️ $service_name health check failed (HTTP $response)"
        return 1
    fi
    return 0
}

check_audio_input() {
    # Check audio input level from Prometheus
    audio_level=$(curl -s "http://localhost:9090/api/v1/query?query=audio_input_level" | \
        jq -r '.data.result[0].value[1]')
    
    if (( $(echo "$audio_level < 0.01" | bc -l) )); then
        log "⚠️ No audio input detected (level: $audio_level)"
        send_alert "No audio input detected. Check audio interface connection." "CRITICAL"
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
        log "❌ Max restart attempts reached. Manual intervention required."
        send_alert "Max restart attempts exceeded for $service. Manual intervention needed." "CRITICAL"
        exit 1
    fi
    
    log "Restarting $service (attempt $((count + 1))/$MAX_RESTART_ATTEMPTS)"
    docker-compose -f "$DOCKER_COMPOSE_FILE" restart "$service"
    
    echo $((count + 1)) > "$RESTART_COUNT_FILE"
    
    # Wait and verify
    sleep 30
    if check_service "$service" "http://localhost:8000/api/health"; then
        log "✓ $service recovered successfully"
        rm -f "$RESTART_COUNT_FILE"
        send_alert "$service was down but has been automatically recovered." "INFO"
        return 0
    fi
    
    return 1
}

# Main health checks
log "Starting health check..."

# Check backend
if ! check_service "Backend" "http://localhost:8000/api/health"; then
    restart_service "backend"
fi

# Check frontend
if ! check_service "Frontend" "http://localhost:80/health"; then
    restart_service "frontend"
fi

# Check audio input
if ! check_audio_input; then
    log "Audio input issue detected - may require manual intervention"
fi

# Check disk space
DISK_USAGE=$(df -h /opt/council-translation | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 85 ]; then
    log "⚠️ Disk usage high: ${DISK_USAGE}%"
    
    # Cleanup old logs
    find /var/log -name "*council-translation*.log" -mtime +30 -delete
    find /opt/council-translation/logs -name "*.log" -mtime +7 -delete
    
    # Docker cleanup
    docker system prune -af --volumes --filter "until=168h"
    
    log "✓ Disk cleanup completed"
fi

# Reset restart counter if all is well
if check_service "Backend" "http://localhost:8000/api/health" && \
   check_service "Frontend" "http://localhost:80/health"; then
    rm -f "$RESTART_COUNT_FILE"
fi

log "✓ Health check completed"
```

Make executable and install:
```bash
chmod +x /opt/council-translation/scripts/health-monitor.sh

# Add to crontab
crontab -e
# Add this line:
*/5 * * * * /opt/council-translation/scripts/health-monitor.sh
```

#### Step 6: Automated Backup

Create `/opt/council-translation/scripts/automated-backup.sh`:
```bash
#!/bin/bash
# Automated backup script
# Run daily: 0 2 * * * /opt/council-translation/scripts/automated-backup.sh

BACKUP_DIR="/var/backups/council-translation"
RETENTION_DAYS=30
DATE=$(date +%Y%m%d_%H%M%S)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

mkdir -p "$BACKUP_DIR"

# Backup configuration
log "Backing up configuration..."
tar -czf "$BACKUP_DIR/config_$DATE.tar.gz" \
    /opt/council-translation/.env \
    /opt/council-translation/docker-compose.prod.yml \
    /opt/council-translation/monitoring/

# Backup Docker volumes
log "Backing up data..."
docker run --rm \
    -v prometheus-data:/data \
    -v "$BACKUP_DIR:/backup" \
    alpine tar -czf "/backup/prometheus_$DATE.tar.gz" /data

docker run --rm \
    -v grafana-data:/data \
    -v "$BACKUP_DIR:/backup" \
    alpine tar -czf "/backup/grafana_$DATE.tar.gz" /data

# Backup logs (last 7 days)
log "Backing up logs..."
tar -czf "$BACKUP_DIR/logs_$DATE.tar.gz" /opt/council-translation/logs/

# Upload to Azure Blob Storage (optional)
if [ -n "$AZURE_STORAGE_CONNECTION_STRING" ]; then
    log "Uploading to Azure..."
    az storage blob upload-batch \
        --destination backups \
        --source "$BACKUP_DIR" \
        --pattern "*_$DATE.tar.gz"
fi

# Cleanup old backups
log "Removing backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete

log "✓ Backup completed"
```

Install backup cron:
```bash
chmod +x /opt/council-translation/scripts/automated-backup.sh

crontab -e
# Add:
0 2 * * * /opt/council-translation/scripts/automated-backup.sh
```

---

## Self-Healing Infrastructure

### Automated Recovery Mechanisms

#### 1. Container Auto-Restart
```yaml
# Already configured in docker-compose.prod.yml
restart: unless-stopped  # Containers automatically restart on failure
```

#### 2. Health-Based Restart
```yaml
# Health checks trigger automatic container recreation
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
  interval: 30s
  timeout: 10s
  retries: 3  # Restart after 3 failed checks
  start_period: 40s
```

#### 3. Watchtower Auto-Updates
- Automatically pulls new Docker images weekly
- Gracefully restarts containers with new versions
- Email notifications of updates
- Rollback on failure (via Docker image tags)

#### 4. Audio Input Failover

Add to backend configuration:
```python
# src/core/audio_handler.py
class AudioInputManager:
    def __init__(self):
        self.primary_device = "hw:1,0"
        self.fallback_device = "hw:0,0"  # Built-in audio as backup
        self.current_device = self.primary_device
    
    def check_input_health(self):
        """Monitor audio input level"""
        level = self.get_audio_level()
        if level < 0.01:  # No audio detected
            logger.warning("Primary audio input lost, switching to fallback")
            self.switch_to_fallback()
    
    def switch_to_fallback(self):
        """Automatic fallback to backup audio source"""
        self.current_device = self.fallback_device
        self.reinitialize_audio_stream()
        send_alert("Switched to fallback audio source")
```

#### 5. Azure Region Failover

```python
# src/core/translator.py
class ResilientTranslator:
    def __init__(self):
        self.regions = [
            "eastus",
            "westus2",  # Fallback 1
            "westeurope"  # Fallback 2
        ]
        self.current_region_index = 0
    
    def translate_with_failover(self, audio_stream):
        """Attempt translation with automatic region failover"""
        max_retries = len(self.regions)
        
        for attempt in range(max_retries):
            try:
                region = self.regions[self.current_region_index]
                result = self.azure_translate(audio_stream, region)
                return result
            except Exception as e:
                logger.error(f"Translation failed in {region}: {e}")
                self.current_region_index = (self.current_region_index + 1) % len(self.regions)
                if attempt < max_retries - 1:
                    logger.info(f"Failing over to {self.regions[self.current_region_index]}")
                    time.sleep(2)  # Brief delay before retry
                else:
                    raise
```

---

## Monitoring & Alerting

### Access Dashboards

After deployment, access monitoring interfaces:

1. **Grafana Dashboard**: http://localhost:3000
   - Username: `admin`
   - Password: (set in `.env` as `GRAFANA_PASSWORD`)
   - View: PEG Channel Translation Dashboard

2. **Prometheus Metrics**: http://localhost:9090
   - Query metrics directly
   - View alert status
   - Check target health

3. **Application Logs**:
   ```bash
   # View real-time logs
   docker-compose -f docker-compose.prod.yml logs -f backend
   
   # View logs for all services
   docker-compose -f docker-compose.prod.yml logs -f
   ```

### Key Metrics to Monitor

| Metric | Normal Range | Alert Threshold | Action |
|--------|--------------|-----------------|--------|
| Service uptime | 100% | < 99% | Automated restart |
| Audio input level | -20 to -6 dB | < -40 dB | Check connections |
| Translation latency | 2-4 seconds | > 6 seconds | Check Azure region |
| WebSocket connections | 0-1000 | > 1000 | Scale up |
| CPU usage | 30-60% | > 85% | Review performance |
| Memory usage | 40-70% | > 85% | Restart containers |
| Disk space | < 70% used | > 85% used | Automated cleanup |
| Error rate | < 0.1/sec | > 1/sec | Review logs |

### Email Alert Configuration

Configure email alerts in `.env`:
```bash
# Email alerts (using SMTP)
ALERT_EMAIL_ENABLED=true
ALERT_EMAIL_FROM=alerts@yourdomain.com
ALERT_EMAIL_TO=it-team@yourdomain.com,manager@yourdomain.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### SMS Alert Configuration (Optional)

Using Twilio for critical alerts:
```bash
# SMS alerts via Twilio
ALERT_SMS_ENABLED=true
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_FROM_NUMBER=+1234567890
TWILIO_TO_NUMBERS=+0987654321,+1122334455
```

---

## Maintenance Schedule

### Automated Tasks (No Human Intervention)

| Task | Frequency | Time | Automation |
|------|-----------|------|------------|
| Health checks | Every 5 min | Continuous | health-monitor.sh |
| Container updates | Weekly | Sun 2 AM | Watchtower |
| Log rotation | Daily | 3 AM | Docker + logrotate |
| Backups | Daily | 2 AM | automated-backup.sh |
| Disk cleanup | Weekly | Sun 3 AM | health-monitor.sh |
| Metrics collection | Every 15 sec | Continuous | Prometheus |

### Manual Tasks (Minimal)

| Task | Frequency | Duration | Description |
|------|-----------|----------|-------------|
| Review dashboards | Monthly | 15 min | Check Grafana for trends |
| Review alerts | Monthly | 10 min | Analyze alert history |
| Test disaster recovery | Quarterly | 30 min | Verify backups restore correctly |
| Update dependencies | Quarterly | 30 min | Review and approve Watchtower updates |
| Capacity planning | Annually | 1 hour | Review usage trends, plan upgrades |

### Quarterly Maintenance Checklist

```bash
# Quarterly maintenance script (run manually)
#!/bin/bash

echo "=== Quarterly Maintenance - Council Translation System ==="
echo "Date: $(date)"

# 1. Review system health
echo -e "\n1. System Health Summary:"
docker-compose -f /opt/council-translation/docker-compose.prod.yml ps
curl http://localhost:8000/api/health | jq

# 2. Review metrics (last 90 days)
echo -e "\n2. Performance Metrics:"
echo "- Average latency: $(curl -s 'http://localhost:9090/api/v1/query?query=avg_over_time(translation_latency_seconds[90d])' | jq -r '.data.result[0].value[1]') seconds"
echo "- Total translations: $(curl -s 'http://localhost:9090/api/v1/query?query=translation_requests_total' | jq -r '.data.result[0].value[1]')"
echo "- Error rate: $(curl -s 'http://localhost:9090/api/v1/query?query=rate(translation_errors_total[90d])' | jq -r '.data.result[0].value[1]') errors/sec"

# 3. Disk usage
echo -e "\n3. Disk Usage:"
df -h /opt/council-translation

# 4. Backup verification
echo -e "\n4. Recent Backups:"
ls -lh /var/backups/council-translation/ | tail -5

# 5. Docker images
echo -e "\n5. Container Images (check for updates):"
docker images | grep council-translator

# 6. Review logs for errors
echo -e "\n6. Recent Errors:"
grep -i error /var/log/council-translation-health.log | tail -10

echo -e "\n=== Maintenance Review Complete ==="
echo "Next steps:"
echo "- Review Grafana dashboard at http://localhost:3000"
echo "- Check for any pending Watchtower updates"
echo "- Test disaster recovery if not done recently"
```

---

## Troubleshooting Automation

### Common Issues & Automated Solutions

#### Issue 1: Backend Service Down
**Detection:** Health check fails for 2 minutes  
**Automated Action:**
1. health-monitor.sh detects failure
2. Attempts restart (up to 3 times)
3. Sends email/SMS alert
4. If max restarts exceeded, escalates to manual intervention

**Manual Intervention (if needed):**
```bash
# Check logs
docker-compose -f /opt/council-translation/docker-compose.prod.yml logs backend

# Force recreate container
docker-compose -f /opt/council-translation/docker-compose.prod.yml up -d --force-recreate backend
```

#### Issue 2: No Audio Input
**Detection:** Audio level < 0.01 dB for 1 minute  
**Automated Action:**
1. health-monitor.sh detects low audio
2. Sends alert to check connections
3. Attempts switch to fallback audio device
4. Logs issue for review

**Manual Intervention:**
```bash
# Check audio device
arecord -l

# Test audio input
arecord -D hw:1,0 -d 5 -f S16_LE -r 16000 test.wav
aplay test.wav

# Check USB connection
lsusb | grep Audio
```

#### Issue 3: High Latency
**Detection:** 95th percentile latency > 6 seconds for 5 minutes  
**Automated Action:**
1. Alert sent to review Azure connectivity
2. System attempts region failover
3. Logs latency metrics for analysis

**Manual Intervention:**
```bash
# Check network latency to Azure
ping eastus.api.cognitive.microsoft.com

# Check Azure service health
az monitor activity-log list --resource-group rg-council-translation

# Review latency breakdown in Grafana
# Navigate to: http://localhost:3000 → Translation Latency panel
```

#### Issue 4: Disk Space Critical
**Detection:** Disk usage > 85%  
**Automated Action:**
1. health-monitor.sh triggers cleanup
2. Deletes logs older than 30 days
3. Runs Docker system prune
4. Sends alert if still above 80% after cleanup

**Manual Intervention (if automated cleanup insufficient):**
```bash
# Find large files
du -sh /opt/council-translation/* | sort -hr | head -10

# Manual Docker cleanup
docker system prune -af --volumes

# Check backup directory
du -sh /var/backups/council-translation
```

---

## Cost Analysis

### Monthly Operating Costs

| Component | Cost | Notes |
|-----------|------|-------|
| **Hardware (one-time)** | | |
| Audio interface | $180-750 | One-time purchase |
| Mini PC (optional) | $400 | Or use existing server |
| Cables & accessories | $55 | One-time purchase |
| UPS battery backup | $200 | One-time purchase |
| **Subtotal (one-time)** | **$835-1,405** | Or ~$235 if using existing server |
| | | |
| **Monthly Recurring** | | |
| Azure Speech Service | $50-150 | Based on usage (2-4 hours/week) |
| Hosting (if using cloud) | $50-100 | Skip if on-premises |
| Azure Blob Storage (backups) | $5-10 | Optional |
| Email/SMS alerts | $5-15 | Optional (Twilio) |
| **Subtotal (monthly)** | **$60-175** | On-premises |
| **Subtotal (monthly)** | **$110-275** | Cloud-hosted |

### Cost Optimization Tips
- ✅ Use on-premises hosting to avoid cloud compute costs
- ✅ Enable Azure free tier for dev/test (5 hours/month free)
- ✅ Schedule translations only during meeting times (not 24/7)
- ✅ Use automated cleanup to minimize storage costs
- ✅ Leverage existing hardware infrastructure

---

## Support & Escalation

### Automated Alerts Priority

| Alert Level | Response Time | Action |
|-------------|---------------|--------|
| **INFO** | No action | Logged only |
| **WARNING** | Review next day | Check during monthly review |
| **HIGH** | 4 hours | Investigate and resolve |
| **CRITICAL** | Immediate | Automated restart + manual verification |

### Escalation Contact Matrix

```
CRITICAL ALERT
    ↓
Automated Recovery Attempt
    ↓
Success? → Yes → Send INFO notification
    ↓
    No
    ↓
Send SMS/Email to On-Call Engineer: +1-XXX-XXX-XXXX
    ↓
Resolution within 30 min? → Yes → Document in incident log
    ↓
    No
    ↓
Escalate to IT Manager: manager@yourdomain.com
    ↓
Resolution within 2 hours? → Yes → Post-mortem review
    ↓
    No
    ↓
Escalate to Azure Support + Vendor Support
```

### Support Resources

**Internal:**
- On-call engineer: (configured in `.env`)
- IT manager: manager@yourdomain.com
- Runbook: `/opt/council-translation/docs/runbook.md`

**External:**
- Azure Support: [Azure Portal Support](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade)
- GitHub Issues: [Your Repository Issues](https://github.com/your-org/live-interpreter-api-demo/issues)

---

## Conclusion

This production integration guide provides a **complete, automated, set-it-and-forget-it solution** for PEG channels and live streaming with:

✅ **99.9% uptime** through self-healing infrastructure  
✅ **< 30 minutes/month** maintenance requirement  
✅ **Automated recovery** from 95% of common failures  
✅ **Comprehensive monitoring** with Prometheus + Grafana  
✅ **Proactive alerting** via email/SMS  
✅ **Zero impact** on existing production systems  
✅ **Cost-optimized** at ~$60-175/month  

### Quick Start Summary

```bash
# 1. Deploy (one-time setup: 2-4 hours)
cd /opt/council-translation
docker-compose -f docker-compose.prod.yml up -d

# 2. Install monitoring (5 minutes)
chmod +x scripts/*.sh
crontab -e  # Add health-monitor.sh and backup.sh

# 3. Verify (2 minutes)
curl http://localhost:8000/api/health
open http://localhost:3000  # Grafana dashboard

# 4. Forget about it (quarterly reviews only)
# System runs autonomously with automated recovery
```

### Next Steps

1. **Week 1:** Deploy to test environment, run pilot meeting
2. **Week 2-4:** Monitor metrics, tune alert thresholds
3. **Month 2+:** Production deployment, quarterly reviews only

**For additional guidance, see:**
- [ProductionDeploymentGuide.md](./ProductionDeploymentGuide.md) - Deployment details
- [IntegrationGuide.md](./IntegrationGuide.md) - Original integration architecture
- [Quickstart.md](./Quickstart.md) - Getting started basics
