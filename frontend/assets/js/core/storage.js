const TOKEN_KEY = "ai_internship_access_token";
const USER_KEY = "current_user_ai_internship";

export const storage = {
  setToken(token) {
    localStorage.setItem(TOKEN_KEY, token);
  },

  getToken() {
    return localStorage.getItem(TOKEN_KEY);
  },

  removeToken() {
    localStorage.removeItem(TOKEN_KEY);
  },

  isAuthenticated() {
    return !!localStorage.getItem(TOKEN_KEY);
  },

  setUser(user) {
    if (!user) return;
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  },

  getUser() {
    const raw = localStorage.getItem(USER_KEY);

    if (!raw || raw === "undefined") return null;

    return JSON.parse(raw);
  },

  clearUser() {
    localStorage.removeItem(USER_KEY);
  },

  clearAll() {
    this.removeToken();
    this.clearUser();
  },
};