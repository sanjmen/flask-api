"""Mock movie service for testing."""

from ..test_data.movie_data import MOCK_MOVIE_DETAILS


class MockMovieService:
    """Mock implementation of movie service for testing."""

    def get_movie_details(self, movie_id: str) -> dict:
        """Get mock movie details."""
        # Convert to string for IMDB-style IDs
        movie_id = str(movie_id)

        if movie_id.startswith("tt"):
            # Return mock data for IMDB IDs
            if movie_id in MOCK_MOVIE_DETAILS:
                return MOCK_MOVIE_DETAILS[movie_id]
            return MOCK_MOVIE_DETAILS["tt0111161"]  # Default to Shawshank

        # For non-IMDB IDs (e.g., TMDB), return a generic response
        return {
            "id": movie_id,
            "title": f"Movie {movie_id}",
            "release_date": "2024-01-01",
            "overview": "A generic movie description...",
            "vote_average": 7.5,
        }
