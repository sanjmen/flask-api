"""Movie service implementation."""

from typing import Dict

from app.domain.ports.movie_repository import MovieRepository


class MovieService:
    """Service for movie-related operations."""

    def __init__(self, movie_repository: MovieRepository):
        """Initialize service with repository."""
        self._repository = movie_repository

    def get_popular_movies(self, page: int = 1) -> Dict:
        """Get popular movies with pagination.

        Args:
            page: Page number for pagination (default: 1)

        Returns:
            Dict containing:
                - movies: List of movie dictionaries
                - page: Current page number
        """
        movies = self._repository.get_popular(page=page)
        return {"movies": movies, "page": page}

    def get_movie_details(self, movie_id: int) -> Dict:
        """Get detailed information for a specific movie.

        Args:
            movie_id: The ID of the movie to retrieve

        Returns:
            Dictionary containing movie details
        """
        return self._repository.get_movie_details(movie_id=movie_id)
