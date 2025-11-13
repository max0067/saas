"""Product forms."""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, TextAreaField, FloatField, IntegerField,
    SelectField, BooleanField, SubmitField
)
from wtforms.validators import DataRequired, Length, Optional, NumberRange


class ProductForm(FlaskForm):
    """Product form."""
    title = StringField(
        'Titre',
        validators=[DataRequired(), Length(max=200)]
    )
    slug = StringField(
        'Slug (URL)',
        validators=[Optional(), Length(max=250)]
    )
    short_description = StringField(
        'Description courte',
        validators=[Optional(), Length(max=500)]
    )
    description = TextAreaField(
        'Description',
        validators=[DataRequired()]
    )
    product_type = SelectField(
        'Type de produit',
        choices=[
            ('programme_sport', 'Programme Sport'),
            ('programme_diete', 'Programme Diète'),
            ('programme_combine', 'Programme Combiné'),
            ('ebook', 'eBook')
        ],
        validators=[DataRequired()]
    )
    difficulty_level = SelectField(
        'Niveau',
        choices=[
            ('', 'Sélectionner...'),
            ('debutant', 'Débutant'),
            ('intermediaire', 'Intermédiaire'),
            ('avance', 'Avancé')
        ],
        validators=[Optional()]
    )
    price = FloatField(
        'Prix (€)',
        validators=[DataRequired(), NumberRange(min=0)]
    )
    original_price = FloatField(
        'Prix original (€)',
        validators=[Optional(), NumberRange(min=0)]
    )
    duration_weeks = IntegerField(
        'Durée (semaines)',
        validators=[Optional(), NumberRange(min=1, max=104)]
    )
    sku = StringField(
        'SKU',
        validators=[Optional(), Length(max=100)]
    )
    stock = IntegerField(
        'Stock',
        validators=[Optional(), NumberRange(min=0)]
    )
    image = FileField(
        'Image principale',
        validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images uniquement!')]
    )
    file = FileField(
        'Fichier (PDF/EPUB)',
        validators=[FileAllowed(['pdf', 'epub'], 'PDF ou EPUB uniquement!')]
    )
    author = StringField(
        'Auteur',
        validators=[Optional(), Length(max=100)]
    )
    pages = IntegerField(
        'Nombre de pages',
        validators=[Optional(), NumberRange(min=1)]
    )
    isbn = StringField(
        'ISBN',
        validators=[Optional(), Length(max=20)]
    )
    max_downloads = IntegerField(
        'Téléchargements maximum',
        validators=[Optional(), NumberRange(min=1)],
        default=5
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


class MealPlanForm(FlaskForm):
    """Meal plan form."""
    name = StringField(
        'Nom du plan',
        validators=[DataRequired(), Length(max=200)]
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()]
    )
    week_number = IntegerField(
        'Semaine',
        validators=[Optional(), NumberRange(min=1)]
    )
    total_days = IntegerField(
        'Jours',
        validators=[DataRequired(), NumberRange(min=1, max=30)],
        default=7
    )
    target_calories = IntegerField(
        'Calories cibles',
        validators=[Optional(), NumberRange(min=500)]
    )
    target_protein = IntegerField(
        'Protéines cibles (g)',
        validators=[Optional(), NumberRange(min=0)]
    )
    target_carbs = IntegerField(
        'Glucides cibles (g)',
        validators=[Optional(), NumberRange(min=0)]
    )
    target_fat = IntegerField(
        'Lipides cibles (g)',
        validators=[Optional(), NumberRange(min=0)]
    )
    submit = SubmitField('Enregistrer')


class RecipeForm(FlaskForm):
    """Recipe form."""
    name = StringField(
        'Nom de la recette',
        validators=[DataRequired(), Length(max=200)]
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()]
    )
    day_number = IntegerField(
        'Jour',
        validators=[DataRequired(), NumberRange(min=1, max=30)]
    )
    meal_type = SelectField(
        'Type de repas',
        choices=[
            ('breakfast', 'Petit-déjeuner'),
            ('lunch', 'Déjeuner'),
            ('dinner', 'Dîner'),
            ('snack', 'Collation')
        ],
        validators=[DataRequired()]
    )
    prep_time_minutes = IntegerField(
        'Temps de préparation (min)',
        validators=[Optional(), NumberRange(min=0)]
    )
    cook_time_minutes = IntegerField(
        'Temps de cuisson (min)',
        validators=[Optional(), NumberRange(min=0)]
    )
    servings = IntegerField(
        'Portions',
        validators=[DataRequired(), NumberRange(min=1)],
        default=1
    )
    instructions = TextAreaField(
        'Instructions',
        validators=[DataRequired()]
    )
    calories = IntegerField(
        'Calories',
        validators=[Optional(), NumberRange(min=0)]
    )
    protein = FloatField(
        'Protéines (g)',
        validators=[Optional(), NumberRange(min=0)]
    )
    carbs = FloatField(
        'Glucides (g)',
        validators=[Optional(), NumberRange(min=0)]
    )
    fat = FloatField(
        'Lipides (g)',
        validators=[Optional(), NumberRange(min=0)]
    )
    image = FileField(
        'Image',
        validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images uniquement!')]
    )
    submit = SubmitField('Enregistrer')


class WorkoutForm(FlaskForm):
    """Workout form."""
    name = StringField(
        'Nom de la séance',
        validators=[DataRequired(), Length(max=200)]
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()]
    )
    week_number = IntegerField(
        'Semaine',
        validators=[Optional(), NumberRange(min=1)]
    )
    day_number = IntegerField(
        'Jour',
        validators=[Optional(), NumberRange(min=1, max=7)]
    )
    duration_minutes = IntegerField(
        'Durée (minutes)',
        validators=[Optional(), NumberRange(min=1)]
    )
    difficulty = SelectField(
        'Difficulté',
        choices=[
            ('', 'Sélectionner...'),
            ('debutant', 'Débutant'),
            ('intermediaire', 'Intermédiaire'),
            ('avance', 'Avancé')
        ],
        validators=[Optional()]
    )
    warmup = TextAreaField(
        'Échauffement',
        validators=[Optional()]
    )
    cooldown = TextAreaField(
        'Retour au calme',
        validators=[Optional()]
    )
    notes = TextAreaField(
        'Notes',
        validators=[Optional()]
    )
    submit = SubmitField('Enregistrer')
