from itertools import islice
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select, tablesample

from app.schemas import MovieSchema
from . import models

class MockMovie:
    def __init__(self, row):
        # just copy all attributes
        for attr in ('id', 'title', 'year', 'duration', 'rating', 'num_votes', 'directors', 'actors'):
            setattr(self, attr, getattr(row, attr))

def gen_mocks(db: Session, count=100) -> list[list[MockMovie]]:
    # select some titles
    titles = db.execute(select(tablesample(models.Movie, 0.06).c.title))
    result = []
    # take at most `count` titles, generate list of responses for each corresponding search query
    for (title, ) in islice(titles, count):
        movs = db.query(models.Movie).filter(models.Movie.title.ilike(f'%{title}%')).all()
        # create mock object out of each orm object
        result.append(list(map(MockMovie, movs)))

    return result

def get_movies(movies):
    if movies:
        schema_movies = []
        for m in movies:
            if isinstance(m.directors, str):
                m.directors = [d.strip() for d in m.directors.split(",")]
            if isinstance(m.actors, str):
                m.actors = [a.strip() for a in m.actors.split(",")]

            schema_movies.append(MovieSchema.model_validate(m))

        return [m.model_dump() for m in schema_movies]
    return None
