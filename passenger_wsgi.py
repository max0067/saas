import sys
import os

# Add application directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Set environment variables
os.environ['FLASK_ENV'] = 'production'

# Import and create the Flask application
from fitgang_app import create_app
application = create_app('production')
