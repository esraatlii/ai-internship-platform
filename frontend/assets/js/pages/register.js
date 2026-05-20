import { authService } from "../services/authService.js";

const form = document.querySelector("form");

const fullNameInput = document.querySelector("#fullname");
const emailInput = document.querySelector("#email");
const passwordInput = document.querySelector("#password");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const full_name = fullNameInput.value.trim();
  const email = emailInput.value.trim();
  const password = passwordInput.value.trim();

  try {
    await authService.register(full_name, email, password);

    alert("Kayıt başarılı. Giriş sayfasına yönlendiriliyorsunuz.");

    window.location.href = "login.html";
  } catch (err) {
    alert(err.message);
  }
});