import { authService } from "../services/authService.js";

const form = document.querySelector("form");

const emailInput = document.querySelector("#email");
const passwordInput = document.querySelector("#password");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = emailInput.value.trim();
  const password = passwordInput.value.trim();

  try {
    await authService.login(email, password);

    alert("Giriş başarılı");

    window.location.href = "../pages/dashboard.html";

  } catch (err) {
    alert(err.message);
  }
});