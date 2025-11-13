"""Meal plan models."""
from datetime import datetime
from fitgang_app import db


class MealPlan(db.Model):
    """Meal plan model."""

    __tablename__ = 'meal_plans'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    # Basic information
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

    # Plan details
    week_number = db.Column(db.Integer)
    total_days = db.Column(db.Integer, default=7)

    # Nutritional targets
    target_calories = db.Column(db.Integer)
    target_protein = db.Column(db.Integer)  # grams
    target_carbs = db.Column(db.Integer)  # grams
    target_fat = db.Column(db.Integer)  # grams

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    product = db.relationship('Product', back_populates='meal_plans')
    recipes = db.relationship('Recipe', back_populates='meal_plan', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<MealPlan {self.name}>'


class Recipe(db.Model):
    """Recipe model."""

    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    meal_plan_id = db.Column(db.Integer, db.ForeignKey('meal_plans.id'))

    # Basic information
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

    # Meal details
    day_number = db.Column(db.Integer)  # Which day (1-7)
    meal_type = db.Column(db.String(50))  # breakfast, lunch, dinner, snack
    prep_time_minutes = db.Column(db.Integer)
    cook_time_minutes = db.Column(db.Integer)
    servings = db.Column(db.Integer, default=1)

    # Instructions
    instructions = db.Column(db.Text, nullable=False)

    # Nutritional information
    calories = db.Column(db.Integer)
    protein = db.Column(db.Float)  # grams
    carbs = db.Column(db.Float)  # grams
    fat = db.Column(db.Float)  # grams
    fiber = db.Column(db.Float)  # grams

    # Media
    image_url = db.Column(db.String(500))

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    meal_plan = db.relationship('MealPlan', back_populates='recipes')
    ingredients = db.relationship('Ingredient', back_populates='recipe', cascade='all, delete-orphan')

    def get_total_time(self):
        """Get total preparation and cooking time."""
        return (self.prep_time_minutes or 0) + (self.cook_time_minutes or 0)

    def __repr__(self):
        return f'<Recipe {self.name}>'


class Ingredient(db.Model):
    """Ingredient model."""

    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)

    # Ingredient details
    name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.String(50))  # e.g., "200g", "2 cups", "1 piece"
    unit = db.Column(db.String(50))
    notes = db.Column(db.String(200))

    # Order in the recipe
    order = db.Column(db.Integer, default=0)

    # Relationships
    recipe = db.relationship('Recipe', back_populates='ingredients')

    def __repr__(self):
        return f'<Ingredient {self.name}>'
