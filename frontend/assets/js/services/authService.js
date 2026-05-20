import { apiClient } from "../core/apiClient.js";
import { storage } from "../core/storage.js";

export const authService = {
  async login(email, password) {
    const data = await apiClient.post(
      "/api/v1/auth/login",
      {
        email,
        password,
      },
      {
        auth: false,
      }
    );

    storage.setToken(data.access_token);

    return data;
  },

  async register(full_name, email, password) {
    return await apiClient.post(
      "/api/v1/auth/register",
      {
        full_name,
        email,
        password,
      },
      {
        auth: false,
      }
    );
  },

  async getCurrentUser() {
    return await apiClient.get("/api/v1/auth/me");
  },

  logout() {
    storage.removeToken();
  },
};