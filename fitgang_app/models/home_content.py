"""Home page content model."""
from datetime import datetime
from fitgang_app import db


class HomeContent(db.Model):
    """Editable home page content."""

    __tablename__ = 'home_content'

    id = db.Column(db.Integer, primary_key=True)

    # Hero Section
    hero_title = db.Column(db.String(200), default='Transforme ton corps.<br>Dépasse tes limites.')
    hero_subtitle = db.Column(db.Text, default='Des programmes de sport et nutrition conçus pour des résultats concrets. Rejoins le mouvement.')
    hero_image = db.Column(db.String(500), default='assets/hero-image.svg')  # Filename or URL
    hero_button_text = db.Column(db.String(100), default='Commencer maintenant')
    hero_button_link = db.Column(db.String(200), default='/shop/programs')
    hero_secondary_button_text = db.Column(db.String(100), default='Outils gratuits')
    hero_secondary_button_link = db.Column(db.String(200), default='/calculators')

    # Featured Products Section
    products_section_title = db.Column(db.String(200), default='Programmes populaires')
    products_section_subtitle = db.Column(db.String(300), default='Choisis le programme adapté à ton objectif')

    # Blog Section
    blog_section_title = db.Column(db.String(200), default='Le blog FitGang')
    blog_section_subtitle = db.Column(db.String(300), default='Conseils, astuces et motivation pour progresser')

    # CTA Section
    cta_title = db.Column(db.String(200), default='Prêt à transformer<br>ton physique ?')
    cta_subtitle = db.Column(db.Text, default='Rejoins des milliers de personnes qui progressent chaque jour avec FitGang.')
    cta_button_text = db.Column(db.String(100), default='Commence gratuitement')
    cta_button_link = db.Column(db.String(200), default='/auth/register')

    # Timestamps
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def get_content():
        """Get or create homepage content."""
        content = HomeContent.query.first()
        if not content:
            content = HomeContent()
            db.session.add(content)
            db.session.commit()
        return content

    def __repr__(self):
        return f'<HomeContent {self.id}>'
