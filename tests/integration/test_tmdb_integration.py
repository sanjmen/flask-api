"""Integration tests for TheMovieDB API integration."""

import os

import pytest

from app.domain.exceptions import MovieAPIResponseError
from app.infrastructure.api.tmdb_client import TMDBClient
from app.infrastructure.repositories.tmdb_repository import TMDBRepository


@pytest.fixture
def tmdb_client():
    """Create TMDBClient with API key from environment."""
    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        pytest.skip("TMDB_API_KEY environment variable not set")
    return TMDBClient(api_key=api_key)


@pytest.fixture
def tmdb_repository(tmdb_client):
    """Create TMDBRepository with the test client."""
    return TMDBRepository(client=tmdb_client)


@pytest.mark.integration
def test_get_popular_movies_integration(tmdb_repository):
    """Test getting popular movies from TheMovieDB API."""
    movies = tmdb_repository.get_popular(page=1)

    assert isinstance(movies, list)
    assert len(movies) > 0

    movie = movies[0]
    assert isinstance(movie, dict)
    assert "id" in movie
    assert "title" in movie
    assert "overview" in movie
    assert "release_date" in movie
    assert "popularity" in movie
    assert "vote_average" in movie


@pytest.mark.integration
def test_get_popular_movies_pagination(tmdb_repository):
    """Test pagination of popular movies."""
    page1_movies = tmdb_repository.get_popular(page=1)
    page2_movies = tmdb_repository.get_popular(page=2)

    # Check that we got movies in both pages
    assert len(page1_movies) > 0
    assert len(page2_movies) > 0

    # Check that pages are not identical
    assert page1_movies != page2_movies

    # Check that most movies are different between pages
    # Some overlap is possible due to movie popularity changes
    page1_ids = {movie["id"] for movie in page1_movies}
    page2_ids = {movie["id"] for movie in page2_movies}
    intersection = page1_ids.intersection(page2_ids)

    # Allow for some overlap (no more than 20% of movies)
    max_allowed_overlap = len(page1_movies) * 0.2
    assert (
        len(intersection) <= max_allowed_overlap
    ), f"Too many movies appear in both pages: {len(intersection)} movies"


@pytest.mark.integration
def test_invalid_api_key_handling(tmdb_repository):
    """Test handling of invalid API key."""
    invalid_client = TMDBClient(api_key="invalid_key")
    invalid_repository = TMDBRepository(client=invalid_client)

    with pytest.raises(MovieAPIResponseError) as exc_info:
        invalid_repository.get_popular()

    assert "Invalid API key" in str(exc_info.value)


@pytest.mark.integration
def test_invalid_page_handling(tmdb_repository):
    """Test handling of invalid page number."""
    with pytest.raises(MovieAPIResponseError) as exc_info:
        tmdb_repository.get_popular(page=1000000)

    error_message = str(exc_info.value)
    assert "page" in error_message.lower()
