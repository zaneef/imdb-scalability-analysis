from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Movie(Base):
    __tablename__ = "movies"
    id = Column(String, primary_key=True, index=True) 
    title = Column(String, index=True)
    year = Column(Integer)
    duration = Column(Integer)
    rating = Column(Float)
    num_votes = Column(Integer)
    directors = Column(String) 
    actors = Column(String)