"""Movie repository interface definition."""

from abc import ABC, abstractmethod
from typing import Dict, List


class MovieRepository(ABC):
    """Port for movie data access."""

    @abstractmethod
    def get_popular(self, page: int = 1) -> List[Dict]:
        """Get popular movies.

        Args:
            page: Page number for pagination

        Returns:
            List of movie dictionaries
        """
        pass

    @abstractmethod
    def get_movie_details(self, movie_id: int) -> Dict:
        """Get detailed information for a specific movie.

        Args:
            movie_id: The ID of the movie to retrieve

        Returns:
            Dictionary containing movie details
        """
        pass
