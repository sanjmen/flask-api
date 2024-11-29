import json
from http import HTTPStatus

import pytest

from app import create_app
from app.application.services.favorites_service import FavoritesService


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


def test_add_favorite(client):
    """Test adding a movie to favorites."""
    # Clear favorites before test
    FavoritesService._favorites.clear()

    # Test invalid request (missing movie_id)
    response = client.post("/api/movies/favorites", json={})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = json.loads(response.data)
    assert data["error"]["code"] == "INVALID_REQUEST"

    # Test adding a movie
    response = client.post("/api/movies/favorites", json={"movie_id": 123})
    assert response.status_code == HTTPStatus.CREATED
    data = json.loads(response.data)
    assert data["movie_id"] == "123"
    assert "created_at" in data
    assert data["id"] == 1

    # Test adding the same movie again
    response = client.post("/api/movies/favorites", json={"movie_id": 123})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = json.loads(response.data)
    assert data["error"]["code"] == "ALREADY_EXISTS"


def test_get_favorites(client):
    """Test getting all favorites."""
    # Clear favorites and add some test data
    FavoritesService._favorites.clear()
    FavoritesService.add_favorite("123")
    FavoritesService.add_favorite("456")

    response = client.get("/api/movies/favorites")
    assert response.status_code == HTTPStatus.OK
    data = json.loads(response.data)
    assert "favorites" in data
    assert len(data["favorites"]) == 2
    assert all("id" in f and "movie_id" in f and "created_at" in f for f in data["favorites"])


def test_remove_favorite(client):
    """Test removing a movie from favorites."""
    # Clear favorites and add test data
    FavoritesService._favorites.clear()
    FavoritesService.add_favorite("123")

    # Test removing with invalid id
    response = client.delete("/api/movies/favorites/999")
    assert response.status_code == HTTPStatus.NOT_FOUND

    # Test removing with valid id
    response = client.delete("/api/movies/favorites/1")
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert len(FavoritesService.get_favorites()) == 0

    # Test removing already removed favorite
    response = client.delete("/api/movies/favorites/1")
    assert response.status_code == HTTPStatus.NOT_FOUND
