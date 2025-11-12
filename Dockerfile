# --- Étape 1 : Image de base ---
FROM python:3.11-slim

# --- Étape 2 : Variables d'environnement ---
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# --- Étape 3 : Installer Git ---
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# --- Étape 4 : Cloner ton dépôt GitHub public ---
WORKDIR /app
RUN git clone --depth=1 https://github.com/goldendatahub/GoldenQuizz.git .

# --- Étape 5 : Installer les dépendances Python ---
RUN pip install --upgrade pip && pip install -r requirements.txt

# --- Étape 6 : Exposer le port NiceGUI ---
EXPOSE 8080

# --- Étape 7 : Commande de démarrage ---
CMD ["python", "main.py"]
