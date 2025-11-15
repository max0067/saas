#!/bin/bash
set -e

echo "=========================================================================="
echo "🔧 CORRECTION AUTOMATIQUE COMPLÈTE DE PASSENGER"
echo "=========================================================================="

echo -e "\n1️⃣ Désactivation de l'ancienne application flask-version..."
if [ -d ~/public_html/flask-version ]; then
    mv ~/public_html/flask-version ~/public_html/flask-version.DISABLED_$(date +%Y%m%d_%H%M%S)
    echo "   ✅ Ancienne app renommée"
else
    echo "   ℹ️  Pas d'ancienne app à désactiver"
fi

echo -e "\n2️⃣ Correction du .htaccess RACINE..."
cat > ~/public_html/.htaccess << 'HTACCESS_EOF'
PassengerEnabled On
PassengerPython /usr/bin/python3
PassengerAppRoot /home/wrbh3411/fitgang_app/saas
PassengerStartupFile passenger_wsgi.py
PassengerAppType wsgi

RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
HTACCESS_EOF
echo "   ✅ .htaccess racine corrigé"

echo -e "\n3️⃣ Correction du .htaccess fitgang.fr..."
cat > ~/public_html/fitgang.fr/.htaccess << 'HTACCESS_EOF2'
PassengerEnabled On
PassengerAppRoot /home/wrbh3411/fitgang_app/saas
PassengerBaseURI /
PassengerPython /usr/bin/python3
PassengerStartupFile passenger_wsgi.py
PassengerAppType wsgi
PassengerFriendlyErrorPages off

PassengerMaxPoolSize 6
PassengerMinInstances 1
PassengerMaxInstancesPerApp 0
PassengerPoolIdleTime 300
PassengerMaxPreloaderIdleTime 0

RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript application/json
</IfModule>

<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/gif "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
</IfModule>

<FilesMatch "\.(env|db|sqlite|py|pyc)$">
    Order allow,deny
    Deny from all
</FilesMatch>
HTACCESS_EOF2
echo "   ✅ .htaccess fitgang.fr corrigé"

echo -e "\n4️⃣ Vérification du passenger_wsgi.py..."
if [ ! -f ~/fitgang_app/saas/passenger_wsgi.py ]; then
    echo "   ⚠️  passenger_wsgi.py manquant, création..."
    cat > ~/fitgang_app/saas/passenger_wsgi.py << 'WSGI_EOF'
#!/usr/bin/env python
import sys
import os

# Add application directory to path
INTERP = "/usr/bin/python3"
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, os.path.dirname(__file__))

# Set environment variables
os.environ['FLASK_ENV'] = 'production'

# Import and create the Flask application
from app import create_app
application = create_app('production')
WSGI_EOF
    chmod +x ~/fitgang_app/saas/passenger_wsgi.py
    echo "   ✅ passenger_wsgi.py créé"
else
    echo "   ✅ passenger_wsgi.py existe déjà"
fi

echo -e "\n5️⃣ Nettoyage des caches Python..."
find ~/fitgang_app/saas -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find ~/fitgang_app/saas -type f -name "*.pyc" -delete 2>/dev/null || true
echo "   ✅ Caches nettoyés"

echo -e "\n6️⃣ Suppression complète de tmp/restart.txt..."
rm -rf ~/fitgang_app/saas/tmp
echo "   ✅ tmp/ supprimé"

echo -e "\n7️⃣ MASSACRE de TOUS les processus Python..."
pkill -9 -u $USER python 2>/dev/null || true
sleep 3
pkill -9 -u $USER python3 2>/dev/null || true
sleep 3
echo "   ✅ Tous les processus Python tués"

echo -e "\n8️⃣ Recréation de tmp/restart.txt..."
mkdir -p ~/fitgang_app/saas/tmp
touch ~/fitgang_app/saas/tmp/restart.txt
echo "   ✅ tmp/restart.txt créé"

echo -e "\n9️⃣ Attente du redémarrage de Passenger..."
sleep 15

echo -e "\n🔍 Vérification des processus Python..."
ps aux | grep python | grep -v grep | grep -v cloudlinux || echo "   ℹ️  Aucun processus Python actif (normal juste après le kill)"

echo -e "\n=========================================================================="
echo "✅ CORRECTION TERMINÉE!"
echo "=========================================================================="
echo ""
echo "MAINTENANT:"
echo "1. Attends 30 secondes que Passenger redémarre"
echo "2. Va sur: https://fitgang.fr/blog"
echo "3. Fais Ctrl+Shift+R pour vider le cache"
echo ""
echo "SI ÇA NE MARCHE TOUJOURS PAS:"
echo "Tu DOIS aller dans cPanel → Setup Python App et:"
echo "  - SUPPRIMER l'application existante"
echo "  - RECRÉER une nouvelle avec Application root: /home/wrbh3411/fitgang_app/saas"
echo "=========================================================================="
echo ""
echo "Vérification dans 30 secondes..."
sleep 30

echo -e "\n🔍 Processus Python après redémarrage:"
ps aux | grep python | grep -v grep | grep -v cloudlinux

echo -e "\n🔍 Vérification .htaccess racine:"
grep "PassengerAppRoot" ~/public_html/.htaccess

echo -e "\n🔍 Test de l'application:"
cd ~/fitgang_app/saas
/usr/bin/python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from app import create_app
    app = create_app('production')
    print('✅ Application peut démarrer depuis /usr/bin/python3')
except Exception as e:
    print(f'❌ ERREUR: {e}')
" 2>&1 | grep -v "identifiant non valable" | grep -v "export:"

echo ""
echo "=========================================================================="
echo "FIN DU SCRIPT"
echo "=========================================================================="
