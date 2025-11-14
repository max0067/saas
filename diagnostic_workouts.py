#!/usr/bin/env python3
"""
Script de diagnostic pour comprendre pourquoi les workouts ne s'affichent pas.

Usage:
    python3 diagnostic_workouts.py YOUR_EMAIL
    python3 diagnostic_workouts.py admin@fitgang.fr
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from fitgang_app import db
from fitgang_app.models.user import User
from fitgang_app.models.order import Order, OrderItem, OrderStatus
from fitgang_app.models.product import Product
from fitgang_app.models.workout import Workout, Exercise, WorkoutExercise


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def diagnostic(user_email):
    """Run diagnostic for a user."""
    print("\n🔍 DIAGNOSTIC WORKOUTS - FITGANG")
    print(f"Recherche pour: {user_email}\n")

    env = os.environ.get('FLASK_ENV', 'production')
    app = create_app(env)

    with app.app_context():
        # 1. Vérifier que l'utilisateur existe
        print_section("1. VÉRIFICATION UTILISATEUR")

        user = User.query.filter_by(email=user_email).first()
        if not user:
            print(f"❌ ERREUR: Aucun utilisateur trouvé avec l'email: {user_email}")
            print("\n💡 Essaye avec un autre email ou vérifie l'orthographe.")
            return

        print(f"✅ Utilisateur trouvé:")
        print(f"   ID: {user.id}")
        print(f"   Email: {user.email}")
        print(f"   Username: {user.username}")
        print(f"   Rôle: {user.role}")

        # 2. Vérifier les commandes
        print_section("2. VÉRIFICATION COMMANDES")

        orders = Order.query.filter_by(user_id=user.id).all()
        print(f"📦 Total commandes: {len(orders)}\n")

        if not orders:
            print("❌ PROBLÈME: Aucune commande trouvée!")
            print("\n💡 Tu dois d'abord acheter un programme pour avoir des workouts.")
            return

        completed_orders = [o for o in orders if o.status == OrderStatus.COMPLETED]
        print(f"   ✅ Commandes complétées: {len(completed_orders)}")
        print(f"   ⏳ Commandes en cours: {len([o for o in orders if o.status in [OrderStatus.PENDING, OrderStatus.PROCESSING]])}")
        print(f"   ❌ Commandes échouées: {len([o for o in orders if o.status == OrderStatus.FAILED])}")
        print(f"   💰 Commandes remboursées: {len([o for o in orders if o.status == OrderStatus.REFUNDED])}")

        if not completed_orders:
            print("\n❌ PROBLÈME: Aucune commande avec le statut COMPLETED!")
            print("\n💡 Pour accéder aux workouts, ta commande doit être COMPLETED.")
            print("   Vérifie le paiement Stripe ou change le statut dans l'admin.")
            return

        # 3. Vérifier les produits achetés
        print_section("3. PRODUITS ACHETÉS")

        purchased_products = []
        for order in completed_orders:
            for item in order.items:
                if item.product:
                    purchased_products.append(item.product)

        if not purchased_products:
            print("❌ PROBLÈME: Aucun produit dans les commandes complétées!")
            return

        print(f"🛍️  Total produits achetés: {len(purchased_products)}\n")

        for i, product in enumerate(purchased_products, 1):
            print(f"   {i}. {product.title}")
            print(f"      ID: {product.id}")
            print(f"      Type: {product.product_type}")
            print(f"      Prix: {product.price}€")
            print()

        # 4. Vérifier les workouts disponibles
        print_section("4. WORKOUTS ASSOCIÉS AUX PRODUITS")

        total_workouts = 0
        products_without_workouts = []

        for product in purchased_products:
            workouts = Workout.query.filter_by(product_id=product.id).all()

            print(f"\n📋 {product.title} (ID: {product.id})")
            print(f"   Workouts trouvés: {len(workouts)}")

            if workouts:
                total_workouts += len(workouts)
                for w in workouts[:3]:  # Afficher max 3
                    print(f"   - {w.name} (Semaine {w.week_number}, Jour {w.day_number})")
                if len(workouts) > 3:
                    print(f"   ... et {len(workouts) - 3} autres")
            else:
                products_without_workouts.append(product)
                print(f"   ❌ Aucun workout!")

        # 5. Résumé et diagnostic final
        print_section("5. DIAGNOSTIC FINAL")

        if total_workouts > 0:
            print(f"✅ Tu as accès à {total_workouts} workouts!")
            print(f"\n🤔 MAIS tu dis ne pas les voir sur /workouts?")
            print("\n💡 Causes possibles:")
            print("   1. Le cache Passenger n'est pas vidé")
            print("      → Fais un STOP puis START dans cPanel (pas juste Restart)")
            print("\n   2. Tu n'es pas connecté avec le bon compte")
            print(f"      → Vérifie que tu es bien connecté avec: {user_email}")
            print("\n   3. Erreur dans le code workouts.py")
            print("      → Vérifie les logs d'erreur dans cPanel")

        else:
            print(f"❌ PROBLÈME IDENTIFIÉ: Tu as acheté {len(purchased_products)} produit(s)")
            print(f"   mais AUCUN workout n'est associé à ces produits!\n")

            print("💡 SOLUTIONS:")
            print("\n   A. Créer des workouts via l'interface admin:")
            print("      1. Va sur https://fitgang.fr/admin/products")
            for p in products_without_workouts:
                print(f"      2. Clique sur '{p.title}'")
                print(f"      3. Cherche une section 'Workouts' ou 'Entraînements'")
                print(f"      4. Ajoute des workouts manuellement")

            print("\n   B. Créer un workout de test en SQL (phpMyAdmin):")
            print("\n      Copie cette requête dans phpMyAdmin:")
            for p in products_without_workouts:
                print(f"""
      INSERT INTO workouts (product_id, name, description, week_number, day_number, duration_minutes, difficulty)
      VALUES (
          {p.id},
          'Séance Test - Jour 1',
          'Entraînement de test',
          1,
          1,
          60,
          'intermediate'
      );
                """.strip())
                break  # Juste le premier

        # 6. Statistiques globales
        print_section("6. STATISTIQUES GLOBALES")

        total_workouts_db = Workout.query.count()
        total_products_db = Product.query.count()
        total_exercises_db = Exercise.query.count()

        print(f"📊 Base de données:")
        print(f"   Total workouts: {total_workouts_db}")
        print(f"   Total products: {total_products_db}")
        print(f"   Total exercises: {total_exercises_db}")

        if total_workouts_db == 0:
            print("\n⚠️  La table workouts est COMPLÈTEMENT VIDE!")
            print("   Il faut créer du contenu workout dans l'admin.")

        print("\n" + "=" * 70)
        print("Fin du diagnostic")
        print("=" * 70 + "\n")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 diagnostic_workouts.py YOUR_EMAIL")
        print("Exemple: python3 diagnostic_workouts.py admin@fitgang.fr")
        sys.exit(1)

    user_email = sys.argv[1]
    diagnostic(user_email)
