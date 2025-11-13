"""Debug endpoint for home content."""
from flask import Blueprint, jsonify
from fitgang_app.models.home_content import HomeContent
from fitgang_app import db

debug_home_bp = Blueprint('debug_home', __name__)


@debug_home_bp.route('/debug/home-content')
def check_home_content():
    """Debug endpoint to check home content."""
    try:
        # Try to query
        content = HomeContent.query.first()
        if content:
            return jsonify({
                'status': 'success',
                'message': 'Content exists',
                'id': content.id,
                'hero_title': content.hero_title,
                'data': {
                    'hero_title': content.hero_title,
                    'hero_subtitle': content.hero_subtitle,
                    'hero_image': content.hero_image,
                }
            })
        else:
            return jsonify({
                'status': 'warning',
                'message': 'Table exists but no content'
            })
    except Exception as e:
        import traceback
        return jsonify({
            'status': 'error',
            'message': str(e),
            'traceback': traceback.format_exc()
        }), 500


@debug_home_bp.route('/debug/home-create')
def create_home_content():
    """Try to create home content."""
    try:
        content = HomeContent.get_content()
        return jsonify({
            'status': 'success',
            'message': 'Content retrieved/created',
            'id': content.id if content else None
        })
    except Exception as e:
        import traceback
        return jsonify({
            'status': 'error',
            'message': str(e),
            'traceback': traceback.format_exc()
        }), 500
