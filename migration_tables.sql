-- ============================================
-- FITGANG DATABASE MIGRATION
-- Creates tables for Programs, Supplements, and eBooks
-- ============================================

-- Table: program_weeks
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: program_days
CREATE TABLE IF NOT EXISTS program_days (
    id INT AUTO_INCREMENT PRIMARY KEY,
    week_id INT NOT NULL,
    day_number INT NOT NULL,
    title VARCHAR(200),
    workout_type VARCHAR(100),
    workout_description TEXT,
    workout_exercises TEXT,
    workout_duration INT,
    workout_video_url VARCHAR(500),
    workout_image_url VARCHAR(500),
    diet_description TEXT,
    diet_calories INT,
    diet_meals TEXT,
    notes TEXT,
    coach_tips TEXT,
    is_rest_day TINYINT(1) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (week_id) REFERENCES program_weeks(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: user_program_progress
CREATE TABLE IF NOT EXISTS user_program_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    current_week INT DEFAULT 1,
    current_day INT DEFAULT 1,
    completed_days TEXT,
    total_workouts_completed INT DEFAULT 0,
    start_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_activity DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: supplements
CREATE TABLE IF NOT EXISTS supplements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(250) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    short_description VARCHAR(500),
    category VARCHAR(100),
    brand VARCHAR(100),
    image_url VARCHAR(500),
    gallery_images TEXT,
    affiliate_link VARCHAR(500) NOT NULL,
    affiliate_code VARCHAR(100),
    benefits TEXT,
    usage_instructions TEXT,
    ingredients TEXT,
    warnings TEXT,
    price_range VARCHAR(50),
    clicks INT DEFAULT 0,
    views INT DEFAULT 0,
    is_published TINYINT(1) DEFAULT 0,
    is_featured TINYINT(1) DEFAULT 0,
    display_order INT DEFAULT 0,
    meta_title VARCHAR(200),
    meta_description VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_slug (slug),
    INDEX idx_published (is_published)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: supplement_recommendations
CREATE TABLE IF NOT EXISTS supplement_recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    supplement_id INT NOT NULL,
    product_id INT NOT NULL,
    recommendation_text TEXT,
    display_order INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (supplement_id) REFERENCES supplements(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Verify tables were created
SHOW TABLES LIKE 'program%';
SHOW TABLES LIKE 'supplement%';
