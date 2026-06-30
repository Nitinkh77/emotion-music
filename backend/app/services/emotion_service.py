import numpy as np
import cv2
from deepface import DeepFace
from app.models.schemas import EmotionResult
import logging

logger = logging.getLogger(__name__)

# Maps DeepFace emotions to music-friendly moods
EMOTION_DISPLAY_MAP = {
    "happy": "Happy",
    "sad": "Sad",
    "angry": "Angry",
    "fear": "Fearful",
    "surprise": "Surprised",
    "disgust": "Disgusted",
    "neutral": "Neutral",
}


def detect_emotion(image_bytes: bytes) -> EmotionResult:
    """
    Accepts raw image bytes, runs DeepFace emotion analysis,
    returns an EmotionResult with dominant emotion and confidence scores.
    """
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Could not decode image. Please upload a valid JPEG or PNG.")

        results = DeepFace.analyze(
            img_path=img,
            actions=["emotion"],
            enforce_detection=True,
            detector_backend="opencv",
        )

        # DeepFace returns a list when multiple faces are detected; use first face
        result = results[0] if isinstance(results, list) else results

        emotions: dict[str, float] = result["emotion"]
        dominant: str = result["dominant_emotion"]
        confidence: float = emotions[dominant]

        return EmotionResult(
            dominant_emotion=EMOTION_DISPLAY_MAP.get(dominant, dominant),
            confidence=round(confidence, 2),
            all_emotions={
                EMOTION_DISPLAY_MAP.get(k, k): round(v, 2)
                for k, v in emotions.items()
            },
        )

    except ValueError as e:
        logger.error("Image decoding error: %s", e)
        raise
    except Exception as e:
        logger.error("Emotion detection failed: %s", e)
        raise RuntimeError(f"Emotion detection failed: {str(e)}") from e
