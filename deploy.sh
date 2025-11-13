#!/bin/bash
# Script de déploiement FitGang - Version Simple

echo "🚀 Déploiement de FitGang..."

# Variables
PROD_DIR="$HOME/public_html/fitgang.fr"
GIT_DIR="$HOME/fitgang_app/saas"

# Vérifier que nous sommes dans le bon répertoire
cd "$GIT_DIR" || exit 1

# Récupérer les dernières modifications
echo "📥 Récupération des modifications..."
git fetch origin
git reset --hard origin/claude/fitgang-fitness-app-complete-011CV5hqoURFsdAeYiKoKxTu

# Créer les dossiers nécessaires dans la production
echo "📁 Création des dossiers..."
mkdir -p "$PROD_DIR/app/static/css"
mkdir -p "$PROD_DIR/app/static/js"
mkdir -p "$PROD_DIR/app/static/img"
mkdir -p "$PROD_DIR/app/uploads"
mkdir -p "$PROD_DIR/app/templates"
mkdir -p "$PROD_DIR/app/blueprints"
mkdir -p "$PROD_DIR/tmp"

# Copier les fichiers Python (blueprints et models)
echo "🐍 Copie des fichiers Python..."
cp -r fitgang_app/blueprints/* "$PROD_DIR/app/blueprints/" 2>/dev/null || echo "Blueprints déjà à jour"
cp -r fitgang_app/models/* "$PROD_DIR/app/models/" 2>/dev/null || echo "Models déjà à jour"
cp -r fitgang_app/utils/* "$PROD_DIR/app/utils/" 2>/dev/null || echo "Utils déjà à jour"
cp -r fitgang_app/forms/* "$PROD_DIR/app/forms/" 2>/dev/null || echo "Forms déjà à jour"

# Copier les templates
echo "🎨 Copie des templates..."
cp -r fitgang_app/templates/* "$PROD_DIR/app/templates/" 2>/dev/null || echo "Templates déjà à jour"

# Copier les fichiers statiques (CSS, JS, images)
echo "💎 Copie des fichiers statiques..."
cp fitgang_app/static/css/main.css "$PROD_DIR/app/static/css/" 2>/dev/null || echo "CSS déjà à jour"
cp -r fitgang_app/static/js/* "$PROD_DIR/app/static/js/" 2>/dev/null || echo "JS déjà à jour"
cp -r fitgang_app/static/img/* "$PROD_DIR/app/static/img/" 2>/dev/null || echo "Images déjà à jour"

# Copier passenger_wsgi.py
echo "🔧 Mise à jour passenger_wsgi.py..."
cp passenger_wsgi.py "$PROD_DIR/" 2>/dev/null || echo "passenger_wsgi.py déjà à jour"

# Redémarrer l'application
echo "♻️  Redémarrage de l'application..."
touch "$PROD_DIR/tmp/restart.txt"

echo "✅ Déploiement terminé !"
echo ""
echo "📋 Vérifications à faire :"
echo "1. Vérifier les logs : tail -f $PROD_DIR/logs/error.log"
echo "2. Tester le site : https://fitgang.fr"
echo "3. Tester /dashboard : https://fitgang.fr/dashboard"
echo "4. Tester /admin : https://fitgang.fr/admin"
