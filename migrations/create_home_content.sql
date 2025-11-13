-- Create home_content table
CREATE TABLE IF NOT EXISTS home_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hero_title VARCHAR(200) DEFAULT 'Transforme ton corps.<br>Dépasse tes limites.',
    hero_subtitle TEXT DEFAULT 'Des programmes de sport et nutrition conçus pour des résultats concrets. Rejoins le mouvement.',
    hero_image VARCHAR(500) DEFAULT 'assets/hero-image.svg',
    hero_button_text VARCHAR(100) DEFAULT 'Commencer maintenant',
    hero_button_link VARCHAR(200) DEFAULT '/shop/programs',
    hero_secondary_button_text VARCHAR(100) DEFAULT 'Outils gratuits',
    hero_secondary_button_link VARCHAR(200) DEFAULT '/calculators',
    products_section_title VARCHAR(200) DEFAULT 'Programmes populaires',
    products_section_subtitle VARCHAR(300) DEFAULT 'Choisis le programme adapté à ton objectif',
    blog_section_title VARCHAR(200) DEFAULT 'Le blog FitGang',
    blog_section_subtitle VARCHAR(300) DEFAULT 'Conseils, astuces et motivation pour progresser',
    cta_title VARCHAR(200) DEFAULT 'Prêt à transformer<br>ton physique ?',
    cta_subtitle TEXT DEFAULT 'Rejoins des milliers de personnes qui progressent chaque jour avec FitGang.',
    cta_button_text VARCHAR(100) DEFAULT 'Commence gratuitement',
    cta_button_link VARCHAR(200) DEFAULT '/auth/register',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Insert default content if table is empty
INSERT INTO home_content (id)
SELECT 1
WHERE NOT EXISTS (SELECT 1 FROM home_content);
