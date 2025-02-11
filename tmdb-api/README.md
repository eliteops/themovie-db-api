# tmdb-api/tmdb-api/README.md

# TMDB-like API

This project is a simple API that mimics the functionality of The Movie Database (TMDB) using Flask and SQLite as the database.

## Project Structure

```
tmdb-api
├── src
│   ├── main.py               # Entry point of the application
│   ├── controllers           # Contains request handling logic
│   ├── models                # Defines data models
│   ├── routes                # API route definitions
│   ├── services              # Business logic and data processing
│   └── database.py           # Database connection and setup
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd tmdb-api
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python src/main.py
   ```

## API Usage

- **Get all movies**: `GET /api/movies`
- **Get movie by ID**: `GET /api/movies/<id>`

## Examples

### Get All Movies

```
GET /api/movies
Response:
[
    {
        "id": 1,
        "title": "Movie Title",
        "genre": "Action"
    },
    ...
]
```

### Get Movie by ID

```
GET /api/movies/1
Response:
{
    "id": 1,
    "title": "Movie Title",
    "genre": "Action",
    "description": "Movie description here."
}
```

## License

This project is licensed under the MIT License.