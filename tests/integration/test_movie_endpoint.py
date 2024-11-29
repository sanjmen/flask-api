"""Integration tests for movie endpoints."""

import pytest


@pytest.mark.integration
def test_get_popular_movies_endpoint(client):
    """Test getting popular movies through the API."""
    response = client.get("/api/movies/popular")

    assert response.status_code == 200
    assert response.content_type == "application/json"

    data = response.get_json()
    assert "movies" in data
    assert "page" in data
    assert isinstance(data["movies"], list)
    assert data["page"] == 1


@pytest.mark.integration
def test_get_popular_movies_with_pagination(client):
    """Test pagination in popular movies endpoint."""
    # Get first page
    response1 = client.get("/api/movies/popular?page=1")
    assert response1.status_code == 200
    data1 = response1.get_json()

    # Get second page
    response2 = client.get("/api/movies/popular?page=2")
    assert response2.status_code == 200
    data2 = response2.get_json()

    # Verify different pages return different movies
    assert data1["movies"] != data2["movies"]
    assert data1["page"] == 1
    assert data2["page"] == 2


@pytest.mark.integration
def test_get_popular_movies_invalid_page(client):
    """Test error handling for invalid page parameter."""
    test_cases = [
        ("0", "Page number must be positive"),
        ("-1", "Page number must be positive"),
        ("abc", "Invalid page number"),
    ]

    for page, expected_error in test_cases:
        response = client.get(f"/api/movies/popular?page={page}")
        assert response.status_code == 400
        assert response.content_type == "application/json"

        data = response.get_json()
        assert "error" in data
        assert data["error"] == expected_error
