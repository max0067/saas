"""Order models."""
from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as SQLEnum
from fitgang_app import db


class OrderStatus(str, Enum):
    """Order status."""
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'
    REFUNDED = 'refunded'


class Order(db.Model):
    """Order model."""

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)

    # User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Order details
    status = db.Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='EUR')

    # Payment
    stripe_payment_intent_id = db.Column(db.String(255))
    stripe_charge_id = db.Column(db.String(255))
    payment_method = db.Column(db.String(50))

    # Customer info
    customer_email = db.Column(db.String(120))
    customer_name = db.Column(db.String(200))
    billing_address = db.Column(db.JSON)

    # Affiliate tracking
    affiliate_code = db.Column(db.String(50))
    affiliate_id = db.Column(db.Integer, db.ForeignKey('affiliates.id'))

    # Access link
    access_code = db.Column(db.String(100), unique=True)  # Unique code for accessing products
    access_link_sent = db.Column(db.Boolean, default=False)

    # Notes (for admin gifts, etc.)
    notes = db.Column(db.Text)

    # Timestamps
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='orders')
    items = db.relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    affiliate = db.relationship('Affiliate', backref='orders')

    def calculate_total(self):
        """Calculate order total from items."""
        self.total_amount = sum(item.subtotal for item in self.items)
        return self.total_amount

    def mark_as_completed(self):
        """Mark order as completed."""
        self.status = OrderStatus.COMPLETED
        self.completed_at = datetime.utcnow()

    def __repr__(self):
        return f'<Order {self.order_number}>'


class OrderItem(db.Model):
    """Order item model."""

    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    # Item details
    product_name = db.Column(db.String(200), nullable=False)  # Snapshot at time of purchase
    quantity = db.Column(db.Integer, default=1, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    # Download tracking
    downloads_count = db.Column(db.Integer, default=0)
    last_download_at = db.Column(db.DateTime)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    order = db.relationship('Order', back_populates='items')
    product = db.relationship('Product')

    def can_download(self):
        """Check if user can still download this item."""
        if self.product.max_downloads is None:
            return True
        return self.downloads_count < self.product.max_downloads

    def increment_download(self):
        """Increment download count."""
        self.downloads_count += 1
        self.last_download_at = datetime.utcnow()
        db.session.commit()

    def __repr__(self):
        return f'<OrderItem {self.id} - {self.product_name}>'
