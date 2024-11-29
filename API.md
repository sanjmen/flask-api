# API Documentation

## Base URL
```
/api
```

## Authentication
All protected endpoints require Bearer token authentication in the Authorization header:
```
Authorization: Bearer <token>
```

Available tokens:
- Admin user (ID: 1): `abcdef1234567890`
- Consumer user (ID: 2): `1234567890`

## Endpoints

### Public Endpoints

#### Get Popular Movies
```http
GET /api/movies/popular
```

Query Parameters:
- `page` (optional): Page number for pagination

Response:
```json
{
    "page": 1,
    "total_pages": 500,
    "total_results": 10000,
    "results": [
        {
            "id": 123,
            "title": "Movie Title",
            "release_date": "2024-01-01",
            "overview": "Movie description",
            "popularity": 123.45,
            "vote_average": 7.8
        }
    ]
}
```

Notes:
- Cached for 30 seconds (configurable via CACHE_DURATION_SECONDS env var)
- Implements retry and exponential backoff on external API failures
- Falls back to cached data on IOError
- All external API errors are logged to stderr

### Protected Endpoints

#### Add Movie to Favorites
```http
POST /api/users/{user_id}/favorites
```
Authentication: Required (Bearer token)

Request Body:
```json
{
    "movie_id": 123
}
```

Response (201 Created):
```json
{
    "id": 456,
    "movie_id": 123,
    "created_at": "2024-01-01T12:00:00Z"
}
```

#### Remove Movie from Favorites
```http
DELETE /api/users/{user_id}/favorites/{id}
```
Authentication: Required (Bearer token)

Response (204 No Content)

#### Get User's Favorite Movies
```http
GET /api/users/{user_id}/favorites
```
Authentication: Required (Bearer token)

Query Parameters:
- `sort`: Sort criteria (optional)
  * `release_date` (default): Sort by movie release date
  * `rating`: Sort by user rating
- `order`: Sort order (optional)
  * `desc` (default): Descending order
  * `asc`: Ascending order

Response:
```json
{
    "favorites": [
        {
            "id": 456,
            "movie_id": 123,
            "title": "Movie Title",
            "release_date": "2024-01-01",
            "overview": "Movie description",
            "popularity": 123.45,
            "vote_average": 7.8,
            "user_rating": 4,
            "created_at": "2024-01-01T12:00:00Z"
        }
    ]
}
```

Notes:
- Returns complete movie details from TheMovieDB
- Includes user's rating if available
- Cached for 30 seconds (configurable)
- Falls back to cached data on external API errors

#### Rate a Movie
```http
POST /api/movies/ratings
```
Authentication: Required (Bearer token)

Request Body:
```json
{
    "movie_id": 123,
    "rating": 4
}
```

Validation:
- Rating must be between 0 and 5 (inclusive)
- Movie must exist in TheMovieDB

Response (201 Created):
```json
{
    "id": 789,
    "movie_id": 123,
    "rating": 4,
    "created_at": "2024-01-01T12:00:00Z"
}
```

#### Update Movie Rating
```http
PUT /api/movies/ratings/{id}
```
Authentication: Required (Bearer token)

Request Body:
```json
{
    "rating": 5
}
```

Validation:
- Rating must be between 0 and 5 (inclusive)
- Rating must exist and belong to the authenticated user

Response (200 OK):
```json
{
    "id": 789,
    "movie_id": 123,
    "rating": 5,
    "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Delete All User Favorites (Admin Only)
```http
DELETE /api/admin/users/{userId}/favorites
```
Authentication: Required (Admin token only)

Response (204 No Content)

## Error Responses

All endpoints return errors in the following format:
```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human readable error message",
        "details": {} // Optional additional information
    }
}
```

Common Error Codes:
- `INVALID_TOKEN`: Missing or invalid authentication token
- `INSUFFICIENT_PERMISSIONS`: Valid token but insufficient permissions
- `INVALID_RATING`: Rating value out of range (0-5)
- `MOVIE_NOT_FOUND`: Movie ID not found in TheMovieDB
- `RATING_NOT_FOUND`: Rating ID not found or doesn't belong to user
- `EXTERNAL_API_ERROR`: Error communicating with TheMovieDB
- `VALIDATION_ERROR`: Request validation failed

HTTP Status Codes:
- 200: Success
- 201: Created
- 204: No Content
- 400: Bad Request (validation errors)
- 401: Unauthorized (missing or invalid token)
- 403: Forbidden (insufficient permissions)
- 404: Not Found
- 500: Internal Server Error
- 503: Service Unavailable (external API unavailable)

## Resilience and Caching

### Caching
- All GET endpoints are cached in Redis
- Default cache duration: 30 seconds
- Configurable via environment variables:
  * `CACHE_DURATION_SECONDS`: Cache duration (default: 30)
  * `REDIS_URL`: Redis connection URL
  * `REDIS_PASSWORD`: Redis password (if required)

### External API Resilience
- Implements retry with exponential backoff:
  * Max retries: 3
  * Initial delay: 1 second
  * Max delay: 5 seconds
  * Exponential multiplier: 2
- Falls back to cached data on failures
- All errors are logged to stderr with:
  * Error details
  * Request context
  * Stack trace
  * Retry attempt number
