"""Admin blog blueprint."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user
from fitgang_app import db
from fitgang_app.models import BlogPost
from fitgang_app.forms.blog import BlogPostForm
from fitgang_app.utils.decorators import admin_required
from fitgang_app.utils.uploads import save_uploaded_file
from slugify import slugify

admin_blog_bp = Blueprint('admin_blog', __name__)


@admin_blog_bp.route('/')
@admin_required
def index():
    """List blog posts."""
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('admin/blog.html', posts=posts)


@admin_blog_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    """Create blog post."""
    form = BlogPostForm()

    if form.validate_on_submit():
        post = BlogPost(author_id=current_user.id)
        form.populate_obj(post)

        if not post.slug:
            post.slug = slugify(post.title)

        if form.featured_image.data:
            success, file_path = save_uploaded_file(form.featured_image.data, folder='blog', file_type='image')
            if success:
                post.featured_image = file_path

        db.session.add(post)
        db.session.commit()

        flash('Article créé!', 'success')
        return redirect(url_for('admin_blog.index'))

    return render_template('admin/blog_form.html', form=form, title='Créer un article')


@admin_blog_bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(post_id):
    """Edit blog post."""
    post = BlogPost.query.get_or_404(post_id)
    form = BlogPostForm(obj=post)

    if form.validate_on_submit():
        form.populate_obj(post)

        if form.featured_image.data:
            success, file_path = save_uploaded_file(form.featured_image.data, folder='blog', file_type='image')
            if success:
                post.featured_image = file_path

        db.session.commit()
        flash('Article mis à jour!', 'success')
        return redirect(url_for('admin_blog.index'))

    return render_template('admin/blog_form.html', form=form, post=post, title='Modifier l\'article')


@admin_blog_bp.route('/<int:post_id>/delete', methods=['POST'])
@admin_required
def delete(post_id):
    """Delete blog post."""
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    flash('Article supprimé.', 'info')
    return redirect(url_for('admin_blog.index'))
