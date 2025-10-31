# Smart Health Tracker

Smart Health Tracker is a full-cycle capstone project that now ships with a working wellness logging prototype. Users can register, record daily health metrics (steps, calories, heart rate, sleep) and review personalized summaries that surface trends and insights.

## 🚀 Current Capabilities
- Web dashboard with authentication, daily metric capture, filtering, and 30-day wellness summaries.
- Lightweight Python backend that persists data with SQLite and exposes JSON APIs secured by session tokens.
- Comprehensive SDLC/STLC/defect documentation to support academic delivery and reporting.

## 🗂️ Repository Structure
```
├── backend/
│   └── app.py                # Zero-dependency Python API + static file server
├── docs/
│   ├── Defect_Life_Cycle.md
│   ├── Final_Report_Template.md
│   ├── SDLC.md
│   ├── SRS.md
│   └── STLC.md
├── web/
│   ├── app.js                # Browser dashboard logic (vanilla JS)
│   ├── index.html            # UI shell rendered by the backend
│   └── styles.css            # Responsive styling for auth + dashboard views
└── README.md
```

SQLite data (`backend/health_tracker.db`) is created on first launch. You can safely delete the file to reset the environment.

## 📄 Key Documents
- **[SRS](docs/SRS.md):** Functional & non-functional requirements, use cases, technology stack.
- **[SDLC Plan](docs/SDLC.md):** Agile sprint roadmap with phase-specific activities.
- **[STLC Plan](docs/STLC.md):** Testing strategy, deliverables, and metrics.
- **[Defect Life Cycle](docs/Defect_Life_Cycle.md):** Workflow, severity matrix, and reporting templates.
- **[Final Report Template](docs/Final_Report_Template.md):** Outline for compiling end-of-project findings.

## 🧭 Prototype Architecture

| Layer        | Technology | Highlights |
| ------------ | ---------- | ---------- |
| Frontend UI  | Vanilla HTML, CSS, JavaScript | Responsive login + dashboard, fetch-based API integration, local session storage. |
| Backend API  | Python standard library (`http.server`, `sqlite3`) | Provides `/api/auth`, `/api/metrics`, `/api/user` endpoints with PBKDF2 password hashing and token authentication. |
| Database     | SQLite      | Auto-initialized schema (`users`, `sessions`, `metrics`) stored locally for ease of testing. |

Refer to the SDLC and STLC documentation for extended design, testing, and rollout guidance.

## 🧪 Getting Started

### Prerequisites
- Python 3.9+ (standard library only, no additional packages required)
- A modern browser such as Chrome, Edge, Firefox, or Safari

### Run the Prototype Locally
1. **Open a terminal in the project root.**
2. **Start the backend + static file server** (this also creates the SQLite database on first launch):
   ```bash
   python backend/app.py
   ```
   The server listens on [http://localhost:8000](http://localhost:8000) by default. Set the `PORT` environment variable before running the command if you need to use a different port (for example, `PORT=8080 python backend/app.py`).
3. **Visit the dashboard** by opening [http://localhost:8000](http://localhost:8000) in your browser. The index page is served directly from the backend, so there is no separate web build step.

### Workflow
1. Register a new account on the landing page.
2. Sign in to receive a secure session token stored in the browser.
3. Add daily health entries with steps, calories, heart rate, sleep, and notes.
4. Filter historical data by date range and monitor 30-day averages in the summary panel.

### Resetting Data
Stop the server and delete `backend/health_tracker.db` to start fresh.

## ✅ Next Steps
- Expand API test coverage (unit + integration) according to the STLC.
- Introduce analytics/alerts derived from thresholds defined in the SRS.
- Implement a companion mobile client (Flutter/React Native) using the same REST API.
- Automate deployment and regression testing through CI/CD pipelines.
