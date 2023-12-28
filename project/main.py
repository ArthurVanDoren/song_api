from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os

import crud
import models
import schemas
from database import SessionLocal, engine

print("We are in the main.......")
if not os.path.exists('./sqlitedb'):
    print("Making folder.......")
    os.makedirs('./sqlitedb')

print("Creating tables.......")
models.Base.metadata.create_all(bind=engine)
print("Tables created.......")

app = FastAPI()


app.mount("/", StaticFiles(directory="static"), name="static")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route to serve the index.html page
@app.get("static/index.html", response_class=HTMLResponse)
def read_index():
    return FileResponse("static/index.html")


@app.post("/songs/", response_model=schemas.Song)
def create_song_with_artist(song: schemas.SongCreateWithArtist, db: Session = Depends(get_db)):
    return crud.create_song_with_artist(db=db, song=song)


@app.get("/songs/", response_model=list[schemas.SongWithArtist])
def read_songs_with_artists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    songs = crud.get_songs_with_artists(db, skip=skip, limit=limit)
    return songs


@app.get("/songs/{song_id}", response_model=schemas.SongWithArtist)
def read_song_with_artist(song_id: int, db: Session = Depends(get_db)):
    db_song = crud.get_song_with_artist(db, song_id=song_id)
    if db_song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return db_song


@app.put("/songs/{song_id}", response_model=schemas.Song)
def update_song(song_id: int, updated_song: schemas.SongUpdate, db: Session = Depends(get_db)):
    db_song = crud.update_song(db, song_id, updated_song)
    if db_song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return db_song


@app.delete("/songs/{song_id}", response_model=schemas.Song)
def delete_song(song_id: int, db: Session = Depends(get_db)):
    db_song = crud.delete_song(db, song_id)
    if db_song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return db_song
