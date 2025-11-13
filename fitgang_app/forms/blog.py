"""Blog forms."""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class BlogPostForm(FlaskForm):
    """Blog post form."""
    title = StringField(
        'Titre',
        validators=[DataRequired(), Length(max=200)]
    )
    slug = StringField(
        'Slug (URL)',
        validators=[Optional(), Length(max=250)]
    )
    excerpt = TextAreaField(
        'Extrait',
        validators=[Optional(), Length(max=500)]
    )
    content = TextAreaField(
        'Contenu',
        validators=[DataRequired()]
    )
    category_id = SelectField(
        'Catégorie',
        coerce=int,
        validators=[Optional()]
    )
    featured_image = FileField(
        'Image à la une',
        validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images uniquement!')]
    )
    meta_title = StringField(
        'Titre SEO',
        validators=[Optional(), Length(max=200)]
    )
    meta_description = TextAreaField(
        'Description SEO',
        validators=[Optional(), Length(max=500)]
    )
    meta_keywords = StringField(
        'Mots-clés SEO',
        validators=[Optional(), Length(max=500)]
    )
    is_published = BooleanField('Publier')
    is_featured = BooleanField('Mettre en avant')
    submit = SubmitField('Enregistrer')


class BlogCategoryForm(FlaskForm):
    """Blog category form."""
    name = StringField(
        'Nom',
        validators=[DataRequired(), Length(max=100)]
    )
    slug = StringField(
        'Slug (URL)',
        validators=[Optional(), Length(max=120)]
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()]
    )
    submit = SubmitField('Enregistrer')
