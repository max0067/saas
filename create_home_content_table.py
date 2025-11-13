"""Create home_content table."""
from fitgang_app import create_app, db
from fitgang_app.models.home_content import HomeContent

app = create_app()

with app.app_context():
    # Create the table
    db.create_all()

    # Create initial content with defaults
    content = HomeContent.query.first()
    if not content:
        content = HomeContent()
        db.session.add(content)
        db.session.commit()
        print("✓ Table home_content créée et contenu initial ajouté")
    else:
        print("✓ Table home_content existe déjà")
