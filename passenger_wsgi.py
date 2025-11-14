#!/usr/bin/env python
import sys
import os

# Add application directory to path
INTERP = "/usr/bin/python3"
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, os.path.dirname(__file__))

# Set environment variables
os.environ['FLASK_ENV'] = 'production'

# Force reload - Updated: 2025-11-14 06:20
# Import and create the Flask application
from fitgang_app import create_app
application = create_app('production')
