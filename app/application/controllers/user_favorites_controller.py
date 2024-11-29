from http import HTTPStatus

from flask import Blueprint, current_app, g, jsonify, request

from ..services.favorites_service import FavoritesService

user_favorites_bp = Blueprint("user_favorites", __name__, url_prefix="/api")

_service_initialized = False


@user_favorites_bp.before_app_request
def initialize_service():
    """Initialize FavoritesService with MovieService dependency"""
    global _service_initialized
    if not _service_initialized and not hasattr(g, "favorites_service_initialized"):
        FavoritesService.initialize(current_app.movie_service)
        g.favorites_service_initialized = True
        _service_initialized = True


@user_favorites_bp.route("/users/<int:user_id>/favorites", methods=["GET"])
def get_user_favorites(user_id: int):
    """Get all favorites for a specific user"""
    try:
        favorites = FavoritesService.get_user_favorites(user_id)
        return jsonify({"favorites": favorites}), HTTPStatus.OK
    except RuntimeError as e:
        return (
            jsonify({"error": {"code": "SERVICE_ERROR", "message": str(e)}}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
    except Exception as e:
        return (
            jsonify({"error": {"code": "INTERNAL_ERROR", "message": f"An unexpected error occurred: {e}"}}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@user_favorites_bp.route("/users/<int:user_id>/favorites", methods=["POST"])
def add_user_favorite(user_id: int):
    """Add a movie to user's favorites"""
    data = request.get_json()
    if not data or "movie_id" not in data:
        return (
            jsonify({"error": {"code": "INVALID_REQUEST", "message": "movie_id is required"}}),
            HTTPStatus.BAD_REQUEST,
        )

    movie_id = str(data["movie_id"])
    favorite = FavoritesService.add_user_favorite(user_id, movie_id)

    if favorite:
        return (
            jsonify(
                {
                    "id": favorite.id,
                    "movie_id": favorite.movie_id,
                    "created_at": favorite.created_at.isoformat(),
                }
            ),
            HTTPStatus.CREATED,
        )

    return (
        jsonify({"error": {"code": "ALREADY_EXISTS", "message": "Movie already in favorites"}}),
        HTTPStatus.BAD_REQUEST,
    )


@user_favorites_bp.route("/users/<int:user_id>/favorites/<int:favorite_id>", methods=["DELETE"])
def remove_user_favorite(user_id: int, favorite_id: int):
    """Remove a specific favorite from user's favorites"""
    if FavoritesService.remove_user_favorite(user_id, favorite_id):
        return "", HTTPStatus.NO_CONTENT

    return jsonify({"error": {"code": "NOT_FOUND", "message": "Favorite not found"}}), HTTPStatus.NOT_FOUND


@user_favorites_bp.route("/admin/users/<int:user_id>/favorites", methods=["DELETE"])
def admin_remove_user_favorites(user_id: int):
    """Admin endpoint to remove all favorites for a user"""
    FavoritesService.remove_all_user_favorites(user_id)
    return "", HTTPStatus.NO_CONTENT
