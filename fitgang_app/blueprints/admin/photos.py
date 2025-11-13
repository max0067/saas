"""Admin photos blueprint."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from fitgang_app import db
from fitgang_app.utils.decorators import admin_required
from fitgang_app.models.user import UserPhoto, User

admin_photos_bp = Blueprint('admin_photos', __name__)


@admin_photos_bp.route('/')
@admin_required
def index():
    """List all user photos."""
    page = request.args.get('page', 1, type=int)
    user_id = request.args.get('user_id', type=int)
    photo_type = request.args.get('photo_type', None)

    query = UserPhoto.query.join(User).order_by(UserPhoto.uploaded_at.desc())

    if user_id:
        query = query.filter(UserPhoto.user_id == user_id)
    if photo_type:
        query = query.filter(UserPhoto.photo_type == photo_type)

    photos = query.paginate(page=page, per_page=24, error_out=False)
    users = User.query.order_by(User.username).all()

    return render_template(
        'admin/photos/index.html',
        photos=photos,
        users=users,
        current_user_id=user_id,
        current_photo_type=photo_type
    )


@admin_photos_bp.route('/<int:photo_id>/delete', methods=['POST'])
@admin_required
def delete(photo_id):
    """Delete a user photo."""
    photo = UserPhoto.query.get_or_404(photo_id)

    # Delete file from filesystem
    import os
    from flask import current_app
    file_path = os.path.join(current_app.root_path, '..', photo.file_path)
    if os.path.exists(file_path):
        os.remove(file_path)

    db.session.delete(photo)
    db.session.commit()

    flash('Photo supprimée avec succès.', 'success')
    return redirect(url_for('admin_photos.index'))


@admin_photos_bp.route('/<int:photo_id>/toggle-public', methods=['POST'])
@admin_required
def toggle_public(photo_id):
    """Toggle photo public status."""
    photo = UserPhoto.query.get_or_404(photo_id)
    photo.is_public = not photo.is_public
    db.session.commit()

    status = 'publique' if photo.is_public else 'privée'
    flash(f'Photo marquée comme {status}.', 'success')
    return redirect(url_for('admin_photos.index'))
