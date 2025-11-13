"""Webhooks blueprint."""
from flask import Blueprint, request, current_app, jsonify
from fitgang_app import db
from fitgang_app.models import Order
import stripe

webhooks_bp = Blueprint('webhooks', __name__)


@webhooks_bp.route('/stripe', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhooks."""
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, current_app.config['STRIPE_WEBHOOK_SECRET']
        )
    except ValueError:
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError:
        return jsonify({'error': 'Invalid signature'}), 400

    # Handle events
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']

        # Update order status
        order = Order.query.filter_by(
            stripe_payment_intent_id=payment_intent['id']
        ).first()

        if order:
            order.mark_as_completed()
            db.session.commit()

    return jsonify({'success': True}), 200
