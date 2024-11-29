"""Tests for TheMovieDB repository."""

import pytest

from app.infrastructure.repositories.tmdb_repository import TMDBRepository


@pytest.fixture
def mock_client(mocker):
    """Create a mock TMDBClient."""
    return mocker.Mock()


@pytest.fixture
def repository(mock_client):
    """Create a TMDBRepository with a mock client."""
    return TMDBRepository(client=mock_client)


def test_get_popular_calls_client_with_correct_params(repository, mock_client):
    """Test that get_popular calls the client with correct parameters."""
    mock_client._get.return_value = {"results": []}

    repository.get_popular(page=2)

    mock_client._get.assert_called_once_with("/movie/popular", params={"page": 2})


def test_get_popular_returns_results_from_response(repository, mock_client):
    """Test that get_popular returns the results from the response."""
    expected_movies = [{"id": 1, "title": "Test Movie"}]
    mock_client._get.return_value = {"results": expected_movies}

    movies = repository.get_popular()

    assert movies == expected_movies


def test_get_popular_returns_empty_list_when_no_results(repository, mock_client):
    """Test that get_popular returns empty list when no results in response."""
    mock_client._get.return_value = {}

    movies = repository.get_popular()

    assert movies == []
