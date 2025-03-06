from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, nullable=False)
    year = Column(Integer, nullable=False)
    genre = Column(String(50), nullable=False)
    imdb_rating = Column(Float, nullable=False)