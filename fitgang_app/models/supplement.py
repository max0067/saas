"""Supplement models for dietary supplements and affiliate products."""
from datetime import datetime
from fitgang_app import db


class Supplement(db.Model):
    """Supplement/Complement model for affiliate products."""

    __tablename__ = 'supplements'

    id = db.Column(db.Integer, primary_key=True)

    # Basic information
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(250), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(500))

    # Category
    category = db.Column(db.String(100))  # Protéine, Créatine, Vitamines, etc.
    brand = db.Column(db.String(100))

    # Media
    image_url = db.Column(db.String(500))
    gallery_images = db.Column(db.JSON)  # Array of image URLs

    # Affiliate link
    affiliate_link = db.Column(db.String(500), nullable=False)
    affiliate_code = db.Column(db.String(100))

    # Display information
    benefits = db.Column(db.JSON)  # Array of benefit strings
    usage_instructions = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    warnings = db.Column(db.Text)

    # Pricing (for display only)
    price_range = db.Column(db.String(50))  # "25-35€" ou "À partir de 29€"

    # Stats
    clicks = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)

    # Status
    is_published = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    display_order = db.Column(db.Integer, default=0)

    # SEO
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.String(500))

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def increment_views(self):
        """Increment product views."""
        self.views += 1
        db.session.commit()

    def increment_clicks(self):
        """Increment affiliate clicks."""
        self.clicks += 1
        db.session.commit()

    def __repr__(self):
        return f'<Supplement {self.name}>'


class SupplementRecommendation(db.Model):
    """Associate supplements with programs/products."""

    __tablename__ = 'supplement_recommendations'

    id = db.Column(db.Integer, primary_key=True)
    supplement_id = db.Column(db.Integer, db.ForeignKey('supplements.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    recommendation_text = db.Column(db.Text)
    display_order = db.Column(db.Integer, default=0)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    supplement = db.relationship('Supplement', backref=db.backref('recommendations', lazy='dynamic'))
    product = db.relationship('Product', backref=db.backref('supplement_recommendations', lazy='dynamic'))

    def __repr__(self):
        return f'<SupplementRecommendation Supplement:{self.supplement_id} Product:{self.product_id}>'
