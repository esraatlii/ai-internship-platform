import { CONFIG } from "./config.js";
import { storage } from "./storage.js";

async function request(
  path,
  {
    method = "GET",
    body = null,
    auth = true,
  } = {}
) {
  const url = `${CONFIG.API_BASE_URL}${path}`;

  const headers = {
    "Content-Type": "application/json",
  };

  if (auth) {
    const token = storage.getToken();

    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }
  }

  const response = await fetch(url, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  });

  const text = await response.text();

  let data = null;

  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = text;
  }

  if (!response.ok) {
    const error = new Error(
      data?.detail || data?.message || "Bir hata oluştu."
    );

    error.status = response.status;
    error.data = data;

    throw error;
  }

  return data;
}

export const apiClient = {
  get(path, options = {}) {
    return request(path, {
      ...options,
      method: "GET",
    });
  },

  post(path, body, options = {}) {
    return request(path, {
      ...options,
      method: "POST",
      body,
    });
  },

  put(path, body, options = {}) {
    return request(path, {
      ...options,
      method: "PUT",
      body,
    });
  },

  patch(path, body, options = {}) {
    return request(path, {
      ...options,
      method: "PATCH",
      body,
    });
  },

  delete(path, options = {}) {
    return request(path, {
      ...options,
      method: "DELETE",
    });
  },
};