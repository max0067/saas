"""Admin blueprints."""
from flask import Blueprint, render_template
from flask_login import login_required
from fitgang_app import db
from fitgang_app.utils.decorators import admin_required
from fitgang_app.models import User, Product, Order, BlogPost, OrderStatus
from sqlalchemy import func

# Main admin blueprint
admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
@admin_required
def index():
    """Admin dashboard."""
    # Get stats
    total_users = User.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.filter_by(status=OrderStatus.COMPLETED).count()
    total_revenue = db.session.query(func.sum(Order.total_amount)).filter_by(status=OrderStatus.COMPLETED).scalar() or 0

    # Recent orders
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()

    return render_template(
        'admin/dashboard.html',
        total_users=total_users,
        total_products=total_products,
        total_orders=total_orders,
        total_revenue=total_revenue,
        recent_orders=recent_orders
    )


# Import other admin blueprints
from fitgang_app.blueprints.admin.users import admin_users_bp
from fitgang_app.blueprints.admin.products import admin_products_bp
from fitgang_app.blueprints.admin.blog import admin_blog_bp
from fitgang_app.blueprints.admin.analytics import admin_analytics_bp
from fitgang_app.blueprints.admin.affiliates import admin_affiliates_bp
from fitgang_app.blueprints.admin.photos import admin_photos_bp
from fitgang_app.blueprints.admin.gifts import admin_gifts_bp
from fitgang_app.blueprints.admin.workouts import admin_workouts_bp
# Temporarily disabled: from fitgang_app.blueprints.admin.home_editor import admin_home_editor_bp

__all__ = [
    'admin_bp',
    'admin_users_bp',
    'admin_products_bp',
    'admin_blog_bp',
    'admin_analytics_bp',
    'admin_affiliates_bp',
    'admin_photos_bp',
    'admin_gifts_bp',
    'admin_workouts_bp',
    # 'admin_home_editor_bp',
]
