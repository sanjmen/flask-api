"""Unit tests for movie service."""

import pytest

from app.application.services.movie_service import MovieService


@pytest.fixture
def mock_repository(mocker):
    """Create a mock repository."""
    return mocker.Mock()


@pytest.fixture
def service(mock_repository):
    """Create a MovieService instance with a mock repository."""
    return MovieService(mock_repository)


def test_get_popular_movies_returns_movies_with_page(service, mock_repository):
    """Test that get_popular_movies returns movies with page number."""
    expected_movies = [{"id": 1, "title": "Test Movie"}]
    mock_repository.get_popular.return_value = expected_movies

    result = service.get_popular_movies(page=1)

    assert result == {"movies": expected_movies, "page": 1}
    mock_repository.get_popular.assert_called_once_with(page=1)


def test_get_popular_movies_uses_default_page(service, mock_repository):
    """Test that get_popular_movies uses default page 1."""
    mock_repository.get_popular.return_value = []

    service.get_popular_movies()

    mock_repository.get_popular.assert_called_once_with(page=1)
