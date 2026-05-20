import { apiClient } from "../core/apiClient.js";

export const cvService = {
  uploadCV(file) {
    const formData = new FormData();
    formData.append("file", file);

    return apiClient.postForm("/api/v1/cv/upload", formData);
  },
};