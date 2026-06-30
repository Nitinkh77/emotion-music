import { useState } from "react";
import { CameraCapture } from "./components/CameraCapture";
import { EmotionDisplay } from "./components/EmotionDisplay";
import { TrackList } from "./components/TrackList";
import { useAnalyze } from "./hooks/useAnalyze";
import "./App.css";

export default function App() {
  const { result, loading, error, analyze, reset } = useAnalyze();
  const [capturedFile, setCapturedFile] = useState(null);

  const handleCapture = (file) => {
    setCapturedFile(file);
  };

  const handleAnalyze = () => {
    if (capturedFile) analyze(capturedFile);
  };

  const handleReset = () => {
    reset();
    setCapturedFile(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="logo">🎵</div>
        <h1 className="app-title">Emotion Music</h1>
        <p className="app-subtitle">Your face sets the mood. We find the music.</p>
      </header>

      <main className="app-main">
        {!result ? (
          <section className="capture-section">
            <CameraCapture onCapture={handleCapture} />

            {error && (
              <div className="error-banner" role="alert">
                ⚠️ {error}
              </div>
            )}

            <button
              className="btn btn-primary btn-lg"
              onClick={handleAnalyze}
              disabled={!capturedFile || loading}
            >
              {loading ? (
                <span className="loading-text">
                  <span className="spinner" /> Detecting emotion…
                </span>
              ) : (
                "Detect My Mood 🎭"
              )}
            </button>
          </section>
        ) : (
          <section className="results-section">
            <p className="result-message">{result.message}</p>
            <EmotionDisplay emotion={result.emotion} />
            <TrackList tracks={result.tracks} playlistName={result.playlist_name} />
            <button className="btn btn-secondary" onClick={handleReset}>
              Try Again
            </button>
          </section>
        )}
      </main>

      <footer className="app-footer">
        <p>Powered by DeepFace & Spotify</p>
      </footer>
    </div>
  );
}
