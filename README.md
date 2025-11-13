# FitGang - Plateforme de Fitness Complète

Application web Flask complète pour la vente de programmes fitness, nutrition, eBooks et coaching en ligne.

## 📋 Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Technologies](#technologies)
- [Pré-requis](#pré-requis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Exécution](#exécution)
- [Structure du projet](#structure-du-projet)
- [API](#api)
- [Tests](#tests)
- [Déploiement](#déploiement)
- [Sécurité & RGPD](#sécurité--rgpd)

## ✨ Fonctionnalités

### Authentification & Utilisateurs
- ✅ Inscription / Connexion / Mot de passe oublié
- ✅ Rôles utilisateurs (admin, coach, user)
- ✅ Profils utilisateurs avec données physiques
- ✅ Photos avant/après privées
- ✅ Gestion des mots de passe par admin (reset, temporaire, force change)

### E-commerce
- ✅ Catalogue de produits (programmes sport, nutrition, combinés, eBooks)
- ✅ Panier et checkout
- ✅ Intégration Stripe (paiements)
- ✅ Codes cadeaux / Gifting
- ✅ Génération de liens d'accès sécurisés
- ✅ Téléchargements limités et tracking

### Contenu
- ✅ Blog / CMS avec éditeur WYSIWYG
- ✅ Catégories et tags
- ✅ Vidéos d'exercices
- ✅ Plans de repas avec recettes détaillées
- ✅ Programmes d'entraînement structurés

### Outils Fitness
- ✅ Calculateur IMC
- ✅ Calculateur TDEE (calories journalières)
- ✅ Calculateur macros (protéines/glucides/lipides)
- ✅ Calculateur 1RM (one rep max)
- ✅ Chronomètre de séance
- ✅ Graphiques de progression (Chart.js)

### Dashboard & Analytics
- ✅ Dashboard utilisateur avec stats
- ✅ Dashboard admin avec analytics
- ✅ Graphiques revenus mensuels
- ✅ Taux de conversion
- ✅ Produits best-sellers

### Marketing & Affiliation
- ✅ Système d'affiliation complet
- ✅ Tracking des clics et conversions
- ✅ Commissions configurables
- ✅ Emails automatiques (bienvenue, achat, cadeaux)

### SEO & Référencement
- ✅ Meta tags dynamiques
- ✅ Sitemap.xml automatique
- ✅ Schema.org markup
- ✅ URLs optimisées (slugs)

## 🛠 Technologies

- **Backend:** Python 3.11+, Flask 3.0
- **Database:** SQLAlchemy 2.x, PostgreSQL / SQLite
- **Auth:** Flask-Login
- **Forms:** Flask-WTF, WTForms
- **Migrations:** Flask-Migrate / Alembic
- **Email:** Flask-Mail
- **Paiements:** Stripe
- **Frontend:** Bootstrap 5, Chart.js
- **Storage:** Local / AWS S3
- **Containerisation:** Docker, docker-compose
- **Tests:** pytest

## 📦 Pré-requis

- Python 3.11+
- Docker & docker-compose (recommandé)
- PostgreSQL 15+ (ou SQLite pour dev)
- Redis (optionnel, pour Celery)
- Compte Stripe (mode test)

## 🚀 Installation

### Option 1: Avec Docker (Recommandé)

```bash
# Cloner le repository
git clone <repository-url>
cd fitgang_app

# Copier le fichier d'environnement
cp .env.example .env

# Éditer .env avec vos configurations
nano .env

# Lancer avec Docker Compose
docker-compose up --build
```

L'application sera accessible sur `http://localhost:5000`

### Option 2: Sans Docker

```bash
# Cloner le repository
git clone <repository-url>
cd fitgang_app

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Copier et configurer .env
cp .env.example .env
nano .env

# Initialiser la base de données
flask db upgrade

# Charger les fixtures (données d'exemple)
python scripts/load_fixtures.py

# Lancer l'application
flask run
```

## ⚙️ Configuration

### Variables d'environnement (.env)

```bash
# Flask
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-in-production

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/fitgang_db
# Ou pour SQLite en dev:
# DATABASE_URL=sqlite:///fitgang.db

# Email (Gmail example)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@fitgang.fr

# Stripe
STRIPE_PUBLIC_KEY=pk_test_your_key
STRIPE_SECRET_KEY=sk_test_your_key
STRIPE_WEBHOOK_SECRET=whsec_your_secret

# AWS S3 (optionnel)
USE_S3=False
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_BUCKET_NAME=fitgang-uploads
AWS_REGION=eu-west-1

# Redis (pour Celery, optionnel)
REDIS_URL=redis://localhost:6379/0
```

### Stripe Configuration

1. Créer un compte Stripe: https://dashboard.stripe.com/register
2. Activer le mode test
3. Copier les clés API (Dashboard → Developers → API keys)
4. Configurer le webhook endpoint: `https://your-domain.com/webhooks/stripe`
5. Copier le webhook secret

## 🎯 Exécution

### Commandes principales

```bash
# Lancer l'application
flask run
# ou
python app.py

# Avec Docker
docker-compose up

# Créer les tables de la DB
flask db upgrade

# Charger les données d'exemple
python scripts/load_fixtures.py

# Créer un admin
flask shell
>>> from fitgang_app.models import User
>>> admin = User(username='admin', email='admin@fitgang.fr', role='admin')
>>> admin.set_password('votre-mot-de-passe')
>>> from fitgang_app import db
>>> db.session.add(admin)
>>> db.session.commit()
>>> exit()
```

### Migrations de base de données

```bash
# Créer une nouvelle migration
flask db migrate -m "Description des changements"

# Appliquer les migrations
flask db upgrade

# Revenir en arrière
flask db downgrade
```

## 📁 Structure du projet

```
fitgang_app/
├── app.py                      # Point d'entrée
├── config.py                   # Configuration
├── requirements.txt            # Dépendances Python
├── Dockerfile                  # Configuration Docker
├── docker-compose.yml          # Services Docker
├── .env.example                # Variables d'environnement
├── fitgang_app/
│   ├── __init__.py            # Factory Flask
│   ├── models/                # Modèles SQLAlchemy
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── blog.py
│   │   ├── order.py
│   │   ├── gift.py
│   │   └── ...
│   ├── blueprints/            # Routes Flask
│   │   ├── auth.py
│   │   ├── shop.py
│   │   ├── blog.py
│   │   ├── admin/
│   │   └── ...
│   ├── forms/                 # WTForms
│   ├── templates/             # Templates HTML
│   ├── static/                # CSS, JS, assets
│   └── utils/                 # Utilitaires
├── scripts/                   # Scripts utilitaires
│   ├── load_fixtures.py
│   ├── generate_gift_code.py
│   └── ...
└── tests/                     # Tests pytest
    ├── test_auth.py
    ├── test_shop.py
    └── ...
```

## 🔌 API

### Endpoints publics

```
GET  /api/products              # Liste des produits
GET  /api/products/<id>         # Détails d'un produit
GET  /api/gifts/validate/<code> # Valider un code cadeau
```

### Endpoints authentifiés

```
GET  /api/user/purchases        # Achats de l'utilisateur
```

### Webhooks

```
POST /webhooks/stripe           # Webhooks Stripe
```

## 🧪 Tests

```bash
# Lancer tous les tests
pytest

# Avec coverage
pytest --cov=fitgang_app

# Tests spécifiques
pytest tests/test_auth.py
pytest tests/test_shop.py
pytest tests/test_gifts.py
```

## 🚀 Déploiement Production

### Checklist pré-déploiement

- [ ] Changer `SECRET_KEY` (générer avec `python -c "import secrets; print(secrets.token_hex(32))"`)
- [ ] Configurer PostgreSQL
- [ ] Activer SSL/HTTPS
- [ ] Configurer les DNS
- [ ] Configurer le serveur email (SMTP)
- [ ] Activer Stripe en mode production
- [ ] Configurer AWS S3 pour les uploads
- [ ] Mettre `SESSION_COOKIE_SECURE=True`
- [ ] Configurer les backups DB
- [ ] Configurer les logs (Sentry, etc.)

### Déploiement avec Docker

```bash
# Build production
docker build -t fitgang:latest .

# Run
docker run -d \
  -p 80:5000 \
  --env-file .env.production \
  fitgang:latest
```

### Avec Gunicorn

```bash
# Installer Gunicorn
pip install gunicorn

# Lancer
gunicorn -w 4 -b 0.0.0.0:8000 "fitgang_app:create_app()"
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/fitgang_app/static;
    }

    location /uploads {
        alias /path/to/fitgang_app/uploads;
    }
}
```

## 🔒 Sécurité & RGPD

### Sécurité

- ✅ Protection CSRF activée
- ✅ Mots de passe hachés (bcrypt)
- ✅ URLs signées pour téléchargements
- ✅ Validation des uploads (taille, type)
- ✅ Sanitization du contenu HTML
- ✅ Rate limiting (via Redis, optionnel)
- ✅ Logs d'audit admin

### RGPD

- ✅ Consentement cookies
- ✅ Droit à l'oubli (suppression de compte)
- ✅ Portabilité des données
- ✅ Politique de confidentialité
- ✅ Gestion des accès (download tracking)

### Checklist RGPD

1. Ajouter bannière de consentement cookies
2. Créer page Politique de confidentialité
3. Créer page Mentions légales
4. Implémenter suppression de compte
5. Implémenter export des données
6. Configurer conservation des données
7. Anonymisation des logs après X jours

## 📧 Configuration Email

### Gmail

1. Activer l'authentification à 2 facteurs
2. Générer un mot de passe d'application
3. Utiliser ce mot de passe dans `MAIL_PASSWORD`

### SendGrid / Mailgun

```bash
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-api-key
```

## 🎨 Personnalisation

Voir [style-guide.md](style-guide.md) pour personnaliser:
- Couleurs et charte graphique
- Logo
- Typographie
- Menus et navigation
- Templates

## 📝 Commandes utiles

```bash
# Générer un code cadeau
python scripts/generate_gift_code.py <product_id> <recipient_email>

# Révoquer un code cadeau
python scripts/revoke_gift.py <gift_code>

# Générer une URL signée
python scripts/generate_signed_url.py <file_path>

# Export CSV des ventes
flask shell
>>> from fitgang_app.models import Order
>>> import csv
>>> # ... script d'export
```

## 🆘 Support & Troubleshooting

### Problèmes communs

**Erreur de connexion DB:**
```bash
# Vérifier que PostgreSQL est lancé
docker-compose ps

# Recréer la DB
docker-compose down -v
docker-compose up
```

**Uploads ne fonctionnent pas:**
```bash
# Vérifier les permissions
chmod 755 uploads/
```

**Emails ne partent pas:**
- Vérifier MAIL_* dans .env
- Vérifier les logs Flask
- Tester SMTP: `telnet smtp.gmail.com 587`

## 🎓 Étapes suivantes / Améliorations possibles

1. **Optimisation performance**
   - Implémenter cache (Redis)
   - Optimiser queries SQL (eager loading)
   - CDN pour assets statiques

2. **Fonctionnalités avancées**
   - Chat en direct (coach ↔ user)
   - Application mobile (API REST)
   - Notifications push
   - Intégration Zoom pour coaching vidéo
   - Gamification (badges, niveaux)

3. **Analytics avancés**
   - Google Analytics / Matomo
   - Heatmaps (Hotjar)
   - A/B Testing
   - Prévisions IA (revenus, churn)

4. **Marketing**
   - Newsletter automatisée (Mailchimp)
   - Funnels de vente
   - Upsells / Cross-sells automatiques
   - Programme de parrainage

5. **Internationalisation**
   - Multi-langues (Flask-Babel)
   - Multi-devises
   - Conformité légale par pays

## 📄 Licence

© 2024 FitGang. Tous droits réservés.

## 👥 Contact

- Email: contact@fitgang.fr
- Site: https://blog.fitgang.fr

---

**Note:** Ce projet est fourni comme MVP complet. Assurez-vous de bien tester et sécuriser avant mise en production.
