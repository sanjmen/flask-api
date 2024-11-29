"""Flask application factory."""

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.application.controllers.home_controller import create_home_blueprint
from app.application.controllers.movie_controller import create_movie_blueprint
from app.infrastructure.api.error_handlers import register_error_handlers

load_dotenv()

db = SQLAlchemy()


def create_app():
    """Create and configure the app."""
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)

    register_error_handlers(app)

    app.register_blueprint(create_home_blueprint())
    app.register_blueprint(create_movie_blueprint())

    return app
