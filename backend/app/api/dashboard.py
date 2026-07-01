from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from collections import Counter
from app.core.database import get_database
from app.api.auth import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/history")
def get_history(current_user: dict = Depends(get_current_user), limit: int = 50):
    db = get_database()
    user_id = str(current_user["_id"])
    entries = list(
        db.emotion_history.find({"user_id": user_id})
        .sort("created_at", -1)
        .limit(limit)
    )
    for e in entries:
        e["_id"] = str(e["_id"])
    return entries


@router.get("/stats")
def get_stats(current_user: dict = Depends(get_current_user)):
    db = get_database()
    user_id = str(current_user["_id"])
    entries = list(db.emotion_history.find({"user_id": user_id}))

    emotion_counts = Counter(e["emotion"] for e in entries)
    total_songs = sum(len(e.get("songs", [])) for e in entries)

    return {
        "total_analyses": len(entries),
        "total_songs_recommended": total_songs,
        "emotion_breakdown": dict(emotion_counts),
        "most_common_emotion": emotion_counts.most_common(1)[0][0] if emotion_counts else None,
    }


@router.get("/favorites")
def get_favorites(current_user: dict = Depends(get_current_user)):
    db = get_database()
    user_id = str(current_user["_id"])
    favs = list(db.favorites.find({"user_id": user_id}).sort("added_at", -1))
    for f in favs:
        f["_id"] = str(f["_id"])
    return favs


@router.post("/favorites")
def add_favorite(item: dict, current_user: dict = Depends(get_current_user)):
    db = get_database()
    user_id = str(current_user["_id"])
    doc = {
        "user_id": user_id,
        "title": item.get("title"),
        "artist": item.get("artist"),
        "youtube_id": item.get("youtube_id"),
    }
    from datetime import datetime
    doc["added_at"] = datetime.utcnow()
    result = db.favorites.insert_one(doc)
    return {"id": str(result.inserted_id), "message": "Added to favorites"}


@router.delete("/favorites/{favorite_id}")
def remove_favorite(favorite_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    user_id = str(current_user["_id"])
    result = db.favorites.delete_one({"_id": ObjectId(favorite_id), "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return {"message": "Removed from favorites"}