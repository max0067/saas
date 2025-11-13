#!/bin/bash
# Script pour réinitialiser la base de données FitGang

echo "🔄 Nettoyage de la base de données..."

# Supprimer l'ancienne base de données
if [ -f "fitgang.db" ]; then
    rm -f fitgang.db
    echo "✅ Ancienne base de données supprimée"
fi

# Supprimer le dossier migrations si existant
if [ -d "migrations" ]; then
    echo "⚠️  Suppression du dossier migrations existant..."
    rm -rf migrations
fi

# Initialiser les migrations
echo "📦 Initialisation des migrations..."
python3 -m flask db init

# Créer la migration initiale
echo "📝 Création de la migration..."
python3 -m flask db migrate -m "Initial migration"

# Appliquer la migration
echo "⚡ Application de la migration..."
python3 -m flask db upgrade

# Charger les données de test
echo "📊 Chargement des données de test..."
python3 scripts/load_fixtures.py

echo ""
echo "✅ Base de données réinitialisée avec succès!"
echo ""
echo "Comptes de test créés :"
echo "  👤 Admin: admin@fitgang.fr / admin123"
echo "  👤 User:  john@example.com / password123"
echo ""
echo "🎁 Code cadeau de test: WELCOME2024"
