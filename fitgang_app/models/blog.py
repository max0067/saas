"""Blog models."""
from datetime import datetime
from fitgang_app import db

# Association table for blog post tags
post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('blog_posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('blog_tags.id'), primary_key=True)
)


class BlogPost(db.Model):
    """Blog post model."""

    __tablename__ = 'blog_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(250), unique=True, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(500))

    # Author
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Category
    category_id = db.Column(db.Integer, db.ForeignKey('blog_categories.id'))

    # Media
    featured_image = db.Column(db.String(500))

    # SEO
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.String(500))
    meta_keywords = db.Column(db.String(500))

    # Status
    is_published = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)

    # Stats
    views = db.Column(db.Integer, default=0)

    # Timestamps
    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    author = db.relationship('User', backref='blog_posts')
    category = db.relationship('BlogCategory', back_populates='posts')
    tags = db.relationship('BlogTag', secondary=post_tags, back_populates='posts')

    def increment_views(self):
        """Increment post views."""
        self.views += 1
        db.session.commit()

    def __repr__(self):
        return f'<BlogPost {self.title}>'


class BlogCategory(db.Model):
    """Blog category model."""

    __tablename__ = 'blog_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    posts = db.relationship('BlogPost', back_populates='category')

    def __repr__(self):
        return f'<BlogCategory {self.name}>'


class BlogTag(db.Model):
    """Blog tag model."""

    __tablename__ = 'blog_tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(60), unique=True, nullable=False, index=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    posts = db.relationship('BlogPost', secondary=post_tags, back_populates='tags')

    def __repr__(self):
        return f'<BlogTag {self.name}>'
