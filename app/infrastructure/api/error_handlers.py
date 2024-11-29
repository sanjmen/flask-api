"""HTTP error handlers for the Flask application."""

from flask import jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    """Register error handlers for the app."""

    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors."""
        app.logger.error("Resource Not Found: %s", str(error))
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed_error(error):
        """Handle 405 errors."""
        app.logger.error("Method Not Allowed: %s", str(error))
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 errors."""
        app.logger.error("Server Error: %s", str(error))
        return jsonify({"error": "Internal server error"}), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle all unhandled exceptions."""
        app.logger.error("Unhandled Exception: %s", str(error))
        if isinstance(error, HTTPException):
            return jsonify({"error": error.description}), error.code
        return jsonify({"error": "Internal server error"}), 500
