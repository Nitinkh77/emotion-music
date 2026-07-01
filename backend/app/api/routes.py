from fastapi import APIRouter, File, UploadFile, HTTPException, Header
from app.models.schemas import MusicResponse
from app.services.emotion_service import detect_emotion
from app.services.music_service import get_tracks_for_emotion
from app.core.config import get_settings
from app.core.database import get_database
from app.core.security import decode_access_token
from bson import ObjectId
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["emotion-music"])

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}


def get_optional_user(authorization: str = Header(None)):
    """Returns the user dict if a valid token is provided, otherwise None. Does not raise."""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload:
        return None
    db = get_database()
    try:
        user = db.users.find_one({"_id": ObjectId(payload["sub"])})
        return user
    except Exception:
        return None


@router.post("/analyze", response_model=MusicResponse)
async def analyze_emotion_and_get_music(
    image: UploadFile = File(..., description="Face image (JPEG/PNG/WebP)"),
    authorization: str = Header(None),
):
    """
    Upload a face image → detect emotion → return Spotify track recommendations.
    If the request includes a valid auth token, the result is saved to the user's history.
    """
    settings = get_settings()

    # Validate file type
    if image.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{image.content_type}'. Use JPEG, PNG, or WebP.",
        )

    # Read and validate file size
    image_bytes = await image.read()
    max_bytes = settings.max_image_size_mb * 1024 * 1024
    if len(image_bytes) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"Image too large. Maximum size is {settings.max_image_size_mb}MB.",
        )

    # Detect emotion
    try:
        emotion_result = detect_emotion(image_bytes)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Fetch music
    try:
        tracks, playlist_name = await get_tracks_for_emotion(emotion_result.dominant_emotion)
    except Exception as e:
        logger.error("Spotify fetch failed: %s", e)
        raise HTTPException(status_code=502, detail="Failed to fetch music recommendations.")

    # Save to history if user is logged in
    current_user = get_optional_user(authorization)
    if current_user:
        try:
            db = get_database()
            db.emotion_history.insert_one({
                "user_id": str(current_user["_id"]),
                "emotion": emotion_result.dominant_emotion,
                "confidence": getattr(emotion_result, "confidence", None),
                "songs": [
                    {"title": t.get("title") if isinstance(t, dict) else getattr(t, "title", None),
                     "artist": t.get("artist") if isinstance(t, dict) else getattr(t, "artist", None)}
                    for t in tracks
                ],
                "created_at": datetime.utcnow(),
            })
        except Exception as e:
            logger.error("Failed to save history: %s", e)

    return MusicResponse(
        emotion=emotion_result,
        tracks=tracks,
        playlist_name=playlist_name,
        message=f"Detected that you're feeling {emotion_result.dominant_emotion.lower()}. Here's your playlist!",
    )


@router.get("/health")
async def health_check():
    return {"status": "ok"}