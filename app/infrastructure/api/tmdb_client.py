"""TheMovieDB API client implementation."""

import time
from typing import Dict, Optional

import requests
from requests.exceptions import ConnectionError, RequestException, Timeout

from app.config import Config
from app.domain.exceptions import MovieAPIConnectionError, MovieAPIResponseError


class TMDBClient:
    """HTTP client for TheMovieDB API."""

    BASE_URL = "https://api.themoviedb.org/3"
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds

    def __init__(self, api_key: str = None):
        """Initialize the client with API key."""
        self.api_key = api_key or Config.TMDB_API_KEY
        if not self.api_key:
            raise ValueError("TMDB_API_KEY is required")

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make a GET request to TheMovieDB API with retries.

        Args:
            endpoint: API endpoint (e.g., /movie/popular)
            params: Optional query parameters

        Returns:
            JSON response from the API

        Raises:
            MovieAPIConnectionError: If there are connection issues
            MovieAPIResponseError: If the API returns an error response
        """
        url = f"{self.BASE_URL}{endpoint}"
        params = params or {}
        params["api_key"] = self.api_key

        for attempt in range(self.MAX_RETRIES):
            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                return response.json()

            except Timeout:
                if attempt == self.MAX_RETRIES - 1:
                    raise MovieAPIConnectionError("Timeout connecting to TheMovieDB API")
                time.sleep(self.RETRY_DELAY)

            except ConnectionError:
                if attempt == self.MAX_RETRIES - 1:
                    raise MovieAPIConnectionError("Failed to connect to TheMovieDB API")
                time.sleep(self.RETRY_DELAY)

            except requests.HTTPError as e:
                if e.response.status_code >= 500 and attempt < self.MAX_RETRIES - 1:
                    time.sleep(self.RETRY_DELAY)
                    continue

                error_msg = f"TheMovieDB API error: {e.response.status_code}"
                try:
                    error_data = e.response.json()
                    if "status_message" in error_data:
                        error_msg = f"{error_msg} - {error_data['status_message']}"
                except ValueError:
                    pass

                raise MovieAPIResponseError(error_msg)

            except RequestException as e:
                if attempt == self.MAX_RETRIES - 1:
                    raise MovieAPIConnectionError(f"Request failed: {str(e)}")
                time.sleep(self.RETRY_DELAY)
