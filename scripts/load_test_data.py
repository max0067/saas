"""Load test data for FitGang: Programs, eBooks, and Supplements."""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from fitgang_app.models import (
    Product, ProductType, DifficultyLevel,
    ProgramWeek, ProgramDay,
    Supplement
)
from slugify import slugify


def create_test_program():
    """Create a test fitness program."""
    print("Creating test program...")

    # Create program
    program = Product(
        title="Programme Prise de Masse 8 Semaines",
        slug="programme-prise-masse-8-semaines",
        short_description="Programme complet pour développer votre masse musculaire en 8 semaines",
        description="""
        <h3>Programme de prise de masse intensive</h3>
        <p>Ce programme de 8 semaines a été conçu pour maximiser votre gain de masse musculaire.</p>
        <ul>
            <li>5 séances par semaine</li>
            <li>Focus sur les exercices composés</li>
            <li>Plan nutritionnel détaillé</li>
            <li>Vidéos d'accompagnement</li>
        </ul>
        """,
        product_type=ProductType.PROGRAMME_COMBINE,
        difficulty_level=DifficultyLevel.INTERMEDIAIRE,
        price=49.99,
        original_price=79.99,
        duration_weeks=8,
        is_published=True,
        is_featured=True
    )
    db.session.add(program)
    db.session.flush()

    # Create weeks
    for week_num in range(1, 9):
        week = ProgramWeek(
            product_id=program.id,
            week_number=week_num,
            title=f"Semaine {week_num} - {'Adaptation' if week_num <= 2 else 'Intensification' if week_num <= 5 else 'Maximisation'}",
            description=f"Objectifs de la semaine {week_num} : développement musculaire progressif",
            goals=f"- Augmenter la charge\n- Maintenir la forme\n- Progresser sur les exercices clés"
        )
        db.session.add(week)
        db.session.flush()

        # Create days for each week
        workout_days = [
            {
                'day': 1,
                'title': 'Pectoraux & Triceps',
                'type': 'Force',
                'exercises': [
                    {'name': 'Développé couché', 'sets': 4, 'reps': '8-10', 'rest': '90s', 'notes': 'Charge progressive'},
                    {'name': 'Développé incliné haltères', 'sets': 3, 'reps': '10-12', 'rest': '60s', 'notes': ''},
                    {'name': 'Écarté poulie', 'sets': 3, 'reps': '12-15', 'rest': '45s', 'notes': 'Contraction maximale'},
                    {'name': 'Dips', 'sets': 3, 'reps': '10-12', 'rest': '60s', 'notes': ''},
                    {'name': 'Extension triceps poulie', 'sets': 3, 'reps': '12-15', 'rest': '45s', 'notes': ''}
                ],
                'duration': 75,
                'diet_calories': 2800,
                'diet_meals': [
                    {'meal_name': 'Petit-déjeuner', 'time': '7h00', 'foods': 'Omelette 4 œufs, 80g flocons avoine, 1 banane', 'calories': 650, 'macros': 'P:40g C:70g L:20g'},
                    {'meal_name': 'Collation', 'time': '10h00', 'foods': 'Shake protéine, 30g amandes', 'calories': 350, 'macros': 'P:30g C:15g L:18g'},
                    {'meal_name': 'Déjeuner', 'time': '13h00', 'foods': '200g poulet, 100g riz basmati, légumes', 'calories': 650, 'macros': 'P:50g C:70g L:12g'},
                    {'meal_name': 'Collation pré-training', 'time': '16h00', 'foods': '2 tranches pain complet, beurre cacahuète, 1 pomme', 'calories': 400, 'macros': 'P:15g C:50g L:15g'},
                    {'meal_name': 'Dîner', 'time': '20h00', 'foods': '200g saumon, 150g patate douce, brocolis', 'calories': 750, 'macros': 'P:45g C:60g L:25g'}
                ]
            },
            {
                'day': 2,
                'title': 'Dos & Biceps',
                'type': 'Force',
                'exercises': [
                    {'name': 'Tractions', 'sets': 4, 'reps': '8-10', 'rest': '90s', 'notes': 'Lestées si possible'},
                    {'name': 'Rowing barre', 'sets': 4, 'reps': '8-10', 'rest': '90s', 'notes': ''},
                    {'name': 'Tirage horizontal', 'sets': 3, 'reps': '10-12', 'rest': '60s', 'notes': ''},
                    {'name': 'Curl barre', 'sets': 3, 'reps': '10-12', 'rest': '60s', 'notes': ''},
                    {'name': 'Curl haltères', 'sets': 3, 'reps': '12-15', 'rest': '45s', 'notes': 'Supination complète'}
                ],
                'duration': 75
            },
            {
                'day': 3,
                'title': 'Repos actif',
                'type': 'Repos',
                'is_rest': True
            },
            {
                'day': 4,
                'title': 'Jambes',
                'type': 'Force',
                'exercises': [
                    {'name': 'Squat', 'sets': 4, 'reps': '8-10', 'rest': '120s', 'notes': 'Exercice roi'},
                    {'name': 'Presse à cuisses', 'sets': 4, 'reps': '10-12', 'rest': '90s', 'notes': ''},
                    {'name': 'Fentes marchées', 'sets': 3, 'reps': '12/jambe', 'rest': '60s', 'notes': ''},
                    {'name': 'Leg curl', 'sets': 3, 'reps': '12-15', 'rest': '60s', 'notes': ''},
                    {'name': 'Mollets debout', 'sets': 4, 'reps': '15-20', 'rest': '45s', 'notes': ''}
                ],
                'duration': 80
            },
            {
                'day': 5,
                'title': 'Épaules & Abdos',
                'type': 'Force',
                'exercises': [
                    {'name': 'Développé militaire', 'sets': 4, 'reps': '8-10', 'rest': '90s', 'notes': ''},
                    {'name': 'Élévations latérales', 'sets': 4, 'reps': '12-15', 'rest': '60s', 'notes': 'Tempo contrôlé'},
                    {'name': 'Oiseau haltères', 'sets': 3, 'reps': '12-15', 'rest': '60s', 'notes': ''},
                    {'name': 'Crunch', 'sets': 3, 'reps': '20', 'rest': '45s', 'notes': ''},
                    {'name': 'Planche', 'sets': 3, 'reps': '60s', 'rest': '60s', 'notes': 'Gainage statique'}
                ],
                'duration': 60
            },
            {
                'day': 6,
                'title': 'Repos',
                'type': 'Repos',
                'is_rest': True
            },
            {
                'day': 7,
                'title': 'Repos',
                'type': 'Repos',
                'is_rest': True
            }
        ]

        for day_data in workout_days:
            day = ProgramDay(
                week_id=week.id,
                day_number=day_data['day'],
                title=day_data['title'],
                workout_type=day_data['type'],
                is_rest_day=day_data.get('is_rest', False)
            )

            if not day.is_rest_day:
                day.workout_description = f"Séance {day_data['type']} - {day_data['title']}"
                day.workout_exercises = day_data.get('exercises', [])
                day.workout_duration = day_data.get('duration', 60)
                day.notes = "Pensez à bien vous échauffer et vous étirer"
                day.coach_tips = "Concentrez-vous sur la qualité de l'exécution plutôt que sur la charge"

                if 'diet_calories' in day_data:
                    day.diet_calories = day_data['diet_calories']
                    day.diet_meals = day_data['diet_meals']
                    day.diet_description = f"Plan nutritionnel pour {day_data['diet_calories']} calories"

            db.session.add(day)

    db.session.commit()
    print(f"✅ Programme créé: {program.title} (ID: {program.id})")
    return program


def create_test_ebook():
    """Create a test eBook."""
    print("Creating test eBook...")

    ebook = Product(
        title="Guide Complet de la Nutrition Sportive",
        slug="guide-nutrition-sportive",
        short_description="Tout ce que vous devez savoir pour optimiser votre alimentation",
        description="""
        <h3>Le guide ultime de la nutrition sportive</h3>
        <p>Découvrez les secrets d'une nutrition optimale pour vos performances sportives.</p>
        <h4>Au programme:</h4>
        <ul>
            <li>Les macronutriments expliqués</li>
            <li>Timing des repas</li>
            <li>Supplémentation intelligente</li>
            <li>Plans de repas détaillés</li>
            <li>Recettes fitness</li>
        </ul>
        """,
        product_type=ProductType.EBOOK,
        author="Coach FitGang",
        pages=150,
        price=19.99,
        original_price=29.99,
        is_published=True,
        is_featured=True
    )
    db.session.add(ebook)
    db.session.commit()

    print(f"✅ eBook créé: {ebook.title} (ID: {ebook.id})")
    return ebook


def create_test_supplements():
    """Create test supplements."""
    print("Creating test supplements...")

    supplements_data = [
        {
            'name': 'Whey Protein Isolate Premium',
            'category': 'Protéine',
            'brand': 'MyProtein',
            'short_description': 'Protéine isolate de haute qualité pour la récupération musculaire',
            'description': 'Notre Whey Protein Isolate contient 90% de protéines pures, idéale pour la prise de masse et la récupération post-entraînement.',
            'benefits': [
                'Favorise la croissance musculaire',
                'Améliore la récupération',
                'Faible en glucides et lipides',
                'Digestion rapide'
            ],
            'usage_instructions': 'Mélanger 30g (1 dose) avec 250-300ml d\'eau ou de lait. Consommer 1-3 fois par jour, idéalement après l\'entraînement.',
            'ingredients': 'Isolat de protéine de lactosérum (lait), émulsifiant (lécithine de soja), arômes naturels, édulcorant (sucralose).',
            'warnings': 'Contient du lait et du soja. Tenir hors de portée des enfants.',
            'price_range': '29-49€',
            'affiliate_link': 'https://www.myprotein.fr',
            'is_featured': True
        },
        {
            'name': 'Créatine Monohydrate Micronisée',
            'category': 'Créatine',
            'brand': 'Optimum Nutrition',
            'short_description': 'Créatine pure pour augmenter force et performance',
            'description': 'Créatine monohydrate micronisée de qualité pharmaceutique, scientifiquement prouvée pour améliorer les performances lors d\'efforts intenses.',
            'benefits': [
                'Augmente la force musculaire',
                'Améliore les performances explosives',
                'Favorise la prise de masse',
                'Réduit la fatigue'
            ],
            'usage_instructions': 'Prendre 5g par jour, de préférence après l\'entraînement avec des glucides rapides.',
            'ingredients': '100% créatine monohydrate micronisée',
            'price_range': '15-25€',
            'affiliate_link': 'https://www.myprotein.fr',
            'is_featured': True
        },
        {
            'name': 'BCAA 2:1:1',
            'category': 'Acides aminés',
            'brand': 'Scitec Nutrition',
            'short_description': 'Acides aminés essentiels pour la récupération',
            'description': 'Complexe d\'acides aminés ramifiés dans le ratio optimal 2:1:1 (Leucine, Isoleucine, Valine) pour soutenir la synthèse protéique.',
            'benefits': [
                'Réduit le catabolisme musculaire',
                'Accélère la récupération',
                'Diminue les courbatures',
                'Maintient l\'énergie pendant l\'entraînement'
            ],
            'usage_instructions': '5-10g avant ou pendant l\'entraînement.',
            'price_range': '20-35€',
            'affiliate_link': 'https://www.myprotein.fr'
        },
        {
            'name': 'Multivitamines Sport Performance',
            'category': 'Vitamines',
            'brand': 'Nutrimuscle',
            'short_description': 'Complexe complet de vitamines et minéraux',
            'description': 'Formule complète spécialement conçue pour les sportifs, avec dosages optimaux de toutes les vitamines et minéraux essentiels.',
            'benefits': [
                'Comble les carences nutritionnelles',
                'Soutient le système immunitaire',
                'Améliore l\'énergie et la vitalité',
                'Optimise les performances'
            ],
            'usage_instructions': '1 comprimé par jour au petit-déjeuner.',
            'price_range': '15-30€',
            'affiliate_link': 'https://www.nutrimuscle.com'
        },
        {
            'name': 'Oméga-3 EPA/DHA',
            'category': 'Acides gras',
            'brand': 'Nutripure',
            'short_description': 'Acides gras essentiels pour la santé et la performance',
            'description': 'Huile de poisson purifiée, riche en EPA et DHA, pour soutenir la santé cardiovasculaire et réduire l\'inflammation.',
            'benefits': [
                'Réduit l\'inflammation',
                'Améliore la santé cardiovasculaire',
                'Soutient la fonction cognitive',
                'Favorise la récupération'
            ],
            'usage_instructions': '2-3 capsules par jour avec les repas.',
            'price_range': '20-40€',
            'affiliate_link': 'https://www.nutripure.fr'
        }
    ]

    created_supplements = []
    for i, data in enumerate(supplements_data):
        supplement = Supplement(
            name=data['name'],
            slug=slugify(data['name']),
            category=data['category'],
            brand=data['brand'],
            short_description=data['short_description'],
            description=data['description'],
            benefits=data['benefits'],
            usage_instructions=data['usage_instructions'],
            ingredients=data.get('ingredients', ''),
            warnings=data.get('warnings', ''),
            price_range=data['price_range'],
            affiliate_link=data['affiliate_link'],
            is_published=True,
            is_featured=data.get('is_featured', False),
            display_order=i
        )
        db.session.add(supplement)
        created_supplements.append(supplement)

    db.session.commit()
    print(f"✅ {len(created_supplements)} compléments créés")
    return created_supplements


def main():
    """Load all test data."""
    with app.app_context():
        print("\n" + "="*60)
        print("🔄 Chargement des données de test FitGang")
        print("="*60 + "\n")

        try:
            # Create test program
            program = create_test_program()

            # Create test eBook
            ebook = create_test_ebook()

            # Create test supplements
            supplements = create_test_supplements()

            print("\n" + "="*60)
            print("✅ Données de test chargées avec succès!")
            print("="*60)
            print("\n📋 Résumé:")
            print(f"   • 1 Programme: {program.title}")
            print(f"   • 1 eBook: {ebook.title}")
            print(f"   • {len(supplements)} Compléments alimentaires")
            print("\n🚀 Accédez au dashboard admin pour voir le résultat:")
            print("   → /admin")
            print("\n🌐 Pages publiques à visiter:")
            print("   → /programmes")
            print("   → /complements")
            print("\n")

        except Exception as e:
            print(f"\n❌ Erreur: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()


if __name__ == '__main__':
    main()
