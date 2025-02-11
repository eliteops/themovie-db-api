from pydantic import BaseModel

class MovieBase(BaseModel):
    title: str
    year: int
    genre: str
    imdb_rating: float

class MovieCreate(MovieBase):
    pass

class MovieResponse(BaseModel):
    id: int
    title: str
    year: int
    genre: str
    imdb_rating: float

class MovieDelete(BaseModel):
    message: dict