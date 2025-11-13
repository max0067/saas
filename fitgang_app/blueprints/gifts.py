"""Gifts blueprint."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from fitgang_app import db
from fitgang_app.models import GiftCode, Product, GiftLog, Order, OrderItem
from fitgang_app.forms.gift import GiftCodeForm, RedeemGiftForm
from fitgang_app.utils.email import send_gift_email
from fitgang_app.utils.decorators import admin_required
from fitgang_app.utils.security import generate_order_number

gifts_bp = Blueprint('gifts', __name__)


@gifts_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    """Create gift code (admin only)."""
    form = GiftCodeForm()

    # Populate product choices
    products = Product.query.filter_by(is_published=True).all()
    form.product_id.choices = [(p.id, p.title) for p in products]

    if form.validate_on_submit():
        code = GiftCode.generate_code()
        gift = GiftCode(
            code=code,
            product_id=form.product_id.data,
            sender_id=current_user.id,
            recipient_email=form.recipient_email.data.lower(),
            message=form.message.data,
            expires_at=datetime.utcnow() + timedelta(days=form.expiration_days.data)
        )

        db.session.add(gift)

        # Log creation
        log = GiftLog(
            gift_code=gift,
            action='created',
            user_id=current_user.id,
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()

        # Send gift email
        send_gift_email(gift)

        flash(f'Code cadeau créé et envoyé à {gift.recipient_email}!', 'success')
        return redirect(url_for('gifts.create'))

    return render_template('gifts/create.html', form=form)


@gifts_bp.route('/redeem', methods=['GET', 'POST'])
@gifts_bp.route('/redeem/<code>', methods=['GET', 'POST'])
@login_required
def redeem(code=None):
    """Redeem gift code."""
    form = RedeemGiftForm()

    if code:
        form.code.data = code

    if form.validate_on_submit():
        gift = GiftCode.query.filter_by(code=form.code.data.upper()).first()

        if not gift:
            flash('Code cadeau invalide.', 'danger')
            return redirect(url_for('gifts.redeem'))

        valid, message = gift.is_valid()
        if not valid:
            flash(message, 'danger')
            return redirect(url_for('gifts.redeem'))

        # Redeem the gift
        success, msg = gift.redeem(current_user.id)

        if success:
            # Create order with the gifted product
            order = Order(
                order_number=generate_order_number(),
                user_id=current_user.id,
                customer_email=current_user.email,
                customer_name=current_user.username,
                total_amount=0,  # Gift, no payment
                payment_method='gift'
            )

            product = Product.query.get(gift.product_id)
            order_item = OrderItem(
                product_id=product.id,
                product_name=product.title,
                quantity=1,
                unit_price=0,
                subtotal=0
            )
            order.items.append(order_item)
            order.mark_as_completed()

            db.session.add(order)

            # Log redemption
            log = GiftLog(
                gift_code=gift,
                action='redeemed',
                user_id=current_user.id,
                ip_address=request.remote_addr
            )
            db.session.add(log)
            db.session.commit()

            flash(f'Code cadeau utilisé! {product.title} a été ajouté à votre compte.', 'success')
            return redirect(url_for('profile.purchases'))
        else:
            flash(msg, 'danger')

    return render_template('gifts/redeem.html', form=form)
