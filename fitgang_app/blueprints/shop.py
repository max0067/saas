"""Shop blueprint."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, current_app
from flask_login import login_required, current_user
from fitgang_app.models import Product, ProductType
import os

shop_bp = Blueprint('shop', __name__)


@shop_bp.route('/')
def catalog():
    """Product catalog - redirects to programs by default."""
    return programs()


@shop_bp.route('/programmes')
def programs():
    """Programs catalog."""
    page = request.args.get('page', 1, type=int)
    difficulty = request.args.get('difficulty', None)

    # Filter for all program types (sport, diet, combined)
    query = Product.query.filter_by(is_published=True).filter(
        Product.product_type.in_([
            ProductType.PROGRAMME_SPORT,
            ProductType.PROGRAMME_DIETE,
            ProductType.PROGRAMME_COMBINE
        ])
    )

    if difficulty:
        query = query.filter_by(difficulty_level=difficulty)

    products = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False
    )

    return render_template('shop/programs.html', products=products)


@shop_bp.route('/ebooks')
def ebooks():
    """Ebooks catalog."""
    page = request.args.get('page', 1, type=int)

    # Filter for ebooks
    query = Product.query.filter_by(is_published=True).filter(
        Product.product_type == ProductType.EBOOK
    )

    products = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False
    )

    return render_template('shop/ebooks.html', products=products)


@shop_bp.route('/<slug>')
def product_detail(slug):
    """Product detail page."""
    product = Product.query.filter_by(slug=slug, is_published=True).first_or_404()

    # Increment views
    product.increment_views()

    # Get related products
    related_products = product.related.limit(4).all()

    return render_template('shop/product.html', product=product, related_products=related_products)


@shop_bp.route('/<slug>/access')
@login_required
def access_product(slug):
    """Access purchased product content."""
    product = Product.query.filter_by(slug=slug, is_published=True).first_or_404()

    # Check if user has access
    if not current_user.is_admin() and not current_user.has_access_to_product(product.id):
        flash('Vous devez acheter ce produit pour y accéder.', 'warning')
        return redirect(url_for('shop.product_detail', slug=slug))

    # Redirect based on product type
    if product.product_type == ProductType.EBOOK:
        # For ebooks, serve the PDF file
        if product.file_path:
            file_full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], product.file_path)
            if os.path.exists(file_full_path):
                return send_file(file_full_path, as_attachment=False)
        flash('Fichier ebook introuvable.', 'danger')
        return redirect(url_for('dashboard.index'))
    else:
        # For programs, redirect to workouts
        return redirect(url_for('workouts.list'))
