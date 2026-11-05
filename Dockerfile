FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt greenlet

# Copy backend application source
COPY backend/ .

# Ensure seed script runs if database does not exist, then start server
EXPOSE 8000

CMD ["sh", "-c", "python -m app.infrastructure.db.seed && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
