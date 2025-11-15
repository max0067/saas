#!/bin/bash
echo "=========================================================================="
echo "🔧 CORRECTION DU .HTACCESS POUR POINTER VERS LE BON RÉPERTOIRE"
echo "=========================================================================="

HTACCESS_DIR=~/public_html/fitgang.fr
HTACCESS_FILE="$HTACCESS_DIR/.htaccess"

echo -e "\n1️⃣ Backup de l'ancien .htaccess..."
if [ -f "$HTACCESS_FILE" ]; then
    cp "$HTACCESS_FILE" "$HTACCESS_FILE.backup_$(date +%Y%m%d_%H%M%S)"
    echo "   ✅ Backup créé"
else
    echo "   ⚠️  Aucun .htaccess trouvé"
fi

echo -e "\n2️⃣ Création du nouveau .htaccess..."
cat > "$HTACCESS_FILE" << 'EOF'
# Configuration Apache pour FitGang sur o2switch
# MISE À JOUR: Pointe vers /home/wrbh3411/fitgang_app/saas (nouveau code)

# Force HTTPS (SSL)
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Configuration Passenger (serveur WSGI d'o2switch)
PassengerEnabled On
PassengerAppRoot /home/wrbh3411/fitgang_app/saas
PassengerBaseURI /
PassengerPython /usr/bin/python3
PassengerStartupFile passenger_wsgi.py
PassengerAppType wsgi
PassengerFriendlyErrorPages off

# Options de performance
PassengerMaxPoolSize 6
PassengerMinInstances 1
PassengerMaxInstancesPerApp 0
PassengerPoolIdleTime 300
PassengerMaxPreloaderIdleTime 0

# Compression Gzip
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript application/json
</IfModule>

# Cache des fichiers statiques
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/gif "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
</IfModule>

# Sécurité
<FilesMatch "\.(env|db|sqlite|py|pyc)$">
    Order allow,deny
    Deny from all
</FilesMatch>
EOF

echo "   ✅ Nouveau .htaccess créé"

echo -e "\n3️⃣ Vérification du changement..."
echo "   Ancien: PassengerAppRoot /home/wrbh3411/public_html/fitgang.fr"
echo "   Nouveau:"
grep "PassengerAppRoot" "$HTACCESS_FILE" | sed 's/^/   /'

echo -e "\n4️⃣ Redémarrage de Passenger..."
pkill -9 -u $USER python
sleep 3
rm -rf ~/fitgang_app/saas/tmp
mkdir -p ~/fitgang_app/saas/tmp
touch ~/fitgang_app/saas/tmp/restart.txt

echo -e "\n=========================================================================="
echo "✅ TERMINÉ!"
echo "=========================================================================="
echo ""
echo "Apache va maintenant charger depuis: /home/wrbh3411/fitgang_app/saas"
echo ""
echo "Attends 30 secondes puis teste:"
echo "  1. https://fitgang.fr/blog (doit montrer 3 cartes avec images)"
echo "  2. https://fitgang.fr/workouts (ne doit plus faire erreur 500)"
echo "  3. Ctrl+Shift+R pour vider le cache du navigateur"
echo ""
echo "=========================================================================="
