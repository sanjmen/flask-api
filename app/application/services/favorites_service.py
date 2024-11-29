from typing import List, Set


class FavoritesService:
    _favorites: Set[str] = set()  # In-memory storage for favorites

    @classmethod
    def add_favorite(cls, movie_id: str) -> bool:
        """Add a movie to favorites"""
        if movie_id in cls._favorites:
            return False
        cls._favorites.add(movie_id)
        return True

    @classmethod
    def remove_favorite(cls, movie_id: str) -> bool:
        """Remove a movie from favorites"""
        if movie_id not in cls._favorites:
            return False
        cls._favorites.remove(movie_id)
        return True

    @classmethod
    def get_favorites(cls) -> List[str]:
        """Get all favorite movies"""
        return list(cls._favorites)

    @classmethod
    def is_favorite(cls, movie_id: str) -> bool:
        """Check if a movie is in favorites"""
        return movie_id in cls._favorites
