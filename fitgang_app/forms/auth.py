"""Authentication forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from fitgang_app.models.user import User


class LoginForm(FlaskForm):
    """Login form."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')


class RegisterForm(FlaskForm):
    """Registration form."""
    username = StringField(
        'Nom d\'utilisateur',
        validators=[
            DataRequired(),
            Length(min=3, max=80, message='Le nom d\'utilisateur doit contenir entre 3 et 80 caractères')
        ]
    )
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Mot de passe',
        validators=[
            DataRequired(),
            Length(min=8, message='Le mot de passe doit contenir au moins 8 caractères')
        ]
    )
    password_confirm = PasswordField(
        'Confirmer le mot de passe',
        validators=[
            DataRequired(),
            EqualTo('password', message='Les mots de passe doivent correspondre')
        ]
    )
    accept_terms = BooleanField(
        'J\'accepte les conditions d\'utilisation',
        validators=[DataRequired(message='Vous devez accepter les conditions d\'utilisation')]
    )
    submit = SubmitField('S\'inscrire')

    def validate_username(self, username):
        """Validate username uniqueness."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ce nom d\'utilisateur est déjà utilisé.')

    def validate_email(self, email):
        """Validate email uniqueness."""
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError('Cette adresse email est déjà utilisée.')


class ForgotPasswordForm(FlaskForm):
    """Forgot password form."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Envoyer le lien de réinitialisation')


class ResetPasswordForm(FlaskForm):
    """Reset password form."""
    password = PasswordField(
        'Nouveau mot de passe',
        validators=[
            DataRequired(),
            Length(min=8, message='Le mot de passe doit contenir au moins 8 caractères')
        ]
    )
    password_confirm = PasswordField(
        'Confirmer le mot de passe',
        validators=[
            DataRequired(),
            EqualTo('password', message='Les mots de passe doivent correspondre')
        ]
    )
    submit = SubmitField('Réinitialiser le mot de passe')
