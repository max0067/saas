"""Affiliate models."""
from datetime import datetime
from fitgang_app import db


class Affiliate(db.Model):
    """Affiliate model."""

    __tablename__ = 'affiliates'

    id = db.Column(db.Integer, primary_key=True)

    # Affiliate details
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    # Commission
    commission_rate = db.Column(db.Float, default=10.0)  # Percentage

    # Status
    is_active = db.Column(db.Boolean, default=True)

    # Stats
    total_clicks = db.Column(db.Integer, default=0)
    total_conversions = db.Column(db.Integer, default=0)
    total_revenue = db.Column(db.Float, default=0.0)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    clicks = db.relationship('AffiliateClick', back_populates='affiliate', cascade='all, delete-orphan')
    conversions = db.relationship('AffiliateConversion', back_populates='affiliate', cascade='all, delete-orphan')

    def get_affiliate_link(self, base_url):
        """Generate affiliate link."""
        return f"{base_url}?ref={self.code}"

    def calculate_commission(self, order_total):
        """Calculate commission amount."""
        return order_total * (self.commission_rate / 100)

    def __repr__(self):
        return f'<Affiliate {self.code} - {self.name}>'


class AffiliateClick(db.Model):
    """Affiliate click tracking."""

    __tablename__ = 'affiliate_clicks'

    id = db.Column(db.Integer, primary_key=True)
    affiliate_id = db.Column(db.Integer, db.ForeignKey('affiliates.id'), nullable=False)

    # Click details
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    referrer = db.Column(db.String(500))
    landing_page = db.Column(db.String(500))

    # UTM parameters
    utm_source = db.Column(db.String(100))
    utm_medium = db.Column(db.String(100))
    utm_campaign = db.Column(db.String(100))

    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    affiliate = db.relationship('Affiliate', back_populates='clicks')

    def __repr__(self):
        return f'<AffiliateClick {self.id}>'


class AffiliateConversion(db.Model):
    """Affiliate conversion tracking."""

    __tablename__ = 'affiliate_conversions'

    id = db.Column(db.Integer, primary_key=True)
    affiliate_id = db.Column(db.Integer, db.ForeignKey('affiliates.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)

    # Conversion details
    order_total = db.Column(db.Float, nullable=False)
    commission_amount = db.Column(db.Float, nullable=False)
    commission_paid = db.Column(db.Boolean, default=False)

    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime)

    # Relationships
    affiliate = db.relationship('Affiliate', back_populates='conversions')
    order = db.relationship('Order')

    def mark_as_paid(self):
        """Mark commission as paid."""
        self.commission_paid = True
        self.paid_at = datetime.utcnow()

    def __repr__(self):
        return f'<AffiliateConversion {self.id}>'
