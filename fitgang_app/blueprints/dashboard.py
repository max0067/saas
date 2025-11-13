"""Dashboard blueprint."""
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from fitgang_app.models import WorkoutSession, Order, OrderStatus, WeightEntry
from fitgang_app.models.user import UserPhoto
from fitgang_app import db
from sqlalchemy import func
from datetime import datetime

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

    # Get weight tracking data (with error handling for missing table)
    weight_entries = []
    weight_stats = None
    try:
        weight_entries = WeightEntry.query.filter_by(user_id=current_user.id).order_by(
            WeightEntry.recorded_at.desc()
        ).limit(30).all()
    except Exception:
        # Table might not exist yet, silently continue
        pass

    # Calculate weight stats
    if weight_entries:
        current_weight = weight_entries[0].weight if weight_entries else None
        starting_weight = weight_entries[-1].weight if len(weight_entries) > 0 else None
        target_weight = current_user.profile.target_weight if current_user.profile else None

        weight_change = None
        if current_weight and starting_weight:
            weight_change = round(current_weight - starting_weight, 1)

        progress_percentage = None
        if starting_weight and target_weight and current_weight:
            total_goal = abs(target_weight - starting_weight)
            current_progress = abs(current_weight - starting_weight)
            if total_goal > 0:
                progress_percentage = round((current_progress / total_goal) * 100, 1)

        weight_stats = {
            'current': current_weight,
            'starting': starting_weight,
            'target': target_weight,
            'change': weight_change,
            'progress': progress_percentage
        }

    return render_template(
        'dashboard/index.html',
        recent_sessions=recent_sessions,
        total_workouts=total_workouts,
        recent_orders=completed_orders,
        user_photos=user_photos,
        weight_entries=weight_entries,
        weight_stats=weight_stats,
        now=datetime.utcnow()
    )


@dashboard_bp.route('/weight/add', methods=['POST'])
@login_required
def add_weight():
    """Add weight entry."""
    try:
        weight = float(request.form.get('weight'))
        notes = request.form.get('notes', '').strip()
        recorded_at_str = request.form.get('recorded_at')

        # Parse date or use current datetime
        if recorded_at_str:
            recorded_at = datetime.strptime(recorded_at_str, '%Y-%m-%d')
        else:
            recorded_at = datetime.utcnow()

        # Create weight entry
        entry = WeightEntry(
            user_id=current_user.id,
            weight=weight,
            notes=notes if notes else None,
            recorded_at=recorded_at
        )

        db.session.add(entry)

        # Update current weight in profile
        if current_user.profile:
            current_user.profile.current_weight = weight
            current_user.profile.calculate_bmi()

        db.session.commit()

        flash('Poids enregistré avec succès!', 'success')
    except (ValueError, TypeError):
        flash('Erreur lors de l\'enregistrement du poids.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur: La table weight_entries n\'existe pas encore. Contactez l\'admin.', 'danger')

    return redirect(url_for('dashboard.index'))


@dashboard_bp.route('/weight/delete/<int:entry_id>', methods=['POST'])
@login_required
def delete_weight(entry_id):
    """Delete weight entry."""
    entry = WeightEntry.query.get_or_404(entry_id)

    # Verify ownership
    if entry.user_id != current_user.id:
        flash('Action non autorisée.', 'danger')
        return redirect(url_for('dashboard.index'))

    db.session.delete(entry)
    db.session.commit()

    flash('Entrée supprimée.', 'info')
    return redirect(url_for('dashboard.index'))


@dashboard_bp.route('/weight/data')
@login_required
def weight_data():
    """Get weight data for charts (API endpoint)."""
    entries = WeightEntry.query.filter_by(user_id=current_user.id).order_by(
        WeightEntry.recorded_at.asc()
    ).all()

    data = {
        'labels': [entry.recorded_at.strftime('%d/%m/%Y') for entry in entries],
        'weights': [entry.weight for entry in entries]
    }

    return jsonify(data)
