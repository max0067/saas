"""Custom decorators for access control."""
from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user


def admin_required(f):
    """Require admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Veuillez vous connecter pour accéder à cette page.', 'warning')
            return redirect(url_for('auth.login'))

        if not current_user.is_admin():
            flash('Vous n\'avez pas les permissions nécessaires.', 'danger')
            abort(403)

        return f(*args, **kwargs)

    return decorated_function


def coach_required(f):
    """Require coach or admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Veuillez vous connecter pour accéder à cette page.', 'warning')
            return redirect(url_for('auth.login'))

        if not (current_user.is_admin() or current_user.is_coach()):
            flash('Vous n\'avez pas les permissions nécessaires.', 'danger')
            abort(403)

        return f(*args, **kwargs)

    return decorated_function


def product_access_required(product_id):
    """Require access to specific product."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Veuillez vous connecter pour accéder à cette page.', 'warning')
                return redirect(url_for('auth.login'))

            # Admin and coaches have access to all products
            if current_user.is_admin() or current_user.is_coach():
                return f(*args, **kwargs)

            # Check if user has purchased the product
            if not current_user.has_access_to_product(product_id):
                flash('Vous devez acheter ce produit pour y accéder.', 'warning')
                return redirect(url_for('shop.product_detail', product_id=product_id))

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def verified_email_required(f):
    """Require verified email."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Veuillez vous connecter pour accéder à cette page.', 'warning')
            return redirect(url_for('auth.login'))

        if not current_user.is_verified:
            flash('Veuillez vérifier votre email pour accéder à cette fonctionnalité.', 'warning')
            return redirect(url_for('main.index'))

        return f(*args, **kwargs)

    return decorated_function
