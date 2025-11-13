"""Pytest configuration and fixtures."""
import pytest
from fitgang_app import create_app, db
from fitgang_app.models import User, UserProfile, Product, ProductType
from slugify import slugify


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture
def auth_client(client, user):
    """Create authenticated client."""
    client.post('/auth/login', data={
        'email': user.email,
        'password': 'password123',
        'remember_me': False
    }, follow_redirects=True)
    return client


@pytest.fixture
def user(app):
    """Create test user."""
    user = User(
        username='testuser',
        email='test@example.com',
        is_active=True,
        is_verified=True
    )
    user.set_password('password123')

    profile = UserProfile(user=user)

    db.session.add(user)
    db.session.add(profile)
    db.session.commit()

    return user


@pytest.fixture
def admin_user(app):
    """Create admin user."""
    admin = User(
        username='admin',
        email='admin@example.com',
        role='admin',
        is_active=True,
        is_verified=True
    )
    admin.set_password('admin123')

    profile = UserProfile(user=admin)

    db.session.add(admin)
    db.session.add(profile)
    db.session.commit()

    return admin


@pytest.fixture
def product(app):
    """Create test product."""
    product = Product(
        title='Test Programme',
        slug=slugify('test-programme'),
        product_type=ProductType.PROGRAMME_SPORT,
        price=49.99,
        description='Test product description',
        is_published=True
    )

    db.session.add(product)
    db.session.commit()

    return product
