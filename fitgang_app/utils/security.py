"""Security utilities."""
import secrets
import string
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer
from flask import current_app


def generate_token(data, salt='default', expires_in=3600):
    """
    Generate secure token.

    Args:
        data: Data to encode in token
        salt: Salt for token generation
        expires_in: Token expiration in seconds

    Returns:
        Token string
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(data, salt=salt)


def verify_token(token, salt='default', max_age=3600):
    """
    Verify and decode token.

    Args:
        token: Token to verify
        salt: Salt used for token generation
        max_age: Maximum token age in seconds

    Returns:
        Decoded data or None if invalid
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        data = serializer.loads(token, salt=salt, max_age=max_age)
        return data
    except Exception as e:
        current_app.logger.error(f"Token verification failed: {str(e)}")
        return None


def generate_password_reset_token(user_id):
    """Generate password reset token."""
    return generate_token(
        {'user_id': user_id, 'timestamp': datetime.utcnow().isoformat()},
        salt='password-reset',
        expires_in=3600  # 1 hour
    )


def verify_password_reset_token(token):
    """Verify password reset token."""
    data = verify_token(token, salt='password-reset', max_age=3600)
    if data:
        return data.get('user_id')
    return None


def generate_random_string(length=32, include_special=False):
    """
    Generate random string.

    Args:
        length: Length of string
        include_special: Include special characters

    Returns:
        Random string
    """
    characters = string.ascii_letters + string.digits
    if include_special:
        characters += string.punctuation

    return ''.join(secrets.choice(characters) for _ in range(length))


def generate_order_number():
    """
    Generate unique order number.

    Format: FG-YYYYMMDD-XXXXX
    """
    timestamp = datetime.utcnow().strftime('%Y%m%d')
    random_part = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    return f"FG-{timestamp}-{random_part}"


def generate_access_code(length=20):
    """Generate access code for digital products."""
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def sanitize_html(html_content):
    """
    Sanitize HTML content to prevent XSS.

    Args:
        html_content: HTML string to sanitize

    Returns:
        Sanitized HTML string
    """
    import bleach

    allowed_tags = [
        'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i',
        'li', 'ol', 'strong', 'ul', 'p', 'br', 'div', 'span', 'h1',
        'h2', 'h3', 'h4', 'h5', 'h6', 'img', 'pre', 'hr', 'table',
        'thead', 'tbody', 'tr', 'th', 'td'
    ]

    allowed_attributes = {
        'a': ['href', 'title', 'target', 'rel'],
        'img': ['src', 'alt', 'title', 'width', 'height'],
        'div': ['class', 'id'],
        'span': ['class', 'id'],
        'p': ['class', 'id'],
        'code': ['class'],
        'pre': ['class'],
        'table': ['class'],
        'td': ['colspan', 'rowspan'],
        'th': ['colspan', 'rowspan']
    }

    allowed_styles = []

    return bleach.clean(
        html_content,
        tags=allowed_tags,
        attributes=allowed_attributes,
        styles=allowed_styles,
        strip=True
    )


def validate_file_size(file, max_size_mb=100):
    """
    Validate file size.

    Args:
        file: FileStorage object
        max_size_mb: Maximum file size in MB

    Returns:
        tuple: (is_valid, error_message)
    """
    file.seek(0, 2)  # Seek to end of file
    file_size = file.tell()  # Get file size
    file.seek(0)  # Reset to beginning

    max_size_bytes = max_size_mb * 1024 * 1024

    if file_size > max_size_bytes:
        return False, f"File size exceeds maximum allowed size of {max_size_mb}MB"

    return True, None


def validate_file_type(file, allowed_mimes):
    """
    Validate file MIME type.

    Args:
        file: FileStorage object
        allowed_mimes: List of allowed MIME types

    Returns:
        tuple: (is_valid, error_message)
    """
    import magic

    file.seek(0)
    file_type = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)

    if file_type not in allowed_mimes:
        return False, f"File type {file_type} is not allowed"

    return True, None
