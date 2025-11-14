"""FitGang Application Entry Point."""
# Force reload - Updated: 2025-11-14 06:22
import os
from fitgang_app import create_app, db
from fitgang_app.models import (
    User, Product, BlogPost, BlogCategory, Workout, Exercise,
    MealPlan, Recipe, Order, OrderItem, GiftCode, Affiliate,
    ProgramWeek, ProgramDay, UserProgramProgress,
    Supplement, SupplementRecommendation
)

app = create_app(os.environ.get('FLASK_ENV', 'development'))
application = app  # For WSGI servers


@app.shell_context_processor
def make_shell_context():
    """Create shell context for flask shell command."""
    return {
        'db': db,
        'User': User,
        'Product': Product,
        'BlogPost': BlogPost,
        'BlogCategory': BlogCategory,
        'Workout': Workout,
        'Exercise': Exercise,
        'MealPlan': MealPlan,
        'Recipe': Recipe,
        'Order': Order,
        'OrderItem': OrderItem,
        'GiftCode': GiftCode,
        'Affiliate': Affiliate,
        'ProgramWeek': ProgramWeek,
        'ProgramDay': ProgramDay,
        'UserProgramProgress': UserProgramProgress,
        'Supplement': Supplement,
        'SupplementRecommendation': SupplementRecommendation,
    }


@app.cli.command()
def create_db():
    """Create database tables."""
    db.create_all()
    print('Database tables created successfully!')


@app.cli.command()
def drop_db():
    """Drop database tables."""
    if input('Are you sure you want to drop all tables? (yes/no): ').lower() == 'yes':
        db.drop_all()
        print('Database tables dropped successfully!')
    else:
        print('Operation cancelled.')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
