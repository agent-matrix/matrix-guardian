# Matrix Guardian

<div align="center">

**AI Control Plane for the Matrix Ecosystem**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Typed: mypy](https://img.shields.io/badge/typed-mypy-blue.svg)](https://github.com/python/mypy)

</div>

---

## About

**Matrix Guardian** is an intelligent, autonomous control plane designed for the Matrix Ecosystem. It continuously monitors the health of MCP (Model Context Protocol) servers, generates safe remediation plans using AI-powered analysis, and enforces human-in-the-loop (HITL) approval by default for maximum safety.

### Key Features

- **Autonomous Health Monitoring**: Continuously observes MCP server health and performance metrics
- **AI-Powered Remediation**: Generates intelligent remediation plans using matrix-ai service
- **Human-in-the-Loop (HITL)**: Enforces approval workflows for critical operations (default mode)
- **Autopilot Mode**: Optional multi-agent orchestrator with strict policy gates for supervised autonomy
- **Policy-Based Governance**: Risk-based decision making with configurable policy enforcement
- **Production-Ready**: Built with FastAPI, async/await patterns, and comprehensive error handling
- **Fully Observable**: Structured JSON logging, event tracking, and audit trails
- **Docker-Ready**: Complete containerization with Docker Compose support

---

## Architecture

```mermaid
flowchart LR
    subgraph Guardian["Matrix Guardian (Control Plane)"]
        API[FastAPI Server]
        Autopilot[Autopilot Worker<br/>Multi-Agent Orchestrator]
        Tools[Health Probers:<br/>HTTP & MCP Echo]
    end

    subgraph MatrixAI["matrix-ai (AI Service)"]
        PlanAPI[POST /v1/plan]
    end

    subgraph Hub["Matrix Hub API"]
        Apps[GET /apps]
        Status[POST /status]
        Events[POST /guardian/*]
    end

    subgraph DB["PostgreSQL Database"]
        Health[Health Checks]
        EventLog[Event Log]
        Proposals[Proposals]
        Jobs[Job Queue]
    end

    Operators((Human Operators))
    Clients((CLI & SDK Users))

    Tools --> API
    API <-->|Health Status| Hub
    Autopilot -->|Context| MatrixAI
    MatrixAI -->|Remediation Plan| Autopilot
    API -->|Persist| DB
    Hub <-->|Read/Write| DB
    Operators -->|Approve/Reject| Hub
    Clients -->|Consume| Hub
```

### Autopilot Decision Pipeline

```mermaid
flowchart TD
    Start([Start Cycle]) --> Discover[1. Discover Targets<br/>from Matrix Hub]
    Discover --> Probe[2. Probe Health<br/>HTTP + MCP Echo]
    Probe --> Score[3. Score & Summarize<br/>Health Metrics]
    Score --> Plan[4. Generate Plan<br/>via matrix-ai]
    Plan --> Policy{5. Policy Gate<br/>Risk Assessment}
    Policy -->|High Risk| HITL[6a. HITL Required<br/>Await Approval]
    Policy -->|Low Risk| Execute[6b. Auto-Execute<br/>Safe Actions]
    HITL --> Record[7. Record Events]
    Execute --> Record
    Record --> End([End Cycle])
```

---

## Installation

### Prerequisites

- **Python**: 3.11 or higher
- **PostgreSQL**: 13 or higher (for state management)
- **Optional**: [UV](https://github.com/astral-sh/uv) for faster dependency installation

### Quick Start

```bash
# Clone the repository
git clone https://github.com/ruslanmv/matrix-guardian.git
cd matrix-guardian

# Install dependencies (using UV for speed, or pip as fallback)
make dev

# Configure environment variables
cp configs/.env.example .env
# Edit .env with your configuration:
#   - DATABASE_URL
#   - MATRIXHUB_API_BASE
#   - MATRIX_AI_BASE
#   - API_TOKEN

# Run the server
make run
```

The API will be available at `http://localhost:8000`

### Using UV (Recommended)

UV is a fast Python package installer from Astral-sh. Install it for significantly faster dependency resolution:

```bash
# Install UV
pip install uv

# Install dependencies (automatically uses UV if available)
make dev
```

### Docker Deployment

```bash
# Start all services (API + PostgreSQL + Autopilot Worker)
make docker-up

# View logs
make docker-logs

# Stop services
make docker-down
```

---

## Usage

### Basic Operations

```bash
# Display all available commands
make help

# Run tests
make test

# Lint and format code
make fmt
make lint

# Type checking
make typecheck

# Run the API server
make run

# Run in development mode (auto-reload)
make run-dev

# Run the Autopilot worker (headless mode)
make run-autopilot
```

### API Endpoints

#### Core Endpoints (Always Available)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/healthz` | Liveness check |
| `GET` | `/readyz` | Readiness check (includes DB health) |
| `POST` | `/threads/{thread_id}/resume` | Resume paused HITL workflow |

#### Autopilot Endpoints (Feature-Flagged)

Enable by setting `AUTOPILOT_API_ENABLED=true`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/autopilot/status` | Get current Autopilot status and metrics |
| `POST` | `/autopilot/plan-once` | Execute a single decision cycle |

### Example API Usage

```bash
# Check server health
curl http://localhost:8000/healthz

# Check readiness (includes database)
curl http://localhost:8000/readyz

# Get Autopilot status (if enabled)
curl http://localhost:8000/autopilot/status

# Trigger a single planning cycle
curl -X POST http://localhost:8000/autopilot/plan-once
```

---

## Configuration

Configuration is managed via environment variables and YAML files. The application loads settings from `configs/settings.yaml` and can be overridden by a `.env` file.

### Required Environment Variables

```bash
# Database connection string
DATABASE_URL=postgresql://user:password@localhost:5432/guardian

# Matrix Hub API base URL
MATRIXHUB_API_BASE=https://api.matrixhub.io

# matrix-ai service base URL
MATRIX_AI_BASE=https://matrix-ai.huggingface.space

# Authentication token
API_TOKEN=your-secret-token-here
```

### Autopilot Configuration

```bash
# Enable Autopilot (default: false)
AUTOPILOT_ENABLED=true

# Enable Autopilot API endpoints (default: false)
AUTOPILOT_API_ENABLED=true

# Autopilot cycle interval in seconds (default: 60)
AUTOPILOT_INTERVAL_SEC=60

# Policy file path
AUTOPILOT_POLICY=src/guardian/agents/policies/default_policy.yaml

# Safe mode: requires HITL for all actions (default: true)
AUTOPILOT_SAFE_MODE=true
```

### HTTP Client Settings

```bash
# HTTP request timeout in seconds
HTTP_TIMEOUT_SECONDS=8.0

# Number of retries for failed requests
HTTP_RETRIES=2

# Exponential backoff multiplier
HTTP_BACKOFF=0.5
```

### Policy Configuration

Edit `src/guardian/agents/policies/default_policy.yaml` to customize risk thresholds and approval rules:

```yaml
autopilot:
  policy:
    safe_mode: true              # Require HITL for all actions
    hitl_enabled: true           # Enable HITL workflows
    risk_max_auto: low           # Maximum risk level for auto-approval
    allowed_hosts:               # Hosts allowed for probing
      - api.matrixhub.io
      - matrix-ai.huggingface.space
```

---

## Running Modes

### Mode 1: HITL-Only (Default)

Traditional human-in-the-loop mode where all actions require manual approval.

```bash
make run
```

### Mode 2: API-Driven Autopilot

Autopilot can be controlled via API endpoints.

```bash
AUTOPILOT_ENABLED=true AUTOPILOT_API_ENABLED=true make run
```

### Mode 3: Headless Worker

Autonomous loop that runs at a fixed interval.

```bash
AUTOPILOT_ENABLED=true make run-autopilot
```

### Mode 4: Full Docker Stack

Complete production stack with PostgreSQL, API server, and Autopilot worker.

```bash
docker compose -f infra/docker/compose.yaml up --build
```

---

## Development

### Project Structure

```
matrix-guardian/
├── src/guardian/                  # Main application source
│   ├── main.py                    # Application entry point
│   ├── config.py                  # Global configuration
│   ├── autopilot_settings.py     # Autopilot-specific config
│   ├── logging.py                 # Structured logging setup
│   ├── app/                       # FastAPI application
│   │   ├── api.py                 # API initialization
│   │   ├── dependencies.py        # Dependency injection
│   │   └── routes/                # API route handlers
│   │       ├── health.py          # Health check endpoints
│   │       ├── resume.py          # HITL resume endpoint
│   │       └── autopilot.py       # Autopilot control endpoints
│   ├── agents/                    # Autopilot orchestration
│   │   ├── autopilot.py           # Main orchestrator
│   │   ├── graph.py               # Decision graph/pipeline
│   │   ├── policy.py              # Policy enforcement
│   │   ├── tools/                 # Health probe tools
│   │   │   ├── http_probe.py      # HTTP health checker
│   │   │   └── mcp_echo.py        # MCP protocol probe
│   │   └── policies/              # Policy definitions
│   │       └── default_policy.yaml
│   ├── services/                  # External service clients
│   │   ├── matrix_hub_client.py   # Matrix Hub API client
│   │   ├── matrix_ai_client.py    # matrix-ai API client
│   │   └── jobs.py                # Job queue service
│   └── runner/                    # Standalone workers
│       └── autopilot_worker.py    # Headless Autopilot runner
├── tests/                         # Test suite
│   ├── test_autopilot_smoke.py    # Smoke tests
│   └── __init__.py                # Test package initialization
├── configs/                       # Configuration files
│   ├── settings.yaml              # Default settings
│   └── .env.example               # Environment template
├── infra/                         # Infrastructure as code
│   └── docker/                    # Docker deployment
│       ├── Dockerfile             # Multi-stage build
│       └── compose.yaml           # Docker Compose stack
├── pyproject.toml                 # Project metadata & dependencies
├── Makefile                       # Development automation
├── README.md                      # This file
└── LICENSE                        # Apache 2.0 license
```

### Development Workflow

```bash
# Install development dependencies
make dev

# Run tests with coverage
make test

# Run linting
make lint

# Auto-format code
make fmt

# Type checking
make typecheck

# Run all checks (lint + typecheck + test)
make check

# Run full CI pipeline
make ci

# Install pre-commit hooks
make pre-commit-install
```

### Code Quality Standards

- **Style Guide**: PEP 8 compliance enforced via Ruff
- **Type Hints**: Full type annotations checked with MyPy
- **Docstrings**: Google-style docstrings for all public APIs
- **Testing**: Pytest with async support and coverage > 80%
- **Security**: Bandit security checks via Ruff

---

## Safety & Security

Matrix Guardian is designed with safety as a primary concern:

1. **Sandbox-First Execution**
   - Short timeouts for all external requests
   - Strict host allowlists
   - Resource limits (CPU, memory)

2. **Policy-Based Governance**
   - All actions flow through policy gate
   - Risk-based decision making
   - HITL enforcement by default

3. **Input Validation**
   - Pydantic schema validation
   - SQL injection prevention
   - XSS protection

4. **Audit Trail**
   - All operations logged with structured JSON
   - Event tracking in database
   - Idempotency key support

5. **Security Scanning**
   - Regular dependency audits
   - Automated security checks in CI/CD

---

## Testing

```bash
# Run all tests with coverage
make test

# Run quick tests (no coverage)
make test-quick

# Run unit tests only
make test-unit

# Run integration tests only
make test-integration

# Generate detailed coverage report
make coverage
```

Test markers:
- `@pytest.mark.unit` - Unit tests (fast, isolated)
- `@pytest.mark.integration` - Integration tests (require external services)
- `@pytest.mark.slow` - Slow tests (can be skipped during development)

---

## Deployment

### Production Checklist

- [ ] Set strong `API_TOKEN` and `DATABASE_URL`
- [ ] Configure `MATRIXHUB_API_BASE` and `MATRIX_AI_BASE`
- [ ] Review and customize `default_policy.yaml`
- [ ] Set `AUTOPILOT_SAFE_MODE=true` for initial deployment
- [ ] Configure structured logging (`LOG_LEVEL=INFO`)
- [ ] Set up database backups
- [ ] Configure monitoring and alerting
- [ ] Review security settings in `config.py`
- [ ] Test HITL approval workflows
- [ ] Run full test suite: `make ci`

### Environment Variables for Production

```bash
# Security
API_TOKEN=<strong-secret-token>
JWT_PUBLIC_KEY_PEM=<public-key-for-jwt-validation>

# Database (use connection pooling)
DATABASE_URL=postgresql://user:pass@db:5432/guardian?pool_size=20

# Logging
LOG_LEVEL=INFO

# Autopilot (start conservatively)
AUTOPILOT_ENABLED=true
AUTOPILOT_SAFE_MODE=true
AUTOPILOT_INTERVAL_SEC=300

# Resource limits
SANDBOX_CPU_LIMIT=2
SANDBOX_MEM_MB=1024
SANDBOX_TIMEOUT_SEC=30
```

---

## Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies (`make dev`)
4. Make your changes with proper type hints and docstrings
5. Run tests and linting (`make check`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to your branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Code Standards

- Follow PEP 8 (enforced by Ruff)
- Add type hints to all functions
- Write Google-style docstrings
- Maintain test coverage > 80%
- Pass all CI checks

---

## License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.

```
Copyright (c) 2025 Ruslan Magana Vsevolodovna

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

---

## Author

**Ruslan Magana**

- Website: [ruslanmv.com](https://ruslanmv.com)
- GitHub: [@ruslanmv](https://github.com/ruslanmv)
- Email: contact@ruslanmv.com

---

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework
- Uses [LangGraph](https://github.com/langchain-ai/langgraph) - For agent orchestration
- Powered by [UV](https://github.com/astral-sh/uv) - Fast Python package installer
- Code quality enforced by [Ruff](https://github.com/astral-sh/ruff) - Ultra-fast linter

---

## Roadmap

- [ ] Advanced policy engine with ML-based risk scoring
- [ ] Web dashboard for monitoring and control
- [ ] Extended MCP protocol support
- [ ] Multi-region deployment support
- [ ] Advanced telemetry and observability
- [ ] Plugin system for custom health checks
- [ ] GraphQL API support

---

<div align="center">

**Matrix Guardian** - *Autonomous Intelligence for Distributed Systems*

Made with ❤️ by [Ruslan Magana](https://ruslanmv.com)

</div>
