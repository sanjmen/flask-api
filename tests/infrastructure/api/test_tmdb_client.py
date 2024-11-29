"""Tests for TheMovieDB API client."""

import pytest
import responses
from requests.exceptions import ConnectionError, Timeout

from app.domain.exceptions import MovieAPIConnectionError, MovieAPIResponseError
from app.infrastructure.api.tmdb_client import TMDBClient


@pytest.fixture
def client():
    """Create a TMDBClient instance for testing."""
    return TMDBClient(api_key="test_key")


@responses.activate
def test_get_makes_request_with_api_key(client):
    """Test that _get method includes API key in request."""
    responses.add(
        responses.GET,
        "https://api.themoviedb.org/3/test",
        json={"success": True},
        status=200,
    )

    response = client._get("/test")

    assert response == {"success": True}
    assert len(responses.calls) == 1
    assert "api_key=test_key" in responses.calls[0].request.url


@responses.activate
def test_get_retries_on_timeout(client, mocker):
    """Test that _get retries on timeout."""
    mocker.patch("time.sleep")  # Don't actually sleep in tests

    # First call times out, second succeeds
    responses.add(responses.GET, "https://api.themoviedb.org/3/test", body=Timeout("Connection timed out"))
    responses.add(
        responses.GET,
        "https://api.themoviedb.org/3/test",
        json={"success": True},
        status=200,
    )

    response = client._get("/test")

    assert response == {"success": True}
    assert len(responses.calls) == 2


@responses.activate
def test_get_retries_on_connection_error(client, mocker):
    """Test that _get retries on connection error."""
    mocker.patch("time.sleep")

    # First call fails with connection error, second succeeds
    responses.add(
        responses.GET, "https://api.themoviedb.org/3/test", body=ConnectionError("Connection refused")
    )
    responses.add(
        responses.GET,
        "https://api.themoviedb.org/3/test",
        json={"success": True},
        status=200,
    )

    response = client._get("/test")

    assert response == {"success": True}
    assert len(responses.calls) == 2


@responses.activate
def test_get_retries_on_500_error(client, mocker):
    """Test that _get retries on 500 error."""
    mocker.patch("time.sleep")

    # First call returns 500, second succeeds
    responses.add(
        responses.GET,
        "https://api.themoviedb.org/3/test",
        json={"error": "Server error"},
        status=500,
    )
    responses.add(
        responses.GET,
        "https://api.themoviedb.org/3/test",
        json={"success": True},
        status=200,
    )

    response = client._get("/test")

    assert response == {"success": True}
    assert len(responses.calls) == 2


@responses.activate
def test_get_raises_error_after_max_retries(client, mocker):
    """Test that _get raises error after max retries."""
    mocker.patch("time.sleep")

    # All calls timeout
    for _ in range(TMDBClient.MAX_RETRIES):
        responses.add(
            responses.GET, "https://api.themoviedb.org/3/test", body=Timeout("Connection timed out")
        )

    with pytest.raises(MovieAPIConnectionError, match="Timeout connecting to TheMovieDB API"):
        client._get("/test")

    assert len(responses.calls) == TMDBClient.MAX_RETRIES


@responses.activate
def test_get_includes_error_message_from_api(client):
    """Test that _get includes API error message in exception."""
    responses.add(
        responses.GET,
        "https://api.themoviedb.org/3/test",
        json={"status_message": "Invalid API key"},
        status=401,
    )

    with pytest.raises(MovieAPIResponseError, match="Invalid API key"):
        client._get("/test")
