import axios from "axios";

const api = axios.create({ baseURL: "/api" });

/**
 * @param {File} imageFile
 * @returns {Promise<import("../types").MusicResponse>}
 */
export async function analyzeEmotion(imageFile) {
  const formData = new FormData();
  formData.append("image", imageFile);
  const { data } = await api.post("/analyze", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}
