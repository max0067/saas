"""Admin analytics blueprint."""
from flask import Blueprint, render_template, jsonify
from fitgang_app.models import Order, User, Product
from fitgang_app.utils.decorators import admin_required
from sqlalchemy import func, extract
from datetime import datetime, timedelta

admin_analytics_bp = Blueprint('admin_analytics', __name__)


@admin_analytics_bp.route('/')
@admin_required
def index():
    """Analytics dashboard."""
    # Revenue by month (last 12 months)
    twelve_months_ago = datetime.utcnow() - timedelta(days=365)

    monthly_revenue = db.session.query(
        extract('year', Order.created_at).label('year'),
        extract('month', Order.created_at).label('month'),
        func.sum(Order.total_amount).label('revenue')
    ).filter(
        Order.status == 'completed',
        Order.created_at >= twelve_months_ago
    ).group_by('year', 'month').all()

    # Best selling products
    best_sellers = db.session.query(
        Product.title,
        func.count(OrderItem.id).label('sales')
    ).join(OrderItem).join(Order).filter(
        Order.status == 'completed'
    ).group_by(Product.title).order_by(func.count(OrderItem.id).desc()).limit(10).all()

    # User registrations by month
    monthly_users = db.session.query(
        extract('year', User.created_at).label('year'),
        extract('month', User.created_at).label('month'),
        func.count(User.id).label('users')
    ).filter(
        User.created_at >= twelve_months_ago
    ).group_by('year', 'month').all()

    return render_template(
        'admin/analytics.html',
        monthly_revenue=monthly_revenue,
        best_sellers=best_sellers,
        monthly_users=monthly_users
    )


@admin_analytics_bp.route('/data/revenue')
@admin_required
def revenue_data():
    """Get revenue data for charts."""
    twelve_months_ago = datetime.utcnow() - timedelta(days=365)

    data = db.session.query(
        extract('year', Order.created_at).label('year'),
        extract('month', Order.created_at).label('month'),
        func.sum(Order.total_amount).label('revenue')
    ).filter(
        Order.status == 'completed',
        Order.created_at >= twelve_months_ago
    ).group_by('year', 'month').all()

    return jsonify({
        'labels': [f'{int(d.year)}-{int(d.month):02d}' for d in data],
        'data': [float(d.revenue) for d in data]
    })
