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

@app.get("/movies/", response_model=list[schemas.MovieOut])
def search_movies(title: str, db: Session = Depends(get_db)):
    movies = crud.get_movie_by_title(db, title)
    if not movies:
        raise HTTPException(status_code=404, detail="Nessun film trovato")
    
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