#!/usr/bin/env python3
"""
Script pour créer la table workouts dans la base de données.
Usage: python3 create_workouts_table.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from fitgang_app import db
from fitgang_app.models.workout import Workout, Exercise, WorkoutExercise, WorkoutSession

print("=" * 70)
print("CRÉATION DE LA TABLE WORKOUTS")
print("=" * 70)

app = create_app('production')

with app.app_context():
    try:
        # Vérifier si la table existe déjà
        inspector = db.inspect(db.engine)
        existing_tables = inspector.get_table_names()

        print(f"\n📊 Tables existantes dans la base: {len(existing_tables)}")

        if 'workouts' in existing_tables:
            print("\n✅ La table 'workouts' existe déjà!")
            # Compter les workouts
            count = Workout.query.count()
            print(f"   Nombre de workouts: {count}")
        else:
            print("\n⚠️  La table 'workouts' n'existe PAS!")
            print("   Création en cours...")

            # Créer toutes les tables liées aux workouts
            db.create_all()

            print("\n✅ Tables créées avec succès!")

        # Afficher toutes les tables après création
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()

        print(f"\n📋 Tables dans la base de données:")
        for i, table in enumerate(sorted(tables), 1):
            indicator = "🆕" if table in ['workouts', 'exercises', 'workout_exercises', 'workout_sessions'] else "  "
            print(f"   {indicator} {i:2d}. {table}")

        print(f"\n✅ Total: {len(tables)} tables")

        # Vérifier que les tables workouts sont bien là
        workout_tables = ['workouts', 'exercises', 'workout_exercises', 'workout_sessions']
        missing = [t for t in workout_tables if t not in tables]

        if missing:
            print(f"\n❌ Tables manquantes: {', '.join(missing)}")
            print("\n💡 Si tu vois cette erreur, il faut créer les tables via SQL:")
            print("   Utilise le fichier CREATE_ALL_MISSING_TABLES.sql dans phpMyAdmin")
        else:
            print(f"\n✅ Toutes les tables workouts sont créées!")
            print("\nTu peux maintenant:")
            print("   1. Aller sur https://fitgang.fr/admin/workouts")
            print("   2. Créer des workouts avec la création rapide")
            print("   3. Voir les workouts sur https://fitgang.fr/workouts")

    except Exception as e:
        print(f"\n❌ ERREUR: {str(e)}")
        import traceback
        print("\n" + traceback.format_exc())
        sys.exit(1)
