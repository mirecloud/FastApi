# Étape 1 : utiliser une image Python officielle
FROM python:3.12-slim

# Étape 2 : définir un répertoire de travail
WORKDIR /app

# Étape 3 : copier les fichiers nécessaires
COPY requirements.txt .

# Étape 4 : installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : copier ton code FastAPI (le dossier SqlAlchemy)
COPY SqlAlchemy ./SqlAlchemy

# Étape 6 : exposer le port
EXPOSE 8000

# Étape 7 : lancer FastAPI
CMD ["fastapi", "dev", "SqlAlchemy/main.py"]

