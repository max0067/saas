# Configuration cPanel pour FitGang

## Étape 1 : Réinitialiser la base de données

Depuis votre répertoire saas, exécutez :

```bash
cd ~/fitgang_app/saas  # ou le chemin où vous avez cloné le projet
chmod +x reset_database.sh
./reset_database.sh
```

Cela va :
- Supprimer l'ancienne base de données
- Recréer toutes les tables
- Charger les données de test

## Étape 2 : Configuration dans cPanel

### 2.1 Accéder à "Setup Python App"

1. Connectez-vous à cPanel
2. Cherchez "Setup Python App" ou "Application Python"
3. Cliquez sur "Create Application"

### 2.2 Configuration de l'application

Entrez EXACTEMENT ces valeurs :

**Python version** : `3.6.8` (ou la version disponible sur votre serveur)

**Application root** : `/home/wrbh3411/fitgang_app/saas`
⚠️ Remplacez `wrbh3411` par votre nom d'utilisateur cPanel si différent

**Application URL** : Choisissez votre domaine
- Par exemple : `fitgang.fr` ou `www.fitgang.fr`
- Ou un sous-domaine : `app.fitgang.fr`

**Application startup file** : `app.py`

**Application entry point** : `app`

**Passenger log file** : Cochez pour activer les logs

### 2.3 Variables d'environnement

Après avoir créé l'application, cliquez sur "Edit" puis ajoutez ces variables d'environnement :

| Nom | Valeur |
|-----|--------|
| `FLASK_APP` | `app.py` |
| `FLASK_ENV` | `production` |
| `SECRET_KEY` | `votre-cle-secrete-changez-moi` |
| `DATABASE_URL` | `sqlite:////home/wrbh3411/fitgang_app/saas/fitgang.db` |

⚠️ **Important** : Pour `DATABASE_URL`, utilisez 4 slashes `////` puis le chemin ABSOLU

### 2.4 Installer les dépendances

cPanel va automatiquement créer un environnement virtuel. Vous devez y installer les dépendances :

1. Dans cPanel Python App, cliquez sur "Run pip install"
2. Ou via SSH :

```bash
cd ~/fitgang_app/saas
source /home/wrbh3411/virtualenv/fitgang_app/saas/3.6/bin/activate
pip install -r requirements_py36_working.txt
```

### 2.5 Redémarrer l'application

Dans cPanel Python App, cliquez sur "Restart" ou créez un fichier :

```bash
touch ~/fitgang_app/saas/tmp/restart.txt
```

## Étape 3 : Configurer le fichier .env

Créez un fichier `.env` dans le répertoire `~/fitgang_app/saas/` :

```bash
cd ~/fitgang_app/saas
cp .env.example .env
nano .env  # ou vi .env
```

Modifiez avec vos vraies valeurs :

```env
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=changez-cette-cle-pour-production-utilisez-une-cle-aleatoire-longue

# Database
DATABASE_URL=sqlite:////home/wrbh3411/fitgang_app/saas/fitgang.db

# Email (utilisez votre SMTP)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=votre-email@gmail.com
MAIL_PASSWORD=votre-mot-de-passe-app
MAIL_DEFAULT_SENDER=noreply@fitgang.fr

# Stripe (obtenez vos clés sur https://dashboard.stripe.com)
STRIPE_PUBLIC_KEY=pk_test_votre_cle_publique
STRIPE_SECRET_KEY=sk_test_votre_cle_secrete
STRIPE_WEBHOOK_SECRET=whsec_votre_secret_webhook

# S3 (optionnel)
USE_S3=False
# Si vous utilisez S3, décommentez :
# AWS_ACCESS_KEY_ID=votre_access_key
# AWS_SECRET_ACCESS_KEY=votre_secret_key
# S3_BUCKET=votre-bucket
# S3_REGION=eu-west-3

# Site
SITE_NAME=FitGang
SITE_URL=https://fitgang.fr
```

## Étape 4 : Permissions

Assurez-vous que les dossiers ont les bonnes permissions :

```bash
cd ~/fitgang_app/saas
chmod 755 .
chmod 644 app.py
chmod 600 .env
chmod 755 fitgang_app
chmod 644 fitgang.db
```

## Étape 5 : Tester

Visitez votre domaine dans un navigateur. Vous devriez voir la page d'accueil de FitGang.

### Comptes de test :

- **Admin** : admin@fitgang.fr / admin123
- **Utilisateur** : john@example.com / password123

### Code cadeau de test :

- **Code** : WELCOME2024

## Dépannage

### L'application ne démarre pas

1. Vérifiez les logs Passenger dans cPanel
2. Vérifiez que tous les chemins sont corrects (pas de `~`, utilisez `/home/wrbh3411/...`)
3. Vérifiez que les dépendances sont installées

### Erreur 500

```bash
tail -f ~/fitgang_app/saas/logs/error.log  # si les logs existent
# ou vérifiez les logs dans cPanel
```

### Problème de base de données

```bash
cd ~/fitgang_app/saas
python3 -c "from app import app, db; app.app_context().push(); print(db.engine.url)"
```

Cela affiche l'URL de connexion à la base de données.

### Redémarrer l'application

```bash
touch ~/fitgang_app/saas/tmp/restart.txt
# ou depuis cPanel Python App > Restart
```

## Notes importantes

1. **NE PAS** essayer de lancer `flask run` sur un hébergement mutualisé - ça ne fonctionnera pas
2. Utilisez UNIQUEMENT cPanel Python App pour gérer l'application
3. Le PDF generation ne fonctionnera pas (reportlab non installé) mais tout le reste fonctionnera
4. Changez **ABSOLUMENT** le `SECRET_KEY` en production
5. Configurez Stripe avec de vraies clés pour accepter les paiements
6. Configurez l'email SMTP pour que les emails fonctionnent

## Support

Si vous rencontrez des problèmes :

1. Vérifiez les logs Passenger dans cPanel
2. Vérifiez que Python 3.6 est bien sélectionné
3. Vérifiez que le chemin absolu est correct partout
4. Assurez-vous que le fichier .env existe et est correct
