"""Flask application factory."""

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.application.controllers.home_controller import create_home_blueprint
from app.application.controllers.movie_controller import create_movie_blueprint
from app.application.services.movie_service import MovieService
from app.infrastructure.api.error_handlers import register_error_handlers
from app.infrastructure.repositories.tmdb_repository import TMDBRepository

load_dotenv()

db = SQLAlchemy()


def create_app():
    """Create and configure the app."""
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)

    register_error_handlers(app)

    # Register blueprints
    app.register_blueprint(create_home_blueprint())

    # Create and register movie service
    movie_repository = TMDBRepository()
    app.movie_service = MovieService(movie_repository=movie_repository)
    app.register_blueprint(create_movie_blueprint(), url_prefix="/api/movies")

    return app
