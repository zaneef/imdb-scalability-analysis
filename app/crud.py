from sqlalchemy.orm import Session
from . import models
from .redis_client import redis_client
from .schemas import MovieSchema

import json

def get_movie_by_title(db: Session, title: str):
    cache_key = title.lower()

    movies = db.query(models.Movie).filter(models.Movie.title.ilike(f"%{ title }%")).limit(100).all()

    if movies:
        schema_movies = []
        for m in movies:
            if isinstance(m.directors, str):
                m.directors = [d.strip() for d in m.directors.split(",")]
            if isinstance(m.actors, str):
                m.actors = [a.strip() for a in m.actors.split(",")]

            schema_movies.append(MovieSchema.from_orm(m))

        return [m.model_dump() for m in schema_movies]
    return None

def cache_get_movie_by_title(db: Session, title: str):
    cache_key = f"movie:{title.lower()}"
    cached = redis_client.get(cache_key)
    if cached:
        print(f"CACHE HIT: {title.lower()}")
        return json.loads(cached)

    movies = db.query(models.Movie).filter(models.Movie.title.ilike(f"%{title}%")).limit(100).all()

    if movies:
        schema_movies = []
        for m in movies:
            if isinstance(m.directors, str):
                m.directors = [d.strip() for d in m.directors.split(",")]
            if isinstance(m.actors, str):
                m.actors = [a.strip() for a in m.actors.split(",")]

            schema_movies.append(MovieSchema.from_orm(m))

        redis_client.set(
            cache_key,
            json.dumps([m.model_dump() for m in schema_movies]),
            ex=21600
        )
        return [m.model_dump() for m in schema_movies]
    return None