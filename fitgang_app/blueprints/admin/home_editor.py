"""Admin home page editor blueprint."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from fitgang_app import db
from fitgang_app.utils.decorators import admin_required
from fitgang_app.models.home_content import HomeContent
from werkzeug.utils import secure_filename
import os

admin_home_editor_bp = Blueprint('admin_home_editor', __name__)


@admin_home_editor_bp.route('/')
@admin_required
def index():
    """Home page editor."""
    content = HomeContent.get_content()
    return render_template('admin/home_editor/index.html', content=content)


@admin_home_editor_bp.route('/update', methods=['POST'])
@admin_required
def update():
    """Update home page content."""
    content = HomeContent.get_content()

    # Hero Section
    content.hero_title = request.form.get('hero_title', '').strip()
    content.hero_subtitle = request.form.get('hero_subtitle', '').strip()
    content.hero_button_text = request.form.get('hero_button_text', '').strip()
    content.hero_button_link = request.form.get('hero_button_link', '').strip()
    content.hero_secondary_button_text = request.form.get('hero_secondary_button_text', '').strip()
    content.hero_secondary_button_link = request.form.get('hero_secondary_button_link', '').strip()

    # Handle hero image upload
    if 'hero_image' in request.files:
        file = request.files['hero_image']
        if file and file.filename:
            filename = secure_filename(file.filename)
            upload_folder = os.path.join('fitgang_app', 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            content.hero_image = f'uploads/{filename}'

    # Products Section
    content.products_section_title = request.form.get('products_section_title', '').strip()
    content.products_section_subtitle = request.form.get('products_section_subtitle', '').strip()

    # Blog Section
    content.blog_section_title = request.form.get('blog_section_title', '').strip()
    content.blog_section_subtitle = request.form.get('blog_section_subtitle', '').strip()

    # CTA Section
    content.cta_title = request.form.get('cta_title', '').strip()
    content.cta_subtitle = request.form.get('cta_subtitle', '').strip()
    content.cta_button_text = request.form.get('cta_button_text', '').strip()
    content.cta_button_link = request.form.get('cta_button_link', '').strip()

    db.session.commit()

    flash('✓ Page d\'accueil mise à jour avec succès !', 'success')
    return redirect(url_for('admin_home_editor.index'))
