"""Profile blueprint."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from fitgang_app import db
from fitgang_app.models import OrderItem
from fitgang_app.forms.profile import ProfileForm, ChangePasswordForm, UploadPhotoForm
from fitgang_app.models.user import UserPhoto
from fitgang_app.utils.uploads import save_uploaded_file

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/')
@login_required
def index():
    """User profile."""
    return render_template('profile/index.html', user=current_user)


@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    """Edit profile."""
    form = ProfileForm(obj=current_user.profile)

    if form.validate_on_submit():
        # Update user email
        current_user.email = form.email.data.lower()

        # Update profile
        form.populate_obj(current_user.profile)

        # Calculate BMI if height and weight available
        if current_user.profile.height and current_user.profile.current_weight:
            current_user.profile.calculate_bmi()

        db.session.commit()
        flash('Profil mis à jour avec succès!', 'success')
        return redirect(url_for('profile.index'))

    # Pre-populate email
    form.email.data = current_user.email
    return render_template('profile/index.html', form=form)


@profile_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password."""
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Mot de passe actuel incorrect.', 'danger')
            return redirect(url_for('profile.change_password'))

        current_user.set_password(form.new_password.data)
        current_user.force_password_change = False
        db.session.commit()

        flash('Mot de passe modifié avec succès!', 'success')
        return redirect(url_for('profile.index'))

    return render_template('profile/change_password.html', form=form)


@profile_bp.route('/photos', methods=['GET', 'POST'])
@login_required
def photos():
    """User photos (before/after)."""
    form = UploadPhotoForm()

    if form.validate_on_submit():
        success, file_path = save_uploaded_file(form.photo.data, folder='user_photos', file_type='image')

        if success:
            photo = UserPhoto(
                user_id=current_user.id,
                filename=form.photo.data.filename,
                file_path=file_path,
                photo_type=form.photo_type.data,
                weight_at_photo=form.weight_at_photo.data,
                description=form.description.data
            )
            db.session.add(photo)
            db.session.commit()

            flash('Photo ajoutée avec succès!', 'success')
            return redirect(url_for('profile.photos'))
        else:
            flash(f'Erreur lors de l\'upload: {file_path}', 'danger')

    photos = UserPhoto.query.filter_by(user_id=current_user.id).order_by(UserPhoto.uploaded_at.desc()).all()
    return render_template('profile/photos.html', photos=photos, form=form)


@profile_bp.route('/purchases')
@login_required
def purchases():
    """User purchases."""
    order_items = OrderItem.query.join(OrderItem.order).filter(
        OrderItem.order.has(user_id=current_user.id, status='completed')
    ).all()

    return render_template('profile/purchases.html', order_items=order_items)
