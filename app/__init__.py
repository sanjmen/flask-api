"""Flask application factory."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.application.controllers.home_controller import create_home_blueprint
from app.infrastructure.api.error_handlers import register_error_handlers

db = SQLAlchemy()


def create_app():
    """Create and configure the app."""
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)

    register_error_handlers(app)

    # Register blueprints
    app.register_blueprint(create_home_blueprint())

    return app
