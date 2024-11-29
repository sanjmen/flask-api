"""Test configuration and fixtures."""

import pytest
from dotenv import load_dotenv

load_dotenv()


def pytest_addoption(parser):
    """Add custom pytest command line options."""
    parser.addoption("--integration", action="store_true", default=False, help="run integration tests")


def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "integration: mark test as integration test")


def pytest_collection_modifyitems(config, items):
    """Skip integration tests unless --integration option is used."""
    if not config.getoption("--integration"):
        skip_integration = pytest.mark.skip(reason="need --integration option to run")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    from app import create_app

    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    return app


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def mock_tmdb_response(mocker):
    """Mock TMDB API responses for integration tests."""

    def _mock_response(endpoint, response_data, status=200):

        def mock_get(*args, **kwargs):
            mock_resp = mocker.Mock()
            mock_resp.status_code = status
            mock_resp.json.return_value = response_data
            return mock_resp

        mocker.patch("requests.get", side_effect=mock_get)

    return _mock_response
