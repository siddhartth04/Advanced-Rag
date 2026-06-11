FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml .
COPY src ./src
COPY data ./data

# Install Python dependencies using pip (uv not available in Docker)
RUN pip install --no-cache-dir -e .

# Expose API port
EXPOSE 8000

# Run API server
CMD ["uvicorn", "rag.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
