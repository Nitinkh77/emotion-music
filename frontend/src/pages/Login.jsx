import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./AuthPages.css";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(email, password);
      navigate("/");
    } catch {
      setError("Invalid email or password.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <form className="auth-form-side" onSubmit={handleSubmit}>
          <div className="auth-brand">🎵 Moodify</div>
          <h2>Welcome Back 👋</h2>
          <p className="auth-subtitle">Log in to see your mood history</p>

          {error && <div className="auth-error">{error}</div>}

          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button className="btn btn-primary" type="submit" disabled={loading}>
            {loading ? "Logging in..." : "Log In"}
          </button>

          <p className="auth-switch">
            Don't have an account? <Link to="/signup">Sign up</Link>
          </p>
        </form>

        <div className="auth-visual-side">
          <div className="auth-waveform">
            <span></span><span></span><span></span>
            <span></span><span></span><span></span>
          </div>
          <p className="auth-visual-title">Welcome back.</p>
          <p className="auth-visual-text">
            Your mood history and favorites are right where you left them.
          </p>
        </div>
      </div>
    </div>
  );
}