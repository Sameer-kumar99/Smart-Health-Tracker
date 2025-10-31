# Smart Health Tracker - SDLC Plan (Agile Model)

## 1. Overview
- **Model Chosen:** Agile Scrum with two-week sprints.
- **Project Duration:** 11 weeks (aligns with academic schedule).
- **Team Roles:**
  - Product Owner: Oversees backlog prioritization.
  - Scrum Master: Facilitates ceremonies, removes blockers.
  - Development Team: Web developers, mobile developers, backend engineer, QA engineer.

## 2. Sprint Breakdown
| Sprint | Weeks | Goals | Key Deliverables |
| ------ | ----- | ----- | ---------------- |
| Sprint 0 | Week 1 | Project kickoff, requirement gathering | Draft SRS, initial backlog |
| Sprint 1 | Weeks 2-3 | Architecture & UI design | Wireframes, architecture diagrams, database schema |
| Sprint 2 | Weeks 4-5 | Core authentication & data models | Auth API, database collections/tables, basic mobile/web login |
| Sprint 3 | Weeks 6-7 | Health data logging & visualization | Data entry forms, API endpoints, dashboards |
| Sprint 4 | Weeks 8-9 | Insights, notifications, testing | Alert engine, integration tests, beta release |
| Sprint 5 | Week 10 | Hardening & deployment | Bug fixes, performance tuning, release candidate |
| Sprint 6 | Week 11 | Evaluation & maintenance | Final demo, documentation, retrospective |

## 3. Phase Activities
### Requirement Phase
- Conduct stakeholder interviews and survey potential users.
- Finalize SRS and obtain approval.
- Prioritize product backlog using MoSCoW method.

### Design Phase
- Create UI wireframes for key user flows (login, dashboard, data entry, insights).
- Define component architecture for React web app and Flutter mobile app.
- Specify REST API contracts and database schema diagrams.

### Implementation Phase
- Develop React web app with modular components and state management (Redux/Context API).
- Develop Flutter mobile app with shared domain models.
- Implement backend services (Node.js/Express) with secure endpoints.
- Configure Firebase/MySQL database and seed with test data.

### Testing Phase
- Execute unit and integration tests per STLC plan.
- Perform usability testing sessions with pilot users.
- Conduct performance benchmarks on critical APIs.

### Deployment Phase
- Set up CI/CD pipeline (GitHub Actions) for automated builds and deployments.
- Deploy backend to cloud environment (Heroku/Firebase/AWS).
- Release web app via Netlify/Vercel and mobile app as APK/TestFlight build for evaluation.

### Maintenance Phase
- Monitor application metrics and error logs.
- Prioritize post-evaluation improvements.
- Document lessons learned and prepare handoff materials.

## 4. Artifacts & Tools
- **Backlog Management:** Jira/Trello board with user stories, tasks, subtasks.
- **Documentation:** Confluence/Notion for sprint notes, diagrams stored under `/docs/`.
- **Version Control:** Git with branching strategy (main, develop, feature branches).
- **Communication:** Slack/Teams, weekly stand-ups, sprint reviews, retrospectives.

## 5. Risk Management
- **Risk:** Wearable API changes mid-project.
  - **Mitigation:** Abstract integration layer, maintain mock data for testing.
- **Risk:** Team bandwidth constraints during exams.
  - **Mitigation:** Adjust sprint scope, maintain buffer stories, cross-train teammates.
- **Risk:** Data privacy non-compliance.
  - **Mitigation:** Conduct security review, follow best practices, enable user data export/delete.

## 6. Acceptance Criteria
- All critical user stories completed and accepted by Product Owner.
- Defect leakage below agreed threshold during evaluation.
- Successful demonstration of web and mobile apps connected to live database.

## 7. Maintenance & Future Enhancements
- Post-evaluation backlog for advanced analytics, AI-based recommendations, and expanded wearable support.
- Plan quarterly releases with incremental improvements.
