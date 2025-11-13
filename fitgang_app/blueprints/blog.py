"""Blog blueprint."""
from flask import Blueprint, render_template, abort, request
from fitgang_app.models import BlogPost, BlogCategory

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def list():
    """Blog post list."""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', None, type=int)

    query = BlogPost.query.filter_by(is_published=True)

    if category_id:
        query = query.filter_by(category_id=category_id)

    posts = query.order_by(BlogPost.published_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    categories = BlogCategory.query.all()

    return render_template('blog/list.html', posts=posts, categories=categories)


@blog_bp.route('/<slug>')
def post_detail(slug):
    """Blog post detail."""
    post = BlogPost.query.filter_by(slug=slug, is_published=True).first_or_404()

    # Increment views
    post.increment_views()

    return render_template('blog/post.html', post=post)
