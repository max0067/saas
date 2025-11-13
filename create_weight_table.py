#!/usr/bin/env python3
"""Create weight_entries table."""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from fitgang_app import create_app, db
from fitgang_app.models.weight_entry import WeightEntry

app = create_app()

with app.app_context():
    try:
        # Create only the weight_entries table
        WeightEntry.__table__.create(db.engine, checkfirst=True)
        print("✓ Table weight_entries créée avec succès!")
    except Exception as e:
        print(f"✗ Erreur: {e}")
        import traceback
        traceback.print_exc()
