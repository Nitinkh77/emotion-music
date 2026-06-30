# 🎵 Emotion-Based Music Generator

Upload or snap a photo of your face → AI detects your emotion → Get a personalized Spotify playlist.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI |
| Emotion AI | DeepFace (OpenCV backend) |
| Music | Spotify Web API via Spotipy |
| Frontend | React 18, Vite |

## Project Structure

```
emotion-music/
├── backend/
│   ├── app/
│   │   ├── api/routes.py        # POST /api/analyze, GET /api/health
│   │   ├── core/config.py       # Settings (env vars)
│   │   ├── models/schemas.py    # Pydantic models
│   │   └── services/
│   │       ├── emotion_service.py  # DeepFace emotion detection
│   │       └── music_service.py    # Spotify track recommendations
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── CameraCapture.jsx  # Webcam + file upload
    │   │   ├── EmotionDisplay.jsx # Emotion scores UI
    │   │   └── TrackList.jsx      # Spotify tracks UI
    │   ├── hooks/useAnalyze.js    # API state hook
    │   ├── services/api.js        # Axios client
    │   ├── App.jsx
    │   └── App.css
    └── index.html
```

## Getting Started

### 1. Spotify API Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create an app → copy **Client ID** and **Client Secret**

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env and fill in your Spotify credentials

uvicorn app.main:app --reload
# API running at http://localhost:8000
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
# App running at http://localhost:5173
```

### 4. Run Tests

```bash
cd backend
pytest tests/ -v
```

## Emotion → Music Mapping

| Emotion | Playlist Vibe | Genres |
|---------|--------------|--------|
| Happy 😄 | Good Vibes Only ☀️ | Pop, Dance |
| Sad 😢 | Let It Out 🌧️ | Acoustic, Indie |
| Angry 😠 | Release the Beast 🔥 | Rock, Metal |
| Fearful 😨 | Breathe Easy 🌿 | Ambient, Classical |
| Surprised 😲 | Plot Twist! ⚡ | Pop, Electronic |
| Disgusted 🤢 | Reset & Recharge 🎧 | Lo-fi, Chill |
| Neutral 😐 | In the Zone 🎵 | Study, Instrumental |

## API Reference

### `POST /api/analyze`
- **Body**: `multipart/form-data` with `image` field (JPEG/PNG/WebP, max 5MB)
- **Response**: `MusicResponse` — detected emotion + Spotify tracks

### `GET /api/health`
- **Response**: `{"status": "ok"}`
