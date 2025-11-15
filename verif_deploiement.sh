#!/bin/bash
echo "======================================================================"
echo "VÉRIFICATION COMPLÈTE DU DÉPLOIEMENT"
echo "======================================================================"

echo -e "\n1. Dernier commit déployé:"
git log -1 --oneline

echo -e "\n2. Vérification du template blog/index.html:"
if grep -q "col-lg-4" fitgang_app/templates/blog/index.html; then
    echo "   ✅ Template utilise col-lg-4 (3 cartes par ligne)"
else
    echo "   ❌ Template utilise encore col-lg-6 (2 cartes par ligne)"
    echo "   → Il faut faire: git pull"
fi

echo -e "\n3. Processus Python Passenger actifs:"
ps aux | grep -i "passenger\|python" | grep -v grep | head -5

echo -e "\n4. Dernière modification de tmp/restart.txt:"
if [ -f tmp/restart.txt ]; then
    ls -la tmp/restart.txt
    echo "   Contenu:"
    cat tmp/restart.txt
else
    echo "   ❌ tmp/restart.txt n'existe pas"
fi

echo -e "\n5. Test des imports Python:"
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from app import create_app
    app = create_app('production')
    print('   ✅ Application Flask peut démarrer')
    print(f'   Debug mode: {app.debug}')
    print(f'   Upload folder: {app.config[\"UPLOAD_FOLDER\"]}')
except Exception as e:
    print(f'   ❌ ERREUR: {e}')
"

echo -e "\n======================================================================"
echo "Si tout est ✅ mais le site ne change pas:"
echo "1. Va dans cPanel → Setup Python App"
echo "2. Vérifie que l'app est RUNNING"
echo "3. Si elle est Running, fais RESTART (cette fois Restart devrait marcher)"
echo "4. Sinon, fais START"
echo "======================================================================"
