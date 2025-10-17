from pydantic import BaseModel, Field
from typing import List

class AlbumArtist(BaseModel):
    id: str
    name: str

class Album(BaseModel):
    id: str
    name: str
    artists: List[AlbumArtist]

class SavedAlbum(BaseModel):
    album: Album

class GetSavedAlbumsResponse(BaseModel):
    items: List[SavedAlbum]
    total: int