"""Admin supplements blueprint."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from fitgang_app import db
from fitgang_app.models import Supplement
from fitgang_app.utils.decorators import admin_required
from fitgang_app.utils.uploads import save_uploaded_file
from slugify import slugify
import json

admin_supplements_bp = Blueprint('admin_supplements', __name__)


@admin_supplements_bp.route('/')
@admin_required
def index():
    """List supplements."""
    page = request.args.get('page', 1, type=int)
    supplements = Supplement.query.order_by(
        Supplement.display_order.asc(),
        Supplement.created_at.desc()
    ).paginate(page=page, per_page=20, error_out=False)

    return render_template('admin/supplements/index.html', supplements=supplements)


@admin_supplements_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    """Create supplement."""
    if request.method == 'POST':
        try:
            supplement = Supplement()
            supplement.name = request.form.get('name')
            supplement.slug = request.form.get('slug') or slugify(request.form.get('name'))
            supplement.short_description = request.form.get('short_description')
            supplement.description = request.form.get('description')
            supplement.category = request.form.get('category')
            supplement.brand = request.form.get('brand')
            supplement.affiliate_link = request.form.get('affiliate_link')
            supplement.affiliate_code = request.form.get('affiliate_code')
            supplement.usage_instructions = request.form.get('usage_instructions')
            supplement.ingredients = request.form.get('ingredients')
            supplement.warnings = request.form.get('warnings')
            supplement.price_range = request.form.get('price_range')
            supplement.is_published = request.form.get('is_published') == 'on'
            supplement.is_featured = request.form.get('is_featured') == 'on'
            supplement.display_order = int(request.form.get('display_order', 0))

            # Handle benefits as JSON array
            benefits_text = request.form.get('benefits', '')
            if benefits_text:
                # Split by newlines and filter empty lines
                benefits_list = [b.strip() for b in benefits_text.split('\n') if b.strip()]
                supplement.benefits = benefits_list

            # Handle image upload
            if 'image' in request.files and request.files['image'].filename:
                file = request.files['image']
                success, file_path = save_uploaded_file(file, folder='supplements', file_type='image')
                if success:
                    supplement.image_url = file_path
                else:
                    flash(f'Avertissement: {file_path}', 'warning')

            db.session.add(supplement)
            db.session.commit()

            flash('Complément créé avec succès!', 'success')
            return redirect(url_for('admin_supplements.index'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la création: {str(e)}', 'danger')

    return render_template('admin/supplements/form.html', supplement=None, title='Créer un complément')


@admin_supplements_bp.route('/<int:supplement_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(supplement_id):
    """Edit supplement."""
    supplement = Supplement.query.get_or_404(supplement_id)

    if request.method == 'POST':
        try:
            supplement.name = request.form.get('name')
            supplement.slug = request.form.get('slug') or slugify(request.form.get('name'))
            supplement.short_description = request.form.get('short_description')
            supplement.description = request.form.get('description')
            supplement.category = request.form.get('category')
            supplement.brand = request.form.get('brand')
            supplement.affiliate_link = request.form.get('affiliate_link')
            supplement.affiliate_code = request.form.get('affiliate_code')
            supplement.usage_instructions = request.form.get('usage_instructions')
            supplement.ingredients = request.form.get('ingredients')
            supplement.warnings = request.form.get('warnings')
            supplement.price_range = request.form.get('price_range')
            supplement.is_published = request.form.get('is_published') == 'on'
            supplement.is_featured = request.form.get('is_featured') == 'on'
            supplement.display_order = int(request.form.get('display_order', 0))

            # Handle benefits
            benefits_text = request.form.get('benefits', '')
            if benefits_text:
                benefits_list = [b.strip() for b in benefits_text.split('\n') if b.strip()]
                supplement.benefits = benefits_list

            # Handle image upload
            if 'image' in request.files and request.files['image'].filename:
                file = request.files['image']
                success, file_path = save_uploaded_file(file, folder='supplements', file_type='image')
                if success:
                    supplement.image_url = file_path
                else:
                    flash(f'Avertissement: {file_path}', 'warning')

            db.session.commit()
            flash('Complément mis à jour!', 'success')
            return redirect(url_for('admin_supplements.index'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la mise à jour: {str(e)}', 'danger')

    return render_template('admin/supplements/form.html', supplement=supplement, title='Modifier le complément')


@admin_supplements_bp.route('/<int:supplement_id>/delete', methods=['POST'])
@admin_required
def delete(supplement_id):
    """Delete supplement."""
    supplement = Supplement.query.get_or_404(supplement_id)
    db.session.delete(supplement)
    db.session.commit()

    flash('Complément supprimé.', 'info')
    return redirect(url_for('admin_supplements.index'))


@admin_supplements_bp.route('/<int:supplement_id>/track-click', methods=['POST'])
def track_click(supplement_id):
    """Track affiliate click (public route)."""
    supplement = Supplement.query.get_or_404(supplement_id)
    supplement.increment_clicks()
    return jsonify({'success': True})
