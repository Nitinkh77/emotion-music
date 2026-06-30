from pydantic import BaseModel
from typing import Optional


class EmotionResult(BaseModel):
    dominant_emotion: str
    confidence: float
    all_emotions: dict[str, float]


class Track(BaseModel):
    id: str
    name: str
    artist: str
    album: str
    preview_url: Optional[str] = None
    spotify_url: str
    image_url: Optional[str] = None
    duration_ms: int


class MusicResponse(BaseModel):
    emotion: EmotionResult
    tracks: list[Track]
    playlist_name: str
    message: str
