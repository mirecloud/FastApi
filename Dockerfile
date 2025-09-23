# Étape 1 : utiliser une image Python officielle
FROM python:3.12.11

# Étape 2 : définir un répertoire de travail
COPY SqlAlchemy ./SqlAlchemy

# Étape 3 : copier les fichiers nécessaires
WORKDIR ./SqlAlchemy
# Étape 4 : installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : copier ton code FastAPI (le dossier SqlAlchemy)

# Étape 6 : exposer le port
EXPOSE 8000

# Étape 7 : lancer FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
