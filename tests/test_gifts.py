"""Test gift code functionality."""
import pytest
from fitgang_app.models import GiftCode
from datetime import datetime, timedelta


def test_create_gift_code_admin_only(auth_client, product):
    """Test that only admins can create gift codes."""
    response = auth_client.get('/gifts/create')

    # Non-admin should be forbidden or redirected
    assert response.status_code in [403, 302]


def test_gift_code_validation(app, product):
    """Test gift code validation."""
    with app.app_context():
        # Create valid gift code
        code = GiftCode(
            code='TEST123',
            product_id=product.id,
            recipient_email='test@example.com',
            expires_at=datetime.utcnow() + timedelta(days=30)
        )

        from fitgang_app import db
        db.session.add(code)
        db.session.commit()

        # Test validation
        valid, message = code.is_valid()
        assert valid is True


def test_expired_gift_code(app, product):
    """Test expired gift code validation."""
    with app.app_context():
        # Create expired gift code
        code = GiftCode(
            code='EXPIRED',
            product_id=product.id,
            recipient_email='test@example.com',
            expires_at=datetime.utcnow() - timedelta(days=1)
        )

        from fitgang_app import db
        db.session.add(code)
        db.session.commit()

        # Test validation
        valid, message = code.is_valid()
        assert valid is False
        assert 'expiré' in message


def test_redeem_gift_code(auth_client, app, product, user):
    """Test redeeming a gift code."""
    with app.app_context():
        # Create gift code
        code = GiftCode(
            code='REDEEM123',
            product_id=product.id,
            recipient_email=user.email,
            expires_at=datetime.utcnow() + timedelta(days=30)
        )

        from fitgang_app import db
        db.session.add(code)
        db.session.commit()

        # Redeem code
        response = auth_client.post('/gifts/redeem', data={
            'code': 'REDEEM123'
        }, follow_redirects=True)

        assert response.status_code == 200

        # Code should be redeemed
        db.session.refresh(code)
        assert code.is_redeemed is True


def test_api_validate_gift_code(client, app, product):
    """Test API gift code validation endpoint."""
    with app.app_context():
        # Create gift code
        code = GiftCode(
            code='API123',
            product_id=product.id,
            recipient_email='test@example.com',
            expires_at=datetime.utcnow() + timedelta(days=30)
        )

        from fitgang_app import db
        db.session.add(code)
        db.session.commit()

        # Test API
        response = client.get('/api/gifts/validate/API123')

        assert response.status_code == 200
        data = response.get_json()
        assert data['valid'] is True


def test_api_invalid_gift_code(client):
    """Test API with invalid gift code."""
    response = client.get('/api/gifts/validate/INVALID')

    assert response.status_code == 404
    data = response.get_json()
    assert data['valid'] is False
