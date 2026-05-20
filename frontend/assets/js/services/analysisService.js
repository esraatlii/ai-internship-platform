import { apiClient } from "../core/apiClient.js";

export const analysisService = {
  async generateAnalysis() {
    return apiClient.post("/api/v1/analysis/generate");
  },
};