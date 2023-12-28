from sqlalchemy.orm import Session
import models
import schemas

def create_song_with_artist(db: Session, song: schemas.SongCreateWithArtist):
    db_song = models.Song(**song.dict())
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song

def get_songs_with_artists(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Song).offset(skip).limit(limit).all()

def get_song_with_artist(db: Session, song_id: int):
    return db.query(models.Song).filter(models.Song.id == song_id).first()

def update_song(db: Session, song_id: int, updated_song: schemas.SongUpdate):
    db_song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if db_song:
        for key, value in updated_song.dict().items():
            setattr(db_song, key, value)
        db.commit()
        db.refresh(db_song)
    return db_song

def delete_song(db: Session, song_id: int):
    db_song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if db_song:
        db.delete(db_song)
        db.commit()
        db.refresh(db_song)
    return db_song
