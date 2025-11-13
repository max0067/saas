"""Admin products blueprint."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from fitgang_app import db
from fitgang_app.models import Product
from fitgang_app.forms.product import ProductForm
from fitgang_app.utils.decorators import admin_required
from fitgang_app.utils.uploads import save_uploaded_file
from slugify import slugify

admin_products_bp = Blueprint('admin_products', __name__)


@admin_products_bp.route('/')
@admin_required
def index():
    """List products."""
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('admin/products.html', products=products)


@admin_products_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    """Create product."""
    form = ProductForm()

    if form.validate_on_submit():
        try:
            product = Product()

            # Manual field assignment for safety
            product.title = form.title.data
            product.slug = form.slug.data if form.slug.data else slugify(form.title.data)
            product.short_description = form.short_description.data
            product.description = form.description.data
            product.product_type = form.product_type.data
            product.difficulty_level = form.difficulty_level.data if form.difficulty_level.data else None
            product.price = form.price.data
            product.original_price = form.original_price.data
            product.duration_weeks = form.duration_weeks.data
            product.is_published = form.is_published.data
            product.is_featured = form.is_featured.data

            # Handle image upload safely
            if hasattr(form, 'image') and form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
                try:
                    success, file_path = save_uploaded_file(form.image.data, folder='products', file_type='image')
                    if success:
                        product.image_url = file_path
                    else:
                        flash(f'Avertissement: {file_path}', 'warning')
                except Exception as e:
                    flash(f'Erreur upload image: {str(e)}', 'warning')

            db.session.add(product)
            db.session.commit()

            flash('Produit créé avec succès!', 'success')
            return redirect(url_for('admin_products.index'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la création: {str(e)}', 'danger')

    return render_template('admin/product_form.html', form=form, title='Créer un produit')


@admin_products_bp.route('/<int:product_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(product_id):
    """Edit product."""
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)

    if form.validate_on_submit():
        try:
            # Manual field assignment for safety
            product.title = form.title.data
            product.slug = form.slug.data if form.slug.data else slugify(form.title.data)
            product.short_description = form.short_description.data
            product.description = form.description.data
            product.product_type = form.product_type.data
            product.difficulty_level = form.difficulty_level.data if form.difficulty_level.data else None
            product.price = form.price.data
            product.original_price = form.original_price.data
            product.duration_weeks = form.duration_weeks.data
            product.is_published = form.is_published.data
            product.is_featured = form.is_featured.data

            # Handle image upload safely
            if hasattr(form, 'image') and form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
                try:
                    success, file_path = save_uploaded_file(form.image.data, folder='products', file_type='image')
                    if success:
                        product.image_url = file_path
                    else:
                        flash(f'Avertissement: {file_path}', 'warning')
                except Exception as e:
                    flash(f'Erreur upload image: {str(e)}', 'warning')

            db.session.commit()
            flash('Produit mis à jour!', 'success')
            return redirect(url_for('admin_products.index'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la mise à jour: {str(e)}', 'danger')

    return render_template('admin/product_form.html', form=form, product=product, title='Modifier le produit')


@admin_products_bp.route('/<int:product_id>/delete', methods=['POST'])
@admin_required
def delete(product_id):
    """Delete product."""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()

    flash('Produit supprimé.', 'info')
    return redirect(url_for('admin_products.index'))
