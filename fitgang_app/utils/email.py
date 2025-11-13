"""Email utilities."""
from flask import render_template, current_app
from flask_mail import Message
from fitgang_app import mail
import threading


def send_async_email(app, msg):
    """Send email asynchronously."""
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, text_body=None, html_body=None, template=None, **kwargs):
    """
    Send email.

    Args:
        subject: Email subject
        recipients: List of recipient email addresses
        text_body: Plain text body (optional)
        html_body: HTML body (optional)
        template: Template name to render for HTML body (optional)
        **kwargs: Additional template variables
    """
    msg = Message(
        subject=subject,
        recipients=recipients if isinstance(recipients, list) else [recipients],
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )

    if text_body:
        msg.body = text_body

    if template:
        msg.html = render_template(f'emails/{template}', **kwargs)
    elif html_body:
        msg.html = html_body

    # Send asynchronously in development/production
    if current_app.config.get('TESTING'):
        mail.send(msg)
    else:
        thread = threading.Thread(
            target=send_async_email,
            args=(current_app._get_current_object(), msg)
        )
        thread.start()


def send_welcome_email(user):
    """Send welcome email to new user."""
    send_email(
        subject=f'Bienvenue sur {current_app.config["SITE_NAME"]} !',
        recipients=[user.email],
        template='welcome.html',
        user=user,
        site_name=current_app.config['SITE_NAME']
    )


def send_password_reset_email(user, token):
    """Send password reset email."""
    reset_url = f"{current_app.config['BASE_URL']}/auth/reset-password/{token}"
    send_email(
        subject='Réinitialisation de votre mot de passe',
        recipients=[user.email],
        template='password_reset.html',
        user=user,
        reset_url=reset_url,
        site_name=current_app.config['SITE_NAME']
    )


def send_admin_password_reset_email(user):
    """Send notification email when admin resets user password."""
    send_email(
        subject='Votre mot de passe a été modifié',
        recipients=[user.email],
        template='password_admin_reset.html',
        user=user,
        site_name=current_app.config['SITE_NAME']
    )


def send_purchase_confirmation_email(order):
    """Send purchase confirmation email."""
    access_url = f"{current_app.config['BASE_URL']}/profile/purchases"

    send_email(
        subject=f'Confirmation de votre achat - Commande #{order.order_number}',
        recipients=[order.customer_email],
        template='purchase.html',
        order=order,
        access_url=access_url,
        site_name=current_app.config['SITE_NAME']
    )


def send_gift_email(gift_code):
    """Send gift email."""
    redeem_url = f"{current_app.config['BASE_URL']}/gifts/redeem/{gift_code.code}"

    sender_name = gift_code.sender.username if gift_code.sender else gift_code.sender_email

    send_email(
        subject=f'{sender_name} vous a offert un cadeau FitGang !',
        recipients=[gift_code.recipient_email],
        template='gift.html',
        gift_code=gift_code,
        sender_name=sender_name,
        redeem_url=redeem_url,
        site_name=current_app.config['SITE_NAME']
    )
