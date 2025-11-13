"""Test shop functionality."""
import pytest
from fitgang_app.models import Order, OrderStatus


def test_product_catalog(client, product):
    """Test product catalog page."""
    response = client.get('/programmes/')

    assert response.status_code == 200
    assert product.title.encode() in response.data


def test_product_detail(client, product):
    """Test product detail page."""
    response = client.get(f'/programmes/{product.slug}')

    assert response.status_code == 200
    assert product.title.encode() in response.data
    assert str(product.price).encode() in response.data


def test_add_to_cart(client, product):
    """Test adding product to cart."""
    response = client.post(f'/cart/add/{product.id}', follow_redirects=True)

    assert response.status_code == 200

    with client.session_transaction() as session:
        assert 'cart' in session
        assert len(session['cart']) == 1
        assert session['cart'][0]['product_id'] == product.id


def test_view_cart(client, product):
    """Test viewing cart."""
    # Add product to cart
    client.post(f'/cart/add/{product.id}')

    response = client.get('/cart/')

    assert response.status_code == 200
    assert product.title.encode() in response.data


def test_remove_from_cart(client, product):
    """Test removing product from cart."""
    # Add product to cart
    client.post(f'/cart/add/{product.id}')

    # Remove from cart
    response = client.get(f'/cart/remove/{product.id}', follow_redirects=True)

    assert response.status_code == 200

    with client.session_transaction() as session:
        assert len(session.get('cart', [])) == 0


def test_checkout_requires_login(client, product):
    """Test that checkout requires login."""
    # Add product to cart
    client.post(f'/cart/add/{product.id}')

    # Try to checkout without login
    response = client.get('/checkout/', follow_redirects=True)

    assert b'Veuillez vous connecter' in response.data or b'login' in response.data


def test_checkout_page(auth_client, product):
    """Test checkout page."""
    # Add product to cart
    auth_client.post(f'/cart/add/{product.id}')

    response = auth_client.get('/checkout/')

    assert response.status_code == 200
    assert product.title.encode() in response.data


def test_product_views_increment(client, product):
    """Test that product views increment."""
    initial_views = product.views

    client.get(f'/programmes/{product.slug}')

    from fitgang_app import db
    db.session.refresh(product)

    assert product.views == initial_views + 1
