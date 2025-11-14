# Changements du 14 Novembre 2025

## 🎨 Design & UI Modernisés (Style Apple)

### 1. Page Produit (`/programmes/programme-seche`)
- ✅ Design Apple complet avec grille 2 colonnes
- ✅ Image sticky avec effet hover élégant
- ✅ Section prix dans carte avec gradient
- ✅ Liste de features modernisée
- ✅ Animations smooth et ombres douces
- ✅ Responsive mobile

**Fichier:** `fitgang_app/templates/shop/product.html`

### 2. Page Profil (`/profile`)
- ✅ Layout Apple-style avec cartes blanches
- ✅ Avatar gradient bleu
- ✅ Grilles de stats avec animations hover
- ✅ Boutons d'actions avec transitions
- ✅ Card admin spéciale avec badge
- ✅ Responsive design

**Fichier:** `fitgang_app/templates/profile/index.html`

### 3. Pages Programmes & Ebooks
- ✅ Suppression des bandeaux de couleurs
- ✅ Fond blanc propre
- ✅ Texte sombre lisible

**Fichiers:** `shop/programs.html`, `shop/ebooks.html`

## 🆕 Nouvelles Fonctionnalités

### Système de Suivi de Poids (`/dashboard`)
- ✅ Nouveau modèle `WeightEntry` en base de données
- ✅ Graphique Chart.js d'évolution du poids
- ✅ 5 statistiques: actuel/départ/objectif/évolution/progression
- ✅ Formulaire d'ajout de pesée (poids, date, notes)
- ✅ Historique des entrées avec suppression
- ✅ API endpoint `/dashboard/weight/data` pour le graphique
- ✅ Migration SQL: `migrations/create_weight_entries.sql`

**Fichiers:**
- `fitgang_app/models/weight_entry.py` (nouveau)
- `fitgang_app/blueprints/dashboard.py` (modifié)
- `fitgang_app/templates/dashboard/index.html` (modifié)

## 🐛 Corrections de Bugs

### 1. Erreur 500 sur `/workouts`
- ✅ Template `list.html` → `index.html`
- ✅ Import `OrderStatus` ajouté
- ✅ Comparaison enum corrigée

**Fichier:** `fitgang_app/blueprints/workouts.py`

### 2. Erreur 500 sur `/calculators`
- ✅ Formulaires simplifiés (sans WTForms)
- ✅ IMC et TDEE fonctionnels
- ✅ Calculs directs depuis request.form

**Fichier:** `fitgang_app/blueprints/calculators.py`

### 3. Blog Admin - Édition d'articles
- ✅ Gestion manuelle des champs (plus de populate_obj)
- ✅ Try/catch avec rollback en cas d'erreur
- ✅ Messages d'erreur explicites à l'utilisateur
- ✅ Ordre des SelectField choices corrigé
- ✅ Date de publication auto-définie si publié

**Fichier:** `fitgang_app/blueprints/admin/blog.py`

### 4. Images - Affichage corrigé partout
- ✅ Gestion des URLs HTTP vs chemins locaux
- ✅ Préfixe `/uploads/` ajouté automatiquement
- ✅ Corrigé sur: admin/blog, purchases, cart, shop

### 5. Dashboard - Protection table manquante
- ✅ Try/catch sur WeightEntry.query
- ✅ Pas de crash si table n'existe pas

## 📊 Base de Données

### Nouvelle Table: `weight_entries`
```sql
CREATE TABLE weight_entries (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    weight REAL NOT NULL,
    notes TEXT,
    recorded_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**⚠️ Action requise:** Créer la table via:
```bash
python3 create_weight_table.py
# OU
sqlite3 fitgang.db < migrations/create_weight_entries.sql
```

## 📦 Commits

1. `6dadf57` - Corrections et modernisation complète
2. `d8ba2ef` - Fix: Amélioration gestion erreurs blog et dashboard
3. `87c2334` - Add: Page de test + force restart serveur
4. `3318c87` - Force: Mise à jour app.py + nettoyage cache Python

## 🚀 Déploiement

Branche: `claude/saccra-fitgang-complete-overhaul-0186TzukF7j2eifnrXaNd51n`

Voir: `DEPLOY_TO_PRODUCTION.md` pour les instructions complètes.

## 🧪 Pages à Tester

1. https://fitgang.fr/profile
2. https://fitgang.fr/dashboard
3. https://fitgang.fr/programmes/programme-seche
4. https://fitgang.fr/calculators
5. https://fitgang.fr/workouts
6. https://fitgang.fr/admin/blog/1/edit

**N'oubliez pas de vider le cache du navigateur!**
