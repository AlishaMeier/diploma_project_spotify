from pydantic import BaseModel, Field
from typing import Optional
from pydantic import BaseModel


class PlaylistOwner(BaseModel):
    id: str
    display_name: Optional[str] = Field(None, alias='display_name')

class Playlist(BaseModel):
    id: str
    name: str
    description: str
    owner: PlaylistOwner
    public: bool

class PlaylistTracks(BaseModel):
    href: str
    total: int

class PlaylistSchema(BaseModel):
    id: str
    name: str
    description: Optional[str]
    public: bool
    owner: PlaylistOwner
    tracks: PlaylistTracks

class CreatedPlaylistResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    public: bool

class AddTrackResponse(BaseModel):
    snapshot_id: str
