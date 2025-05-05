from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "La tua web app FastAPI è attiva!"}
