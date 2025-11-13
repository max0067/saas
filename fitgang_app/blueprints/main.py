"""Main blueprint."""
from flask import Blueprint, render_template, send_file, current_app, abort
from fitgang_app.models import BlogPost, Product
from fitgang_app.utils.uploads import verify_signed_url_token
import os

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Homepage."""
    from flask import Response
    return Response("TEST - L'accueil fonctionne!", mimetype='text/plain')


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
