import { storage } from "../core/storage.js";
import { cvService } from "../services/cvService.js";
import { githubService } from "../services/githubService.js";
import { analysisService } from "../services/analysisService.js";
window.addEventListener("beforeunload", () => {
  console.trace("Sayfa yenileniyor / kapanıyor");
});
const cvInput = document.getElementById("cv-upload");
const startAnalysisBtn = document.getElementById("start-analysis");

const cvStatus = document.getElementById("cv-status");
const githubStatus = document.getElementById("github-status");
const analysisStatus = document.getElementById("analysis-status");

function checkAuth() {
  const token = storage.getToken();

  if (!token) {
    window.location.href = "./login.html";
  }
}

function loadDashboardStatus() {
  const savedCvName = localStorage.getItem("uploaded_cv_name");
  const savedGithubUsername = localStorage.getItem("github_username");
  const savedAnalysisScore = localStorage.getItem("analysis_score");

  if (savedCvName) {
    cvStatus.textContent = `CV yüklendi: ${savedCvName}`;
    cvStatus.style.color = "green";
  }

  if (savedGithubUsername) {
    githubStatus.textContent = `GitHub analiz edildi: ${savedGithubUsername}`;
    githubStatus.style.color = "green";
  }

  if (savedAnalysisScore) {
    analysisStatus.textContent = `Analiz tamamlandı. Skor: ${savedAnalysisScore}/100`;
    analysisStatus.style.color = "green";
  }
}

cvInput.addEventListener("change", async (event) => {
  event.preventDefault();

  const file = event.target.files[0];

  if (!file) return;

  try {
    cvStatus.textContent = "CV yükleniyor...";
    cvStatus.style.color = "#6b7280";

    const result = await cvService.uploadCV(file);

    console.log("CV upload result:", result);

    localStorage.setItem("uploaded_cv_name", file.name);

    cvStatus.textContent = `CV yüklendi: ${file.name}`;
    cvStatus.style.color = "green";
  } catch (error) {
    console.error("CV upload error:", error);

    cvStatus.textContent = error.message;
    cvStatus.style.color = "red";
  }
});

window.promptGithub = async function () {
  const githubUrl = prompt("GitHub profil linkini gir:");

  if (!githubUrl) return;

  try {
    githubStatus.textContent = "GitHub analiz ediliyor...";
    githubStatus.style.color = "#6b7280";

    const result = await githubService.analyzeGithub(githubUrl);

    console.log("GitHub analyze result:", result);

    localStorage.setItem("github_username", result.username);

    githubStatus.textContent = `GitHub analiz edildi: ${result.username}`;
    githubStatus.style.color = "green";
  } catch (error) {
    console.error("GitHub analyze error:", error);

    githubStatus.textContent = error.message;
    githubStatus.style.color = "red";
  }
};

startAnalysisBtn.addEventListener("click", async () => {
  try {
    analysisStatus.textContent = "AI analizi oluşturuluyor...";
    analysisStatus.style.color = "#6b7280";

    const result = await analysisService.generateAnalysis();

    console.log("Analysis result:", result);

    localStorage.setItem("analysis_score", result.score);

    analysisStatus.textContent = `Analiz tamamlandı. Skor: ${result.score}/100`;
    analysisStatus.style.color = "green";
  } catch (error) {
    console.error("Analysis error:", error);

    analysisStatus.textContent = error.message;
    analysisStatus.style.color = "red";
  }
});

checkAuth();
loadDashboardStatus();