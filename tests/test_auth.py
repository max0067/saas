"""Test authentication."""
import pytest
from fitgang_app.models import User


def test_register(client):
    """Test user registration."""
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'password123',
        'password_confirm': 'password123',
        'accept_terms': True
    }, follow_redirects=True)

    assert response.status_code == 200
    assert User.query.filter_by(email='new@example.com').first() is not None


def test_register_duplicate_email(client, user):
    """Test registration with duplicate email."""
    response = client.post('/auth/register', data={
        'username': 'anotheruser',
        'email': user.email,
        'password': 'password123',
        'password_confirm': 'password123',
        'accept_terms': True
    })

    assert b'Cette adresse email est déjà utilisée' in response.data


def test_login(client, user):
    """Test user login."""
    response = client.post('/auth/login', data={
        'email': user.email,
        'password': 'password123',
        'remember_me': False
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Connexion réussie' in response.data


def test_login_wrong_password(client, user):
    """Test login with wrong password."""
    response = client.post('/auth/login', data={
        'email': user.email,
        'password': 'wrongpassword',
        'remember_me': False
    })

    assert b'Email ou mot de passe incorrect' in response.data


def test_logout(auth_client):
    """Test logout."""
    response = auth_client.get('/auth/logout', follow_redirects=True)

    assert response.status_code == 200
    assert b'déconnecté' in response.data


def test_forgot_password(client, user):
    """Test forgot password."""
    response = client.post('/auth/forgot-password', data={
        'email': user.email
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'lien de réinitialisation' in response.data


def test_force_password_change(client, user):
    """Test force password change."""
    user.force_password_change = True
    from fitgang_app import db
    db.session.commit()

    response = client.post('/auth/login', data={
        'email': user.email,
        'password': 'password123'
    }, follow_redirects=True)

    assert b'changer votre mot de passe' in response.data


def test_protected_route_requires_login(client):
    """Test that protected routes require login."""
    response = client.get('/dashboard/', follow_redirects=True)

    assert b'Veuillez vous connecter' in response.data or b'login' in response.data
