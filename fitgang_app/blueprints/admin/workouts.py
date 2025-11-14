"""Admin workouts management blueprint."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from fitgang_app import db
from fitgang_app.models.workout import Workout, Exercise, WorkoutExercise
from fitgang_app.models.product import Product, ProductType
from fitgang_app.utils.decorators import admin_required

admin_workouts_bp = Blueprint('admin_workouts', __name__)


@admin_workouts_bp.route('/')
@admin_required
def index():
    """List all workouts."""
    # Group workouts by product - tous les programmes sportifs
    products = Product.query.filter(
        Product.product_type.in_([
            ProductType.PROGRAMME_SPORT,
            ProductType.PROGRAMME_DIETE,
            ProductType.PROGRAMME_COMBINE
        ])
    ).all()

    workouts_by_product = {}
    for product in products:
        workouts_by_product[product.id] = {
            'product': product,
            'workouts': Workout.query.filter_by(product_id=product.id).order_by(
                Workout.week_number, Workout.day_number
            ).all()
        }

    return render_template('admin/workouts/index.html', workouts_by_product=workouts_by_product)


@admin_workouts_bp.route('/product/<int:product_id>/create', methods=['GET', 'POST'])
@admin_required
def create(product_id):
    """Create a new workout for a product."""
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        try:
            workout = Workout(
                product_id=product_id,
                name=request.form.get('name'),
                description=request.form.get('description'),
                week_number=int(request.form.get('week_number', 1)),
                day_number=int(request.form.get('day_number', 1)),
                duration_minutes=int(request.form.get('duration_minutes', 60)) if request.form.get('duration_minutes') else None,
                difficulty=request.form.get('difficulty'),
                warmup=request.form.get('warmup'),
                cooldown=request.form.get('cooldown'),
                notes=request.form.get('notes')
            )

            db.session.add(workout)
            db.session.commit()

            flash(f'Workout "{workout.name}" créé avec succès!', 'success')
            return redirect(url_for('admin_workouts.index'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la création: {str(e)}', 'danger')

    return render_template('admin/workouts/form.html', product=product, workout=None)


@admin_workouts_bp.route('/<int:workout_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(workout_id):
    """Edit a workout."""
    workout = Workout.query.get_or_404(workout_id)

    if request.method == 'POST':
        try:
            workout.name = request.form.get('name')
            workout.description = request.form.get('description')
            workout.week_number = int(request.form.get('week_number', 1))
            workout.day_number = int(request.form.get('day_number', 1))
            workout.duration_minutes = int(request.form.get('duration_minutes', 60)) if request.form.get('duration_minutes') else None
            workout.difficulty = request.form.get('difficulty')
            workout.warmup = request.form.get('warmup')
            workout.cooldown = request.form.get('cooldown')
            workout.notes = request.form.get('notes')

            db.session.commit()

            flash(f'Workout "{workout.name}" mis à jour!', 'success')
            return redirect(url_for('admin_workouts.index'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la mise à jour: {str(e)}', 'danger')

    return render_template('admin/workouts/form.html', product=workout.product, workout=workout)


@admin_workouts_bp.route('/<int:workout_id>/delete', methods=['POST'])
@admin_required
def delete(workout_id):
    """Delete a workout."""
    workout = Workout.query.get_or_404(workout_id)

    try:
        db.session.delete(workout)
        db.session.commit()
        flash(f'Workout "{workout.name}" supprimé.', 'info')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression: {str(e)}', 'danger')

    return redirect(url_for('admin_workouts.index'))


@admin_workouts_bp.route('/product/<int:product_id>/quick-create', methods=['POST'])
@admin_required
def quick_create_week(product_id):
    """Quickly create a full week of workouts."""
    product = Product.query.get_or_404(product_id)

    try:
        week_number = int(request.form.get('week_number', 1))
        days_per_week = int(request.form.get('days_per_week', 5))

        workout_templates = [
            {'day': 1, 'name': 'Séance Push (Pectoraux, Épaules, Triceps)', 'difficulty': 'intermediate'},
            {'day': 2, 'name': 'Séance Pull (Dos, Biceps)', 'difficulty': 'intermediate'},
            {'day': 3, 'name': 'Séance Jambes (Quadriceps, Ischio, Mollets)', 'difficulty': 'advanced'},
            {'day': 4, 'name': 'Séance Upper Body (Haut du corps)', 'difficulty': 'intermediate'},
            {'day': 5, 'name': 'Séance Full Body + Cardio', 'difficulty': 'intermediate'},
            {'day': 6, 'name': 'Séance Cardio HIIT', 'difficulty': 'beginner'},
            {'day': 7, 'name': 'Repos actif / Mobilité', 'difficulty': 'beginner'},
        ]

        created_count = 0
        for i in range(min(days_per_week, len(workout_templates))):
            template = workout_templates[i]

            # Check if workout already exists
            existing = Workout.query.filter_by(
                product_id=product_id,
                week_number=week_number,
                day_number=template['day']
            ).first()

            if not existing:
                workout = Workout(
                    product_id=product_id,
                    name=f"Semaine {week_number} - {template['name']}",
                    description=f"Entraînement jour {template['day']} de la semaine {week_number}",
                    week_number=week_number,
                    day_number=template['day'],
                    duration_minutes=60,
                    difficulty=template['difficulty'],
                    warmup='5-10 minutes de cardio léger + étirements dynamiques',
                    cooldown='Étirements statiques 5-10 minutes',
                    notes='Hydrate-toi bien pendant la séance!'
                )
                db.session.add(workout)
                created_count += 1

        db.session.commit()
        flash(f'{created_count} workouts créés pour la semaine {week_number}!', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la création rapide: {str(e)}', 'danger')

    return redirect(url_for('admin_workouts.index'))
