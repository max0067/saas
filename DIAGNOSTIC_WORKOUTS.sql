-- =====================================================
-- DIAGNOSTIC: Pourquoi les workouts sont vides?
-- Copie ces requêtes dans phpMyAdmin pour comprendre
-- =====================================================

-- 1. VÉRIFIER SI LA TABLE WORKOUTS EXISTE ET A DES DONNÉES
SELECT 'Total workouts dans la base:' AS info, COUNT(*) AS nombre FROM workouts;

-- 2. VOIR TOUS LES WORKOUTS EXISTANTS
SELECT id, product_id, name, week_number, day_number
FROM workouts
ORDER BY product_id, week_number, day_number;

-- 3. VÉRIFIER LES PRODUITS (PROGRAMMES)
SELECT id, name, product_type
FROM products
WHERE product_type = 'program'
ORDER BY id;

-- 4. VÉRIFIER QUELLE EST TON ID UTILISATEUR
-- Remplace 'TON_EMAIL' par ton vrai email
SELECT id, email, username, role
FROM users
WHERE email = 'TON_EMAIL' OR role = 'admin';

-- 5. VÉRIFIER TES COMMANDES
-- Remplace USER_ID par ton id de l'étape 4
SELECT o.id, o.user_id, o.status, o.created_at
FROM orders o
WHERE o.user_id = USER_ID
ORDER BY o.created_at DESC;

-- 6. VÉRIFIER LES ITEMS DE TES COMMANDES
-- Remplace USER_ID par ton id
SELECT oi.order_id, oi.product_id, p.name, o.status
FROM order_items oi
JOIN orders o ON oi.order_id = o.id
JOIN products p ON oi.product_id = p.id
WHERE o.user_id = USER_ID;

-- 7. VÉRIFIER SI TON PRODUIT A DES WORKOUTS
-- Remplace PRODUCT_ID par l'id du produit de l'étape 6
SELECT * FROM workouts WHERE product_id = PRODUCT_ID;


-- =====================================================
-- SOLUTION TEMPORAIRE: Créer un workout de test
-- =====================================================

-- Si aucun workout n'existe, en créer un de test
-- Remplace PRODUCT_ID par l'id de ton produit
INSERT INTO workouts (product_id, name, description, week_number, day_number, duration_minutes, difficulty, warmup, cooldown, notes)
VALUES (
    PRODUCT_ID,  -- <-- REMPLACE PAR TON PRODUCT_ID
    'Séance Test - Jour 1',
    'Entraînement de test pour vérifier que le système fonctionne',
    1,  -- Semaine 1
    1,  -- Jour 1
    60,  -- 60 minutes
    'intermediate',
    '5 minutes de cardio léger + étirements dynamiques',
    'Étirements statiques 10 minutes',
    'N\'oublie pas de bien t\'hydrater!'
);

-- Vérifier que ça a marché
SELECT * FROM workouts ORDER BY id DESC LIMIT 1;
