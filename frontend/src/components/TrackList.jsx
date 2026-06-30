function formatDuration(ms) {
  const m = Math.floor(ms / 60000);
  const s = Math.floor((ms % 60000) / 1000).toString().padStart(2, "0");
  return `${m}:${s}`;
}

export function TrackList({ tracks, playlistName }) {
  return (
    <div className="tracklist">
      <h3 className="tracklist-title">{playlistName}</h3>
      <ul className="tracks">
        {tracks.map((track, i) => (
          <li key={track.id} className="track-item">
            <span className="track-number">{i + 1}</span>
            {track.image_url && (
              <img src={track.image_url} alt={track.album} className="track-art" />
            )}
            <div className="track-info">
              <a
                href={track.spotify_url}
                target="_blank"
                rel="noopener noreferrer"
                className="track-name"
              >
                {track.name}
              </a>
              <p className="track-artist">{track.artist}</p>
            </div>
            <div className="track-right">
              {track.preview_url && (
                <audio controls src={track.preview_url} className="track-preview" />
              )}
              <span className="track-duration">{formatDuration(track.duration_ms)}</span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
