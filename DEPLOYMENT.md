# Matrix Guardian - Deployment Guide

This guide covers all deployment options for Matrix Guardian, from local development to production containerized deployment.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Production Deployment](#production-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (for containerized deployment)
- PostgreSQL 16+ (if running locally without Docker)
- Make (optional, for convenience commands)

### Installation & Run (Local)

```bash
# Install dependencies
make install

# Run the server
make run
```

The API will be available at `http://localhost:8000`

### Installation & Run (Docker)

```bash
# Build and run containers
make build-container
make run-container
```

The API will be available at `http://localhost:8000`

---

## Local Development

### 1. Setup Virtual Environment

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Install project dependencies
make install

# Or manually:
pip install -e .
```

### 3. Install Development Dependencies

```bash
# Install dev dependencies (testing, linting, etc.)
make dev

# Or manually:
pip install -r requirements-dev.txt
```

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

**Required Configuration:**
- `DATABASE_URL`: PostgreSQL connection string
- `MATRIXHUB_API_BASE`: Matrix Hub API endpoint
- `MATRIX_AI_BASE`: Matrix AI service endpoint
- `API_TOKEN`: Authentication token

### 5. Run the Application

```bash
# Start the Guardian API server
make run

# Or run directly with uvicorn:
uvicorn guardian.main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. Run the Autopilot Worker (Optional)

```bash
# In a separate terminal
make run-autopilot

# Or run directly:
python -m guardian.runner.autopilot_worker
```

### 7. Access the Application

- **API Endpoint**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## Docker Deployment

Docker deployment provides a containerized, production-ready environment with PostgreSQL, Guardian API, and Autopilot worker.

### Architecture

The Docker deployment includes:
- **PostgreSQL 16**: Database service
- **Guardian API**: Main API server (2 workers)
- **Autopilot Worker**: Background agent orchestration

### Available Make Commands

```bash
# Build the Docker image
make build-container

# Start all containers (detached mode)
make run-container

# View container logs
make logs-container

# Stop all containers
make stop-container

# Restart containers
make restart-container

# Stop and remove all containers + volumes
make clean-containers
```

### Manual Docker Commands

```bash
# Build the image
docker build -f infra/docker/Dockerfile -t matrix-guardian:latest .

# Run with docker-compose
cd infra/docker
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down

# Remove all data (including database)
docker-compose down -v
```

### Container Details

#### Guardian API Container
- **Port**: 8000
- **Workers**: 2 Uvicorn workers
- **Health Check**: Every 30s
- **Restart Policy**: unless-stopped
- **User**: Non-root (guardian)

#### Autopilot Worker Container
- **Function**: Runs autonomous agent loop
- **Interval**: 60 seconds (configurable)
- **Safe Mode**: Enabled by default
- **Restart Policy**: unless-stopped

#### PostgreSQL Container
- **Version**: 16-alpine
- **Port**: 5432
- **Health Check**: Every 10s
- **Data Persistence**: Named volume

---

## Production Deployment

### Prerequisites

1. **Server Requirements**:
   - Linux server (Ubuntu 22.04+ recommended)
   - 2+ CPU cores
   - 4GB+ RAM
   - 20GB+ disk space
   - Docker & Docker Compose installed

2. **Domain & SSL**:
   - Registered domain name
   - SSL certificate (Let's Encrypt recommended)
   - Reverse proxy (Nginx/Traefik)

### Step 1: Clone Repository

```bash
git clone https://github.com/agent-matrix/matrix-guardian.git
cd matrix-guardian
```

### Step 2: Configure Environment

```bash
# Copy and edit environment file
cp .env.example .env
nano .env
```

**Production Configuration Checklist**:

- ✅ Strong `POSTGRES_PASSWORD` (use password generator)
- ✅ Secure `API_TOKEN` for authentication
- ✅ Production `MATRIXHUB_API_BASE` endpoint
- ✅ Production `MATRIX_AI_BASE` endpoint
- ✅ Set `LOG_LEVEL=warning` or `error`
- ✅ Configure AI provider API keys
- ✅ Set `AUTOPILOT_SAFE_MODE=true`

### Step 3: Build and Deploy

```bash
# Build the production image
make build-container

# Start all services
make run-container

# Verify deployment
docker ps
docker-compose -f infra/docker/compose.yaml logs
```

### Step 4: Configure Reverse Proxy (Nginx Example)

```nginx
server {
    listen 80;
    server_name guardian.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Step 5: Setup SSL (Let's Encrypt)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d guardian.yourdomain.com

# Auto-renewal is configured automatically
```

### Step 6: Setup Monitoring (Optional)

```bash
# View container stats
docker stats

# Check logs
make logs-container

# Health check endpoint
curl http://localhost:8000/health
```

### Step 7: Backup Strategy

```bash
# Backup database
docker exec matrix_db pg_dump -U matrix matrix_guardian > backup.sql

# Restore database
cat backup.sql | docker exec -i matrix_db psql -U matrix matrix_guardian

# Backup volumes
docker run --rm -v matrix_postgres_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/db-backup.tar.gz /data
```

---

## Environment Configuration

### Core Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_USER` | `matrix` | PostgreSQL username |
| `POSTGRES_PASSWORD` | `matrix` | PostgreSQL password (CHANGE IN PRODUCTION!) |
| `POSTGRES_DB` | `matrix_guardian` | PostgreSQL database name |
| `POSTGRES_PORT` | `5432` | PostgreSQL port |
| `GUARDIAN_PORT` | `8000` | Guardian API port |
| `LOG_LEVEL` | `info` | Log level (debug/info/warning/error) |
| `UVICORN_WORKERS` | `2` | Number of API workers |
| `API_TOKEN` | `dev-secret-token` | API authentication token |

### Matrix Ecosystem

| Variable | Description |
|----------|-------------|
| `MATRIXHUB_API_BASE` | Matrix Hub API endpoint |
| `MATRIX_AI_BASE` | Matrix AI service endpoint (HuggingFace Space) |

### Autopilot Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `AUTOPILOT_ENABLED` | `true` | Enable autopilot worker |
| `AUTOPILOT_API_ENABLED` | `false` | Enable autopilot API endpoints |
| `AUTOPILOT_INTERVAL_SEC` | `60` | Agent execution interval |
| `AUTOPILOT_SAFE_MODE` | `true` | Require human approval for high-risk actions |
| `AUTOPILOT_POLICY` | `src/guardian/agents/policies/default_policy.yaml` | Policy file path |

### AI Providers (Optional)

```bash
# OpenAI
OPENAI_API_KEY=sk-...

# Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-...

# WatsonX
WATSONX_API_KEY=...
WATSONX_PROJECT_ID=...

# Ollama (local)
OLLAMA_BASE_URL=http://localhost:11434
```

---

## Troubleshooting

### Container Issues

**Problem**: Containers won't start
```bash
# Check container logs
docker-compose -f infra/docker/compose.yaml logs

# Check container status
docker ps -a

# Rebuild containers
make clean-containers
make build-container
make run-container
```

**Problem**: Database connection failed
```bash
# Check database health
docker exec matrix_db pg_isready -U matrix

# Check environment variables
docker exec matrix_guardian_app env | grep DATABASE

# Restart database
docker-compose -f infra/docker/compose.yaml restart db
```

### Network Issues

**Problem**: Can't access API
```bash
# Check if port is bound
netstat -tulpn | grep 8000

# Check container network
docker network inspect matrix_network

# Check firewall
sudo ufw status
sudo ufw allow 8000/tcp
```

### Performance Issues

**Problem**: Slow response times
```bash
# Increase workers
# Edit .env: UVICORN_WORKERS=4
make restart-container

# Check resource usage
docker stats

# Check database performance
docker exec matrix_db psql -U matrix -d matrix_guardian -c "SELECT * FROM pg_stat_activity;"
```

### Data Issues

**Problem**: Data loss after restart
```bash
# Check volume status
docker volume ls
docker volume inspect matrix_postgres_data

# Verify volume mount
docker inspect matrix_db | grep -A 10 Mounts
```

### Autopilot Issues

**Problem**: Autopilot worker not running
```bash
# Check worker logs
docker logs matrix_autopilot_worker

# Restart worker
docker restart matrix_autopilot_worker

# Check worker status
docker exec matrix_autopilot_worker ps aux
```

---

## Maintenance

### Updating the Application

```bash
# Pull latest changes
git pull origin main

# Rebuild containers
make build-container

# Restart with new image
make restart-container
```

### Database Migrations

```bash
# Enter container
docker exec -it matrix_db psql -U matrix -d matrix_guardian

# Run migrations (example)
# Add your migration commands here
```

### Log Management

```bash
# View logs
make logs-container

# Clear logs (careful!)
docker-compose -f infra/docker/compose.yaml logs --tail=0

# Rotate logs (configure docker daemon)
# Edit /etc/docker/daemon.json:
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

---

## Security Best Practices

1. **Change Default Credentials**: Always change default passwords in production
2. **Use Environment Variables**: Never commit secrets to git
3. **Enable HTTPS**: Always use SSL/TLS in production
4. **Network Isolation**: Use Docker networks for inter-container communication
5. **Regular Updates**: Keep base images and dependencies updated
6. **Backup Regularly**: Implement automated backup strategy
7. **Monitor Logs**: Set up centralized logging and monitoring
8. **Limit Exposure**: Only expose necessary ports
9. **Use Secrets Management**: Consider Docker secrets or Vault for sensitive data
10. **Enable Safe Mode**: Keep `AUTOPILOT_SAFE_MODE=true` in production

---

## Getting Help

- **Documentation**: See README.md and ARCHITECTURE.md
- **Issues**: https://github.com/agent-matrix/matrix-guardian/issues
- **Logs**: `make logs-container` for detailed error messages

---

## Appendix: Complete Make Command Reference

```bash
# Development
make help              # Show all available commands
make install           # Install project dependencies
make dev               # Install all dependencies (dev + prod)
make run               # Run Guardian API locally
make run-autopilot     # Run Autopilot worker locally
make test              # Run tests
make fmt               # Format code
make lint              # Lint code
make clean             # Clean generated files

# Docker/Production
make build-container   # Build Docker image
make run-container     # Start all containers
make stop-container    # Stop all containers
make logs-container    # View container logs
make restart-container # Restart containers
make clean-containers  # Stop and remove all containers + data
```

---

**Matrix Guardian** - AI Control Plane for the Matrix Ecosystem
Version: 2.1.0-autopilot
