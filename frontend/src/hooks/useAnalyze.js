import { useState, useCallback } from "react";
import { analyzeEmotion } from "../services/api";

export function useAnalyze() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyze = useCallback(async (file) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await analyzeEmotion(file);
      setResult(data);
    } catch (err) {
      const msg =
        err.response?.data?.detail ||
        "Something went wrong. Please try again.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setResult(null);
    setError(null);
  }, []);

  return { result, loading, error, analyze, reset };
}
