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
