"""Gift forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange


class GiftCodeForm(FlaskForm):
    """Gift code creation form."""
    product_id = SelectField(
        'Produit',
        coerce=int,
        validators=[DataRequired()]
    )
    recipient_email = StringField(
        'Email du destinataire',
        validators=[DataRequired(), Email()]
    )
    message = TextAreaField(
        'Message personnalisé',
        validators=[Optional(), Length(max=500)]
    )
    expiration_days = IntegerField(
        'Expiration (jours)',
        validators=[DataRequired(), NumberRange(min=1, max=365)],
        default=365
    )
    submit = SubmitField('Créer le code cadeau')


class RedeemGiftForm(FlaskForm):
    """Redeem gift code form."""
    code = StringField(
        'Code cadeau',
        validators=[DataRequired(), Length(max=50)]
    )
    submit = SubmitField('Utiliser le code')
