"""Admin gifts blueprint - Offrir des produits aux utilisateurs."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from fitgang_app import db
from fitgang_app.utils.decorators import admin_required
from fitgang_app.models.user import User
from fitgang_app.models.product import Product
from fitgang_app.models.order import Order, OrderItem, OrderStatus
from fitgang_app.utils.security import generate_order_number, generate_access_code
from datetime import datetime

admin_gifts_bp = Blueprint('admin_gifts', __name__)


@admin_gifts_bp.route('/')
@admin_required
def index():
    """Gift management page."""
    users = User.query.filter_by(is_active=True).order_by(User.username).all()
    products = Product.query.filter_by(is_published=True).order_by(Product.title).all()

    # Get recent gifts (orders with notes containing "Cadeau")
    recent_gifts = Order.query.filter(
        Order.notes.contains('Cadeau Admin')
    ).order_by(Order.created_at.desc()).limit(20).all()

    return render_template(
        'admin/gifts/index.html',
        users=users,
        products=products,
        recent_gifts=recent_gifts
    )


@admin_gifts_bp.route('/give', methods=['POST'])
@admin_required
def give():
    """Give a product to a user."""
    user_id = request.form.get('user_id', type=int)
    product_id = request.form.get('product_id', type=int)
    gift_note = request.form.get('gift_note', '').strip()

    if not user_id or not product_id:
        flash('Veuillez sélectionner un utilisateur et un produit.', 'danger')
        return redirect(url_for('admin_gifts.index'))

    user = User.query.get_or_404(user_id)
    product = Product.query.get_or_404(product_id)

    # Check if user already has this product
    existing_access = user.has_access_to_product(product_id)
    if existing_access:
        flash(f'{user.username} a déjà accès à {product.title}.', 'warning')
        return redirect(url_for('admin_gifts.index'))

    # Create a gift order
    order = Order(
        order_number=generate_order_number(),
        user_id=user.id,
        customer_email=user.email,
        customer_name=user.username,
        access_code=generate_access_code(),
        status=OrderStatus.COMPLETED,
        total_amount=0.0,  # Free gift
        notes=f'Cadeau Admin: {gift_note}' if gift_note else 'Cadeau Admin'
    )

    # Add product to order
    order_item = OrderItem(
        product_id=product.id,
        product_name=product.title,
        quantity=1,
        unit_price=0.0,  # Free
        subtotal=0.0
    )
    order.items.append(order_item)

    db.session.add(order)
    db.session.commit()

    flash(f'✓ {product.title} offert à {user.username} avec succès !', 'success')
    return redirect(url_for('admin_gifts.index'))


@admin_gifts_bp.route('/<int:order_id>/revoke', methods=['POST'])
@admin_required
def revoke(order_id):
    """Revoke a gift (delete the order)."""
    order = Order.query.get_or_404(order_id)

    if not order.notes or 'Cadeau Admin' not in order.notes:
        flash('Cette commande n\'est pas un cadeau.', 'danger')
        return redirect(url_for('admin_gifts.index'))

    user_username = order.user.username if order.user else 'Utilisateur supprimé'
    product_names = ', '.join([item.product_name for item in order.items])

    db.session.delete(order)
    db.session.commit()

    flash(f'Cadeau révoqué : {product_names} de {user_username}', 'success')
    return redirect(url_for('admin_gifts.index'))
