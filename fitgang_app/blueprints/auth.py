"""Authentication blueprint."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from datetime import datetime
from fitgang_app import db
from fitgang_app.models.user import User, UserProfile
from fitgang_app.forms.auth import LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm
from fitgang_app.utils.email import send_welcome_email, send_password_reset_email
from fitgang_app.utils.security import generate_password_reset_token, verify_password_reset_token

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()

        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Votre compte a été désactivé.', 'danger')
                return redirect(url_for('auth.login'))

            # Check if password change is forced
            if user.force_password_change:
                flash('Vous devez changer votre mot de passe.', 'warning')
                login_user(user)
                return redirect(url_for('profile.change_password'))

            login_user(user, remember=form.remember_me.data)
            user.last_login_at = datetime.utcnow()
            db.session.commit()

            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('dashboard.index')

            flash('Connexion réussie!', 'success')
            return redirect(next_page)
        else:
            flash('Email ou mot de passe incorrect.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register page."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    form = RegisterForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data.lower()
        )
        user.set_password(form.password.data)

        # Create profile
        profile = UserProfile(user=user)

        db.session.add(user)
        db.session.add(profile)
        db.session.commit()

        # Send welcome email
        send_welcome_email(user)

        flash('Inscription réussie! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
def logout():
    """Logout."""
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password page."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    form = ForgotPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()

        if user:
            token = generate_password_reset_token(user.id)
            user.password_reset_token = token
            db.session.commit()

            send_password_reset_email(user, token)

        # Always show success message for security
        flash('Si l\'email existe, un lien de réinitialisation a été envoyé.', 'info')
        return redirect(url_for('auth.login'))

    return render_template('auth/forgot_password.html', form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password page."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    user_id = verify_password_reset_token(token)

    if not user_id:
        flash('Le lien de réinitialisation est invalide ou a expiré.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    user = User.query.get(user_id)

    if not user or user.password_reset_token != token:
        flash('Le lien de réinitialisation est invalide.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.password_reset_token = None
        user.force_password_change = False
        db.session.commit()

        flash('Votre mot de passe a été réinitialisé avec succès.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', form=form, token=token)
