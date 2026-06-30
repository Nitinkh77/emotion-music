import { useRef, useState, useCallback } from "react";

const EMOTION_EMOJI = {
  Happy: "😄", Sad: "😢", Angry: "😠",
  Fearful: "😨", Surprised: "😲", Disgusted: "🤢", Neutral: "😐",
};

export function CameraCapture({ onCapture }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [streaming, setStreaming] = useState(false);
  const [preview, setPreview] = useState(null);

  const startCamera = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
      videoRef.current.play();
      setStreaming(true);
      setPreview(null);
    } catch {
      alert("Camera access denied. Please allow camera permissions.");
    }
  }, []);

  const stopStream = useCallback(() => {
    videoRef.current?.srcObject?.getTracks().forEach((t) => t.stop());
    setStreaming(false);
  }, []);

  const capture = useCallback(() => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);
    canvas.toBlob((blob) => {
      const url = URL.createObjectURL(blob);
      setPreview(url);
      stopStream();
      const file = new File([blob], "capture.jpg", { type: "image/jpeg" });
      onCapture(file);
    }, "image/jpeg", 0.9);
  }, [onCapture, stopStream]);

  const handleUpload = useCallback((e) => {
    const file = e.target.files[0];
    if (!file) return;
    setPreview(URL.createObjectURL(file));
    stopStream();
    onCapture(file);
  }, [onCapture, stopStream]);

  return (
    <div className="capture-container">
      <video ref={videoRef} className={`camera-feed ${streaming ? "" : "hidden"}`} />
      <canvas ref={canvasRef} className="hidden" />

      {preview && (
        <img src={preview} alt="Captured face" className="preview-image" />
      )}

      {!streaming && !preview && (
        <div className="capture-placeholder">
          <span className="placeholder-icon">📷</span>
          <p>Use your camera or upload a photo</p>
        </div>
      )}

      <div className="capture-actions">
        {!streaming ? (
          <button className="btn btn-primary" onClick={startCamera}>
            Open Camera
          </button>
        ) : (
          <button className="btn btn-accent" onClick={capture}>
            📸 Snap Photo
          </button>
        )}
        <label className="btn btn-secondary">
          Upload Photo
          <input
            type="file"
            accept="image/jpeg,image/png,image/webp"
            className="hidden"
            onChange={handleUpload}
          />
        </label>
      </div>
    </div>
  );
}

export { EMOTION_EMOJI };
