# FitGang - Guide de Style & Personnalisation

Ce guide vous aide à personnaliser l'apparence et le contenu de votre application FitGang.

## 🎨 Charte Graphique

### Palette de Couleurs

Les couleurs principales sont définies dans `fitgang_app/static/css/main.css`:

```css
:root {
    --white: #ffffff;
    --gray-50: #fafafa;
    --gray-100: #f5f5f5;
    --gray-200: #e5e5e5;
    --gray-400: #a3a3a3;
    --gray-600: #525252;
    --gray-900: #171717;
    --red: #ED2F2F;           /* Couleur principale FitGang */
    --red-hover: #d42828;      /* Hover state */
}
```

### Modifier les Couleurs

1. Ouvrir `fitgang_app/static/css/main.css`
2. Modifier les valeurs dans `:root`
3. Les changements s'appliqueront automatiquement partout

**Exemple:** Changer le rouge en bleu

```css
:root {
    --red: #2563eb;           /* Nouveau bleu */
    --red-hover: #1d4ed8;     /* Hover bleu foncé */
}
```

## 🖼 Logo & Images

### Remplacer le Logo

1. Créer votre logo au format SVG, PNG ou JPG
2. Placer dans `fitgang_app/static/assets/logo-fitgang.svg`
3. Dimensions recommandées: 200x50px (ratio 4:1)

### Logo Source

Le logo officiel FitGang est disponible sur: https://blog.fitgang.fr

Pour récupérer et créer un SVG placeholder:

```bash
# Créer un logo SVG simple
cat > fitgang_app/static/assets/logo-fitgang.svg << 'EOF'
<svg width="120" height="32" xmlns="http://www.w3.org/2000/svg">
  <text x="0" y="24" font-family="Inter, Arial" font-size="24" font-weight="700" fill="#ED2F2F">
    FitGang
  </text>
</svg>
EOF
```

### Images Placeholder

Ajouter des images par défaut pour les produits:

```bash
# Dans fitgang_app/static/assets/
- placeholder-product.jpg  (600x400px)
- hero-image.jpg          (1200x600px)
- no-image.png            (400x400px)
```

## ✏️ Typographie

### Police Principale

Police actuelle: **Inter** (Google Fonts)

Chargée dans `fitgang_app/templates/base.html`:

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

### Changer la Police

1. Choisir une police sur Google Fonts
2. Remplacer le lien dans `base.html`
3. Modifier `--font-family` dans `main.css`:

```css
:root {
    --font-family: 'Votre Police', sans-serif;
}
```

**Polices recommandées:**
- **Sport/Moderne:** Montserrat, Poppins, Roboto
- **Élégant:** Raleway, Lato, Open Sans
- **Bold/Impact:** Oswald, Anton, Bebas Neue

## 📝 Textes & Contenu

### Modifier les Textes de l'App

**Page d'accueil** (`fitgang_app/templates/index.html`):
```html
<h1 class="display-4 fw-bold mb-4">Transformez votre corps avec FitGang</h1>
```

**Footer** (`fitgang_app/templates/base.html`):
```html
<h5 class="fw-bold">FitGang</h5>
<p class="text-muted">Votre plateforme de fitness complète</p>
```

**Nom du site** (`config.py`):
```python
SITE_NAME = os.environ.get('SITE_NAME', 'FitGang')
SITE_DESCRIPTION = os.environ.get('SITE_DESCRIPTION', 'Votre plateforme de fitness complète')
```

Ou dans `.env`:
```bash
SITE_NAME=Votre Nom
SITE_DESCRIPTION=Votre description
```

## 🧭 Navigation & Menus

### Menu Principal

Fichier: `fitgang_app/templates/base.html`

```html
<ul class="navbar-nav ms-auto">
    <li class="nav-item">
        <a class="nav-link" href="{{ url_for('shop.catalog') }}">Programmes</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="{{ url_for('blog.list') }}">Blog</a>
    </li>
    <!-- Ajouter vos liens ici -->
</ul>
```

### Ajouter un Lien

```html
<li class="nav-item">
    <a class="nav-link" href="/votre-page">Nouveau Lien</a>
</li>
```

### Footer

Fichier: `fitgang_app/templates/base.html`

```html
<div class="col-md-4">
    <h6>Liens rapides</h6>
    <ul class="list-unstyled">
        <li><a href="#">Votre lien</a></li>
    </ul>
</div>
```

## 🎯 Boutons & Call-to-Actions

### Styles de Boutons

```html
<!-- Bouton principal (rouge) -->
<a href="#" class="btn btn-danger">Acheter maintenant</a>

<!-- Bouton secondaire (outline) -->
<a href="#" class="btn btn-outline-danger">En savoir plus</a>

<!-- Bouton light -->
<a href="#" class="btn btn-light">Continuer</a>

<!-- Tailles -->
<a href="#" class="btn btn-danger btn-sm">Petit</a>
<a href="#" class="btn btn-danger">Normal</a>
<a href="#" class="btn btn-danger btn-lg">Grand</a>
```

## 📦 Ajouter un Produit

### Via l'Interface Admin

1. Se connecter en tant qu'admin
2. Aller sur `/admin/products`
3. Cliquer "Créer un produit"
4. Remplir le formulaire:
   - Titre
   - Type (Sport, Diète, Combiné, eBook)
   - Prix
   - Description
   - Image
   - etc.
5. Cocher "Publier"
6. Enregistrer

### Via Code (Fixtures)

Fichier: `scripts/load_fixtures.py`

```python
product = Product(
    title='Mon Nouveau Programme',
    slug=slugify('mon-nouveau-programme'),
    product_type=ProductType.PROGRAMME_SPORT,
    difficulty_level=DifficultyLevel.DEBUTANT,
    price=49.99,
    duration_weeks=8,
    description='Description complète...',
    is_published=True,
    is_featured=True
)
db.session.add(product)
db.session.commit()
```

## 📄 Créer un Plan de Repas

### Via l'Interface Admin

1. Créer d'abord un produit (type: Programme Diète ou Combiné)
2. Aller dans "Meal Plans"
3. Créer un nouveau plan lié au produit
4. Ajouter des recettes pour chaque jour

### Structure Recommandée

```
Plan de Repas (7 jours)
├── Jour 1
│   ├── Petit-déjeuner (Recette 1)
│   ├── Déjeuner (Recette 2)
│   ├── Dîner (Recette 3)
│   └── Collation (Recette 4)
├── Jour 2
...
```

## 🎁 Créer un Code Promo

### Via l'Interface

1. Admin → Gifts → Créer
2. Sélectionner le produit
3. Email destinataire
4. Message personnalisé
5. Date d'expiration
6. Enregistrer

### Via Script

```bash
python scripts/generate_gift_code.py <product_id> <email@example.com>
```

## 👤 Configurer les Affiliés

### Ajouter un Affilié

1. Admin → Affiliates → Créer
2. Remplir:
   - Code (ex: FITPRO10)
   - Nom
   - Email
   - Taux de commission (%)
3. Enregistrer

### Lien d'Affiliation

Format: `https://your-domain.com?ref=FITPRO10`

L'affilié partage ce lien, et les ventes sont trackées automatiquement.

## 🖌 Personnaliser le Design

### Cartes de Produits

Fichier: `fitgang_app/templates/shop/catalog.html`

```html
<div class="card product-card">
    <img src="{{ product.image_url }}" class="card-img-top">
    <div class="card-body">
        <h5>{{ product.title }}</h5>
        <p>{{ product.short_description }}</p>
        <span class="price">{{ product.price }}€</span>
    </div>
</div>
```

### Border Radius

Dans `main.css`, modifier:

```css
.card {
    border-radius: 12px;  /* Augmenter pour plus arrondi */
}

.btn {
    border-radius: 10px;  /* Boutons */
}
```

### Ombres

```css
.card:hover {
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);  /* Augmenter pour plus prononcé */
}
```

## 📧 Personnaliser les Emails

### Templates

Fichiers dans `fitgang_app/templates/emails/`:

- `welcome.html` - Email de bienvenue
- `purchase.html` - Confirmation d'achat
- `gift.html` - Email cadeau
- `password_reset.html` - Reset mot de passe

### Modifier un Template

Exemple `welcome.html`:

```html
<div class="header" style="background-color: #ED2F2F;">
    <h1>Bienvenue chez Votre Marque !</h1>
</div>

<div class="content">
    <p>Votre message personnalisé...</p>
</div>
```

**Note:** Utiliser inline CSS pour les emails (compatibilité clients mail).

## 🎨 Thème Sombre

Pour ajouter un mode sombre:

1. Ajouter dans `main.css`:

```css
@media (prefers-color-scheme: dark) {
    :root {
        --white: #1a1a1a;
        --gray-900: #ffffff;
        --gray-100: #2d2d2d;
        /* etc. */
    }
}
```

2. Ou créer un toggle manuel avec JavaScript

## 📱 Responsive Design

Le design est déjà responsive (Bootstrap 5). Pour personnaliser:

```css
/* Mobile */
@media (max-width: 768px) {
    .hero-section h1 {
        font-size: 2rem;  /* Titre plus petit sur mobile */
    }
}

/* Tablette */
@media (max-width: 992px) {
    /* Vos styles tablette */
}
```

## 🔧 Outils Utiles

### Générateur de Palette

- [Coolors.co](https://coolors.co/) - Générateur de palettes
- [Adobe Color](https://color.adobe.com/) - Roue chromatique

### Polices

- [Google Fonts](https://fonts.google.com/) - Polices gratuites
- [Font Pair](https://www.fontpair.co/) - Combinaisons de polices

### Images

- [Unsplash](https://unsplash.com/) - Photos gratuites fitness
- [Pexels](https://www.pexels.com/) - Photos et vidéos
- [SVGOMG](https://jakearchibald.github.io/svgomg/) - Optimiser SVG

### Icons

- [Bootstrap Icons](https://icons.getbootstrap.com/)
- [Heroicons](https://heroicons.com/)
- [Feather Icons](https://feathericons.com/)

## 🚀 Checklist Lancement

Avant de lancer votre site:

- [ ] Remplacer le logo
- [ ] Changer les couleurs si nécessaire
- [ ] Personnaliser les textes (accueil, footer, etc.)
- [ ] Ajouter vos produits
- [ ] Configurer les emails
- [ ] Tester le processus d'achat
- [ ] Vérifier le responsive mobile
- [ ] Configurer Stripe en production
- [ ] Ajouter Politique de Confidentialité / CGV
- [ ] Tester tous les formulaires
- [ ] Vérifier le SEO (meta tags)

---

Pour toute question, consultez la documentation complète dans `README.md` ou contactez le support.
