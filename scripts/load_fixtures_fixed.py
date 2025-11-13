"""Load sample fixtures into database."""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fitgang_app import create_app, db
from fitgang_app.models import (
    User, UserProfile, Product, ProductType, DifficultyLevel,
    BlogPost, BlogCategory, Workout, Exercise, MealPlan, Recipe, Ingredient,
    Affiliate, GiftCode
)
from datetime import datetime, timedelta
from slugify import slugify


def create_fixtures():
    """Create sample data."""
    app = create_app('development')
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()

        # Create admin user
        print("Creating users...")
        admin = User(
            username='admin',
            email='admin@fitgang.fr',
            role='admin',
            is_active=True,
            is_verified=True
        )
        admin.set_password('admin123')

        admin_profile = UserProfile(
            user=admin,
            first_name='Admin',
            last_name='FitGang',
            height=180,
            current_weight=80
        )

        # Create regular user
        user = User(
            username='john',
            email='john@example.com',
            role='user',
            is_active=True,
            is_verified=True
        )
        user.set_password('password123')

        user_profile = UserProfile(
            user=user,
            first_name='John',
            last_name='Doe',
            height=175,
            current_weight=75,
            target_weight=70
        )

        db.session.add_all([admin, admin_profile, user, user_profile])

        # Create blog categories
        print("Creating blog categories...")
        cat_nutrition = BlogCategory(
            name='Nutrition',
            slug='nutrition',
            description='Conseils nutritionnels et recettes'
        )
        cat_training = BlogCategory(
            name='Entraînement',
            slug='entrainement',
            description='Programmes et conseils d\'entraînement'
        )

        db.session.add_all([cat_nutrition, cat_training])

        # Create blog posts
        print("Creating blog posts...")
        posts = [
            {
                'title': '10 aliments essentiels pour la prise de muscle',
                'content': 'La nutrition est la clé de la réussite...',
                'category': cat_nutrition,
                'is_featured': True
            },
            {
                'title': 'Comment progresser au développé couché',
                'content': 'Le développé couché est un exercice fondamental...',
                'category': cat_training,
                'is_featured': True
            },
            {
                'title': 'Les bases de la perte de poids',
                'content': 'Pour perdre du poids efficacement...',
                'category': cat_nutrition,
                'is_featured': False
            }
        ]

        for post_data in posts:
            post = BlogPost(
                title=post_data['title'],
                slug=slugify(post_data['title']),
                content=post_data['content'],
                excerpt=post_data['content'][:150],
                author=admin,
                category=post_data['category'],
                is_published=True,
                is_featured=post_data['is_featured'],
                published_at=datetime.utcnow()
            )
            db.session.add(post)

        # Create products
        print("Creating products...")
        products = [
            {
                'title': 'Programme Prise de Masse 12 Semaines',
                'product_type': ProductType.PROGRAMME_SPORT,
                'difficulty_level': DifficultyLevel.INTERMEDIAIRE,
                'price': 49.99,
                'duration_weeks': 12,
                'description': 'Programme complet de prise de masse sur 12 semaines',
                'is_featured': True
            },
            {
                'title': 'Plan Nutritionnel Perte de Poids',
                'product_type': ProductType.PROGRAMME_DIETE,
                'difficulty_level': DifficultyLevel.DEBUTANT,
                'price': 39.99,
                'duration_weeks': 8,
                'description': 'Plan nutritionnel pour perdre du poids sainement',
                'is_featured': True
            },
            {
                'title': 'Programme Complet Transformation',
                'product_type': ProductType.PROGRAMME_COMBINE,
                'difficulty_level': DifficultyLevel.AVANCE,
                'price': 79.99,
                'duration_weeks': 16,
                'description': 'Programme complet sport + nutrition',
                'is_featured': True
            },
            {
                'title': 'Guide Complet de la Musculation',
                'product_type': ProductType.EBOOK,
                'price': 19.99,
                'description': 'eBook complet sur la musculation',
                'author': 'FitGang Team',
                'pages': 150,
                'is_featured': False
            },
            {
                'title': 'Recettes Healthy',
                'product_type': ProductType.EBOOK,
                'price': 14.99,
                'description': '50 recettes saines et délicieuses',
                'author': 'FitGang Team',
                'pages': 80,
                'is_featured': False
            }
        ]

        for prod_data in products:
            product = Product(
                title=prod_data['title'],
                slug=slugify(prod_data['title']),
                product_type=prod_data['product_type'],
                difficulty_level=prod_data.get('difficulty_level'),
                price=prod_data['price'],
                duration_weeks=prod_data.get('duration_weeks'),
                description=prod_data['description'],
                short_description=prod_data['description'][:100],
                sku=f"FG-{prod_data['title'][:5].upper()}",
                is_published=True,
                is_featured=prod_data['is_featured'],
                author=prod_data.get('author'),
                pages=prod_data.get('pages'),
                published_at=datetime.utcnow()
            )
            db.session.add(product)

        # Create exercises
        print("Creating exercises...")
        exercises = [
            {'name': 'Développé couché', 'muscle_group': 'Pectoraux', 'equipment': 'Barre'},
            {'name': 'Squat', 'muscle_group': 'Jambes', 'equipment': 'Barre'},
            {'name': 'Soulevé de terre', 'muscle_group': 'Dos', 'equipment': 'Barre'},
            {'name': 'Développé militaire', 'muscle_group': 'Épaules', 'equipment': 'Barre'},
            {'name': 'Tractions', 'muscle_group': 'Dos', 'equipment': 'Barre fixe'}
        ]

        for ex_data in exercises:
            exercise = Exercise(
                name=ex_data['name'],
                slug=slugify(ex_data['name']),
                muscle_group=ex_data['muscle_group'],
                equipment=ex_data['equipment'],
                difficulty='intermediaire'
            )
            db.session.add(exercise)

        # Create affiliates
        print("Creating affiliates...")
        affiliates = [
            {'code': 'FITPRO', 'name': 'FitPro Influencer', 'email': 'fitpro@example.com', 'commission_rate': 15},
            {'code': 'MUSCU10', 'name': 'Musculation Channel', 'email': 'muscu@example.com', 'commission_rate': 10}
        ]

        for aff_data in affiliates:
            affiliate = Affiliate(**aff_data)
            db.session.add(affiliate)

        # Create gift code
        print("Creating gift codes...")
        gift = GiftCode(
            code='WELCOME2024',
            product_id=1,
            sender_id=admin.id,
            recipient_email='test@example.com',
            message='Bienvenue sur FitGang!',
            expires_at=datetime.utcnow() + timedelta(days=365)
        )
        db.session.add(gift)

        db.session.commit()
        print("✅ Fixtures loaded successfully!")
        print("\nAdmin credentials:")
        print("  Email: admin@fitgang.fr")
        print("  Password: admin123")
        print("\nUser credentials:")
        print("  Email: john@example.com")
        print("  Password: password123")
        print("\nGift code: WELCOME2024")


if __name__ == '__main__':
    create_fixtures()
