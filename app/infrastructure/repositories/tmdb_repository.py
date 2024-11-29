"""TheMovieDB repository implementation."""

from typing import Dict, List

from app.domain.ports.movie_repository import MovieRepository
from app.infrastructure.api.tmdb_client import TMDBClient


class TMDBRepository(MovieRepository):
    """Adapter for TheMovieDB API."""

    def __init__(self, client: TMDBClient = None):
        """Initialize repository with TMDBClient."""
        self.client = client or TMDBClient()

    def get_popular(self, page: int = 1) -> List[Dict]:
        """Get popular movies from TheMovieDB.

        Args:
            page: Page number for pagination

        Returns:
            List of movie dictionaries
        """
        response = self.client._get("/movie/popular", params={"page": page})
        return response.get("results", [])
