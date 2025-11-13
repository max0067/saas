"""Admin ebooks blueprint."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from fitgang_app import db
from fitgang_app.models import Product, ProductType
from fitgang_app.utils.decorators import admin_required
from fitgang_app.utils.uploads import save_uploaded_file
from slugify import slugify
import os

admin_ebooks_bp = Blueprint('admin_ebooks', __name__)


@admin_ebooks_bp.route('/')
@admin_required
def index():
    """List ebooks."""
    page = request.args.get('page', 1, type=int)
    ebooks = Product.query.filter_by(product_type=ProductType.EBOOK).order_by(
        Product.created_at.desc()
    ).paginate(page=page, per_page=20, error_out=False)

    return render_template('admin/ebooks/index.html', ebooks=ebooks)


@admin_ebooks_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    """Create ebook."""
    if request.method == 'POST':
        try:
            product = Product()
            product.title = request.form.get('title')
            product.slug = request.form.get('slug') or slugify(request.form.get('title'))
            product.short_description = request.form.get('short_description')
            product.description = request.form.get('description')
            product.product_type = ProductType.EBOOK
            product.author = request.form.get('author')
            product.pages = int(request.form.get('pages', 0)) if request.form.get('pages') else None
            product.isbn = request.form.get('isbn')
            product.price = float(request.form.get('price', 0))
            product.original_price = float(request.form.get('original_price', 0)) if request.form.get('original_price') else None
            product.is_published = request.form.get('is_published') == 'on'
            product.is_featured = request.form.get('is_featured') == 'on'

            # Handle cover image upload
            if 'image' in request.files and request.files['image'].filename:
                file = request.files['image']
                success, file_path = save_uploaded_file(file, folder='ebooks/covers', file_type='image')
                if success:
                    product.image_url = file_path
                else:
                    flash(f'Avertissement image: {file_path}', 'warning')

            # Handle PDF file upload
            if 'file' in request.files and request.files['file'].filename:
                file = request.files['file']
                success, file_path = save_uploaded_file(file, folder='ebooks/files', file_type='document')
                if success:
                    product.file_path = file_path
                    product.file_format = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'pdf'
                    # Get file size
                    try:
                        full_path = os.path.join('uploads', file_path)
                        if os.path.exists(full_path):
                            product.file_size = os.path.getsize(full_path)
                    except:
                        pass
                else:
                    flash(f'Avertissement fichier: {file_path}', 'warning')

            db.session.add(product)
            db.session.commit()

            flash('eBook créé avec succès!', 'success')
            return redirect(url_for('admin_ebooks.index'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la création: {str(e)}', 'danger')

    return render_template('admin/ebooks/form.html', product=None, title='Créer un eBook')


@admin_ebooks_bp.route('/<int:product_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(product_id):
    """Edit ebook."""
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        try:
            product.title = request.form.get('title')
            product.slug = request.form.get('slug') or slugify(request.form.get('title'))
            product.short_description = request.form.get('short_description')
            product.description = request.form.get('description')
            product.author = request.form.get('author')
            product.pages = int(request.form.get('pages', 0)) if request.form.get('pages') else None
            product.isbn = request.form.get('isbn')
            product.price = float(request.form.get('price', 0))
            product.original_price = float(request.form.get('original_price', 0)) if request.form.get('original_price') else None
            product.is_published = request.form.get('is_published') == 'on'
            product.is_featured = request.form.get('is_featured') == 'on'

            # Handle cover image upload
            if 'image' in request.files and request.files['image'].filename:
                file = request.files['image']
                success, file_path = save_uploaded_file(file, folder='ebooks/covers', file_type='image')
                if success:
                    product.image_url = file_path
                else:
                    flash(f'Avertissement image: {file_path}', 'warning')

            # Handle PDF file upload
            if 'file' in request.files and request.files['file'].filename:
                file = request.files['file']
                success, file_path = save_uploaded_file(file, folder='ebooks/files', file_type='document')
                if success:
                    product.file_path = file_path
                    product.file_format = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'pdf'
                    try:
                        full_path = os.path.join('uploads', file_path)
                        if os.path.exists(full_path):
                            product.file_size = os.path.getsize(full_path)
                    except:
                        pass
                else:
                    flash(f'Avertissement fichier: {file_path}', 'warning')

            db.session.commit()
            flash('eBook mis à jour!', 'success')
            return redirect(url_for('admin_ebooks.index'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la mise à jour: {str(e)}', 'danger')

    return render_template('admin/ebooks/form.html', product=product, title='Modifier l\'eBook')


@admin_ebooks_bp.route('/<int:product_id>/delete', methods=['POST'])
@admin_required
def delete(product_id):
    """Delete ebook."""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()

    flash('eBook supprimé.', 'info')
    return redirect(url_for('admin_ebooks.index'))
