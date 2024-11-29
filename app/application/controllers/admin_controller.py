from http import HTTPStatus

from flask import Blueprint

from ..services.favorites_service import FavoritesService

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.route("/users/<int:user_id>/favorites", methods=["DELETE"])
def delete_user_favorites(user_id: int):
    """Delete all favorites for a specific user."""
    FavoritesService.remove_all_user_favorites(user_id)
    return "", HTTPStatus.NO_CONTENT
