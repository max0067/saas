-- =====================================================
-- CREATION DE TOUTES LES TABLES MANQUANTES
-- À exécuter dans phpMyAdmin pour la base wrbh3411_fitgang
-- =====================================================

-- 1. TABLE WEIGHT_ENTRIES (suivi de poids)
-- Note: Utilise INT au lieu de INTEGER pour éviter l'erreur Foreign Key
CREATE TABLE IF NOT EXISTS weight_entries (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    weight DECIMAL(5,2) NOT NULL,
    notes TEXT,
    recorded_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    INDEX idx_weight_entries_user_id (user_id),
    INDEX idx_weight_entries_recorded_at (recorded_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- 2. TABLE BLOG_CATEGORIES (catégories de blog)
CREATE TABLE IF NOT EXISTS blog_categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(120) NOT NULL UNIQUE,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_blog_categories_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- 3. TABLE BLOG_TAGS (tags de blog)
CREATE TABLE IF NOT EXISTS blog_tags (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    slug VARCHAR(60) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_blog_tags_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- 4. TABLE BLOG_POSTS (articles de blog)
CREATE TABLE IF NOT EXISTS blog_posts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(250) NOT NULL UNIQUE,
    content TEXT NOT NULL,
    excerpt VARCHAR(500),

    author_id INT NOT NULL,
    category_id INT,

    featured_image VARCHAR(500),

    meta_title VARCHAR(200),
    meta_description VARCHAR(500),
    meta_keywords VARCHAR(500),

    is_published TINYINT(1) DEFAULT 0,
    is_featured TINYINT(1) DEFAULT 0,

    views INT DEFAULT 0,

    published_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (author_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES blog_categories (id) ON DELETE SET NULL,

    INDEX idx_blog_posts_slug (slug),
    INDEX idx_blog_posts_author (author_id),
    INDEX idx_blog_posts_category (category_id),
    INDEX idx_blog_posts_published (is_published),
    INDEX idx_blog_posts_published_at (published_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- 5. TABLE POST_TAGS (association blog posts <-> tags)
CREATE TABLE IF NOT EXISTS post_tags (
    post_id INT NOT NULL,
    tag_id INT NOT NULL,

    PRIMARY KEY (post_id, tag_id),
    FOREIGN KEY (post_id) REFERENCES blog_posts (id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES blog_tags (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- 6. VÉRIFIER SI LA TABLE WORKOUTS EXISTE
-- Si elle n'existe pas, la créer:
CREATE TABLE IF NOT EXISTS workouts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT,

    name VARCHAR(200) NOT NULL,
    description TEXT,

    week_number INT,
    day_number INT,
    duration_minutes INT,
    difficulty VARCHAR(20),

    warmup TEXT,
    cooldown TEXT,
    notes TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE,
    INDEX idx_workouts_product (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- 7. TABLE EXERCISES (bibliothèque d'exercices)
CREATE TABLE IF NOT EXISTS exercises (
    id INT PRIMARY KEY AUTO_INCREMENT,

    name VARCHAR(200) NOT NULL UNIQUE,
    slug VARCHAR(250) NOT NULL UNIQUE,
    description TEXT,

    muscle_group VARCHAR(100),
    equipment VARCHAR(200),
    difficulty VARCHAR(20),

    video_url VARCHAR(500),
    thumbnail_url VARCHAR(500),
    instructions TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_exercises_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- 8. TABLE WORKOUT_EXERCISES (exercices dans un workout)
CREATE TABLE IF NOT EXISTS workout_exercises (
    id INT PRIMARY KEY AUTO_INCREMENT,
    workout_id INT NOT NULL,
    exercise_id INT NOT NULL,

    `order` INT DEFAULT 0,
    sets INT,
    reps VARCHAR(50),
    rest_seconds INT,
    notes TEXT,

    FOREIGN KEY (workout_id) REFERENCES workouts (id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercises (id) ON DELETE CASCADE,
    INDEX idx_workout_exercises_workout (workout_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =====================================================
-- DONNÉES DE TEST (OPTIONNEL)
-- =====================================================

-- Créer une catégorie de blog par défaut
INSERT IGNORE INTO blog_categories (name, slug, description)
VALUES ('Nutrition', 'nutrition', 'Articles sur la nutrition et l\'alimentation'),
       ('Entraînement', 'entrainement', 'Articles sur l\'entraînement et le fitness'),
       ('Motivation', 'motivation', 'Articles motivationnels');

-- Créer quelques tags par défaut
INSERT IGNORE INTO blog_tags (name, slug)
VALUES ('Perte de poids', 'perte-de-poids'),
       ('Prise de masse', 'prise-de-masse'),
       ('Cardio', 'cardio'),
       ('Musculation', 'musculation');
