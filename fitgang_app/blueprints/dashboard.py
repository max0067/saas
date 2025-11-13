"""Dashboard blueprint."""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from fitgang_app.models import WorkoutSession, Order, OrderStatus
from fitgang_app.models.user import UserPhoto
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    """User dashboard."""
    # Get recent workout sessions
    recent_sessions = WorkoutSession.query.filter_by(user_id=current_user.id).order_by(
        WorkoutSession.created_at.desc()
    ).limit(5).all()

    # Get workout stats
    total_workouts = WorkoutSession.query.filter_by(user_id=current_user.id).count()

    # Get purchase stats
    completed_orders = Order.query.filter_by(
        user_id=current_user.id,
        status=OrderStatus.COMPLETED
    ).all()

    # Get user photos for progress tracking
    user_photos = UserPhoto.query.filter_by(user_id=current_user.id).order_by(
        UserPhoto.uploaded_at.desc()
    ).limit(6).all()

    return render_template(
        'dashboard/index.html',
        recent_sessions=recent_sessions,
        total_workouts=total_workouts,
        recent_orders=completed_orders,
        user_photos=user_photos
    )
