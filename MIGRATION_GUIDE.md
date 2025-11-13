# Guide de Migration FitGang

## Mise à jour de la base de données

Cette mise à jour majeure introduit de nouvelles fonctionnalités pour FitGang :
- Programmes structurés (semaines/jours)
- eBooks avec téléchargement
- Compléments alimentaires / Affiliations

### Nouvelles Tables

1. **program_weeks** - Semaines des programmes
2. **program_days** - Jours des programmes avec détails entraînement/diète
3. **user_program_progress** - Suivi de progression utilisateur
4. **supplements** - Compléments alimentaires
5. **supplement_recommendations** - Recommandations de compléments

### Instructions de Migration

#### Option 1 : Migration automatique (recommandée)

Si vous avez Flask-Migrate configuré :

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Générer la migration
flask db migrate -m "Add programs, supplements, and enhanced ebook support"

# Appliquer la migration
flask db upgrade
```

#### Option 2 : Migration manuelle

Si Flask-Migrate n'est pas disponible, exécutez les commandes SQL suivantes :

```sql
-- Table: program_weeks
CREATE TABLE program_weeks (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    product_id INTEGER NOT NULL,
    week_number INTEGER NOT NULL,
    title VARCHAR(200),
    description TEXT,
    goals TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Table: program_days
CREATE TABLE program_days (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    week_id INTEGER NOT NULL,
    day_number INTEGER NOT NULL,
    title VARCHAR(200),
    workout_type VARCHAR(100),
    workout_description TEXT,
    workout_exercises JSON,
    workout_duration INTEGER,
    workout_video_url VARCHAR(500),
    workout_image_url VARCHAR(500),
    diet_description TEXT,
    diet_calories INTEGER,
    diet_meals JSON,
    notes TEXT,
    coach_tips TEXT,
    is_rest_day BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (week_id) REFERENCES program_weeks(id) ON DELETE CASCADE
);

-- Table: user_program_progress
CREATE TABLE user_program_progress (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    current_week INTEGER DEFAULT 1,
    current_day INTEGER DEFAULT 1,
    completed_days JSON,
    total_workouts_completed INTEGER DEFAULT 0,
    start_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_activity DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Table: supplements
CREATE TABLE supplements (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(250) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    short_description VARCHAR(500),
    category VARCHAR(100),
    brand VARCHAR(100),
    image_url VARCHAR(500),
    gallery_images JSON,
    affiliate_link VARCHAR(500) NOT NULL,
    affiliate_code VARCHAR(100),
    benefits JSON,
    usage_instructions TEXT,
    ingredients TEXT,
    warnings TEXT,
    price_range VARCHAR(50),
    clicks INTEGER DEFAULT 0,
    views INTEGER DEFAULT 0,
    is_published BOOLEAN DEFAULT FALSE,
    is_featured BOOLEAN DEFAULT FALSE,
    display_order INTEGER DEFAULT 0,
    meta_title VARCHAR(200),
    meta_description VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_slug (slug),
    INDEX idx_published (is_published),
    INDEX idx_category (category)
);

-- Table: supplement_recommendations
CREATE TABLE supplement_recommendations (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    supplement_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    recommendation_text TEXT,
    display_order INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (supplement_id) REFERENCES supplements(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Indexes pour performance
CREATE INDEX idx_program_weeks_product ON program_weeks(product_id);
CREATE INDEX idx_program_days_week ON program_days(week_id);
CREATE INDEX idx_user_progress_user ON user_program_progress(user_id);
CREATE INDEX idx_user_progress_product ON user_program_progress(product_id);
```

### Vérification

Après la migration, vérifiez que toutes les tables ont été créées :

```sql
SHOW TABLES;
```

Vous devriez voir :
- program_weeks
- program_days
- user_program_progress
- supplements
- supplement_recommendations

### Nouvelles Routes Admin

Accédez au dashboard admin pour utiliser les nouvelles fonctionnalités :

- **Programmes** : `/admin/programs` - Créer et gérer les programmes structurés
- **eBooks** : `/admin/ebooks` - Gérer les livres numériques
- **Compléments** : `/admin/supplements` - Gérer les produits affiliés

### Nouvelles Routes Publiques

- **Compléments** : `/complements` - Page publique des compléments alimentaires
- **Détail complément** : `/complements/<slug>` - Page de détail avec lien affilié

### Notes Importantes

1. **Dossiers d'upload** : Assurez-vous que les dossiers suivants existent et sont accessibles en écriture :
   - `uploads/products/`
   - `uploads/ebooks/covers/`
   - `uploads/ebooks/files/`
   - `uploads/workouts/`
   - `uploads/supplements/`

2. **Permissions** : Toutes les routes admin sont protégées avec `@admin_required`

3. **Fonctionnalités** :
   - Programmes structurés par semaine et jour avec JSON pour exercices et repas
   - Téléchargement sécurisé d'eBooks pour les utilisateurs
   - Tracking des clics sur liens d'affiliation

### Support

En cas de problème, vérifiez les logs de l'application et assurez-vous que :
- La base de données est accessible
- Les permissions de fichiers sont correctes
- Tous les modules Python requis sont installés

## Résumé des Changements

### Modèles Ajoutés
- `ProgramWeek`, `ProgramDay`, `UserProgramProgress`
- `Supplement`, `SupplementRecommendation`

### Blueprints Ajoutés
- `admin/programs` - CRUD complet pour programmes structurés
- `admin/ebooks` - CRUD pour eBooks
- `admin/supplements` - CRUD pour compléments
- `supplements` - Section publique compléments

### Templates Ajoutés
- Templates admin pour gestion complète
- Templates publics pour affichage compléments
- Templates d'erreur (404, 500)

### Corrections
- Erreur "Incomplete response" dans cart.py
- Erreur "Incomplete response" dans profile.py
- Templates manquants ajoutés

### Améliorations
- Dashboard admin modernisé
- Interface de gestion intuitive
- Support complet pour programmes structurés
- Système de tracking pour affiliations
