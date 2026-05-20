import { apiClient } from "../core/apiClient.js";

export const githubService = {
  async analyzeGithub(githubUrl) {
    return apiClient.post("/api/v1/github/analyze", {
      github_url: githubUrl,
    });
  },
};