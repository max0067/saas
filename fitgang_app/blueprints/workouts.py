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
    debug_info = {
        'total_orders': len(current_user.orders) if current_user.orders else 0,
        'completed_orders': 0,
        'orders_detail': [],
        'error': None
    }

    try:
        for order in current_user.orders:
            try:
                order_info = {
                    'id': order.id,
                    'status': order.status.value if hasattr(order.status, 'value') else str(order.status),
                    'is_completed': order.status == OrderStatus.COMPLETED,
                    'items_count': len(order.items) if order.items else 0,
                    'items': []
                }

                if order.status == OrderStatus.COMPLETED:
                    debug_info['completed_orders'] += 1
                    for item in order.items:
                        try:
                            # Vérifier que le produit existe
                            if not item.product:
                                continue

                            # Vérifier si workouts existe comme attribut
                            has_workouts = False
                            workouts_count = 0
                            try:
                                if hasattr(item.product, 'workouts') and item.product.workouts:
                                    has_workouts = True
                                    workouts_count = len(item.product.workouts)
                                    workouts.extend(item.product.workouts)
                            except:
                                pass

                            item_info = {
                                'product_id': item.product_id,
                                'product_name': item.product.title if item.product else 'N/A',
                                'has_workouts': has_workouts,
                                'workouts_count': workouts_count
                            }
                            order_info['items'].append(item_info)
                        except Exception as item_error:
                            debug_info['error'] = f"Erreur item: {str(item_error)}"

                debug_info['orders_detail'].append(order_info)
            except Exception as order_error:
                debug_info['error'] = f"Erreur commande: {str(order_error)}"
    except Exception as e:
        debug_info['error'] = f"Erreur générale: {str(e)}"

    return render_template('workouts/index.html', workouts=workouts, debug_info=debug_info)


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
