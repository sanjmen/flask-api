from http import HTTPStatus

import pytest

from app import create_app
from app.application.services.favorites_service import FavoritesService

from .mocks.mock_movie_service import MockMovieService


@pytest.fixture
def app():
    """Create and configure a test Flask application instance."""
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # Use MockMovieService for testing
    app.movie_service = MockMovieService()

    yield app


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture(autouse=True)
def clear_favorites(app):
    """Clear favorites before each test."""
    with app.app_context():
        FavoritesService._favorites.clear()
        FavoritesService._user_favorites.clear()
        FavoritesService._next_id = 1
        FavoritesService._movie_service = None
        FavoritesService.initialize(app.movie_service)


def test_get_user_favorites(client):
    """Test getting user favorites."""
    # Add a favorite first
    response = client.post("/api/users/1/favorites", json={"movie_id": "tt0111161"})
    assert response.status_code == HTTPStatus.CREATED

    # Get favorites
    response = client.get("/api/users/1/favorites")
    assert response.status_code == HTTPStatus.OK

    data = response.get_json()
    favorites = data["favorites"]
    assert len(favorites) == 1

    favorite = favorites[0]
    assert favorite["movie"]["id"] == "tt0111161"
    assert favorite["movie"]["title"] == "The Shawshank Redemption"
    assert "created_at" in favorite


def test_add_user_favorite(client):
    """Test adding a movie to user favorites."""
    response = client.post("/api/users/1/favorites", json={"movie_id": "tt0111161"})
    assert response.status_code == HTTPStatus.CREATED

    data = response.get_json()
    assert data["movie_id"] == "tt0111161"
    assert "created_at" in data


def test_add_user_favorite_invalid_request(client):
    """Test adding a favorite with invalid request data."""
    # Missing movie_id
    response = client.post("/api/users/1/favorites", json={})
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_remove_user_favorite(client):
    """Test removing a movie from user favorites."""
    # Add a favorite first
    response = client.post("/api/users/1/favorites", json={"movie_id": "tt0111161"})
    assert response.status_code == HTTPStatus.CREATED
    data = response.get_json()
    favorite_id = data["id"]

    # Remove the favorite
    response = client.delete(f"/api/users/1/favorites/{favorite_id}")
    assert response.status_code == HTTPStatus.NO_CONTENT

    # Verify it's gone
    response = client.get("/api/users/1/favorites")
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert len(data["favorites"]) == 0


def test_remove_nonexistent_favorite(client):
    """Test removing a favorite that doesn't exist."""
    response = client.delete("/api/users/1/favorites/999")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_admin_remove_user_favorites(client):
    """Test admin endpoint to remove all favorites for a user."""
    # Add some favorites first
    client.post("/api/users/1/favorites", json={"movie_id": "tt0111161"})
    client.post("/api/users/1/favorites", json={"movie_id": "tt0068646"})

    # Remove all favorites
    response = client.delete("/api/admin/users/1/favorites")
    assert response.status_code == HTTPStatus.NO_CONTENT

    # Verify they're gone
    response = client.get("/api/users/1/favorites")
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert len(data["favorites"]) == 0
