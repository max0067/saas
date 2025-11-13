"""Cart blueprint."""
from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from fitgang_app.models import Product

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/')
def index():
    """View cart."""
    cart_items = session.get('cart', [])
    items = []
    total = 0

    for item in cart_items:
        product = Product.query.get(item['product_id'])
        if product:
            items.append({
                'product': product,
                'quantity': item['quantity']
            })
            total += product.price * item['quantity']

    return render_template('cart/index.html', cart_items=items, total=total)


@cart_bp.route('/add/<int:product_id>', methods=['POST'])
def add(product_id):
    """Add product to cart."""
    product = Product.query.get_or_404(product_id)

    if not product.is_in_stock():
        flash('Ce produit n\'est plus en stock.', 'danger')
        return redirect(url_for('shop.product_detail', slug=product.slug))

    cart = session.get('cart', [])

    # Check if product already in cart
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += 1
            break
    else:
        cart.append({'product_id': product_id, 'quantity': 1})

    session['cart'] = cart
    flash(f'{product.title} ajouté au panier!', 'success')
    return redirect(url_for('cart.index'))


@cart_bp.route('/remove/<int:product_id>', methods=['POST'])
def remove(product_id):
    """Remove product from cart."""
    cart = session.get('cart', [])
    cart = [item for item in cart if item['product_id'] != product_id]
    session['cart'] = cart

    flash('Produit retiré du panier.', 'info')
    return redirect(url_for('cart.index'))


@cart_bp.route('/clear')
def clear():
    """Clear cart."""
    session['cart'] = []
    flash('Panier vidé.', 'info')
    return redirect(url_for('cart.index'))
