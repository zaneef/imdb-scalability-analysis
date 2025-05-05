from pydantic import BaseModel
from typing import List

class MovieOut(BaseModel):
    id: str
    title: str
    year: int
    duration: int
    rating: float
    num_votes: int
    directors: List[str]
    actors: List[str]

    class Config:
        orm_mode = True