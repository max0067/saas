"""Weight tracking model."""
from datetime import datetime
from fitgang_app import db


class WeightEntry(db.Model):
    """Weight entry model for tracking user weight over time."""

    __tablename__ = 'weight_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Weight data
    weight = db.Column(db.Float, nullable=False)  # in kg

    # Optional metadata
    notes = db.Column(db.Text)

    # Timestamps
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref='weight_entries')

    def __repr__(self):
        return f'<WeightEntry {self.id} - {self.weight}kg>'
