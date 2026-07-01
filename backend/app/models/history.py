from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class SongItem(BaseModel):
    title: str
    artist: Optional[str] = None
    youtube_id: Optional[str] = None


class EmotionHistoryEntry(BaseModel):
    user_id: str
    emotion: str
    confidence: Optional[float] = None
    songs: List[SongItem] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)


class FavoriteItem(BaseModel):
    user_id: str
    title: str
    artist: Optional[str] = None
    youtube_id: Optional[str] = None
    added_at: datetime = Field(default_factory=datetime.utcnow)