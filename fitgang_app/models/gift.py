"""Gift code models."""
from datetime import datetime, timedelta
from fitgang_app import db
import secrets
import string


class GiftCode(db.Model):
    """Gift code model."""

    __tablename__ = 'gift_codes'

    id = db.Column(db.Integer, primary_key=True)

    # Code details
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    # Sender and recipient
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    sender_email = db.Column(db.String(120))
    recipient_email = db.Column(db.String(120), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Set when redeemed

    # Message
    message = db.Column(db.Text)

    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_redeemed = db.Column(db.Boolean, default=False)
    max_uses = db.Column(db.Integer, default=1)
    uses_count = db.Column(db.Integer, default=0)

    # Expiration
    expires_at = db.Column(db.DateTime, nullable=False)

    # Timestamps
    redeemed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    product = db.relationship('Product')
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_gifts')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_gifts')
    logs = db.relationship('GiftLog', back_populates='gift_code', cascade='all, delete-orphan')

    @staticmethod
    def generate_code(length=12):
        """Generate a unique gift code."""
        characters = string.ascii_uppercase + string.digits
        while True:
            code = ''.join(secrets.choice(characters) for _ in range(length))
            if not GiftCode.query.filter_by(code=code).first():
                return code

    def is_valid(self):
        """Check if gift code is valid."""
        if not self.is_active:
            return False, "Ce code cadeau a été désactivé."
        if self.is_redeemed and self.uses_count >= self.max_uses:
            return False, "Ce code cadeau a déjà été utilisé."
        if datetime.utcnow() > self.expires_at:
            return False, "Ce code cadeau a expiré."
        return True, "Code valide"

    def redeem(self, user_id):
        """Redeem the gift code."""
        valid, message = self.is_valid()
        if not valid:
            return False, message

        self.uses_count += 1
        if self.uses_count >= self.max_uses:
            self.is_redeemed = True
            self.redeemed_at = datetime.utcnow()

        if not self.recipient_id:
            self.recipient_id = user_id

        return True, "Code cadeau utilisé avec succès!"

    def revoke(self):
        """Revoke the gift code."""
        self.is_active = False

    def __repr__(self):
        return f'<GiftCode {self.code}>'


class GiftLog(db.Model):
    """Gift code activity log."""

    __tablename__ = 'gift_logs'

    id = db.Column(db.Integer, primary_key=True)
    gift_code_id = db.Column(db.Integer, db.ForeignKey('gift_codes.id'), nullable=False)

    # Log details
    action = db.Column(db.String(50), nullable=False)  # created, sent, redeemed, revoked
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    details = db.Column(db.JSON)

    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    gift_code = db.relationship('GiftCode', back_populates='logs')
    user = db.relationship('User')

    def __repr__(self):
        return f'<GiftLog {self.id} - {self.action}>'
