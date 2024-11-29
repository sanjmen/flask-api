"""Movie endpoints controller."""

from flask import Blueprint, current_app, jsonify, request

from app.domain.exceptions import TMDBError


def create_movie_blueprint():
    """Create blueprint for movie endpoints."""
    blueprint = Blueprint("movies", __name__)

    @blueprint.route("/popular", methods=["GET"])
    def get_popular_movies():
        """Get popular movies with pagination."""
        try:
            page = request.args.get("page", 1)
            try:
                page = int(page)
                if page < 1:
                    return jsonify({"error": "Page number must be positive"}), 400
            except ValueError:
                return jsonify({"error": "Invalid page number"}), 400

            movie_service = current_app.movie_service
            movies = movie_service.get_popular_movies(page=page)
            return jsonify(movies)
        except TMDBError as e:
            current_app.logger.error(f"Error getting popular movies: {str(e)}")
            return jsonify({"error": str(e)}), 500
        except Exception as e:
            current_app.logger.error(f"Unexpected error getting popular movies: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

    @blueprint.route("/<int:movie_id>", methods=["GET"])
    def get_movie_details(movie_id: int):
        """Get detailed information for a specific movie.

        Args:
            movie_id: The ID of the movie to retrieve

        Returns:
            JSON response with movie details
        """
        try:
            movie_service = current_app.movie_service
            movie = movie_service.get_movie_details(movie_id=movie_id)
            if movie is None:
                return jsonify({"error": "Movie not found"}), 404
            return jsonify(movie)
        except TMDBError as e:
            current_app.logger.error(f"Error getting movie details: {str(e)}")
            return jsonify({"error": str(e)}), 500
        except Exception as e:
            current_app.logger.error(f"Unexpected error getting movie details: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

    return blueprint
