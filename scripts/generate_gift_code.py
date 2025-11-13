"""Generate a gift code."""
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from fitgang_app import db
from fitgang_app.models import GiftCode, Product
from fitgang_app.utils.email import send_gift_email


def generate_gift_code(product_id, recipient_email, sender_email=None, message=None, days=365):
    """Generate a new gift code."""
    with app.app_context():
        # Check if product exists
        product = Product.query.get(product_id)
        if not product:
            print(f"❌ Product with ID {product_id} not found.")
            return

        # Generate code
        code = GiftCode.generate_code()

        # Create gift code
        gift = GiftCode(
            code=code,
            product_id=product_id,
            sender_email=sender_email,
            recipient_email=recipient_email,
            message=message,
            expires_at=datetime.utcnow() + timedelta(days=days)
        )

        db.session.add(gift)
        db.session.commit()

        print(f"✅ Gift code generated successfully!")
        print(f"Code: {code}")
        print(f"Product: {product.title}")
        print(f"Recipient: {recipient_email}")
        print(f"Expires: {gift.expires_at.strftime('%Y-%m-%d')}")

        # Send email
        try:
            send_gift_email(gift)
            print("📧 Email sent to recipient.")
        except Exception as e:
            print(f"⚠️  Email could not be sent: {str(e)}")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python generate_gift_code.py <product_id> <recipient_email> [sender_email] [message] [days]")
        print("\nExample:")
        print("  python generate_gift_code.py 1 user@example.com")
        print("  python generate_gift_code.py 1 user@example.com admin@fitgang.fr 'Bon anniversaire!' 365")
        sys.exit(1)

    product_id = int(sys.argv[1])
    recipient_email = sys.argv[2]
    sender_email = sys.argv[3] if len(sys.argv) > 3 else None
    message = sys.argv[4] if len(sys.argv) > 4 else None
    days = int(sys.argv[5]) if len(sys.argv) > 5 else 365

    generate_gift_code(product_id, recipient_email, sender_email, message, days)
