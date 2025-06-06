#!/bin/bash

# Make this file executable: chmod +x init-open-space-docs.sh
# Run it with: ./init-open-space-docs.sh

# Crée le projet
mkdocs new OpenSpace
cd OpenSpace || exit

# Crée les fichiers supplémentaires
cat > docs/installation.md <<EOL
# Installation

Instructions pour installer et lancer le projet OpenSpace.
EOL

cat > docs/architecture.md <<EOL
# Architecture

Vue d'ensemble de l'architecture du projet.
EOL

cat > docs/api.md <<EOL
# API

Documentation des points d'API disponibles.
EOL

# Écrase le mkdocs.yml avec un menu customisé
cat > mkdocs.yml <<EOL
site_name: OpenSpace
theme:
  name: material

nav:
  - Accueil: index.md
  - Installation: installation.md
  - Architecture: architecture.md
  - API: api.md
EOL

# Démarre le serveur local
mkdocs serve
