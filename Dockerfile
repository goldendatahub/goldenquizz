FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Installer Git et uv (gestionnaire Python moderne)
RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*
RUN pip install uv

WORKDIR /app

# Cloner ton dépôt GitHub public
RUN git clone --depth=1 https://github.com/goldendatahub/goldenquizz.git .

# Installer les dépendances avec uv
RUN uv pip install -e .

EXPOSE 8080

# Démarrer ton app
CMD ["uv", "run", "python", "-m", "goldenquizz.server"]
