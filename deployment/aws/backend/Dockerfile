# ========================================================
# Nexus AI Backend — Production Multi-Stage Dockerfile
# Optimized for AWS App Runner / ECS / Render / Cloud Run
# ========================================================

# --------------------------------------------------------
# Stage 1: Build & Dependencies
# --------------------------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv for ultra-fast dependency resolution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency specifications
COPY pyproject.toml uv.lock ./

# Sync dependencies to virtual environment
RUN uv venv /app/.venv && \
    uv pip sync --no-cache

# --------------------------------------------------------
# Stage 2: Runtime Image
# --------------------------------------------------------
FROM python:3.12-slim AS runner

WORKDIR /app

# Create non-root user for security compliance
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -s /bin/bash -m appuser

# Copy virtualenv and application code from builder
COPY --from=builder /app/.venv /app/.venv
COPY ./app ./app
COPY ./pyproject.toml ./

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Ensure non-root ownership
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

# Healthcheck endpoint verification
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start FastAPI application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
