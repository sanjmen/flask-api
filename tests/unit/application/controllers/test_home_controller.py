"""Unit tests for home controller."""

from flask import Flask

from app.application.controllers.home_controller import create_home_blueprint


def test_create_home_blueprint():
    """Test create_home_blueprint returns a Blueprint."""
    bp = create_home_blueprint()
    assert bp.name == "home"
    assert bp.url_prefix is None


def test_home_endpoint():
    """Test home endpoint returns correct response."""
    app = Flask(__name__)

    app.register_blueprint(create_home_blueprint())

    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.content_type == "application/json"

    data = response.get_json()
    assert data == {"message": "Welcome to the Popular Movies API!"}
