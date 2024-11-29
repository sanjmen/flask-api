"""Movie endpoints controller."""

from flask import Blueprint, jsonify, request

from app.application.services.movie_service import MovieService
from app.infrastructure.repositories.tmdb_repository import TMDBRepository


def create_movie_blueprint() -> Blueprint:
    """Create blueprint for movie-related endpoints."""
    blueprint = Blueprint("movies", __name__, url_prefix="/api/movies")
    movie_service = MovieService(TMDBRepository())

    @blueprint.route("/popular", methods=["GET"])
    def get_popular_movies():
        """Get popular movies endpoint."""
        try:
            page = int(request.args.get("page", 1))
            if page < 1:
                return jsonify({"error": "Page number must be positive"}), 400

            result = movie_service.get_popular_movies(page=page)
            return jsonify(result)

        except ValueError:
            return jsonify({"error": "Invalid page number"}), 400

    return blueprint
