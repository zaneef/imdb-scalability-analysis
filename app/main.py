from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database, crud, schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["Root"])
def read_root():
    return {"msg": "Hello World!"}

@app.get("/movies/", response_model=list[schemas.MovieOut], tags=["Movies"])
def search_movies(title: str, db: Session = Depends(get_db)):
    movies = crud.get_movie_by_title(db, title)
    if not movies:
        raise HTTPException(status_code=404, detail=f"No film found with title { title }.")
    else:
        def format_movie(m):
            return schemas.MovieOut(
                id=m.id,
                title=m.title,
                year=m.year,
                duration=m.duration,
                rating=m.rating,
                num_votes=m.num_votes,
                directors=[d.strip() for d in m.directors.split(",")] if m.directors else [],
                actors=[a.strip() for a in m.actors.split(",")] if m.actors else []
            )
        
        return [format_movie(m) for m in movies]
