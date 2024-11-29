import os


class Config:
    """Flask application configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:password@db:5432/movies_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask configuration
    TESTING = os.getenv("FLASK_ENV") == "test"
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"

    # Redis configuration
    REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
    CACHE_DURATION_SECONDS = int(os.getenv("CACHE_DURATION_SECONDS", "30"))

    # TheMovieDB configuration
    TMDB_API_KEY = os.getenv("TMDB_API_KEY")
