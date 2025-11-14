#!/bin/bash
echo "======================================================================"
echo "VÉRIFICATION DES FICHIERS BLOG SUR LE SERVEUR"
echo "======================================================================"

echo -e "\n1. Fichier text_filters.py existe?"
if [ -f "fitgang_app/utils/text_filters.py" ]; then
    echo "   ✅ OUI - fitgang_app/utils/text_filters.py existe"
    echo "   Premières lignes:"
    head -5 fitgang_app/utils/text_filters.py
else
    echo "   ❌ NON - fitgang_app/utils/text_filters.py N'EXISTE PAS!"
    echo "   → Il faut faire: git pull"
fi

echo -e "\n2. Le filtre est-il enregistré dans __init__.py?"
if grep -q "register_filters" fitgang_app/__init__.py; then
    echo "   ✅ OUI - register_filters trouvé dans __init__.py"
    grep -A2 "register_filters" fitgang_app/__init__.py
else
    echo "   ❌ NON - register_filters N'EST PAS dans __init__.py"
    echo "   → Il faut faire: git pull"
fi

echo -e "\n3. Le template blog/post.html utilise-t-il smart_content?"
if grep -q "smart_content" fitgang_app/templates/blog/post.html; then
    echo "   ✅ OUI - smart_content trouvé dans blog/post.html"
    grep "smart_content" fitgang_app/templates/blog/post.html
else
    echo "   ❌ NON - Le template utilise encore {{ post.content|safe }}"
    grep "post.content" fitgang_app/templates/blog/post.html
    echo "   → Il faut faire: git pull"
fi

echo -e "\n4. Dernier commit git:"
git log -1 --oneline

echo -e "\n======================================================================"
echo "RÉSUMÉ"
echo "======================================================================"
echo "Si tu vois des ❌, fais:"
echo "   git pull origin claude/saccra-fitgang-complete-overhaul-0186TzukF7j2eifnrXaNd51n"
echo ""
echo "Puis OBLIGATOIREMENT dans cPanel:"
echo "   Setup Python App → STOP APPLICATION → Attendre 1 min → START"
echo "======================================================================"
