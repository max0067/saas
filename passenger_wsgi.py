import sys
import os

# Add application directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Set environment variables
os.environ['FLASK_APP'] = 'app.py'
os.environ['FLASK_ENV'] = 'production'

# Import the Flask application
from app import app as application
