"""Public supplements blueprint."""
from flask import Blueprint, render_template, redirect, url_for, jsonify
from fitgang_app.models import Supplement

supplements_bp = Blueprint('supplements', __name__)


@supplements_bp.route('/')
def index():
    """List supplements."""
    # Get published supplements ordered by display_order and featured status
    featured_supplements = Supplement.query.filter_by(
        is_published=True,
        is_featured=True
    ).order_by(Supplement.display_order.asc()).all()

    all_supplements = Supplement.query.filter_by(
        is_published=True
    ).order_by(Supplement.display_order.asc(), Supplement.created_at.desc()).all()

    # Group by category
    categories = {}
    for supp in all_supplements:
        cat = supp.category or 'Autres'
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(supp)

    return render_template(
        'supplements/index.html',
        featured_supplements=featured_supplements,
        categories=categories
    )


@supplements_bp.route('/<slug>')
def detail(slug):
    """View supplement details."""
    supplement = Supplement.query.filter_by(slug=slug, is_published=True).first_or_404()
    supplement.increment_views()

    # Get related supplements from same category
    related = Supplement.query.filter(
        Supplement.category == supplement.category,
        Supplement.id != supplement.id,
        Supplement.is_published == True
    ).limit(3).all()

    return render_template('supplements/detail.html', supplement=supplement, related=related)


@supplements_bp.route('/<int:supplement_id>/click', methods=['POST'])
def track_click(supplement_id):
    """Track affiliate click."""
    supplement = Supplement.query.get_or_404(supplement_id)
    supplement.increment_clicks()
    return jsonify({'success': True, 'redirect_url': supplement.affiliate_link})
