# Smart Health Tracker - Defect Life Cycle & Tracking Process

## 1. Defect Workflow
1. **Identification:** Tester discovers issue during test execution and validates reproducibility.
2. **Logging:** Tester records defect in Jira/Trello/Excel with detailed steps, attachments, and severity.
3. **Triage:** QA Lead and Product Owner review severity/priority, assign to responsible developer.
4. **Assignment:** Developer accepts defect and begins investigation.
5. **Resolution:** Developer fixes defect, updates status to "Ready for Retest" with build number and notes.
6. **Verification:** Tester retests using provided build; if pass, mark "Closed"; if fail, revert to "Reopened".
7. **Closure:** Product Owner reviews closed defects during sprint review; document lessons learned for major incidents.

## 2. Status Values
- **New:** Defect logged, awaiting triage.
- **Assigned:** Ownership granted to developer/engineer.
- **In Progress:** Fix being implemented.
- **Ready for Retest:** Fix deployed to test environment.
- **Reopened:** Issue persists after retest.
- **Deferred:** Scheduled for future release (with justification).
- **Duplicate:** Matches existing defect entry.
- **Closed:** Verified and accepted by QA/Product Owner.

## 3. Severity & Priority Matrix
| Severity | Description | Priority Guidance |
| -------- | ----------- | ----------------- |
| Critical | System crash/data loss/security breach | P0 - Immediate fix |
| Major | Core feature unusable or incorrect results | P1 - Fix in current sprint |
| Moderate | Feature works with limitations or workaround | P2 - Schedule in next sprint |
| Minor | Cosmetic/UI discrepancies | P3 - Fix as time permits |
| Trivial | Typos or negligible issues | P4 - Optional |

## 4. Defect Report Template
- **Defect ID:** `SHT-<incremental number>`
- **Title:** Concise summary of issue.
- **Description:** Steps to reproduce, expected vs actual results.
- **Environment:** Build version, device/browser, OS.
- **Attachments:** Screenshots, logs, videos.
- **Severity/Priority:** Per matrix above.
- **Assigned To:** Developer responsible.
- **Status:** Current workflow status.
- **Comments:** Investigation notes and resolution details.

## 5. Sample Excel Columns
`ID | Summary | Module | Severity | Priority | Status | Assigned To | Reported By | Environment | Created On | Retest Date | Resolution`

## 6. Reporting & Metrics
- Daily defect count and severity distribution shared during stand-ups.
- Weekly defect trend chart (opened vs closed) presented in sprint review.
- Defect leakage tracked between QA and UAT/production environments.

## 7. Tools & Integrations
- Jira/Trello integrated with GitHub for referencing commits and pull requests.
- Slack notifications for critical defect status changes.
- Dashboard widget summarizing open defects by module (web, mobile, backend).

## 8. Best Practices
- Ensure reproducibility before logging.
- Provide minimal test data set or credentials.
- Link defects to user stories/test cases for traceability.
- Retrospectives to analyze root cause of high-severity defects and implement preventive actions.
