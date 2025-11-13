"""Product models."""
from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as SQLEnum
from fitgang_app import db


class ProductType(str, Enum):
    """Product types."""
    PROGRAMME_SPORT = 'programme_sport'
    PROGRAMME_DIETE = 'programme_diete'
    PROGRAMME_COMBINE = 'programme_combine'
    EBOOK = 'ebook'


class DifficultyLevel(str, Enum):
    """Difficulty levels."""
    DEBUTANT = 'debutant'
    INTERMEDIAIRE = 'intermediaire'
    AVANCE = 'avance'


# Association table for product tags
product_tags = db.Table(
    'product_tags',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('tag', db.String(50), primary_key=True)
)

# Association table for related products
related_products = db.Table(
    'related_products',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('related_product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)


class Product(db.Model):
    """Product model."""

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)

    # Basic information
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(250), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(500))

    # Product type
    product_type = db.Column(SQLEnum(ProductType), nullable=False)
    difficulty_level = db.Column(SQLEnum(DifficultyLevel))

    # Pricing
    price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float)  # For showing discounts
    currency = db.Column(db.String(3), default='EUR')

    # Inventory
    sku = db.Column(db.String(100), unique=True)
    stock = db.Column(db.Integer)  # Null = unlimited
    is_digital = db.Column(db.Boolean, default=True)

    # Programme details
    duration_weeks = db.Column(db.Integer)  # Programme duration

    # Media
    image_url = db.Column(db.String(500))
    preview_video_url = db.Column(db.String(500))
    gallery_images = db.Column(db.JSON)  # Array of image URLs

    # Files (for eBooks and downloadables)
    file_path = db.Column(db.String(500))  # Main file (PDF, EPUB, etc.)
    file_size = db.Column(db.Integer)  # in bytes
    file_format = db.Column(db.String(20))  # pdf, epub, etc.
    preview_pages = db.Column(db.Integer, default=10)  # Number of preview pages

    # eBook specific
    author = db.Column(db.String(100))
    isbn = db.Column(db.String(20))
    pages = db.Column(db.Integer)

    # Download restrictions
    max_downloads = db.Column(db.Integer, default=5)

    # SEO
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.String(500))
    meta_keywords = db.Column(db.String(500))

    # Status
    is_published = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)

    # Stats
    views = db.Column(db.Integer, default=0)
    sales_count = db.Column(db.Integer, default=0)

    # Timestamps
    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    tags = db.relationship(
        'Product',
        secondary=product_tags,
        lazy='subquery',
        viewonly=True
    )
    related = db.relationship(
        'Product',
        secondary=related_products,
        primaryjoin=(related_products.c.product_id == id),
        secondaryjoin=(related_products.c.related_product_id == id),
        lazy='dynamic'
    )
    meal_plans = db.relationship('MealPlan', back_populates='product', cascade='all, delete-orphan')
    workouts = db.relationship('Workout', back_populates='product', cascade='all, delete-orphan')

    def get_discount_percentage(self):
        """Calculate discount percentage."""
        if self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0

    def is_in_stock(self):
        """Check if product is in stock."""
        if self.stock is None:  # Unlimited stock
            return True
        return self.stock > 0

    def increment_views(self):
        """Increment product views."""
        self.views += 1
        db.session.commit()

    def __repr__(self):
        return f'<Product {self.title}>'
