#!/usr/bin/env python3
"""
Script pour créer TOUTES les tables manquantes d'un coup.
Usage: python3 fix_all_500_errors.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from fitgang_app import db

print("=" * 70)
print("CRÉATION DE TOUTES LES TABLES MANQUANTES")
print("=" * 70)

app = create_app('production')

with app.app_context():
    print("\n📊 Création des tables...")

    try:
        # Importer TOUS les modèles pour que SQLAlchemy les connaisse
        from fitgang_app.models.user import User, UserProfile, UserPhoto
        from fitgang_app.models.blog import BlogPost, BlogCategory, BlogTag
        from fitgang_app.models.product import Product
        from fitgang_app.models.order import Order, OrderItem
        from fitgang_app.models.workout import Workout, Exercise, WorkoutExercise, WorkoutSession
        from fitgang_app.models.weight_entry import WeightEntry
        from fitgang_app.models.meal import MealPlan, Recipe, Ingredient
        from fitgang_app.models.supplement import Supplement, SupplementRecommendation
        from fitgang_app.models.affiliate import Affiliate, AffiliateClick, AffiliateConversion
        from fitgang_app.models.gift import GiftCode, GiftLog
        from fitgang_app.models.home_content import HomeContent
        from fitgang_app.models.program import ProgramWeek, ProgramDay, UserProgramProgress

        # Créer TOUTES les tables
        db.create_all()

        print("\n✅ Tables créées avec succès!")

        # Afficher toutes les tables
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()

        print(f"\n📋 Tables dans la base de données ({len(tables)} total):")

        # Tables critiques pour les pages qui ont erreur 500
        critical_tables = ['workouts', 'user_photos', 'users']

        for table in sorted(tables):
            indicator = "✅" if table in critical_tables else "  "
            print(f"   {indicator} {table}")

        # Vérifier les tables critiques
        print("\n🔍 Vérification des tables critiques:")

        if 'workouts' in tables:
            print("   ✅ workouts existe → /workouts devrait marcher")
        else:
            print("   ❌ workouts manquante!")

        if 'user_photos' in tables:
            print("   ✅ user_photos existe → /profile/photos devrait marcher")
        else:
            print("   ❌ user_photos manquante!")

        if 'users' in tables:
            print("   ✅ users existe → /auth/forgot-password devrait marcher")
        else:
            print("   ❌ users manquante!")

        # Créer des données de test pour le blog si nécessaire
        if BlogCategory.query.count() == 0:
            print("\n📝 Création des catégories de blog par défaut...")
            categories = [
                BlogCategory(name='Nutrition', slug='nutrition',
                           description='Articles sur la nutrition et l\'alimentation'),
                BlogCategory(name='Entraînement', slug='entrainement',
                           description='Articles sur l\'entraînement et le fitness'),
                BlogCategory(name='Motivation', slug='motivation',
                           description='Articles motivationnels'),
            ]
            db.session.add_all(categories)
            db.session.commit()
            print("   ✅ 3 catégories créées")

        if BlogTag.query.count() == 0:
            print("\n🏷️  Création des tags de blog par défaut...")
            tags = [
                BlogTag(name='Perte de poids', slug='perte-de-poids'),
                BlogTag(name='Prise de masse', slug='prise-de-masse'),
                BlogTag(name='Cardio', slug='cardio'),
                BlogTag(name='Musculation', slug='musculation'),
            ]
            db.session.add_all(tags)
            db.session.commit()
            print("   ✅ 4 tags créés")

        print("\n" + "=" * 70)
        print("🎉 SUCCÈS! Toutes les tables sont prêtes.")
        print("=" * 70)
        print("\nMaintenant:")
        print("1. Redémarre Passenger (STOP puis START)")
        print("2. Teste les URLs:")
        print("   - https://fitgang.fr/workouts")
        print("   - https://fitgang.fr/profile/photos")
        print("   - https://fitgang.fr/auth/forgot-password")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ ERREUR: {str(e)}")
        import traceback
        print("\n" + traceback.format_exc())
        sys.exit(1)
