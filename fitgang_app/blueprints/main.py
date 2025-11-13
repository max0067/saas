"""Main blueprint."""
from flask import Blueprint, render_template, send_file, current_app, abort
from fitgang_app.models import BlogPost, Product, HomeContent
from fitgang_app.utils.uploads import verify_signed_url_token
import os

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Homepage."""
    featured_posts = BlogPost.query.filter_by(is_published=True, is_featured=True).limit(3).all()
    featured_products = Product.query.filter_by(is_published=True, is_featured=True).limit(3).all()

    try:
        home_content = HomeContent.get_content()
    except Exception as e:
        # Fallback to default content if database error
        print(f"Error loading HomeContent, using defaults: {e}")
        # Create a temporary object with defaults (not saved to DB)
        home_content = type('obj', (object,), {
            'hero_title': 'Transforme ton corps.<br>Dépasse tes limites.',
            'hero_subtitle': 'Des programmes de sport et nutrition conçus pour des résultats concrets. Rejoins le mouvement.',
            'hero_image': 'assets/hero-image.svg',
            'hero_button_text': 'Commencer maintenant',
            'hero_button_link': '/shop/programs',
            'hero_secondary_button_text': 'Outils gratuits',
            'hero_secondary_button_link': '/calculators',
            'products_section_title': 'Programmes populaires',
            'products_section_subtitle': 'Choisis le programme adapté à ton objectif',
            'blog_section_title': 'Le blog FitGang',
            'blog_section_subtitle': 'Conseils, astuces et motivation pour progresser',
            'cta_title': 'Prêt à transformer<br>ton physique ?',
            'cta_subtitle': 'Rejoins des milliers de personnes qui progressent chaque jour avec FitGang.',
            'cta_button_text': 'Commence gratuitement',
            'cta_button_link': '/auth/register'
        })()

    return render_template(
        'index.html',
        featured_posts=featured_posts,
        featured_products=featured_products,
        content=home_content
    )


@main_bp.route('/download/<token>')
def download_file(token):
    """Secure file download."""
    expiration = current_app.config['SIGNED_URL_EXPIRATION_HOURS'] * 3600
    file_path = verify_signed_url_token(token, max_age=expiration)

    if not file_path:
        abort(404)

    full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_path)

    if not os.path.exists(full_path):
        abort(404)

    return send_file(full_path, as_attachment=True)
