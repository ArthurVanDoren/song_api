from typing import List
from pydantic import BaseModel

class SongBase(BaseModel):
    title: str
    artist: str

class SongCreateWithArtist(SongBase):
    pass

class SongUpdate(SongBase):
    pass

class Song(SongBase):
    id: int

    class Config:
        orm_mode = True

class SongWithArtist(Song):
    pass
