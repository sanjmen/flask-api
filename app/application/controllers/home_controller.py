"""Home controller module."""

from flask import Blueprint, jsonify


def create_home_blueprint() -> Blueprint:
    """
    Create and configure the home blueprint.

    Returns:
        Blueprint: Flask Blueprint for home routes
    """
    bp = Blueprint("home", __name__)

    @bp.route("/", methods=["GET"])
    def home():
        """
        Welcome endpoint.

        Returns:
            JSON response with welcome message
        """
        return jsonify({"message": "Welcome to the Popular Movies API!"}), 200

    return bp
