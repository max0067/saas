"""User models."""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from fitgang_app import db


class User(UserMixin, db.Model):
    """User model."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # User roles
    role = db.Column(db.String(20), default='user')  # admin, coach, user
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)

    # Password management
    force_password_change = db.Column(db.Boolean, default=False)
    last_password_change_at = db.Column(db.DateTime, default=datetime.utcnow)
    password_reset_token = db.Column(db.String(255), nullable=True)
    password_reset_expires = db.Column(db.DateTime, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = db.Column(db.DateTime)

    # Relationships
    profile = db.relationship('UserProfile', back_populates='user', uselist=False, cascade='all, delete-orphan')
    photos = db.relationship('UserPhoto', back_populates='user', cascade='all, delete-orphan')
    workout_sessions = db.relationship('WorkoutSession', back_populates='user', cascade='all, delete-orphan')
    orders = db.relationship('Order', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password):
        """Set password hash."""
        self.password_hash = generate_password_hash(password)
        self.last_password_change_at = datetime.utcnow()

    def check_password(self, password):
        """Check password hash."""
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        """Check if user is admin."""
        return self.role == 'admin'

    def is_coach(self):
        """Check if user is coach."""
        return self.role == 'coach'

    def has_access_to_product(self, product_id):
        """Check if user has access to a product."""
        from fitgang_app.models.order import OrderStatus
        for order in self.orders:
            if order.status == OrderStatus.COMPLETED:
                for item in order.items:
                    if item.product_id == product_id:
                        return True
        return False

    def __repr__(self):
        return f'<User {self.username}>'


class UserProfile(db.Model):
    """User profile model."""

    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    # Personal information
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(20))  # male, female, other

    # Physical attributes
    height = db.Column(db.Float)  # in cm
    current_weight = db.Column(db.Float)  # in kg
    target_weight = db.Column(db.Float)  # in kg

    # Goals and preferences
    fitness_goal = db.Column(db.String(100))
    activity_level = db.Column(db.String(50))
    dietary_preferences = db.Column(db.Text)

    # Calculated values (stored for convenience)
    bmi = db.Column(db.Float)
    tdee = db.Column(db.Float)  # Total Daily Energy Expenditure

    # Settings
    preferred_language = db.Column(db.String(10), default='fr')
    timezone = db.Column(db.String(50), default='Europe/Paris')
    newsletter_subscribed = db.Column(db.Boolean, default=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='profile')

    def calculate_bmi(self):
        """Calculate BMI if height and weight are available."""
        if self.height and self.current_weight:
            height_m = self.height / 100
            self.bmi = round(self.current_weight / (height_m ** 2), 2)
        return self.bmi

    def __repr__(self):
        return f'<UserProfile {self.user_id}>'


class UserPhoto(db.Model):
    """User before/after photos."""

    __tablename__ = 'user_photos'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Photo details
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    photo_type = db.Column(db.String(20), nullable=False)  # before, after, progress

    # Metadata
    weight_at_photo = db.Column(db.Float)
    description = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=False)

    # Timestamps
    taken_at = db.Column(db.DateTime, default=datetime.utcnow)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='photos')

    def __repr__(self):
        return f'<UserPhoto {self.id} - {self.photo_type}>'
