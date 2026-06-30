from fastapi import APIRouter, File, UploadFile, HTTPException
from app.models.schemas import MusicResponse
from app.services.emotion_service import detect_emotion
from app.services.music_service import get_tracks_for_emotion
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["emotion-music"])

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}


@router.post("/analyze", response_model=MusicResponse)
async def analyze_emotion_and_get_music(
    image: UploadFile = File(..., description="Face image (JPEG/PNG/WebP)"),
):
    """
    Upload a face image → detect emotion → return Spotify track recommendations.
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

    return MusicResponse(
        emotion=emotion_result,
        tracks=tracks,
        playlist_name=playlist_name,
        message=f"Detected that you're feeling {emotion_result.dominant_emotion.lower()}. Here's your playlist!",
    )


@router.get("/health")
async def health_check():
    return {"status": "ok"}
