"""Workouts blueprint."""
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from fitgang_app.models import Workout, Exercise
from fitgang_app.models.order import OrderStatus

workouts_bp = Blueprint('workouts', __name__)


@workouts_bp.route('/')
@login_required
def list():
    """List available workouts."""
    # Get workouts from purchased programs
    workouts = []
    for order in current_user.orders:
        if order.status == OrderStatus.COMPLETED:
            for item in order.items:
                if item.product.workouts:
                    workouts.extend(item.product.workouts)

    return render_template('workouts/index.html', workouts=workouts)


@workouts_bp.route('/<int:workout_id>')
@login_required
def detail(workout_id):
    """Workout detail."""
    workout = Workout.query.get_or_404(workout_id)

    # Check if user has access
    if not current_user.is_admin() and not current_user.has_access_to_product(workout.product_id):
        flash('Vous devez acheter ce programme pour y accéder.', 'warning')
        return redirect(url_for('shop.programs'))

    return render_template('workouts/detail.html', workout=workout)


@workouts_bp.route('/exercises')
def exercises():
    """Exercise library."""
    exercises = Exercise.query.all()
    return render_template('workouts/exercises.html', exercises=exercises)
