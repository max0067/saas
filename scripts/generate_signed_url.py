"""Generate a signed URL for secure file download."""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from fitgang_app.utils.uploads import generate_signed_url


def generate_url(file_path, expiration_hours=24):
    """Generate signed URL for file."""
    with app.app_context():
        expiration = expiration_hours * 3600  # Convert to seconds

        url = generate_signed_url(file_path, expiration)

        if url:
            print(f"✅ Signed URL generated successfully!")
            print(f"File: {file_path}")
            print(f"Expires in: {expiration_hours} hours")
            print(f"\nURL:")
            print(url)
        else:
            print(f"❌ Failed to generate signed URL for {file_path}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python generate_signed_url.py <file_path> [expiration_hours]")
        print("\nExample:")
        print("  python generate_signed_url.py products/files/ebook.pdf")
        print("  python generate_signed_url.py products/files/ebook.pdf 48")
        sys.exit(1)

    file_path = sys.argv[1]
    expiration_hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24

    generate_url(file_path, expiration_hours)
