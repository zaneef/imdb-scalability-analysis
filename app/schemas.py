from pydantic import BaseModel
from typing import List

class MovieSchema(BaseModel):
    id: str
    title: str
    year: int
    duration: int
    rating: float
    num_votes: int
    directors: List[str]
    actors: List[str]

    class Config:
        from_attributes = True
        orm_mode = True