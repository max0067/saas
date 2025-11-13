"""Admin users blueprint."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from fitgang_app import db
from fitgang_app.models import User
from fitgang_app.utils.decorators import admin_required
from fitgang_app.utils.email import send_admin_password_reset_email
from fitgang_app.utils.security import generate_random_string

admin_users_bp = Blueprint('admin_users', __name__)


@admin_users_bp.route('/')
@admin_required
def index():
    """List users."""
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('admin/users.html', users=users)


@admin_users_bp.route('/<int:user_id>/reset-password', methods=['POST'])
@admin_required
def reset_password(user_id):
    """Admin reset user password."""
    user = User.query.get_or_404(user_id)

    # Generate temporary password
    temp_password = generate_random_string(12)
    user.set_password(temp_password)
    user.force_password_change = True

    db.session.commit()

    # Send email notification
    send_admin_password_reset_email(user)

    flash(f'Mot de passe temporaire pour {user.username}: {temp_password}', 'info')
    flash('L\'utilisateur devra changer son mot de passe à la prochaine connexion.', 'warning')

    return redirect(url_for('admin_users.index'))


@admin_users_bp.route('/<int:user_id>/toggle-active', methods=['POST'])
@admin_required
def toggle_active(user_id):
    """Toggle user active status."""
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()

    status = 'activé' if user.is_active else 'désactivé'
    flash(f'Utilisateur {user.username} {status}.', 'success')

    return redirect(url_for('admin_users.index'))


@admin_users_bp.route('/<int:user_id>/change-role', methods=['POST'])
@admin_required
def change_role(user_id):
    """Change user role."""
    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role')

    if new_role in ['user', 'coach', 'admin']:
        user.role = new_role
        db.session.commit()
        flash(f'Rôle de {user.username} changé en {new_role}.', 'success')
    else:
        flash('Rôle invalide.', 'danger')

    return redirect(url_for('admin_users.index'))
