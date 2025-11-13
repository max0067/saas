"""FitGang Flask Application Factory."""
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()


def create_app(config_name=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Load config
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    from config import config
    app.config.from_object(config.get(config_name, config['default']))

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    csrf.init_app(app)

    # Initialize login manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        from fitgang_app.models.user import User
        return User.query.get(int(user_id))

    # Register blueprints
    from fitgang_app.blueprints.main import main_bp
    from fitgang_app.blueprints.auth import auth_bp
    from fitgang_app.blueprints.dashboard import dashboard_bp
    from fitgang_app.blueprints.profile import profile_bp
    from fitgang_app.blueprints.blog import blog_bp
    from fitgang_app.blueprints.shop import shop_bp
    from fitgang_app.blueprints.cart import cart_bp
    from fitgang_app.blueprints.checkout import checkout_bp
    from fitgang_app.blueprints.workouts import workouts_bp
    from fitgang_app.blueprints.calculators import calculators_bp
    from fitgang_app.blueprints.supplements import supplements_bp
    from fitgang_app.blueprints.gifts import gifts_bp
    from fitgang_app.blueprints.webhooks import webhooks_bp
    from fitgang_app.blueprints.api import api_bp

    # Admin blueprints
    from fitgang_app.blueprints.admin import (
        admin_bp, admin_users_bp, admin_products_bp,
        admin_blog_bp, admin_analytics_bp, admin_affiliates_bp
    )
    from fitgang_app.blueprints.admin.programs import admin_programs_bp
    from fitgang_app.blueprints.admin.ebooks import admin_ebooks_bp
    from fitgang_app.blueprints.admin.supplements import admin_supplements_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(shop_bp, url_prefix='/programmes')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(checkout_bp, url_prefix='/checkout')
    app.register_blueprint(workouts_bp, url_prefix='/workouts')
    app.register_blueprint(calculators_bp, url_prefix='/calculators')
    app.register_blueprint(supplements_bp, url_prefix='/complements')
    app.register_blueprint(gifts_bp, url_prefix='/gifts')
    app.register_blueprint(webhooks_bp, url_prefix='/webhooks')
    app.register_blueprint(api_bp, url_prefix='/api')

    # Admin blueprints
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(admin_users_bp, url_prefix='/admin/users')
    app.register_blueprint(admin_products_bp, url_prefix='/admin/products')
    app.register_blueprint(admin_programs_bp, url_prefix='/admin/programs')
    app.register_blueprint(admin_ebooks_bp, url_prefix='/admin/ebooks')
    app.register_blueprint(admin_supplements_bp, url_prefix='/admin/supplements')
    app.register_blueprint(admin_blog_bp, url_prefix='/admin/blog')
    app.register_blueprint(admin_analytics_bp, url_prefix='/admin/analytics')
    app.register_blueprint(admin_affiliates_bp, url_prefix='/admin/affiliates')

    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # Register context processors
    @app.context_processor
    def inject_globals():
        from datetime import datetime
        return {
            'now': datetime.utcnow(),
            'site_name': app.config['SITE_NAME']
        }

    # SEO routes
    @app.route('/robots.txt')
    def robots():
        return app.send_static_file('robots.txt')

    @app.route('/sitemap.xml')
    def sitemap():
        from fitgang_app.utils.seo import generate_sitemap
        return generate_sitemap(app)

    # Uploads route
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        """Serve uploaded files."""
        from flask import send_from_directory
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app
