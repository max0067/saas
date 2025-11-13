# 🚀 Guide de Démarrage Rapide FitGang

## Étape 1 : Prérequis

Assurez-vous d'avoir :
- Python 3.8+ installé
- Base de données MySQL/MariaDB accessible
- Variables d'environnement configurées

## Étape 2 : Installation

```bash
# 1. Activer l'environnement virtuel (si nécessaire)
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 2. Installer les dépendances (si pas déjà fait)
pip install -r requirements.txt

# 3. Créer les dossiers d'upload
mkdir -p uploads/{products,ebooks/{covers,files},workouts,supplements}
chmod 755 uploads -R
```

## Étape 3 : Migration de la Base de Données

### Option A : Avec Flask-Migrate (Recommandé)

```bash
# Initialiser les migrations (si première fois)
flask db init

# Générer la migration
flask db migrate -m "Add programs, supplements, and enhanced ebook support"

# Appliquer la migration
flask db upgrade
```

### Option B : Sans Flask-Migrate

Consultez le fichier `MIGRATION_GUIDE.md` pour les scripts SQL manuels.

## Étape 4 : Charger les Données de Test

```bash
# Charger des exemples de programmes, eBooks et compléments
python scripts/load_test_data.py
```

Ceci va créer :
- ✅ 1 Programme de 8 semaines (Prise de masse)
- ✅ 1 eBook (Guide Nutrition)
- ✅ 5 Compléments alimentaires

## Étape 5 : Créer un Compte Admin

```bash
# Lancer Python shell
flask shell

# Dans le shell Python :
from fitgang_app.models import User
from fitgang_app import db

# Créer un admin
admin = User(email='admin@fitgang.com', is_admin=True)
admin.set_password('admin123')
db.session.add(admin)
db.session.commit()
exit()
```

## Étape 6 : Lancer l'Application

```bash
# Mode développement
python app.py

# Ou avec Flask
flask run
```

L'application sera accessible sur : **http://localhost:5000**

## Étape 7 : Explorer les Fonctionnalités

### Dashboard Admin
Connectez-vous avec le compte admin créé :
- URL : **http://localhost:5000/auth/login**
- Email : `admin@fitgang.com`
- Mot de passe : `admin123`

Puis accédez au dashboard : **http://localhost:5000/admin**

### Pages à Tester

#### Admin
- `/admin` - Dashboard principal
- `/admin/programs` - Gestion des programmes
- `/admin/ebooks` - Gestion des eBooks
- `/admin/supplements` - Gestion des compléments
- `/admin/blog` - Gestion du blog
- `/admin/users` - Gestion des utilisateurs

#### Public
- `/` - Page d'accueil
- `/programmes` - Catalogue des programmes
- `/complements` - Page des compléments alimentaires
- `/blog` - Articles de blog
- `/profile/purchases` - Mes achats (nécessite connexion)

## 🎯 Fonctionnalités Principales

### 1. Programmes Sport & Diète
- Création de programmes structurés par semaine et jour
- Éditeur d'entraînement avec exercices (JSON)
- Plan nutritionnel détaillé par repas (JSON)
- Vidéos et images d'accompagnement
- Duplication de programme en 1 clic

### 2. eBooks
- Upload de fichiers PDF/EPUB
- Téléchargement sécurisé pour acheteurs
- Gestion des métadonnées (auteur, pages, ISBN)
- Prix personnalisable (gratuit ou payant)

### 3. Compléments / Affiliations
- Catalogue de produits affiliés
- Tracking automatique des clics
- Organisation par catégorie
- Bénéfices, ingrédients, avertissements
- Ordre d'affichage personnalisable

### 4. Dashboard Utilisateur
- Historique des achats
- Accès aux programmes achetés
- Téléchargement des eBooks
- Suivi de progression (à venir)

## 📝 Créer du Contenu Manuellement

### Créer un Programme

1. Allez sur `/admin/programs`
2. Cliquez sur "Nouveau programme"
3. Remplissez les informations :
   - Titre, description, type
   - Niveau de difficulté
   - Durée en semaines
   - Prix
4. Enregistrez
5. Modifiez chaque semaine et jour pour ajouter le contenu détaillé

**Astuce** : Pour les exercices et repas, utilisez le format JSON :
```json
[
  {
    "name": "Squat",
    "sets": 4,
    "reps": "8-10",
    "rest": "90s",
    "notes": "Charge progressive"
  }
]
```

### Créer un eBook

1. Allez sur `/admin/ebooks`
2. Cliquez sur "Nouvel eBook"
3. Remplissez les informations
4. Uploadez la couverture (image)
5. Uploadez le fichier PDF
6. Enregistrez

### Créer un Complément

1. Allez sur `/admin/supplements`
2. Cliquez sur "Nouveau complément"
3. Remplissez les informations
4. Ajoutez les bénéfices (un par ligne)
5. Collez le lien d'affiliation
6. Enregistrez

## ⚠️ Dépannage

### Erreur de connexion à la base de données
Vérifiez votre fichier `.env` ou `config.py` :
```python
SQLALCHEMY_DATABASE_URI = 'mysql://user:password@localhost/fitgang'
```

### Erreur "No module named 'slugify'"
```bash
pip install python-slugify
```

### Erreur d'upload de fichier
Vérifiez que les dossiers `uploads/` existent et ont les bonnes permissions :
```bash
chmod 755 uploads -R
```

### Les templates ne se chargent pas
Assurez-vous que vous êtes dans le bon répertoire et que `fitgang_app/templates/` contient tous les fichiers.

## 🔧 Configuration Additionnelle

### Variables d'Environnement Recommandées

Créez un fichier `.env` :
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=votre-clé-secrète-très-longue
SQLALCHEMY_DATABASE_URI=mysql://user:password@localhost/fitgang
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

### Configuration Email (optionnel)
Pour les notifications :
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=votre-email@gmail.com
MAIL_PASSWORD=votre-mot-de-passe-app
```

## 📚 Documentation Complète

Pour plus d'informations, consultez :
- `MIGRATION_GUIDE.md` - Guide de migration de la base de données
- `README.md` - Documentation générale du projet

## 💡 Conseils

1. **Commencez par les données de test** : Utilisez `scripts/load_test_data.py` pour voir immédiatement le résultat
2. **Explorez le dashboard admin** : C'est là que toute la magie opère
3. **Testez l'interface publique** : Visitez `/complements` pour voir l'affichage
4. **Dupliquez plutôt que recréer** : Utilisez la fonction de duplication pour les programmes

## 🎉 C'est Parti !

Vous êtes maintenant prêt à utiliser FitGang !

Questions ? Problèmes ? Consultez les guides ou vérifiez les logs de l'application.

**Bonne création de contenu !** 💪
