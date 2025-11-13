# 🚨 IMPORTANT : Comment Déployer les Modifications

## 📍 Situation Actuelle

### ✅ Ce qui est FAIT :
- Toutes les modifications sont **commités sur GitHub**
- Branche : `claude/saccra-fitgang-complete-overhaul-0186TzukF7j2eifnrXaNd51n`
- 29 fichiers modifiés/créés
- Toutes les fonctionnalités sont prêtes

### ❌ Ce qui MANQUE :
- Les modifications **NE SONT PAS** sur fitgang.fr
- Le site en production utilise encore l'ancienne version
- C'est pourquoi vous voyez toujours les erreurs

## 🎯 Solution : Déployer sur le Serveur

Vous avez **2 options** :

---

## Option 1 : Déploiement Automatique (Plus Simple)

### Étape 1 : Se connecter au serveur fitgang.fr

```bash
# Via SSH
ssh votre_utilisateur@fitgang.fr

# Ou via cPanel > Terminal
```

### Étape 2 : Aller dans le répertoire de l'application

```bash
cd /chemin/vers/votre/application/fitgang
# Exemple : cd /home/fitgang/public_html
```

### Étape 3 : Sauvegarder l'ancienne version

```bash
# IMPORTANT : Toujours sauvegarder avant de modifier !
cp -r . ../backup_fitgang_$(date +%Y%m%d)
```

### Étape 4 : Récupérer les modifications

```bash
# Récupérer la branche avec les modifications
git fetch origin

# Fusionner les modifications dans votre branche actuelle
git merge origin/claude/saccra-fitgang-complete-overhaul-0186TzukF7j2eifnrXaNd51n

# OU basculer directement sur la branche
git checkout claude/saccra-fitgang-complete-overhaul-0186TzukF7j2eifnrXaNd51n
```

### Étape 5 : Mettre à jour la base de données

```bash
# Se connecter à MySQL
mysql -u votre_user -p votre_base_de_donnees

# Puis copier-coller les commandes SQL du fichier MIGRATION_GUIDE.md
# Ou quitter MySQL et utiliser :
mysql -u votre_user -p votre_base_de_donnees < migration.sql
```

### Étape 6 : Créer les dossiers d'upload

```bash
mkdir -p uploads/products uploads/ebooks/covers uploads/ebooks/files uploads/workouts uploads/supplements
chmod 755 uploads -R
```

### Étape 7 : Redémarrer l'application

```bash
# Méthode 1 : Toucher le fichier WSGI (Passenger)
touch passenger_wsgi.py
touch tmp/restart.txt

# Méthode 2 : Redémarrer Apache
sudo systemctl restart apache2

# Méthode 3 : Via cPanel
# Aller dans "Application Manager" ou "Python App" et cliquer sur "Restart"
```

### Étape 8 : Tester !

Allez sur :
- https://fitgang.fr/admin/users ← Devrait fonctionner
- https://fitgang.fr/cart ← Devrait fonctionner
- https://fitgang.fr/admin/programs ← Nouvelle section
- https://fitgang.fr/complements ← Nouvelle section

---

## Option 2 : Via cPanel Git Version Control

Si vous avez accès à cPanel avec Git Version Control :

### Étape 1 : Se connecter à cPanel
- Allez sur : https://fitgang.fr/cpanel

### Étape 2 : Ouvrir "Git Version Control"
- Cherchez "Git™ Version Control" dans cPanel

### Étape 3 : Gérer le Repository
- Cliquez sur "Manage" à côté de votre repository
- Dans "Pull or Deploy", sélectionnez la branche :
  ```
  claude/saccra-fitgang-complete-overhaul-0186TzukF7j2eifnrXaNd51n
  ```
- Cliquez sur "Update from Remote"

### Étape 4 : Base de données
- Allez dans phpMyAdmin
- Sélectionnez votre base de données
- Onglet "SQL"
- Copiez-collez les commandes SQL du fichier `MIGRATION_GUIDE.md`
- Exécutez

### Étape 5 : Redémarrer
- Via cPanel > "Application Manager" ou "Setup Python App"
- Cliquez sur "Restart"

---

## 🔍 Vérification

Après le déploiement, vérifiez que **TOUT FONCTIONNE** :

### Pages qui DOIVENT fonctionner maintenant :
- ✅ /admin/users (plus d'erreur)
- ✅ /cart (plus d'erreur)
- ✅ /admin/dashboard (nouvelles sections visibles)

### Nouvelles pages disponibles :
- ✅ /admin/programs (créer des programmes)
- ✅ /admin/ebooks (gérer les eBooks)
- ✅ /admin/supplements (gérer les compléments)
- ✅ /complements (page publique)

---

## 📊 Scripts de Migration SQL

Si vous préférez copier-coller le SQL directement, voici un résumé :

```sql
-- Créer les tables pour les programmes
CREATE TABLE IF NOT EXISTS program_weeks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    week_number INT NOT NULL,
    title VARCHAR(200),
    description TEXT,
    goals TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS program_days (
    id INT AUTO_INCREMENT PRIMARY KEY,
    week_id INT NOT NULL,
    day_number INT NOT NULL,
    title VARCHAR(200),
    workout_type VARCHAR(100),
    workout_description TEXT,
    workout_exercises JSON,
    workout_duration INT,
    workout_video_url VARCHAR(500),
    workout_image_url VARCHAR(500),
    diet_description TEXT,
    diet_calories INT,
    diet_meals JSON,
    notes TEXT,
    coach_tips TEXT,
    is_rest_day BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (week_id) REFERENCES program_weeks(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_program_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    current_week INT DEFAULT 1,
    current_day INT DEFAULT 1,
    completed_days JSON,
    total_workouts_completed INT DEFAULT 0,
    start_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_activity DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Créer la table pour les compléments
CREATE TABLE IF NOT EXISTS supplements (
    id INT AUTO_INCREMENT PRIMARY KEY,
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
    clicks INT DEFAULT 0,
    views INT DEFAULT 0,
    is_published BOOLEAN DEFAULT FALSE,
    is_featured BOOLEAN DEFAULT FALSE,
    display_order INT DEFAULT 0,
    meta_title VARCHAR(200),
    meta_description VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_slug (slug),
    INDEX idx_published (is_published)
);

CREATE TABLE IF NOT EXISTS supplement_recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    supplement_id INT NOT NULL,
    product_id INT NOT NULL,
    recommendation_text TEXT,
    display_order INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (supplement_id) REFERENCES supplements(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);
```

---

## ❓ Questions Fréquentes

### Q: Pourquoi je ne vois pas les modifications sur fitgang.fr ?
**R:** Parce que les modifications sont sur GitHub mais pas encore sur votre serveur. Vous devez déployer en suivant les étapes ci-dessus.

### Q: Vais-je perdre mes données ?
**R:** Non ! La migration ajoute seulement de nouvelles tables. Vos données existantes ne seront pas touchées. Mais faites quand même une sauvegarde par sécurité.

### Q: Et si ça ne marche pas ?
**R:** Vous pourrez toujours revenir en arrière avec la sauvegarde que vous avez faite à l'étape 3.

### Q: Combien de temps ça prend ?
**R:** 10-15 minutes si vous suivez les étapes dans l'ordre.

### Q: Je n'ai pas accès SSH, que faire ?
**R:** Utilisez l'Option 2 avec cPanel, ou demandez à votre hébergeur de faire le déploiement.

---

## 🆘 Besoin d'Aide ?

Si vous n'êtes pas à l'aise avec ces étapes :

1. **Contactez votre hébergeur** - Ils peuvent faire le déploiement pour vous
2. **Utilisez cPanel** - C'est plus simple et visuel
3. **Faites-le étape par étape** - Ne sautez aucune étape

---

## ✅ Checklist Avant de Déployer

- [ ] J'ai sauvegardé ma base de données
- [ ] J'ai sauvegardé mes fichiers
- [ ] J'ai accès SSH ou cPanel
- [ ] J'ai les identifiants MySQL
- [ ] J'ai lu toutes les étapes

## ✅ Checklist Après le Déploiement

- [ ] Le site s'affiche toujours
- [ ] /admin/users fonctionne
- [ ] /cart fonctionne
- [ ] /admin/programs est accessible
- [ ] /admin/ebooks est accessible
- [ ] /admin/supplements est accessible
- [ ] /complements s'affiche
- [ ] Aucune erreur 500 dans les logs

---

**Une fois déployé, vous pourrez utiliser toutes les nouvelles fonctionnalités ! 🎉**
