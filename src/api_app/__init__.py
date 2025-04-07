import os
from flask import Flask
from .config import config_by_name
from .extensions import db
from .routes import api_bp
from .commands import register_commands

def create_app(config_name='default'):
    """Application Factory Function."""
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration
    cfg = config_by_name[config_name]
    app.config.from_object(cfg)

    # Ensure the instance folder exists (for SQLite DB)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass # Already exists

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(api_bp, url_prefix='/api') # Add /api prefix to all routes

    # Register CLI commands
    register_commands(app)

    # Optional: Add a simple root route for basic check
    @app.route('/')
    def index():
        return "API Server is running."

    return app
