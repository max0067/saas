"""Database models for FitGang application."""
from fitgang_app.models.user import User, UserProfile, UserPhoto
from fitgang_app.models.product import Product, ProductType, DifficultyLevel
from fitgang_app.models.blog import BlogPost, BlogCategory, BlogTag
from fitgang_app.models.workout import Workout, Exercise, WorkoutExercise, WorkoutSession
from fitgang_app.models.meal import MealPlan, Recipe, Ingredient
from fitgang_app.models.order import Order, OrderItem, OrderStatus
from fitgang_app.models.gift import GiftCode, GiftLog
from fitgang_app.models.affiliate import Affiliate, AffiliateClick, AffiliateConversion

__all__ = [
    'User',
    'UserProfile',
    'UserPhoto',
    'Product',
    'ProductType',
    'DifficultyLevel',
    'BlogPost',
    'BlogCategory',
    'BlogTag',
    'Workout',
    'Exercise',
    'WorkoutExercise',
    'WorkoutSession',
    'MealPlan',
    'Recipe',
    'Ingredient',
    'Order',
    'OrderItem',
    'OrderStatus',
    'GiftCode',
    'GiftLog',
    'Affiliate',
    'AffiliateClick',
    'AffiliateConversion',
]
