#!/bin/bash
echo "======================================================================="
echo "🔍 DIAGNOSTIC COMPLET DU SERVEUR FITGANG.FR"
echo "======================================================================="

echo -e "\n📁 1. DANS QUEL RÉPERTOIRE SUIS-JE?"
pwd
echo "   Utilisateur: $(whoami)"

echo -e "\n📂 2. VÉRIFICATION DES DEUX EMPLACEMENTS POSSIBLES"
echo "   A. ~/public_html/saas existe?"
if [ -d ~/public_html/saas ]; then
    echo "      ✅ OUI - ~/public_html/saas existe"
    cd ~/public_html/saas
    echo "      Dernier commit:"
    git log -1 --oneline 2>&1 || echo "      ❌ Pas un repository git"
else
    echo "      ❌ NON - ~/public_html/saas n'existe pas"
fi

echo -e "\n   B. ~/fitgang_app/saas existe?"
if [ -d ~/fitgang_app/saas ]; then
    echo "      ✅ OUI - ~/fitgang_app/saas existe"
    cd ~/fitgang_app/saas
    echo "      Dernier commit:"
    git log -1 --oneline 2>&1 || echo "      ❌ Pas un repository git"
else
    echo "      ❌ NON - ~/fitgang_app/saas n'existe pas"
fi

echo -e "\n🎯 3. OÙ EST PASSENGER_WSGI.PY?"
echo "   A. Dans ~/public_html/saas?"
if [ -f ~/public_html/saas/passenger_wsgi.py ]; then
    echo "      ✅ TROUVÉ - ~/public_html/saas/passenger_wsgi.py"
    echo "      Contenu (10 premières lignes):"
    head -10 ~/public_html/saas/passenger_wsgi.py | sed 's/^/         /'
else
    echo "      ❌ PAS TROUVÉ"
fi

echo -e "\n   B. Dans ~/fitgang_app/saas?"
if [ -f ~/fitgang_app/saas/passenger_wsgi.py ]; then
    echo "      ✅ TROUVÉ - ~/fitgang_app/saas/passenger_wsgi.py"
    echo "      Contenu (10 premières lignes):"
    head -10 ~/fitgang_app/saas/passenger_wsgi.py | sed 's/^/         /'
else
    echo "      ❌ PAS TROUVÉ"
fi

echo -e "\n   C. Ailleurs?"
find ~ -name "passenger_wsgi.py" -type f 2>/dev/null | while read f; do
    echo "      🔍 Trouvé: $f"
done

echo -e "\n🐍 4. PROCESSUS PYTHON EN COURS"
echo "   Processus Passenger/Python actifs:"
ps aux | grep -E "passenger|python" | grep -v grep | head -10 | sed 's/^/      /'

echo -e "\n📝 5. TEMPLATE BLOG/INDEX.HTML - QUE CONTIENT-IL?"
if [ -f ~/fitgang_app/saas/fitgang_app/templates/blog/index.html ]; then
    echo "   📂 Dans ~/fitgang_app/saas:"
    grep -n "col-lg" ~/fitgang_app/saas/fitgang_app/templates/blog/index.html | head -5 | sed 's/^/      /'
elif [ -f ~/public_html/saas/fitgang_app/templates/blog/index.html ]; then
    echo "   📂 Dans ~/public_html/saas:"
    grep -n "col-lg" ~/public_html/saas/fitgang_app/templates/blog/index.html | head -5 | sed 's/^/      /'
else
    echo "   ❌ TEMPLATE NON TROUVÉ!"
fi

echo -e "\n🔄 6. FICHIER TMP/RESTART.TXT"
if [ -f ~/fitgang_app/saas/tmp/restart.txt ]; then
    echo "   ✅ ~/fitgang_app/saas/tmp/restart.txt existe"
    ls -la ~/fitgang_app/saas/tmp/restart.txt | sed 's/^/      /'
elif [ -f ~/public_html/saas/tmp/restart.txt ]; then
    echo "   ✅ ~/public_html/saas/tmp/restart.txt existe"
    ls -la ~/public_html/saas/tmp/restart.txt | sed 's/^/      /'
else
    echo "   ❌ tmp/restart.txt non trouvé"
fi

echo -e "\n🌐 7. CONFIGURATION APACHE/PASSENGER"
echo "   Recherche de fichiers .htaccess:"
find ~ -name ".htaccess" -type f 2>/dev/null | head -5 | while read f; do
    echo "      🔍 $f"
    echo "         Contenu:"
    cat "$f" | sed 's/^/            /'
done

echo -e "\n📊 8. GIT STATUS DANS LE RÉPERTOIRE PRINCIPAL"
if [ -d ~/fitgang_app/saas/.git ]; then
    cd ~/fitgang_app/saas
    echo "   📂 Dans ~/fitgang_app/saas:"
    echo "      Branche actuelle:"
    git branch | sed 's/^/         /'
    echo "      Status:"
    git status -s | sed 's/^/         /'
    echo "      Dernier commit:"
    git log -1 --oneline | sed 's/^/         /'
elif [ -d ~/public_html/saas/.git ]; then
    cd ~/public_html/saas
    echo "   📂 Dans ~/public_html/saas:"
    echo "      Branche actuelle:"
    git branch | sed 's/^/         /'
    echo "      Status:"
    git status -s | sed 's/^/         /'
    echo "      Dernier commit:"
    git log -1 --oneline | sed 's/^/         /'
fi

echo -e "\n🖼️ 9. IMAGES BLOG - EXISTENT-ELLES?"
if [ -d ~/fitgang_app/saas/uploads/blog ]; then
    echo "   📂 Dans ~/fitgang_app/saas/uploads/blog:"
    ls -lah ~/fitgang_app/saas/uploads/blog | head -10 | sed 's/^/      /'
elif [ -d ~/public_html/saas/uploads/blog ]; then
    echo "   📂 Dans ~/public_html/saas/uploads/blog:"
    ls -lah ~/public_html/saas/uploads/blog | head -10 | sed 's/^/      /'
else
    echo "   ❌ Aucun dossier uploads/blog trouvé"
fi

echo -e "\n⚙️ 10. CONFIG.PY - UPLOAD_FOLDER"
if [ -f ~/fitgang_app/saas/config.py ]; then
    echo "   📂 Dans ~/fitgang_app/saas/config.py:"
    grep -n "UPLOAD_FOLDER" ~/fitgang_app/saas/config.py | sed 's/^/      /'
elif [ -f ~/public_html/saas/config.py ]; then
    echo "   📂 Dans ~/public_html/saas/config.py:"
    grep -n "UPLOAD_FOLDER" ~/public_html/saas/config.py | sed 's/^/      /'
fi

echo -e "\n======================================================================="
echo "🎯 CONCLUSION - CE QUE PASSENGER UTILISE VRAIMENT"
echo "======================================================================="

# Test de démarrage Python pour voir le chemin réel
if [ -d ~/fitgang_app/saas ]; then
    cd ~/fitgang_app/saas
    echo "Test depuis ~/fitgang_app/saas:"
    python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from app import create_app
    app = create_app('production')
    print('   ✅ App démarre depuis: ~/fitgang_app/saas')
    print(f'   Upload folder: {app.config.get(\"UPLOAD_FOLDER\", \"NON DÉFINI\")}')
except Exception as e:
    print(f'   ❌ ERREUR: {e}')
" 2>&1 | sed 's/^/   /'
fi

echo -e "\n======================================================================="
echo "📋 ENVOIE-MOI TOUTE CETTE SORTIE!"
echo "======================================================================="
