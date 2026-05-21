import { authService } from "../services/authService.js";
import { storage } from "../core/storage.js";

const form = document.querySelector("form");

const emailInput = document.querySelector("#email");
const passwordInput = document.querySelector("#password");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = emailInput.value.trim();
  const password = passwordInput.value.trim();

  try {
    const result = await authService.login(email, password);

    storage.setToken(result.access_token);

    if (result.current_user) {
      storage.setUser(result.current_user);
    }

  window.location.href = "../pages/dashboard.html";
      alert("Giriş başarılı");

      window.location.href = "../pages/dashboard.html";
    } catch (err) {
      alert(err.message);
    }
});