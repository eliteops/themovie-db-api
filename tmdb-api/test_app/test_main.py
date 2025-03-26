import pytest
import httpx 
import pytest_asyncio
from app.main import app
from dotenv import load_dotenv
import os
from test_db import engine, sessionlocal, get_db, Base

# Load test environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Set testing environment
os.environ["TESTING"] = "true"

# Create the test database tables
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

# Override the database dependency for testing
app.dependency_overrides[get_db] = override_get_db

# Fixture for the async client
@pytest_asyncio.fixture()
async def client():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

# Test cases
@pytest.mark.asyncio
async def test_create_movie(client):
    movie_data = {"title": "Inception", "year": 2010, "genre": "sci-fi", "imdb_rating": 8.1}
    response = await client.post("/create_movie/", json=movie_data)
    print(response.content)
    assert response.status_code == 200
    assert response.json()["title"] == "Inception"
    assert response.json()["year"] == 2010

'''-------------------------------------------------------------------------------------------------'''

@pytest.mark.asyncio
async def test_read_movies(client):
    # Create a movie first
    movie_data = {"title": "Interstellar", "year": 2014, "genre": "sci-fi", "imdb_rating": 8.1}
    response = await client.post("/create_movie/", json=movie_data)
        # Test reading movies
    response = await client.get("/read_movies/")
    assert response.status_code == 200
    print(response.json())
    assert len(response.json()) > 0

'''---------------------------------------------------------------------------------------------------'''
@pytest.mark.asyncio
async def test_read_specific_movie(client):
    # Create a movie first
    movie_data = {"title": "The Dark Knight", "year": 2008, "genre": "sci-fi", "imdb_rating": 7.1}
    create_response = await client.post("/create_movie/", json=movie_data)
    movie_id = create_response.json()["id"]

    # Test reading the specific movie
    response = await client.get(f"/read_specific_movie/{movie_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "The Dark Knight"
    assert response.json()["year"] == 2008
    assert response.json()["genre"] == "sci-fi"
    assert response.json()["imdb_rating"] == 7.1

@pytest.mark.asyncio
async def test_update_movie(client):
    # Create a movie first
    movie_data = {"title": "The Matrix", "year": 1999, "genre": "sci-fi", "imdb_rating": 8.7}
    create_response = await client.post("/create_movie/", json=movie_data)
    movie_id = create_response.json()["id"]

    # Update the movie
    updated_movie_data = {"title": "The Matrix Reloaded", "year": 2003, "genre": "sci-fi", "imdb_rating": 7.2}
    response = await client.put(f"/update_movie/{movie_id}", json=updated_movie_data)
    assert response.status_code == 200
    assert response.json()["title"] == "The Matrix Reloaded"
    assert response.json()["year"] == 2003
    assert response.json()["imdb_rating"] == 7.2


@pytest.mark.asyncio
async def test_delete_movie(client):
    # Create a movie first
    movie_data = {"title": "Avatar", "year": 2009, "genre": "sci-fi", "imdb_rating": 7.8}
    create_response = await client.post("/create_movie/", json=movie_data)
    movie_id = create_response.json()["id"]

    # Delete the movie
    response = await client.delete(f"/delete_movie/{movie_id}")
    assert response.status_code == 200
    assert response.json()["id"] == movie_id
    assert response.json()["message"] == f"movie id {movie_id} deleted successfully."

    # Verify the movie is deleted
    response = await client.get(f"/read_specific_movie/{movie_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"
