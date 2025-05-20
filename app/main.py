from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import models, database, crud, schemas

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