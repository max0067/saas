"""Profile forms."""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, FloatField, DateField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange


class ProfileForm(FlaskForm):
    """Profile update form."""
    first_name = StringField('Prénom', validators=[Optional(), Length(max=50)])
    last_name = StringField('Nom', validators=[Optional(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    date_of_birth = DateField('Date de naissance', validators=[Optional()], format='%Y-%m-%d')
    gender = SelectField(
        'Sexe',
        choices=[('', 'Sélectionner...'), ('male', 'Homme'), ('female', 'Femme'), ('other', 'Autre')],
        validators=[Optional()]
    )
    height = FloatField('Taille (cm)', validators=[Optional(), NumberRange(min=50, max=300)])
    current_weight = FloatField('Poids actuel (kg)', validators=[Optional(), NumberRange(min=20, max=500)])
    target_weight = FloatField('Poids cible (kg)', validators=[Optional(), NumberRange(min=20, max=500)])
    fitness_goal = StringField('Objectif fitness', validators=[Optional(), Length(max=100)])
    activity_level = SelectField(
        'Niveau d\'activité',
        choices=[
            ('', 'Sélectionner...'),
            ('sedentary', 'Sédentaire'),
            ('light', 'Légère activité'),
            ('moderate', 'Activité modérée'),
            ('active', 'Très actif'),
            ('very_active', 'Extrêmement actif')
        ],
        validators=[Optional()]
    )
    dietary_preferences = TextAreaField('Préférences alimentaires', validators=[Optional()])
    submit = SubmitField('Mettre à jour le profil')


class ChangePasswordForm(FlaskForm):
    """Change password form."""
    current_password = PasswordField('Mot de passe actuel', validators=[DataRequired()])
    new_password = PasswordField(
        'Nouveau mot de passe',
        validators=[
            DataRequired(),
            Length(min=8, message='Le mot de passe doit contenir au moins 8 caractères')
        ]
    )
    new_password_confirm = PasswordField(
        'Confirmer le nouveau mot de passe',
        validators=[
            DataRequired(),
            EqualTo('new_password', message='Les mots de passe doivent correspondre')
        ]
    )
    submit = SubmitField('Changer le mot de passe')


class UploadPhotoForm(FlaskForm):
    """Upload photo form."""
    photo = FileField(
        'Photo',
        validators=[
            DataRequired(),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images uniquement!')
        ]
    )
    photo_type = SelectField(
        'Type de photo',
        choices=[('before', 'Avant'), ('after', 'Après'), ('progress', 'Progression')],
        validators=[DataRequired()]
    )
    weight_at_photo = FloatField('Poids (kg)', validators=[Optional(), NumberRange(min=20, max=500)])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Uploader')
