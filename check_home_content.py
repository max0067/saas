#!/usr/bin/env python
"""Check home_content table."""
import sys
sys.path.insert(0, '/home/user/saas')

from fitgang_app import create_app, db
from fitgang_app.models.home_content import HomeContent

app = create_app()

with app.app_context():
    try:
        # Check if table exists and has data
        content = HomeContent.query.first()
        if content:
            print(f"✓ Table home_content existe et a des données (id={content.id})")
            print(f"  - hero_title: {content.hero_title[:50]}...")
            print(f"  - hero_image: {content.hero_image}")
        else:
            print("⚠ Table home_content existe mais est vide")
            # Try to create default content
            print("  Création du contenu par défaut...")
            content = HomeContent()
            db.session.add(content)
            db.session.commit()
            print(f"✓ Contenu créé avec id={content.id}")
    except Exception as e:
        print(f"✗ Erreur: {e}")
        import traceback
        traceback.print_exc()
