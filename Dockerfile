# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Installer les dépendances de compilation
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements et installer
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Installer uniquement les dépendances runtime
RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copier les dependencies du builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copier le code de l'app
COPY backend/ .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Exposer le port
EXPOSE 8000

# Variables d'environnement par défaut
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production

# Lancer l'app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
