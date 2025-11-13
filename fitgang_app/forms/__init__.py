"""Forms for FitGang application."""
from fitgang_app.forms.auth import LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm
from fitgang_app.forms.profile import ProfileForm, ChangePasswordForm
from fitgang_app.forms.blog import BlogPostForm, BlogCategoryForm
from fitgang_app.forms.product import ProductForm, MealPlanForm, RecipeForm, WorkoutForm
from fitgang_app.forms.calculators import BMIForm, TDEEForm, MacrosForm, OneRMForm
from fitgang_app.forms.gift import GiftCodeForm, RedeemGiftForm

__all__ = [
    'LoginForm',
    'RegisterForm',
    'ForgotPasswordForm',
    'ResetPasswordForm',
    'ProfileForm',
    'ChangePasswordForm',
    'BlogPostForm',
    'BlogCategoryForm',
    'ProductForm',
    'MealPlanForm',
    'RecipeForm',
    'WorkoutForm',
    'BMIForm',
    'TDEEForm',
    'MacrosForm',
    'OneRMForm',
    'GiftCodeForm',
    'RedeemGiftForm',
]
