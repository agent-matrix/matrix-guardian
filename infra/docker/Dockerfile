# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates tini && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY pyproject.toml /app/
RUN pip install --upgrade pip && pip install .

# Copy the rest of the application code
COPY src /app/src
COPY configs /app/configs
COPY scripts /app/scripts

# Expose the port the app runs on
EXPOSE 8000

# Use Tini as the entrypoint to properly handle signals
ENTRYPOINT ["/usr/bin/tini", "--"]

# Run the application
CMD ["uvicorn", "guardian.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
