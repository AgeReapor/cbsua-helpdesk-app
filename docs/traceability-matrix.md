# Requirements Traceability Matrix

**Document ID:** CBSUA-RTM-001  
**Version:** 1.0  
**Status:** Initial traceability baseline for validation

This matrix links customer problems (WHY) to customer needs (WHAT), system requirements (HOW), architecture elements and verification evidence. The mapping is intentionally many-to-many where one requirement contributes to more than one need or problem.

## 1. Problem → Need → Requirement traceability

| Customer problem | Customer need | Functional requirements | Non-functional requirements | Architecture elements |
|---|---|---|---|---|
| CP-01 — Requesters lack a consistently traceable request channel | CN-01.1 — Submit ICT request and receive reference | FR-01, FR-02, FR-03, FR-04 | NFR-09, NFR-13 | Requester portal, Ticket intake, Ticket entity |
| CP-01 — Requesters lack permitted request follow-up | CN-01.2 — View only authorized ticket details and updates | FR-05, FR-07 | NFR-02, NFR-03, NFR-04, NFR-13 | Requester portal, Ticket, Ticket message, Authorization model |
| CP-02 — ICT lacks a shared visible work queue | CN-02.1 — Shared new/unassigned/active queue | FR-08, FR-09, FR-11, FR-15, FR-16, FR-21 | NFR-06 | Office, Service Team, Ticket, Team queue |
| CP-02 — Work ownership is unclear | CN-02.2 — Allocate and monitor work | FR-12, FR-13, FR-17, FR-20 | NFR-10 | Assignment, Team membership, Ticket event |
| CP-03 — Communication and context are fragmented | CN-03.1 — Communication and history in ticket context | FR-07, FR-23, FR-24, FR-26, FR-30 | NFR-10, NFR-13 | Ticket message, Ticket event, Notification |
| CP-04 — Service owners lack reliable workload evidence | CN-04.1 — Monitor volume, status and workload | FR-20, FR-21, FR-45, FR-46, FR-48 | NFR-10, NFR-11 | Manager views, Reporting, Ticket |
| CP-04 — Response/resolution performance is unclear | CN-04.2 — Review service performance | FR-39, FR-40, FR-43, FR-44, FR-47 | NFR-10, NFR-11 | Service policy, Ticket timestamps, Reporting |
| CP-05 — Shared platform may expose confidential tickets | CN-05.1 — Restrict access by role and office/team | FR-05, FR-32, FR-36, FR-37 | NFR-02, NFR-03, NFR-04, NFR-13 | Identity, Permission, Office, Team membership, Authorization model |
| CP-05 — Staff access lifecycle may be uncontrolled | CN-05.2 — Provision, disable and audit staff | FR-31, FR-33, FR-34, FR-35, FR-38 | NFR-02, NFR-10 | User, Team membership, Frappe identity/permission |
| CP-06 — Platform ownership and code boundaries may be unclear | CN-06.1 — Separate hosting/framework/product/institution behavior | FR-10 | NFR-06, NFR-07, NFR-08, NFR-12, NFR-14 | Pilot control plane, Frappe, Helpdesk, Telephony, CBSUA extension |
| CP-05 / CP-06 — Future onboarding may weaken existing boundaries | CN-06.2 — Controlled office onboarding | FR-10, FR-14, FR-38, FR-44, FR-49 | NFR-04, NFR-06, NFR-08, NFR-14 | Office onboarding flow, Office, Service Team, Authorization model |

## 2. Functional requirement verification index

| Requirement range | Verification focus | Minimum evidence |
|---|---|---|
| FR-01–07 | Requester intake and communication | Create ticket, reference, requester identity and visibility tests |
| FR-08–14 | Office association and routing | ICT-only destination and correct routing test; future destination hidden |
| FR-15–21 | Queue and assignment | Agent/manager queue tests and assignment evidence |
| FR-22–30 | Processing and resolution | Reply/internal comment visibility, status history and resolution tests |
| FR-31–38 | Authentication and authorization | Role provisioning, disabled account and negative access tests |
| FR-39–44 | Service targets and notifications | Approved policy, calendar boundary and notification test evidence |
| FR-45–49 | Reporting and monitoring | ICT workload and status reports; future office filters after onboarding |

## 3. Non-functional requirement verification index

| Requirement | Evidence |
|---|---|
| NFR-01 | Production HTTPS configuration inspection |
| NFR-02 | Unauthenticated staff access denied |
| NFR-03 | Server-side permission tests for every protected operation |
| NFR-04 | Cross-office negative test suite, including direct URLs and attachments |
| NFR-05 | Successful database and file backup restoration |
| NFR-06 | Architecture review showing office onboarding without a separate Helpdesk product |
| NFR-07 | Design review documenting why native configuration is or is not sufficient |
| NFR-08 | CI/release evidence against pinned framework/product revisions |
| NFR-09 | Browser/device compatibility test results |
| NFR-10 | Audit log inspection for ticket and administrative events |
| NFR-11 | Monitoring, backup, restore and named operations owner |
| NFR-12 | Immutable release manifest |
| NFR-13 | Approved privacy/records policy and matching configuration |
| NFR-14 | Repository/layer review and extension test suite |

## 4. Phase 1 acceptance traceability

| Acceptance criterion | Requirement set | Evidence artifact |
|---|---|---|
| AC-01 Requester submits and receives reference | FR-01–04 | Requester intake test |
| AC-02 Ticket enters ICT queue | FR-08–12, FR-15 | Routing and queue test |
| AC-03 Authorized agent processes ticket | FR-16, FR-22 | Agent role test |
| AC-04 Customer reply and internal comment are distinct | FR-23–24 | Visibility test |
| AC-05 Permitted status, priority and assignment updates | FR-12, FR-17, FR-25 | Workflow test |
| AC-06 Information request, resolution and closure | FR-26–30 | End-to-end lifecycle test |
| AC-07 Requester sees only permitted tickets | FR-05, NFR-03–04 | Requester isolation suite |
| AC-08 ICT manager monitors queue/workload | FR-20–21, FR-45–47 | Manager report demonstration |
| AC-09 Non-ICT staff denied ICT agent access | FR-32, NFR-03–04 | Negative role test |
| AC-10 Staff account lifecycle works | FR-33–35 | Provision/disable test |
| AC-11 SLA and notification behavior matches approved policy | FR-39–43 | Policy and notification test |
| AC-12 Backup and restore verified | NFR-05, NFR-11 | Restore report |
| AC-13 Immutable revisions recorded | NFR-08, NFR-12 | Release manifest |
| AC-14 ICT owner accepts workflow | All Phase 1 Must requirements | Signed acceptance record |

## 5. Traceability validation rules

A review is incomplete if:
- a customer need has no parent customer problem;
- a customer problem has no corresponding customer need or an explicitly accepted reason;
- a functional requirement has no parent need;
- a requirement has no verification method;
- a Must requirement has no Phase 1 acceptance evidence;
- an architecture element has no requirement or platform responsibility;
- a test checks only UI visibility while bypass paths remain untested.

The traceability chain is reviewed at each RPM lifecycle gate and whenever a requirement or architecture boundary changes.

## 6. Known traceability limitations

- CP statements are grounded in the existing project scope, not measured operational research. Stakeholders must validate the problem statements and baseline impacts.
- CN and CP mappings are an initial analytical model and require workshop validation.
- Requirements are carried forward from the existing SRS with clarified language and verification fields.
- Exact Helpdesk DocType mapping and test automation identifiers are pending pinned-version inspection.
- Quantitative NFR thresholds remain TBD until service owners approve measurable targets.
