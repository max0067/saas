#!/bin/bash
# Script de diagnostic pour l'erreur 500 sur /admin/programs

echo "========================================="
echo "DIAGNOSTIC FITGANG - Erreur 500"
echo "========================================="
echo ""

echo "1. VÉRIFICATION DES TABLES DE BASE DE DONNÉES"
echo "---------------------------------------------"
mysql -u wrbh3411_fitgang -p wrbh3411_fitgang -e "SHOW TABLES LIKE 'program%';" 2>&1
mysql -u wrbh3411_fitgang -p wrbh3411_fitgang -e "SHOW TABLES LIKE 'supplement%';" 2>&1
echo ""

echo "2. VÉRIFICATION DES DERNIÈRES ERREURS PYTHON"
echo "---------------------------------------------"
if [ -f "/home/wrbh3411/logs/error_log" ]; then
    tail -50 /home/wrbh3411/logs/error_log | grep -A 5 "fitgang"
elif [ -f "/home/wrbh3411/fitgang_app/saas/logs/error.log" ]; then
    tail -50 /home/wrbh3411/fitgang_app/saas/logs/error.log
elif [ -f "/var/log/apache2/error_log" ]; then
    tail -50 /var/log/apache2/error_log | grep -A 5 "fitgang"
else
    echo "Logs non trouvés dans les emplacements standards"
fi
echo ""

echo "3. VÉRIFICATION DE L'APPLICATION PYTHON"
echo "----------------------------------------"
cd /home/wrbh3411/fitgang_app/saas
python3 -c "
try:
    from fitgang_app.blueprints.admin.programs import admin_programs_bp
    print('✓ Blueprint admin_programs importé avec succès')
except Exception as e:
    print('✗ Erreur import admin_programs:', e)

try:
    from fitgang_app.models.program import ProgramWeek, ProgramDay
    print('✓ Modèles ProgramWeek et ProgramDay importés avec succès')
except Exception as e:
    print('✗ Erreur import modèles program:', e)

try:
    from fitgang_app import create_app
    app = create_app()
    print('✓ Application Flask créée avec succès')
except Exception as e:
    print('✗ Erreur création app:', e)
" 2>&1
echo ""

echo "4. VÉRIFICATION DES FICHIERS CLÉS"
echo "----------------------------------"
ls -la /home/wrbh3411/fitgang_app/saas/fitgang_app/blueprints/admin/programs.py
ls -la /home/wrbh3411/fitgang_app/saas/fitgang_app/models/program.py
echo ""

echo "========================================="
echo "FIN DU DIAGNOSTIC"
echo "========================================="
