import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def make_fake_image() -> bytes:
    """Returns minimal valid PNG bytes."""
    import struct, zlib
    def chunk(name, data):
        c = name + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(b"\x00\xff\xff\xff"))
    png += chunk(b"IEND", b"")
    return png


@patch("app.api.routes.detect_emotion")
@patch("app.api.routes.get_tracks_for_emotion")
def test_analyze_happy_path(mock_music, mock_emotion):
    from app.models.schemas import EmotionResult, Track
    mock_emotion.return_value = EmotionResult(
        dominant_emotion="Happy",
        confidence=92.5,
        all_emotions={"Happy": 92.5, "Neutral": 7.5},
    )
    mock_music.return_value = (
        [Track(id="1", name="Song", artist="Artist", album="Album",
               spotify_url="https://open.spotify.com/track/1", duration_ms=200000)],
        "Good Vibes Only ☀️",
    )
    resp = client.post(
        "/api/analyze",
        files={"image": ("face.png", make_fake_image(), "image/png")},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["emotion"]["dominant_emotion"] == "Happy"
    assert len(data["tracks"]) == 1
    assert "Good Vibes" in data["playlist_name"]


def test_analyze_rejects_non_image():
    resp = client.post(
        "/api/analyze",
        files={"image": ("file.pdf", b"%PDF", "application/pdf")},
    )
    assert resp.status_code == 415


def test_health():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
