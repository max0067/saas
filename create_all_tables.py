#!/usr/bin/env python3
"""
Script pour créer TOUTES les tables manquantes dans la base de données.
Fonctionne avec SQLite, MySQL, MariaDB, PostgreSQL.

Usage:
    python3 create_all_tables.py
"""
import os
import sys

# Ajouter le dossier parent au path pour pouvoir importer l'app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from fitgang_app import db

# Import de tous les modèles pour que SQLAlchemy les connaisse
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


def create_all_tables():
    """Créer toutes les tables dans la base de données."""

    print("=" * 60)
    print("CRÉATION DE TOUTES LES TABLES MANQUANTES")
    print("=" * 60)

    # Créer l'application
    env = os.environ.get('FLASK_ENV', 'production')
    print(f"\n📌 Environnement: {env}")

    app = create_app(env)

    with app.app_context():
        # Afficher la base de données utilisée
        db_url = app.config['SQLALCHEMY_DATABASE_URI']

        # Masquer le mot de passe dans l'affichage
        if '@' in db_url:
            parts = db_url.split('@')
            before_at = parts[0].split('://')
            if len(before_at) > 1 and ':' in before_at[1]:
                user = before_at[1].split(':')[0]
                db_url_safe = f"{before_at[0]}://{user}:****@{parts[1]}"
            else:
                db_url_safe = db_url
        else:
            db_url_safe = db_url

        print(f"📊 Base de données: {db_url_safe}\n")

        # Détecter le type de base de données
        if 'sqlite' in db_url:
            db_type = 'SQLite'
        elif 'mysql' in db_url or 'mariadb' in db_url:
            db_type = 'MySQL/MariaDB'
        elif 'postgresql' in db_url:
            db_type = 'PostgreSQL'
        else:
            db_type = 'Inconnu'

        print(f"🔧 Type détecté: {db_type}\n")

        # Créer toutes les tables
        print("⏳ Création des tables en cours...")

        try:
            db.create_all()
            print("✅ Toutes les tables ont été créées avec succès!\n")

            # Afficher les tables créées
            print("📋 Tables créées:")
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()

            for i, table in enumerate(sorted(tables), 1):
                print(f"   {i:2d}. {table}")

            print(f"\n✅ Total: {len(tables)} tables\n")

            # Créer des données de test pour le blog
            print("📝 Création des données de test pour le blog...")

            # Vérifier si les catégories existent déjà
            if BlogCategory.query.count() == 0:
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
                print("   ✅ 3 catégories de blog créées")
            else:
                print("   ℹ️  Catégories déjà existantes")

            # Vérifier si les tags existent déjà
            if BlogTag.query.count() == 0:
                tags = [
                    BlogTag(name='Perte de poids', slug='perte-de-poids'),
                    BlogTag(name='Prise de masse', slug='prise-de-masse'),
                    BlogTag(name='Cardio', slug='cardio'),
                    BlogTag(name='Musculation', slug='musculation'),
                ]
                db.session.add_all(tags)
                db.session.commit()
                print("   ✅ 4 tags de blog créés")
            else:
                print("   ℹ️  Tags déjà existants")

            print("\n" + "=" * 60)
            print("🎉 SUCCÈS! Toutes les tables sont prêtes.")
            print("=" * 60)

            return True

        except Exception as e:
            print(f"\n❌ ERREUR lors de la création des tables:")
            print(f"   {str(e)}\n")

            if db_type == 'MySQL/MariaDB':
                print("⚠️  Si tu vois une erreur Foreign Key:")
                print("   → Utilise phpMyAdmin et le fichier CREATE_ALL_MISSING_TABLES.sql")
                print("   → Ou vérifie que toutes les tables parentes existent d'abord\n")

            return False


if __name__ == '__main__':
    success = create_all_tables()
    sys.exit(0 if success else 1)
