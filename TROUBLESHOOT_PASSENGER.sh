#!/bin/bash
# Script de dépannage Passenger pour forcer le rechargement
# À exécuter sur wrbh3411@down

echo "═══════════════════════════════════════════════════════"
echo "  TROUBLESHOOTING PASSENGER - FitGang"
echo "═══════════════════════════════════════════════════════"
echo ""

# 1. Vérifier où on est
echo "1. Vérification du répertoire actuel:"
pwd
echo ""

# 2. Vérifier les fichiers récents
echo "2. Date de modification de passenger_wsgi.py:"
ls -lh passenger_wsgi.py
echo ""

echo "3. Date de modification du template profile:"
ls -lh fitgang_app/templates/profile/index.html
echo ""

# 4. Vérifier le contenu du template (premières lignes)
echo "4. Premières lignes de profile/index.html:"
head -20 fitgang_app/templates/profile/index.html | grep -E "(extends|:root|apple-blue)"
echo ""

# 5. Nettoyer TOUS les fichiers cache Python de manière agressive
echo "5. Nettoyage AGRESSIF du cache Python..."
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type f -name "*.pyo" -delete 2>/dev/null
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null
echo "   ✓ Cache Python nettoyé"
echo ""

# 6. Supprimer le dossier tmp et le recréer
echo "6. Recréation du dossier tmp..."
rm -rf tmp
mkdir -p tmp/pids
echo "   ✓ Dossier tmp recréé"
echo ""

# 7. Modifier passenger_wsgi.py pour forcer rechargement
echo "7. Ajout timestamp à passenger_wsgi.py..."
TIMESTAMP=$(date +%Y-%m-%d_%H:%M:%S)
if grep -q "Force reload timestamp:" passenger_wsgi.py; then
    sed -i "s/Force reload timestamp:.*/Force reload timestamp: $TIMESTAMP/" passenger_wsgi.py
else
    sed -i "2i# Force reload timestamp: $TIMESTAMP" passenger_wsgi.py
fi
echo "   ✓ Timestamp ajouté: $TIMESTAMP"
echo ""

# 8. Modifier app.py aussi
echo "8. Ajout timestamp à app.py..."
if grep -q "Force reload - Updated:" app.py; then
    sed -i "s/Force reload - Updated:.*/Force reload - Updated: $TIMESTAMP/" app.py
else
    sed -i "2i# Force reload - Updated: $TIMESTAMP" app.py
fi
echo "   ✓ Timestamp ajouté"
echo ""

# 9. Créer tmp/restart.txt avec contenu
echo "9. Création tmp/restart.txt avec timestamp..."
echo "Restart requested at: $TIMESTAMP" > tmp/restart.txt
echo "   ✓ tmp/restart.txt créé"
echo ""

# 10. Afficher les process Passenger actuels
echo "10. Processus Passenger actuels:"
ps aux | grep -i passenger | grep -v grep
echo ""

echo "═══════════════════════════════════════════════════════"
echo "  ÉTAPES SUIVANTES À FAIRE MANUELLEMENT:"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "1. Allez dans cPanel → Setup Python App"
echo ""
echo "2. Trouvez votre application FitGang"
echo ""
echo "3. Cliquez sur 'STOP APPLICATION' (pas restart!)"
echo ""
echo "4. Attendez 30 secondes"
echo ""
echo "5. Cliquez sur 'START APPLICATION'"
echo ""
echo "6. Attendez 30 secondes"
echo ""
echo "7. Testez: https://fitgang.fr/profile"
echo "   (Ouvrez en navigation privée + Ctrl+F5)"
echo ""
echo "8. Vérifiez la source HTML - cherchez '--apple-blue'"
echo ""
echo "═══════════════════════════════════════════════════════"
