"""Admin programs blueprint."""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from fitgang_app import db
from fitgang_app.models import Product, ProductType, ProgramWeek, ProgramDay
from fitgang_app.utils.decorators import admin_required
from fitgang_app.utils.uploads import save_uploaded_file
from slugify import slugify
import json

admin_programs_bp = Blueprint('admin_programs', __name__)


@admin_programs_bp.route('/')
@admin_required
def index():
    """List programs."""
    page = request.args.get('page', 1, type=int)
    programs = Product.query.filter(
        Product.product_type.in_([
            ProductType.PROGRAMME_SPORT,
            ProductType.PROGRAMME_DIETE,
            ProductType.PROGRAMME_COMBINE
        ])
    ).order_by(Product.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('admin/programs/index.html', programs=programs)


@admin_programs_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    """Create program."""
    if request.method == 'POST':
        try:
            product = Product()
            product.title = request.form.get('title')
            product.slug = request.form.get('slug') or slugify(request.form.get('title'))
            product.short_description = request.form.get('short_description')
            product.description = request.form.get('description')
            product.product_type = request.form.get('product_type')
            product.difficulty_level = request.form.get('difficulty_level') or None
            product.price = float(request.form.get('price', 0))
            product.original_price = float(request.form.get('original_price', 0)) if request.form.get('original_price') else None
            product.duration_weeks = int(request.form.get('duration_weeks', 4))
            product.is_published = request.form.get('is_published') == 'on'
            product.is_featured = request.form.get('is_featured') == 'on'

            # Handle image upload
            if 'image' in request.files and request.files['image'].filename:
                file = request.files['image']
                success, file_path = save_uploaded_file(file, folder='products', file_type='image')
                if success:
                    product.image_url = file_path
                else:
                    flash(f'Avertissement: {file_path}', 'warning')

            db.session.add(product)
            db.session.flush()  # Get product ID

            # Create week structure
            for week_num in range(1, product.duration_weeks + 1):
                week = ProgramWeek(
                    product_id=product.id,
                    week_number=week_num,
                    title=f"Semaine {week_num}",
                    description=""
                )
                db.session.add(week)
                db.session.flush()

                # Create days for each week
                for day_num in range(1, 8):
                    day = ProgramDay(
                        week_id=week.id,
                        day_number=day_num,
                        title=f"Jour {day_num}"
                    )
                    db.session.add(day)

            db.session.commit()

            flash('Programme créé avec succès! Vous pouvez maintenant configurer les semaines et les jours.', 'success')
            return redirect(url_for('admin_programs.edit', product_id=product.id))

        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la création: {str(e)}', 'danger')

    return render_template('admin/programs/form.html', product=None, title='Créer un programme')


@admin_programs_bp.route('/<int:product_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(product_id):
    """Edit program."""
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        try:
            product.title = request.form.get('title')
            product.slug = request.form.get('slug') or slugify(request.form.get('title'))
            product.short_description = request.form.get('short_description')
            product.description = request.form.get('description')
            product.product_type = request.form.get('product_type')
            product.difficulty_level = request.form.get('difficulty_level') or None
            product.price = float(request.form.get('price', 0))
            product.original_price = float(request.form.get('original_price', 0)) if request.form.get('original_price') else None
            product.is_published = request.form.get('is_published') == 'on'
            product.is_featured = request.form.get('is_featured') == 'on'

            # Handle duration change
            new_duration = int(request.form.get('duration_weeks', product.duration_weeks))
            if new_duration != product.duration_weeks:
                # Adjust weeks if duration changed
                current_weeks = product.weeks.count()
                if new_duration > current_weeks:
                    # Add new weeks
                    for week_num in range(current_weeks + 1, new_duration + 1):
                        week = ProgramWeek(
                            product_id=product.id,
                            week_number=week_num,
                            title=f"Semaine {week_num}"
                        )
                        db.session.add(week)
                        db.session.flush()

                        for day_num in range(1, 8):
                            day = ProgramDay(
                                week_id=week.id,
                                day_number=day_num,
                                title=f"Jour {day_num}"
                            )
                            db.session.add(day)
                elif new_duration < current_weeks:
                    # Remove extra weeks
                    for week in product.weeks.filter(ProgramWeek.week_number > new_duration).all():
                        db.session.delete(week)

                product.duration_weeks = new_duration

            # Handle image upload
            if 'image' in request.files and request.files['image'].filename:
                file = request.files['image']
                success, file_path = save_uploaded_file(file, folder='products', file_type='image')
                if success:
                    product.image_url = file_path
                else:
                    flash(f'Avertissement: {file_path}', 'warning')

            db.session.commit()
            flash('Programme mis à jour!', 'success')
            return redirect(url_for('admin_programs.edit', product_id=product.id))

        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la mise à jour: {str(e)}', 'danger')

    # Get weeks with days
    weeks = product.weeks.order_by(ProgramWeek.week_number).all()

    return render_template('admin/programs/form.html', product=product, weeks=weeks, title='Modifier le programme')


@admin_programs_bp.route('/<int:product_id>/week/<int:week_id>', methods=['GET', 'POST'])
@admin_required
def edit_week(product_id, week_id):
    """Edit program week."""
    product = Product.query.get_or_404(product_id)
    week = ProgramWeek.query.get_or_404(week_id)

    if request.method == 'POST':
        try:
            week.title = request.form.get('title')
            week.description = request.form.get('description')
            week.goals = request.form.get('goals')
            db.session.commit()
            flash('Semaine mise à jour!', 'success')
            return redirect(url_for('admin_programs.edit', product_id=product_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur: {str(e)}', 'danger')

    return render_template('admin/programs/week_form.html', product=product, week=week)


@admin_programs_bp.route('/<int:product_id>/day/<int:day_id>', methods=['GET', 'POST'])
@admin_required
def edit_day(product_id, day_id):
    """Edit program day."""
    product = Product.query.get_or_404(product_id)
    day = ProgramDay.query.get_or_404(day_id)

    if request.method == 'POST':
        try:
            day.title = request.form.get('title')
            day.workout_type = request.form.get('workout_type')
            day.workout_description = request.form.get('workout_description')
            day.workout_duration = int(request.form.get('workout_duration', 0)) if request.form.get('workout_duration') else None
            day.workout_video_url = request.form.get('workout_video_url')
            day.diet_description = request.form.get('diet_description')
            day.diet_calories = int(request.form.get('diet_calories', 0)) if request.form.get('diet_calories') else None
            day.notes = request.form.get('notes')
            day.coach_tips = request.form.get('coach_tips')
            day.is_rest_day = request.form.get('is_rest_day') == 'on'

            # Handle exercises JSON
            exercises_json = request.form.get('workout_exercises')
            if exercises_json:
                try:
                    day.workout_exercises = json.loads(exercises_json)
                except:
                    pass

            # Handle meals JSON
            meals_json = request.form.get('diet_meals')
            if meals_json:
                try:
                    day.diet_meals = json.loads(meals_json)
                except:
                    pass

            # Handle image upload
            if 'workout_image' in request.files and request.files['workout_image'].filename:
                file = request.files['workout_image']
                success, file_path = save_uploaded_file(file, folder='workouts', file_type='image')
                if success:
                    day.workout_image_url = file_path

            db.session.commit()
            flash('Jour mis à jour!', 'success')
            return redirect(url_for('admin_programs.edit', product_id=product_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur: {str(e)}', 'danger')

    return render_template('admin/programs/day_form_simple.html', product=product, day=day)


@admin_programs_bp.route('/<int:product_id>/delete', methods=['POST'])
@admin_required
def delete(product_id):
    """Delete program."""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()

    flash('Programme supprimé.', 'info')
    return redirect(url_for('admin_programs.index'))


@admin_programs_bp.route('/<int:product_id>/duplicate', methods=['POST'])
@admin_required
def duplicate(product_id):
    """Duplicate program."""
    original = Product.query.get_or_404(product_id)

    try:
        # Create new product
        new_product = Product()
        new_product.title = f"{original.title} (Copie)"
        new_product.slug = f"{original.slug}-copie"
        new_product.short_description = original.short_description
        new_product.description = original.description
        new_product.product_type = original.product_type
        new_product.difficulty_level = original.difficulty_level
        new_product.price = original.price
        new_product.original_price = original.original_price
        new_product.duration_weeks = original.duration_weeks
        new_product.image_url = original.image_url
        new_product.is_published = False

        db.session.add(new_product)
        db.session.flush()

        # Copy weeks and days
        for orig_week in original.weeks.order_by(ProgramWeek.week_number).all():
            new_week = ProgramWeek(
                product_id=new_product.id,
                week_number=orig_week.week_number,
                title=orig_week.title,
                description=orig_week.description,
                goals=orig_week.goals
            )
            db.session.add(new_week)
            db.session.flush()

            for orig_day in orig_week.days:
                new_day = ProgramDay(
                    week_id=new_week.id,
                    day_number=orig_day.day_number,
                    title=orig_day.title,
                    workout_type=orig_day.workout_type,
                    workout_description=orig_day.workout_description,
                    workout_exercises=orig_day.workout_exercises,
                    workout_duration=orig_day.workout_duration,
                    workout_video_url=orig_day.workout_video_url,
                    workout_image_url=orig_day.workout_image_url,
                    diet_description=orig_day.diet_description,
                    diet_calories=orig_day.diet_calories,
                    diet_meals=orig_day.diet_meals,
                    notes=orig_day.notes,
                    coach_tips=orig_day.coach_tips,
                    is_rest_day=orig_day.is_rest_day
                )
                db.session.add(new_day)

        db.session.commit()
        flash('Programme dupliqué avec succès!', 'success')
        return redirect(url_for('admin_programs.edit', product_id=new_product.id))

    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la duplication: {str(e)}', 'danger')
        return redirect(url_for('admin_programs.index'))
