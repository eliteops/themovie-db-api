from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .models import Movie
from .schemas import MovieCreate, MovieResponse, MovieDelete
from typing import List

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

@app.post("/create_movie/", response_model=MovieResponse)
async def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    print(movie.dict())
    db_movie = Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return MovieResponse(**db_movie.__dict__)

@app.get("/read_movies/", response_model=List[MovieResponse])
async def read_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    movies = db.query(Movie).offset(skip).limit(limit).all()
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found")
    return movies

@app.get("/read_specific_movie/{movie_id}", response_model=MovieResponse)
async def read_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.put("/update_movie/{movie_id}", response_model=MovieResponse)
async def update_movie(movie_id: int, movie: MovieCreate, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # using model_dump method to get the dictionary of the movie object and
    #  items() method to get the key, value pairs in iterable mode
    for key, value in movie.dict().items():
        setattr(db_movie, key, value)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.delete("/delete_movie/{movie_id}", response_model=MovieDelete)
async def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(db_movie)
    db.commit()
    return MovieDelete(id=movie_id, message=f"movie id {movie_id} deleted successfully.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)