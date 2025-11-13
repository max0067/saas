#!/bin/bash
#############################################
# DÉPLOIEMENT FITGANG - ULTRA SIMPLE
# Copie/colle juste ces commandes une par une
#############################################

echo "========================================="
echo "🚀 DÉPLOIEMENT FITGANG"
echo "========================================="
echo ""

# 1. Aller dans le dossier git
echo "📁 Étape 1/5: Navigation vers le dossier git..."
cd ~/fitgang_app/saas || { echo "❌ Erreur: dossier git introuvable"; exit 1; }
echo "✅ Dans le bon dossier"
echo ""

# 2. Récupérer les modifications
echo "📥 Étape 2/5: Récupération des modifications..."
git fetch origin
git reset --hard origin/claude/fitgang-fitness-app-complete-011CV5hqoURFsdAeYiKoKxTu
echo "✅ Code mis à jour"
echo ""

# 3. Copier vers la production
echo "📋 Étape 3/5: Copie des fichiers..."

# Fichiers Python corrigés
cp fitgang_app/blueprints/admin/__init__.py ~/public_html/fitgang.fr/app/blueprints/admin/
cp fitgang_app/blueprints/admin/products.py ~/public_html/fitgang.fr/app/blueprints/admin/
cp fitgang_app/blueprints/dashboard.py ~/public_html/fitgang.fr/app/blueprints/
cp fitgang_app/utils/uploads.py ~/public_html/fitgang.fr/app/utils/

# Templates corrigés
cp -r fitgang_app/templates/admin/blog.html ~/public_html/fitgang.fr/app/templates/admin/ 2>/dev/null
cp -r fitgang_app/templates/admin/blog_form.html ~/public_html/fitgang.fr/app/templates/admin/ 2>/dev/null
cp -r fitgang_app/templates/blog/list.html ~/public_html/fitgang.fr/app/templates/blog/ 2>/dev/null
cp -r fitgang_app/templates/shop/catalog.html ~/public_html/fitgang.fr/app/templates/shop/ 2>/dev/null

# CSS avec nouvelle couleur
cp fitgang_app/static/css/main.css ~/public_html/fitgang.fr/app/static/css/

echo "✅ Fichiers copiés"
echo ""

# 4. Créer les dossiers uploads si besoin
echo "📂 Étape 4/5: Vérification des dossiers..."
mkdir -p ~/public_html/fitgang.fr/app/uploads/products
mkdir -p ~/public_html/fitgang.fr/tmp
chmod 755 ~/public_html/fitgang.fr/app/uploads
chmod 755 ~/public_html/fitgang.fr/app/uploads/products
echo "✅ Dossiers créés"
echo ""

# 5. Redémarrer l'application
echo "♻️  Étape 5/5: Redémarrage de l'application..."
touch ~/public_html/fitgang.fr/tmp/restart.txt
echo "✅ Application redémarrée"
echo ""

echo "========================================="
echo "✨ DÉPLOIEMENT TERMINÉ !"
echo "========================================="
echo ""
echo "🌐 TESTE CES URLS :"
echo "1. https://fitgang.fr"
echo "2. https://fitgang.fr/dashboard"
echo "3. https://fitgang.fr/admin"
echo "4. https://fitgang.fr/admin/products/create"
echo ""
echo "⚠️  SI ERREUR, VOIR LES LOGS :"
echo "tail -50 ~/public_html/fitgang.fr/logs/error.log"
echo ""
