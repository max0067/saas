# 🚀 Guide de Déploiement FitGang

## Situation Actuelle

Les modifications ont été développées sur la branche :
```
claude/saccra-fitgang-complete-overhaul-0186TzukF7j2eifnrXaNd51n
```

Ces modifications **ne sont PAS encore en production** sur fitgang.fr. Elles doivent être fusionnées et déployées.

## Étapes de Déploiement

### Étape 1 : Vérifier les Modifications Localement

```bash
# Vérifier la branche actuelle
git branch

# Voir les fichiers modifiés
git log --oneline -10
```

### Étape 2 : Fusionner dans la Branche Principale

```bash
# Retourner sur la branche principale (main ou master)
git checkout main
# ou
git checkout master

# Fusionner les modifications
git merge claude/saccra-fitgang-complete-overhaul-0186TzukF7j2eifnrXaNd51n

# Vérifier qu'il n'y a pas de conflits
git status
```

### Étape 3 : Pousser sur GitHub

```bash
# Pousser la branche principale avec les modifications
git push origin main
# ou
git push origin master
```

### Étape 4 : Déployer sur le Serveur de Production

#### Option A : Via SSH + Git Pull

```bash
# Se connecter au serveur
ssh user@fitgang.fr

# Aller dans le répertoire de l'application
cd /path/to/fitgang

# Sauvegarder l'état actuel (important!)
cp -r . ../fitgang_backup_$(date +%Y%m%d_%H%M%S)

# Récupérer les dernières modifications
git fetch origin
git pull origin main  # ou master

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les nouvelles dépendances (si nécessaire)
pip install -r requirements.txt
```

#### Option B : Via cPanel ou Interface Web

Si votre hébergeur utilise cPanel :
1. Accédez au Git Version Control dans cPanel
2. Sélectionnez votre repository
3. Cliquez sur "Pull or Deploy"
4. Sélectionnez la branche `main` ou `master`

### Étape 5 : Mettre à Jour la Base de Données

```bash
# Sur le serveur, activer l'environnement virtuel
source venv/bin/activate

# Option A : Migration automatique
flask db upgrade

# Option B : Migration manuelle
# Connectez-vous à MySQL et exécutez les scripts SQL du MIGRATION_GUIDE.md
mysql -u votre_user -p votre_database < migration.sql
```

### Étape 6 : Créer les Dossiers d'Upload

```bash
# Sur le serveur
mkdir -p uploads/products uploads/ebooks/covers uploads/ebooks/files uploads/workouts uploads/supplements
chmod 755 uploads -R
chown www-data:www-data uploads -R  # ou l'utilisateur web approprié
```

### Étape 7 : Redémarrer l'Application

#### Pour Apache avec mod_wsgi ou Passenger :
```bash
# Toucher le fichier WSGI pour redémarrer
touch passenger_wsgi.py
# ou
touch tmp/restart.txt
```

#### Pour Gunicorn :
```bash
sudo systemctl restart fitgang
# ou
sudo supervisorctl restart fitgang
```

#### Pour un serveur de développement :
```bash
pkill -f "python app.py"
python app.py &
```

### Étape 8 : Charger les Données de Test (Optionnel)

```bash
# Sur le serveur
source venv/bin/activate
python scripts/load_test_data.py
```

### Étape 9 : Vérifier le Déploiement

Testez les URLs suivantes :
- ✅ https://fitgang.fr/
- ✅ https://fitgang.fr/admin
- ✅ https://fitgang.fr/admin/users
- ✅ https://fitgang.fr/admin/programs
- ✅ https://fitgang.fr/admin/ebooks
- ✅ https://fitgang.fr/admin/supplements
- ✅ https://fitgang.fr/cart
- ✅ https://fitgang.fr/complements
- ✅ https://fitgang.fr/profile/purchases

## Résolution de Problèmes

### Erreur "Incomplete Response" Persiste

**Cause possible** : L'application n'a pas été redémarrée correctement.

**Solution** :
```bash
# Forcer le redémarrage
sudo systemctl restart apache2  # pour Apache
# ou
sudo systemctl restart nginx && sudo systemctl restart gunicorn  # pour Nginx + Gunicorn
# ou
touch passenger_wsgi.py && touch tmp/restart.txt  # pour Passenger
```

### Erreur de Base de Données

**Cause** : Les nouvelles tables n'ont pas été créées.

**Solution** :
```bash
# Vérifier les tables
mysql -u user -p database_name -e "SHOW TABLES;"

# Si les tables manquent, exécuter la migration
flask db upgrade
# ou utiliser les scripts SQL manuels du MIGRATION_GUIDE.md
```

### Erreur 500 Internal Server Error

**Solution** :
```bash
# Vérifier les logs d'erreur
tail -f /var/log/apache2/error.log
# ou
tail -f /var/log/nginx/error.log
# ou
tail -f logs/error.log

# Vérifier les permissions
chmod 755 fitgang_app -R
chmod 755 uploads -R
```

### Templates Non Trouvés

**Cause** : Les nouveaux templates n'ont pas été déployés.

**Solution** :
```bash
# Vérifier que les templates existent
ls -la fitgang_app/templates/admin/
ls -la fitgang_app/templates/supplements/
ls -la fitgang_app/templates/errors/

# Si manquants, forcer le pull
git fetch origin
git reset --hard origin/main  # ATTENTION : écrase les modifications locales
```

### Fichiers d'Upload Non Accessibles

**Solution** :
```bash
# Corriger les permissions
chown -R www-data:www-data uploads/
chmod -R 755 uploads/

# Vérifier la configuration Apache/Nginx
# Assurez-vous que le répertoire uploads/ est accessible
```

## Checklist de Déploiement

Avant de déployer :
- [ ] Sauvegarder la base de données actuelle
- [ ] Sauvegarder les fichiers de l'application
- [ ] Tester localement toutes les fonctionnalités
- [ ] Vérifier que tous les fichiers sont commités

Pendant le déploiement :
- [ ] Mettre le site en mode maintenance (optionnel)
- [ ] Fusionner et pousser les modifications
- [ ] Se connecter au serveur
- [ ] Faire un pull des modifications
- [ ] Exécuter les migrations de base de données
- [ ] Créer les dossiers d'upload
- [ ] Redémarrer l'application

Après le déploiement :
- [ ] Tester toutes les URLs listées ci-dessus
- [ ] Vérifier les logs d'erreur
- [ ] Tester la création d'un programme
- [ ] Tester la création d'un eBook
- [ ] Tester la création d'un complément
- [ ] Vérifier l'affichage public de /complements
- [ ] Retirer le mode maintenance

## Configuration Serveur Recommandée

### Apache (.htaccess ou VirtualHost)
```apache
<Directory /path/to/fitgang>
    Options -Indexes +FollowSymLinks
    AllowOverride All
    Require all granted
</Directory>

<Directory /path/to/fitgang/uploads>
    Options -Indexes
    AllowOverride None
    Require all granted
</Directory>
```

### Nginx
```nginx
location /uploads/ {
    alias /path/to/fitgang/uploads/;
    autoindex off;
}

location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## Support

Si vous rencontrez des problèmes :
1. Consultez les logs d'erreur
2. Vérifiez les permissions des fichiers
3. Assurez-vous que la base de données est à jour
4. Vérifiez que l'application a été redémarrée

## Notes Importantes

⚠️ **Sauvegardez toujours avant de déployer !**

⚠️ **Testez d'abord sur un environnement de staging si possible**

⚠️ **Vérifiez que votre serveur a assez d'espace disque pour les uploads**

---

Pour plus d'informations :
- `MIGRATION_GUIDE.md` - Guide de migration de la base de données
- `QUICKSTART.md` - Guide de démarrage rapide
- `README.md` - Documentation générale
