"""Calculator forms."""
from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class BMIForm(FlaskForm):
    """BMI calculator form."""
    weight = FloatField(
        'Poids (kg)',
        validators=[DataRequired(), NumberRange(min=20, max=500, message='Poids invalide')]
    )
    height = FloatField(
        'Taille (cm)',
        validators=[DataRequired(), NumberRange(min=50, max=300, message='Taille invalide')]
    )
    submit = SubmitField('Calculer l\'IMC')


class TDEEForm(FlaskForm):
    """TDEE (Total Daily Energy Expenditure) calculator form."""
    weight = FloatField(
        'Poids (kg)',
        validators=[DataRequired(), NumberRange(min=20, max=500)]
    )
    height = FloatField(
        'Taille (cm)',
        validators=[DataRequired(), NumberRange(min=50, max=300)]
    )
    age = IntegerField(
        'Âge',
        validators=[DataRequired(), NumberRange(min=10, max=120)]
    )
    gender = SelectField(
        'Sexe',
        choices=[('male', 'Homme'), ('female', 'Femme')],
        validators=[DataRequired()]
    )
    activity_level = SelectField(
        'Niveau d\'activité',
        choices=[
            ('sedentary', 'Sédentaire (peu ou pas d\'exercice)'),
            ('light', 'Légère (exercice 1-3 jours/semaine)'),
            ('moderate', 'Modérée (exercice 3-5 jours/semaine)'),
            ('active', 'Active (exercice 6-7 jours/semaine)'),
            ('very_active', 'Très active (exercice intense quotidien)')
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Calculer la TDEE')


class MacrosForm(FlaskForm):
    """Macros calculator form."""
    calories = IntegerField(
        'Calories quotidiennes',
        validators=[DataRequired(), NumberRange(min=500, max=10000)]
    )
    goal = SelectField(
        'Objectif',
        choices=[
            ('lose', 'Perte de poids'),
            ('maintain', 'Maintien'),
            ('gain', 'Prise de masse')
        ],
        validators=[DataRequired()]
    )
    diet_type = SelectField(
        'Type de régime',
        choices=[
            ('balanced', 'Équilibré'),
            ('low_carb', 'Faible en glucides'),
            ('high_protein', 'Riche en protéines'),
            ('keto', 'Keto')
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Calculer les macros')


class OneRMForm(FlaskForm):
    """One Rep Max calculator form."""
    weight = FloatField(
        'Poids soulevé (kg)',
        validators=[DataRequired(), NumberRange(min=1, max=1000)]
    )
    reps = IntegerField(
        'Répétitions',
        validators=[DataRequired(), NumberRange(min=1, max=20)]
    )
    submit = SubmitField('Calculer le 1RM')
