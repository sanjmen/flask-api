# Movie API

A Flask-based RESTful API for managing movie information, integrating with TheMovieDB. Built with hexagonal architecture, this API allows users to browse popular movies, maintain favorites lists, and rate movies.

## Features

- Browse popular movies from TheMovieDB
- Rate movies (0-5 stars)
- Manage favorite movies list
- Token-based authentication
- Redis caching
- Resilient external API calls
- Comprehensive test coverage

## Tech Stack

- **Framework**: Flask
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis
- **External API**: TheMovieDB
- **Testing**: pytest
- **CI/CD**: GitHub Actions
- **Documentation**: OpenAPI/Swagger
- **Containerization**: Docker & Docker Compose

## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- TheMovieDB API Key

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/sanjmen/flask-api.git
cd flask-api
```

2. Copy the example environment file:
```bash
cp .env.example .env
```

3. Update the `.env` file with your configuration:
```env
# Flask configuration
FLASK_APP=app.main:app
FLASK_ENV=development
FLASK_DEBUG=1

# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=movies
DATABASE_URL=postgresql://postgres:password@db:5432/movies_db

# Redis
REDIS_URL=redis://redis:6379/0
CACHE_DURATION_SECONDS=30

# TheMovieDB
TMDB_API_KEY=your_api_key_here
```

4. Start the services with Docker Compose:
```bash
docker compose up --build
```

The API will be available at `http://localhost:5000/api`

## Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install pre-commit hooks:
```bash
pre-commit install
```

4. Run the tests:
```bash
pytest
```

## Project Structure

```
flask-api/
├── app/
│   ├── application/        # Application layer (controllers, DTOs)
│   ├── domain/            # Domain layer (entities, repositories interfaces)
│   └── infrastructure/    # Infrastructure layer (implementations)
├── tests/
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── docker/               # Docker configuration files
├── .github/              # GitHub Actions workflows
├── API.md               # API documentation
├── docker-compose.yml
└── requirements.txt
```

## Development Status

### 1. Initial Setup
- [x] Project Structure
  - [x] Hexagonal architecture setup
  - [x] Application layers (application, domain, infrastructure)
  - [x] Directory organization
  - [x] Basic Flask application structure
- [x] Development Environment
  - [x] Docker configuration
  - [x] Docker Compose setup
  - [x] Environment variables configuration
  - [x] Pre-commit hooks
- [x] Database Setup
  - [x] PostgreSQL configuration
  - [x] SQLAlchemy integration
  - [x] Basic database connection
- [x] CI/CD Pipeline
  - [x] GitHub Actions workflow
  - [x] Basic test automation
  - [x] Code quality checks
- [x] Documentation
  - [x] API documentation structure
  - [x] README with setup instructions
  - [x] Development roadmap
- [x] Testing Foundation
  - [x] pytest configuration
  - [x] Basic test structure
  - [x] First endpoint test

### 2. TheMovieDB Integration
- [x] HTTP client implementation
- [x] Adapter in hexagonal architecture
- [x] Error handling and retries
- [x] Integration tests

### 3. API Endpoints Implementation
- [x] GET /api/movies/popular
- [ ] GET /api/movies/{id}
- [ ] GET /api/movies/search
- [ ] Favorites Management
  - [ ] Database models and repositories
  - [ ] GET /api/movies/favorites
  - [ ] POST /api/movies/favorites
  - [ ] DELETE /api/movies/favorites/{id}
  - [ ] Admin endpoint for user favorites
- [ ] Movie Ratings
  - [ ] Database models and repositories
  - [ ] POST /api/movies/ratings
  - [ ] PUT /api/movies/ratings/{id}

### 4. Caching Implementation
- [ ] Redis configuration
- [ ] Cache middleware for GET endpoints
- [ ] Fallback mechanisms
- [ ] Cache tests

### 5. Authentication & Security
- [ ] Bearer token authentication
- [ ] Role-based access control
- [ ] Security tests

### 6. Final Steps
- [ ] Performance optimizations
- [ ] Complete CI/CD pipeline
- [ ] Production configuration
- [ ] OpenAPI specification
- [ ] Final documentation updates

## Testing

### Running Tests

Run unit tests:
```bash
pytest
```

Run integration tests:
```bash
pytest --integration
```

Note: Integration tests require a valid TMDB_API_KEY environment variable.

## API Documentation

See [API.md](API.md) for detailed endpoint documentation.

Quick endpoint overview:
- `GET /api/movies/popular` - Get popular movies
- `GET /api/movies/favorites` - Get user's favorite movies
- `POST /api/movies/favorites` - Add movie to favorites
- `DELETE /api/movies/favorites/{id}` - Remove movie from favorites
- `POST /api/movies/ratings` - Rate a movie
- `PUT /api/movies/ratings/{id}` - Update movie rating

## Authentication

The API uses Bearer token authentication. Available tokens:
- Admin: `abcdef1234567890`
- User: `1234567890`

Example:
```bash
curl -H "Authorization: Bearer abcdef1234567890" http://localhost:5000/api/movies/favorites
```

## Caching

- GET endpoints are cached in Redis for 30 seconds (configurable)
- Cache duration can be modified via `CACHE_DURATION_SECONDS` environment variable
- Failed external API calls fall back to cached data

## Error Handling

- All errors return a consistent JSON format
- External API calls implement retry with exponential backoff
- Detailed error logging to stderr
- See [API.md](API.md) for error codes and formats

## CI/CD

GitHub Actions workflows:
- Run tests
- Code quality checks
- Security scanning
- Docker image building

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
