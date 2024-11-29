"""Integration tests for home endpoint."""


def test_home_endpoint_integration(client):
    """Test home endpoint integration."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.content_type == "application/json"

    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Welcome to the Popular Movies API!"


def test_home_endpoint_method_not_allowed(client):
    """Test home endpoint returns 405 for non-GET methods."""
    methods = ["POST", "PUT", "DELETE", "PATCH"]

    for method in methods:
        response = client.open("/", method=method)
        assert response.status_code == 405
        assert response.content_type == "application/json"

        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Method not allowed"
