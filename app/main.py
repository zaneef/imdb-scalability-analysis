from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import json

from . import models, database, crud, schemas
from .redis_client import redis_client

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def warmup_cache(db: Session):
    top_movies = db.query(models.Movie).order_by(models.Movie.num_votes.desc()).limit(5000).all()

    schema_movies = []
    for m in top_movies:
        cache_key = f"movie:{m.title.lower()}"
        if not redis_client.get(cache_key):
            if isinstance(m.directors, str):
                m.directors = [d.strip() for d in m.directors.split(",")]
            if isinstance(m.actors, str):
                m.actors = [a.strip() for a in m.actors.split(",")]
            schema = schemas.MovieSchema.from_orm(m)

            redis_client.set(
                cache_key,
                json.dumps([schema.model_dump()]),
                ex=21600
            )

@app.on_event("startup")
def startup_event():
    db = next(get_db())
    warmup_cache(db)

@app.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/ping")
def pong(request: Request):
    return {"response": "pong"}

@app.get("/movies/", response_model=list[schemas.MovieSchema])
def search_movies(title: str, db: Session = Depends(get_db)):
    movies = crud.cache_get_movie_by_title(db, title.strip('"'))
    if not movies:
        raise HTTPException(status_code=404, detail="No film found.")
    return movies
