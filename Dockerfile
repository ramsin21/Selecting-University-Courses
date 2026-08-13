# ==========================================
# Backend - Multi-stage Dockerfile for FastAPI
# ==========================================

# ---------- Builder Stage ----------
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Install build dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies to user directory
RUN pip install --no-cache-dir --user -r requirements.txt


# ---------- Runtime Stage ----------
FROM python:3.11-slim AS runtime

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/home/appuser/.local/bin:$PATH

# Create non-root user and group
RUN groupadd -r appuser && useradd -r -g appuser -m -d /home/appuser appuser

# Set working directory
WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser . .

# Create data directory for JSON storage with proper permissions
RUN mkdir -p /app/data/files && chown -R appuser:appuser /app/data

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/debug/storage || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]