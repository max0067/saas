"""Shop blueprint."""
from flask import Blueprint, render_template, request
from fitgang_app.models import Product

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

    query = Product.query.filter_by(is_published=True, product_type='program')

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

    query = Product.query.filter_by(is_published=True, product_type='ebook')

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
