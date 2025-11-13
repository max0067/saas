"""Flask Blueprints."""
from fitgang_app.blueprints.main import main_bp
from fitgang_app.blueprints.auth import auth_bp
from fitgang_app.blueprints.dashboard import dashboard_bp
from fitgang_app.blueprints.profile import profile_bp
from fitgang_app.blueprints.blog import blog_bp
from fitgang_app.blueprints.shop import shop_bp
from fitgang_app.blueprints.cart import cart_bp
from fitgang_app.blueprints.checkout import checkout_bp
from fitgang_app.blueprints.workouts import workouts_bp
from fitgang_app.blueprints.calculators import calculators_bp
from fitgang_app.blueprints.gifts import gifts_bp
from fitgang_app.blueprints.webhooks import webhooks_bp
from fitgang_app.blueprints.api import api_bp
from fitgang_app.blueprints.admin import (
    admin_bp, admin_users_bp, admin_products_bp,
    admin_blog_bp, admin_analytics_bp, admin_affiliates_bp
)

__all__ = [
    'main_bp',
    'auth_bp',
    'dashboard_bp',
    'profile_bp',
    'blog_bp',
    'shop_bp',
    'cart_bp',
    'checkout_bp',
    'workouts_bp',
    'calculators_bp',
    'gifts_bp',
    'webhooks_bp',
    'api_bp',
    'admin_bp',
    'admin_users_bp',
    'admin_products_bp',
    'admin_blog_bp',
    'admin_analytics_bp',
    'admin_affiliates_bp',
]
