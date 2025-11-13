"""API blueprint."""
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from fitgang_app.models import Product, User, Order, GiftCode

api_bp = Blueprint('api', __name__)


@api_bp.route('/products', methods=['GET'])
def products():
    """Get products list."""
    products = Product.query.filter_by(is_published=True).all()

    return jsonify({
        'products': [{
            'id': p.id,
            'title': p.title,
            'slug': p.slug,
            'price': p.price,
            'product_type': p.product_type.value,
            'difficulty_level': p.difficulty_level.value if p.difficulty_level else None,
            'image_url': p.image_url
        } for p in products]
    })


@api_bp.route('/products/<int:product_id>', methods=['GET'])
def product_detail(product_id):
    """Get product details."""
    product = Product.query.get_or_404(product_id)

    return jsonify({
        'id': product.id,
        'title': product.title,
        'slug': product.slug,
        'description': product.description,
        'price': product.price,
        'product_type': product.product_type.value,
        'difficulty_level': product.difficulty_level.value if product.difficulty_level else None,
        'duration_weeks': product.duration_weeks,
        'image_url': product.image_url
    })


@api_bp.route('/user/purchases', methods=['GET'])
@login_required
def user_purchases():
    """Get user purchases."""
    orders = Order.query.filter_by(user_id=current_user.id, status='completed').all()

    return jsonify({
        'purchases': [{
            'order_number': order.order_number,
            'total_amount': order.total_amount,
            'created_at': order.created_at.isoformat(),
            'items': [{
                'product_name': item.product_name,
                'quantity': item.quantity,
                'unit_price': item.unit_price
            } for item in order.items]
        } for order in orders]
    })


@api_bp.route('/gifts/validate/<code>', methods=['GET'])
def validate_gift_code(code):
    """Validate gift code."""
    gift = GiftCode.query.filter_by(code=code.upper()).first()

    if not gift:
        return jsonify({'valid': False, 'message': 'Code invalide'}), 404

    valid, message = gift.is_valid()

    return jsonify({
        'valid': valid,
        'message': message,
        'product_id': gift.product_id if valid else None,
        'expires_at': gift.expires_at.isoformat() if valid else None
    })
