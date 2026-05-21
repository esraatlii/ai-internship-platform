import { storage } from "../core/storage.js";
import { cvService } from "../services/cvService.js";
import { githubService } from "../services/githubService.js";
import { analysisService } from "../services/analysisService.js";

const analysisResultSection = document.getElementById("analysis-result-section");
const resultScore = document.getElementById("result-score");
const resultSummary = document.getElementById("result-summary");
const resultMissingSkills = document.getElementById("result-missing-skills");
const resultEmail = document.getElementById("result-email");
const resultLinkedin = document.getElementById("result-linkedin");

const cvInput = document.getElementById("cv-upload");
const startAnalysisBtn = document.getElementById("start-analysis");

const cvStatus = document.getElementById("cv-status");
const githubStatus = document.getElementById("github-status");
const analysisStatus = document.getElementById("analysis-status");

const userName = document.getElementById("user-name");
const logoutBtn = document.getElementById("logout-btn");
const activityTableBody = document.getElementById("activity-table-body");

function checkAuth() {
  const token = storage.getToken();

  if (!token) {
    window.location.href = "./login.html";
  }
}

function setupLogout() {
  if (!logoutBtn) return;

  logoutBtn.addEventListener("click", (event) => {
    event.preventDefault();

    storage.clearAll();

    window.location.href = "./login.html";
  });
}

function loadCurrentUser() {
  const currentUser = storage.getUser();

  if (!currentUser || !userName) return;

  userName.textContent = currentUser.full_name;
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

function getActivities() {
  const rawActivities = localStorage.getItem("recent_activities");

  if (!rawActivities) return [];

  try {
    return JSON.parse(rawActivities);
  } catch (error) {
    console.error("Activity parse error:", error);
    localStorage.removeItem("recent_activities");
    return [];
  }
}

function saveActivities(activities) {
  localStorage.setItem("recent_activities", JSON.stringify(activities));
}

function addActivity(action, status) {
  const activities = getActivities();

  const newActivity = {
    action,
    status,
    date: new Date().toLocaleDateString("tr-TR"),
  };

  activities.unshift(newActivity);

  saveActivities(activities);
}

function loadActivities() {
  if (!activityTableBody) return;

  const activities = getActivities();

  activityTableBody.innerHTML = "";

  if (activities.length === 0) {
    activityTableBody.innerHTML = `
      <tr>
        <td colspan="3">Henüz işlem yapılmadı.</td>
      </tr>
    `;
    return;
  }

  activities.forEach((activity) => {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${activity.action}</td>
      <td>${activity.date}</td>
      <td>
        <span class="status completed">
          ${activity.status}
        </span>
      </td>
    `;

    activityTableBody.appendChild(row);
  });
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

    addActivity("CV Yükleme", "Tamamlandı");
    loadActivities();
  } catch (error) {
    console.error("CV upload error:", error);

    cvStatus.textContent = error.message;
    cvStatus.style.color = "red";

    addActivity("CV Yükleme", "Başarısız");
    loadActivities();
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

    addActivity("GitHub Analizi", "Tamamlandı");
    loadActivities();
  } catch (error) {
    console.error("GitHub analyze error:", error);

    githubStatus.textContent = error.message;
    githubStatus.style.color = "red";

    addActivity("GitHub Analizi", "Başarısız");
    loadActivities();
  }
};

startAnalysisBtn.addEventListener("click", async () => {
  try {
    analysisStatus.textContent = "AI analizi oluşturuluyor...";
    analysisStatus.style.color = "#6b7280";

    const result = await analysisService.generateAnalysis();

    analysisResultSection.classList.remove("hidden");

    resultScore.textContent = `${result.score}/100`;
    resultSummary.textContent = result.summary;
    resultMissingSkills.textContent = result.missing_skills;
    resultEmail.textContent = result.internship_email;
    resultLinkedin.textContent = result.linkedin_message;

    console.log("Analysis result:", result);

    localStorage.setItem("analysis_score", result.score);

    analysisStatus.textContent = `Analiz tamamlandı. Skor: ${result.score}/100`;
    analysisStatus.style.color = "green";

    addActivity("AI Analizi", "Tamamlandı");
    loadActivities();
  } catch (error) {
    console.error("Analysis error:", error);

    analysisStatus.textContent = error.message;
    analysisStatus.style.color = "red";

    addActivity("AI Analizi", "Başarısız");
    loadActivities();
  }
});

checkAuth();
loadDashboardStatus();
loadCurrentUser();
setupLogout();
loadActivities();