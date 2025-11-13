"""Revoke a gift code."""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from fitgang_app import db
from fitgang_app.models import GiftCode


def revoke_gift(code):
    """Revoke a gift code."""
    with app.app_context():
        gift = GiftCode.query.filter_by(code=code.upper()).first()

        if not gift:
            print(f"❌ Gift code '{code}' not found.")
            return

        if not gift.is_active:
            print(f"⚠️  Gift code '{code}' is already inactive.")
            return

        gift.revoke()
        db.session.commit()

        print(f"✅ Gift code '{code}' has been revoked.")
        print(f"Product: {gift.product.title}")
        print(f"Recipient: {gift.recipient_email}")
        print(f"Was redeemed: {'Yes' if gift.is_redeemed else 'No'}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python revoke_gift.py <gift_code>")
        print("\nExample:")
        print("  python revoke_gift.py WELCOME2024")
        sys.exit(1)

    code = sys.argv[1]
    revoke_gift(code)
