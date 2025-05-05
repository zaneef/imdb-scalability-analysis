from sqlalchemy.orm import Session
from . import models

def get_movie_by_title(db: Session, title: str):
    return db.query(models.Movie).filter(models.Movie.title.ilike(f"%{title}%")).all()