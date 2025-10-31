# Smart Health Tracker - Software Requirement Specification

## 1. Introduction
- **Purpose:** Define the functional and non-functional requirements for the Smart Health Tracker web and mobile applications.
- **Scope:** Provide a cross-platform system for users to monitor key health metrics such as steps, calories, heart rate, and sleep, offering insights and alerts.
- **Definitions, Acronyms, Abbreviations:**
  - **SHT:** Smart Health Tracker
  - **UI:** User Interface
  - **API:** Application Programming Interface
  - **NFR:** Non-functional Requirement
- **References:** Project roadmap, health device integration guidelines, wearable SDK documentation.

## 2. Overall Description
- **Product Perspective:** Hybrid system comprised of a web dashboard, mobile application, backend services, and persistent database. Optional integration with wearable APIs.
- **Product Functions:**
  - Secure user authentication and profile management.
  - Manual and automated health data capture.
  - Visualization dashboards (daily, weekly, monthly trends).
  - Personalized insights, recommendations, and alert notifications.
  - Goal management and progress tracking.
- **User Classes and Characteristics:**
  - **End Users:** Individuals tracking personal health metrics.
  - **Administrators:** Manage system configuration, monitor analytics.
  - **Wearable Integrators (optional):** Configure device APIs and troubleshoot integration issues.
- **Operating Environment:**
  - Web: Modern browsers (Chrome, Firefox, Edge, Safari).
  - Mobile: Android (API level 21+) or iOS (13+).
  - Backend: Node.js runtime with REST APIs hosted on cloud (e.g., AWS, Firebase functions).
  - Database: Cloud-based document (Firebase Firestore) or relational (MySQL) storage.
- **Design and Implementation Constraints:**
  - Must comply with data privacy regulations (GDPR-like best practices).
  - Utilize secure authentication (OAuth 2.0 / JWT).
  - Offline mode supported on mobile via local persistence.
- **Assumptions and Dependencies:**
  - Users own wearable devices capable of exposing REST/Bluetooth APIs (optional).
  - Stable internet connectivity for synchronization.
  - Third-party APIs remain available and reliable.

## 3. Functional Requirements
1. **Account Management**
   - Users can register with email/password or OAuth provider.
   - Users can view and update profile information.
   - Password recovery via email.
2. **Health Data Capture**
   - Users can manually log steps, calories, heart rate, and sleep duration.
   - System fetches metrics from integrated wearables on demand or scheduled intervals.
   - Backend validates incoming data for completeness and consistency.
3. **Dashboard & Visualization**
   - Users can view daily, weekly, and monthly summaries.
   - Charts and trend lines highlight progress toward goals.
   - Insights module surfaces anomalies (e.g., irregular sleep patterns).
4. **Goal & Alert Management**
   - Users can define goals for each metric and receive alerts when goals are met or missed.
   - Notifications delivered via email push (web) and push notifications (mobile).
5. **Data Synchronization**
   - Client applications sync with backend on login, on pull-to-refresh, and at scheduled intervals.
   - Conflict resolution prioritizes latest timestamp.
6. **Administration**
   - Admin panel for viewing aggregated usage statistics and managing system configuration.

## 4. Non-Functional Requirements
- **Performance:** API responses within 300 ms for 95% of requests; mobile app loads dashboard within 2 seconds on standard hardware.
- **Security:** Enforce HTTPS, secure storage of credentials, JWT expiration and refresh tokens, role-based authorization.
- **Reliability:** 99% uptime target during evaluation week; automated backups daily.
- **Usability:** Responsive design, WCAG 2.1 AA accessibility compliance, intuitive navigation with onboarding tutorials.
- **Scalability:** Support at least 1,000 concurrent users during demonstrations.
- **Maintainability:** Modular architecture with documented API contracts and unit tests covering >70% of core modules.
- **Portability:** Mobile app built with Flutter/React Native to support both Android and iOS from single codebase.

## 5. Use Case Diagrams
- **UC-01:** User logs in and views dashboard (actors: User, Authentication Service, Analytics Engine).
- **UC-02:** User logs new health entry (actors: User, Data Service, Database).
- **UC-03:** System sends health alert (actors: Notification Service, User).
- **UC-04:** Admin reviews aggregated analytics (actors: Admin, Admin Dashboard, Database).

> Diagram artifacts will be stored in `/docs/diagrams/` once created.

## 6. Technology Stack and Tools
- **Frontend (Web):** React, TypeScript, Material UI.
- **Frontend (Mobile):** Flutter with Dart (or React Native with TypeScript as alternative).
- **Backend:** Node.js (Express) or Firebase Cloud Functions.
- **Database:** Firebase Firestore (primary) with optional MySQL for relational reporting.
- **Authentication:** Firebase Auth / Auth0.
- **CI/CD:** GitHub Actions for automated tests and deployments.
- **Project Management:** Jira / Trello.
- **Testing Tools:** Jest, React Testing Library, Flutter test, Postman, Cypress.

## 7. Appendices
- **Glossary:** Dashboard, Metric, Goal, Insight, Alert.
- **Open Issues:** Final selection between Flutter and React Native pending team skill assessment.
