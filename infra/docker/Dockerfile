# Multi-stage build for production-ready Matrix Guardian
# Stage 1: Builder
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /build

# Copy only dependency files first (for better caching)
COPY pyproject.toml README.md ./
COPY src ./src

# Install Python dependencies in a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip wheel setuptools && \
    pip install --no-cache-dir .

# Stage 2: Runtime
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    tini \
    libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN groupadd -r guardian && useradd -r -g guardian guardian

# Set the working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY --chown=guardian:guardian src ./src
COPY --chown=guardian:guardian configs ./configs
COPY --chown=guardian:guardian scripts ./scripts

# Create necessary directories with proper permissions
RUN mkdir -p /app/logs /app/data && \
    chown -R guardian:guardian /app

# Switch to non-root user
USER guardian

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose the port the app runs on
EXPOSE 8000

# Use Tini as the entrypoint to properly handle signals
ENTRYPOINT ["/usr/bin/tini", "--"]

# Run the application with optimized settings
CMD ["uvicorn", "guardian.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--proxy-headers", \
     "--workers", "2", \
     "--log-level", "info"]
