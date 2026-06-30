import { EMOTION_EMOJI } from "./CameraCapture";

export function EmotionDisplay({ emotion }) {
  const emoji = EMOTION_EMOJI[emotion.dominant_emotion] || "🎭";
  const sorted = Object.entries(emotion.all_emotions).sort(([, a], [, b]) => b - a);

  return (
    <div className="emotion-card">
      <div className="emotion-hero">
        <span className="emotion-emoji">{emoji}</span>
        <div>
          <h2 className="emotion-name">{emotion.dominant_emotion}</h2>
          <p className="emotion-confidence">{emotion.confidence.toFixed(1)}% confidence</p>
        </div>
      </div>
      <div className="emotion-bars">
        {sorted.map(([name, score]) => (
          <div key={name} className="bar-row">
            <span className="bar-label">{name}</span>
            <div className="bar-track">
              <div
                className="bar-fill"
                style={{ width: `${score}%` }}
                data-active={name === emotion.dominant_emotion}
              />
            </div>
            <span className="bar-value">{score.toFixed(1)}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}
