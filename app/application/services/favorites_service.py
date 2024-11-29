from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Set


@dataclass
class Favorite:
    id: int
    movie_id: str
    created_at: datetime


class FavoritesService:
    _favorites: Set[str] = set()  # In-memory storage for favorites
    _user_favorites: Dict[int, List[Favorite]] = {}  # User-specific favorites
    _next_id: int = 1
    _movie_service = None

    @classmethod
    def initialize(cls, movie_service):
        """Initialize the service with movie service dependency"""
        cls._movie_service = movie_service

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

    @classmethod
    def get_user_favorites(cls, user_id: int) -> List[Dict]:
        """Get all favorites for a specific user with movie details"""
        if not cls._movie_service:
            raise RuntimeError("Movie service not initialized")

        favorites = cls._user_favorites.get(user_id, [])
        result = []

        for favorite in favorites:
            try:
                movie_details = cls._movie_service.get_movie_details(favorite.movie_id)
                result.append(
                    {"id": favorite.id, "movie": movie_details, "created_at": favorite.created_at.isoformat()}
                )
            except Exception as e:
                # Log error but continue with next favorite
                print(f"Error fetching movie details for {favorite.movie_id}: {str(e)}")
                continue

        # Sort by release date
        return sorted(result, key=lambda x: x["movie"].get("release_date", ""), reverse=True)

    @classmethod
    def add_user_favorite(cls, user_id: int, movie_id: str) -> Favorite:
        """Add a movie to user's favorites"""
        if user_id not in cls._user_favorites:
            cls._user_favorites[user_id] = []

        # Check if movie is already in favorites
        if any(f.movie_id == movie_id for f in cls._user_favorites[user_id]):
            return None

        favorite = Favorite(id=cls._next_id, movie_id=movie_id, created_at=datetime.now(timezone.utc))
        cls._next_id += 1
        cls._user_favorites[user_id].append(favorite)
        return favorite

    @classmethod
    def remove_user_favorite(cls, user_id: int, favorite_id: int) -> bool:
        """Remove a specific favorite from user's favorites"""
        if user_id not in cls._user_favorites:
            return False

        favorites = cls._user_favorites[user_id]
        for i, favorite in enumerate(favorites):
            if favorite.id == favorite_id:
                favorites.pop(i)
                return True
        return False

    @classmethod
    def remove_all_user_favorites(cls, user_id: int) -> None:
        """Remove all favorites for a user"""
        if user_id in cls._user_favorites:
            cls._user_favorites[user_id] = []

    @classmethod
    def is_admin(cls, user_id: int) -> bool:
        """Check if a user is an admin"""
        # For simplicity, let's consider user_id=1 as admin
        return user_id == 1
