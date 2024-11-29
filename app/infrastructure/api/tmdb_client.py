"""TheMovieDB API client."""

import time
from typing import Dict, Optional

import requests

from app.config import Config
from app.domain.exceptions import MovieAPIConnectionError, MovieAPIResponseError


class TMDBClient:
    """Client for TheMovieDB API."""

    BASE_URL = "https://api.themoviedb.org/3"
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds
    TIMEOUT = 10

    def __init__(self, api_key: str = None):
        """Initialize the client with API key."""
        self.api_key = api_key or Config.TMDB_API_KEY
        if not self.api_key:
            raise ValueError("TMDB_API_KEY is required")

    def _get(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make a GET request to TheMovieDB API.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            Response data as dictionary or None if resource not found

        Raises:
            MovieAPIConnectionError: If the API request fails due to connection issues
            MovieAPIResponseError: If the API request fails due to response errors
        """
        if params is None:
            params = {}

        params["api_key"] = self.api_key
        url = f"{self.BASE_URL}{endpoint}"

        for attempt in range(self.MAX_RETRIES):
            try:
                response = requests.get(url, params=params, timeout=self.TIMEOUT)

                if response.status_code == 404:
                    return None

                response.raise_for_status()
                return response.json()

            except requests.Timeout:
                if attempt == self.MAX_RETRIES - 1:
                    raise MovieAPIConnectionError("Timeout connecting to TheMovieDB API")
                time.sleep(self.RETRY_DELAY)

            except requests.ConnectionError:
                if attempt == self.MAX_RETRIES - 1:
                    raise MovieAPIConnectionError("Failed to connect to TheMovieDB API")
                time.sleep(self.RETRY_DELAY)

            except requests.HTTPError as e:
                if response.status_code >= 500:
                    if attempt == self.MAX_RETRIES - 1:
                        raise MovieAPIConnectionError(f"TheMovieDB API server error: {response.status_code}")
                    time.sleep(self.RETRY_DELAY)
                else:
                    error_message = response.json().get("status_message", str(e))
                    raise MovieAPIResponseError(error_message)

            except Exception as e:
                raise MovieAPIConnectionError(f"Unexpected error: {str(e)}")
