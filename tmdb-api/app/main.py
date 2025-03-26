from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .models import Movie
from .schemas import MovieCreate, MovieResponse, MovieDelete
from typing import List
import aioredis
import os
from fastapi.encoders import jsonable_encoder
import json

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Initialize Redis only if not in test mode
redis = None
if not os.getenv("TESTING"):
    try:
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        redis = aioredis.from_url(f"redis://{redis_host}:{redis_port}", decode_responses=True)
    except Exception as e:
        print(f"Redis connection failed: {e}")
        redis = None

@app.post("/create_movie/", response_model=MovieResponse)
async def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    print(movie.dict())
    db_movie = Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    if redis:
        try:
            movie_json = jsonable_encoder(db_movie)
            await redis.set(f"movie:{db_movie.id}", json.dumps(movie_json))
        except Exception as e:
            print(f"Redis operation failed: {e}")
    return MovieResponse(**db_movie.__dict__)

@app.get("/read_movies/", response_model=List[MovieResponse])
async def read_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    movies = db.query(Movie).offset(skip).limit(limit).all()
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found")
    return movies

@app.get("/read_specific_movie/{movie_id}", response_model=MovieResponse)
async def read_movie(movie_id: int, db: Session = Depends(get_db)):
    if redis:
        try:
            cached_movie = await redis.get(f"movie:{movie_id}")
            if cached_movie:
                return MovieResponse.parse_raw(cached_movie)
        except Exception as e:
            print(f"Redis operation failed: {e}")
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    if redis:
        try:
            movie_json = jsonable_encoder(movie)
            await redis.set(f"movie:{movie_id}", json.dumps(movie_json))
        except Exception as e:
            print(f"Redis operation failed: {e}")
    return movie

@app.put("/update_movie/{movie_id}", response_model=MovieResponse)
async def update_movie(movie_id: int, movie: MovieCreate, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    for key, value in movie.dict().items():
        setattr(db_movie, key, value)
    db.commit()
    db.refresh(db_movie)
    if redis:
        try:
            movie_json = jsonable_encoder(db_movie)
            await redis.set(f"movie:{db_movie.id}", json.dumps(movie_json))
        except Exception as e:
            print(f"Redis operation failed: {e}")
    return db_movie

@app.delete("/delete_movie/{movie_id}", response_model=MovieDelete)
async def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(db_movie)
    db.commit()
    if redis:
        try:
            await redis.delete(f"movie:{movie_id}")
        except Exception as e:
            print(f"Redis operation failed: {e}")
    return MovieDelete(id=movie_id, message=f"movie id {movie_id} deleted successfully.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)