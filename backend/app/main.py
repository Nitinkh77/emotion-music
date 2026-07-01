from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.api.auth import router as auth_router
from app.api.dashboard import router as dashboard_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Emotion-Based Music Generator",
    description="Upload a face image, detect your emotion, get a Spotify playlist.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(auth_router)
app.include_router(dashboard_router)


@app.on_event("startup")
async def startup_event():
    print("🎵 Emotion Music API is running!")