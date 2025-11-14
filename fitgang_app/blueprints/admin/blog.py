"""Admin blog blueprint."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user
from fitgang_app import db
from fitgang_app.models import BlogPost, BlogCategory
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

    # Définir les choices pour le SelectField category_id
    categories = BlogCategory.query.all()
    form.category_id.choices = [(0, '-- Aucune catégorie --')] + [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        post = BlogPost(author_id=current_user.id)
        form.populate_obj(post)

        # Si aucune catégorie sélectionnée (0), mettre à None
        if post.category_id == 0:
            post.category_id = None

        # Si publié, définir la date de publication
        if post.is_published:
            from datetime import datetime
            post.published_at = datetime.utcnow()

        if not post.slug:
            post.slug = slugify(post.title)

        if form.featured_image.data and hasattr(form.featured_image.data, 'filename'):
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

    # Définir les choices pour le SelectField category_id AVANT de créer le form
    categories = BlogCategory.query.all()

    form = BlogPostForm(obj=post)
    form.category_id.choices = [(0, '-- Aucune catégorie --')] + [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        try:
            # Récupérer les données du formulaire manuellement pour mieux contrôler
            post.title = form.title.data
            post.slug = form.slug.data if form.slug.data else slugify(form.title.data)
            post.content = form.content.data
            post.excerpt = form.excerpt.data
            post.meta_title = form.meta_title.data
            post.meta_description = form.meta_description.data
            post.meta_keywords = form.meta_keywords.data
            post.is_published = form.is_published.data
            post.is_featured = form.is_featured.data

            # Gérer la catégorie
            category_id = form.category_id.data
            if category_id == 0 or category_id is None:
                post.category_id = None
            else:
                post.category_id = category_id

            # Si publié et pas encore de date de publication, définir maintenant
            if post.is_published and not post.published_at:
                from datetime import datetime
                post.published_at = datetime.utcnow()

            # Gérer l'image - vérifier que c'est bien un fichier uploadé et pas une string
            if form.featured_image.data and hasattr(form.featured_image.data, 'filename'):
                success, file_path = save_uploaded_file(form.featured_image.data, folder='blog', file_type='image')
                if success:
                    post.featured_image = file_path

            db.session.commit()
            flash('Article mis à jour!', 'success')
            return redirect(url_for('admin_blog.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la mise à jour: {str(e)}', 'danger')
            import traceback
            print(traceback.format_exc())

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
