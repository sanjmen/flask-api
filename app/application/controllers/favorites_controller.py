from datetime import datetime, timezone
from http import HTTPStatus

from flask import Blueprint, jsonify, request

from ..services.favorites_service import FavoritesService

favorites_bp = Blueprint("favorites", __name__, url_prefix="/api/movies")


@favorites_bp.route("/favorites", methods=["GET"])
def get_favorites():
    """Get all favorites"""
    favorites = FavoritesService.get_favorites()
    return (
        jsonify(
            {
                "favorites": [
                    {
                        "id": idx + 1,  # Using index as temporary id
                        "movie_id": movie_id,
                        "created_at": datetime.now(timezone.utc).isoformat(),
                    }
                    for idx, movie_id in enumerate(favorites)
                ]
            }
        ),
        HTTPStatus.OK,
    )


@favorites_bp.route("/favorites", methods=["POST"])
def add_favorite():
    """Add a movie to favorites"""
    data = request.get_json()
    if not data or "movie_id" not in data:
        return (
            jsonify({"error": {"code": "INVALID_REQUEST", "message": "movie_id is required"}}),
            HTTPStatus.BAD_REQUEST,
        )

    movie_id = str(data["movie_id"])
    if FavoritesService.add_favorite(movie_id):
        response = {
            "id": len(FavoritesService.get_favorites()),  # Temporary id
            "movie_id": movie_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        return jsonify(response), HTTPStatus.CREATED

    return (
        jsonify({"error": {"code": "ALREADY_EXISTS", "message": "Movie already in favorites"}}),
        HTTPStatus.BAD_REQUEST,
    )


@favorites_bp.route("/favorites/<int:id>", methods=["DELETE"])
def remove_favorite(id: int):
    """Remove a movie from favorites"""
    favorites = FavoritesService.get_favorites()
    if id <= 0 or id > len(favorites):
        return (
            jsonify({"error": {"code": "NOT_FOUND", "message": "Favorite not found"}}),
            HTTPStatus.NOT_FOUND,
        )

    movie_id = list(favorites)[id - 1]  # Convert to list to get by index
    if FavoritesService.remove_favorite(movie_id):
        return "", HTTPStatus.NO_CONTENT

    return jsonify({"error": {"code": "NOT_FOUND", "message": "Favorite not found"}}), HTTPStatus.NOT_FOUND
