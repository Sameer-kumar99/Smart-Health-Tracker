const API_BASE = "";
const state = {
  token: localStorage.getItem("sht_token"),
  user: JSON.parse(localStorage.getItem("sht_user") || "null"),
};

const loginTab = document.getElementById("login-tab");
const registerTab = document.getElementById("register-tab");
const loginForm = document.getElementById("login-form");
const registerForm = document.getElementById("register-form");
const loginFeedback = document.getElementById("login-feedback");
const registerFeedback = document.getElementById("register-feedback");
const metricForm = document.getElementById("metric-form");
const metricFeedback = document.getElementById("metric-feedback");
const dashboard = document.getElementById("dashboard");
const authSection = document.getElementById("auth-section");
const welcomeMessage = document.getElementById("welcome-message");
const profileSummary = document.getElementById("profile-summary");
const summaryList = document.getElementById("summary-list");
const metricsTable = document.getElementById("metrics-table");
const filterButton = document.getElementById("filter-button");
const filterStart = document.getElementById("filter-start");
const filterEnd = document.getElementById("filter-end");
const logoutButton = document.getElementById("logout-button");
const yearSpan = document.getElementById("year");

yearSpan.textContent = new Date().getFullYear();

function switchTab(tab) {
  if (tab === "login") {
    loginTab.classList.add("active");
    registerTab.classList.remove("active");
    loginForm.classList.add("active");
    registerForm.classList.remove("active");
  } else {
    loginTab.classList.remove("active");
    registerTab.classList.add("active");
    loginForm.classList.remove("active");
    registerForm.classList.add("active");
  }
  loginFeedback.textContent = "";
  registerFeedback.textContent = "";
}

loginTab.addEventListener("click", () => switchTab("login"));
registerTab.addEventListener("click", () => switchTab("register"));

async function apiRequest(path, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };
  if (state.token) {
    headers["Authorization"] = `Token ${state.token}`;
  }
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });
  const text = await response.text();
  let data = {};
  try {
    data = text ? JSON.parse(text) : {};
  } catch (err) {
    console.error("Failed to parse response", err, text);
  }
  if (!response.ok) {
    const errorMessage = data.error || `Request failed with status ${response.status}`;
    throw new Error(errorMessage);
  }
  return data;
}

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  loginFeedback.textContent = "Signing in...";
  const formData = new FormData(loginForm);
  const payload = Object.fromEntries(formData.entries());
  try {
    const data = await apiRequest("/api/auth/login", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    state.token = data.token;
    state.user = data.user;
    localStorage.setItem("sht_token", state.token);
    localStorage.setItem("sht_user", JSON.stringify(state.user));
    loginFeedback.textContent = "Login successful!";
    await loadDashboard();
  } catch (error) {
    loginFeedback.textContent = error.message;
  }
});

registerForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  registerFeedback.textContent = "Creating your account...";
  const formData = new FormData(registerForm);
  const payload = Object.fromEntries(formData.entries());
  try {
    await apiRequest("/api/auth/register", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    registerFeedback.textContent = "Account created! Please sign in.";
    registerForm.reset();
    switchTab("login");
  } catch (error) {
    registerFeedback.textContent = error.message;
  }
});

metricForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  metricFeedback.textContent = "Saving entry...";
  const formData = new FormData(metricForm);
  const payload = Object.fromEntries(formData.entries());
  try {
    await apiRequest("/api/metrics", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    metricFeedback.textContent = "Entry saved!";
    metricForm.reset();
    await Promise.all([loadMetrics(), loadSummary(), loadProfile()]);
  } catch (error) {
    metricFeedback.textContent = error.message;
  }
});

filterButton.addEventListener("click", loadMetrics);
logoutButton.addEventListener("click", () => {
  state.token = null;
  state.user = null;
  localStorage.removeItem("sht_token");
  localStorage.removeItem("sht_user");
  dashboard.classList.add("hidden");
  authSection.classList.remove("hidden");
});

async function loadProfile() {
  try {
    const { user } = await apiRequest("/api/user/profile");
    state.user = user;
    localStorage.setItem("sht_user", JSON.stringify(state.user));
    welcomeMessage.textContent = `Welcome back, ${user.name}!`;
    profileSummary.textContent = `You have logged ${user.entries} wellness entr${
      user.entries === 1 ? "y" : "ies"
    }.`;
  } catch (error) {
    console.error(error);
  }
}

async function loadSummary() {
  summaryList.innerHTML = "<li>Loading...</li>";
  try {
    const { summary } = await apiRequest("/api/metrics/summary");
    const items = [
      { label: "Entries", value: summary.entries },
      { label: "Avg Steps", value: summary.avg_steps },
      { label: "Avg Calories", value: summary.avg_calories },
      { label: "Avg Heart Rate", value: summary.avg_heart_rate },
      { label: "Avg Sleep", value: `${summary.avg_sleep} hrs` },
    ];
    summaryList.innerHTML = items
      .map((item) => `<li><span>${item.label}</span><span>${item.value}</span></li>`)
      .join("");
  } catch (error) {
    summaryList.innerHTML = `<li class="error">${error.message}</li>`;
  }
}

async function loadMetrics() {
  metricsTable.innerHTML = "<tr><td colspan=6>Loading...</td></tr>";
  const params = new URLSearchParams();
  if (filterStart.value) params.append("start", filterStart.value);
  if (filterEnd.value) params.append("end", filterEnd.value);
  const query = params.toString();
  try {
    const { metrics } = await apiRequest(`/api/metrics${query ? `?${query}` : ""}`);
    if (metrics.length === 0) {
      metricsTable.innerHTML = "<tr><td colspan=6>No entries yet. Add your first record!</td></tr>";
      return;
    }
    metricsTable.innerHTML = metrics
      .map(
        (metric) => `
        <tr>
          <td>${metric.recorded_for}</td>
          <td>${metric.steps}</td>
          <td>${metric.calories}</td>
          <td>${metric.heart_rate}</td>
          <td>${metric.sleep_hours}</td>
          <td>${metric.notes || "-"}</td>
        </tr>`
      )
      .join("");
  } catch (error) {
    metricsTable.innerHTML = `<tr><td colspan=6>${error.message}</td></tr>`;
  }
}

async function loadDashboard() {
  if (!state.token) {
    dashboard.classList.add("hidden");
    authSection.classList.remove("hidden");
    return;
  }
  authSection.classList.add("hidden");
  dashboard.classList.remove("hidden");
  await Promise.all([loadProfile(), loadSummary(), loadMetrics()]);
}

if (state.token) {
  loadDashboard().catch(() => {
    state.token = null;
    localStorage.removeItem("sht_token");
    localStorage.removeItem("sht_user");
  });
}
