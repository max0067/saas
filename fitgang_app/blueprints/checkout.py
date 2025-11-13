"""Checkout blueprint."""
from flask import Blueprint, render_template, redirect, url_for, session, flash, request, current_app
from flask_login import current_user, login_required
from fitgang_app import db
from fitgang_app.models import Product, Order, OrderItem
from fitgang_app.utils.security import generate_order_number, generate_access_code
from fitgang_app.utils.email import send_purchase_confirmation_email
import stripe

checkout_bp = Blueprint('checkout', __name__)


@checkout_bp.route('/')
@login_required
def index():
    """Checkout page."""
    cart_items = session.get('cart', [])

    if not cart_items:
        flash('Votre panier est vide.', 'warning')
        return redirect(url_for('shop.programs'))

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

    # Initialize Stripe
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

    return render_template(
        'shop/checkout.html',
        items=items,
        total=total,
        stripe_public_key=current_app.config['STRIPE_PUBLIC_KEY']
    )


@checkout_bp.route('/create-payment-intent', methods=['POST'])
@login_required
def create_payment_intent():
    """Create Stripe payment intent."""
    cart_items = session.get('cart', [])

    if not cart_items:
        return {'error': 'Cart is empty'}, 400

    # Calculate total
    total = 0
    for item in cart_items:
        product = Product.query.get(item['product_id'])
        if product:
            total += product.price * item['quantity']

    # Initialize Stripe
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(total * 100),  # Convert to cents
            currency='eur',
            metadata={
                'user_id': current_user.id,
                'email': current_user.email
            }
        )

        return {'clientSecret': intent.client_secret}

    except Exception as e:
        return {'error': str(e)}, 500


@checkout_bp.route('/success')
@login_required
def success():
    """Checkout success page."""
    payment_intent_id = request.args.get('payment_intent')

    if not payment_intent_id:
        flash('Commande invalide.', 'danger')
        return redirect(url_for('shop.programs'))

    # Create order
    cart_items = session.get('cart', [])
    order = Order(
        order_number=generate_order_number(),
        user_id=current_user.id,
        customer_email=current_user.email,
        customer_name=current_user.username,
        stripe_payment_intent_id=payment_intent_id,
        access_code=generate_access_code()
    )

    total = 0
    for item in cart_items:
        product = Product.query.get(item['product_id'])
        if product:
            order_item = OrderItem(
                product_id=product.id,
                product_name=product.title,
                quantity=item['quantity'],
                unit_price=product.price,
                subtotal=product.price * item['quantity']
            )
            order.items.append(order_item)
            total += order_item.subtotal

    order.total_amount = total
    order.mark_as_completed()

    db.session.add(order)
    db.session.commit()

    # Send confirmation email
    send_purchase_confirmation_email(order)

    # Clear cart
    session['cart'] = []

    flash('Votre commande a été confirmée! Vous allez recevoir un email avec vos accès.', 'success')
    return render_template('shop/success.html', order=order)
