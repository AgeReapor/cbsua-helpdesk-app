# Software Requirements Specification

**System:** CBSUA Digital Helpdesk and Ticketing System  
**Document ID:** CBSUA-SRS-001  
**Version:** 1.0 (handoff baseline)  
**Status:** Baseline for stakeholder validation  
**Prepared:** 2026-11-12  
**Initial operational office:** ICT Office  
**Hosting/runtime direction:** CBSUA Pilot-managed local Frappe platform  
**Product foundation:** CBSUA Frappe Helpdesk fork

> This specification defines the institutional product requirements. Pilot is the local hosting and orchestration layer; it is not the ticketing product. The diagrams and conceptual data model describe the logical system, not an assertion about exact DocTypes, tables, or deployed topology.

## Document control

| Field | Value |
|---|---|
| Owner | CBSUA project/service owner (to be assigned) |
| Technical custodian | CBSUA ICT / application team (to be assigned) |
| Approvers | ICT service owner, project sponsor, privacy/security representative (names pending) |
| Source baseline | Existing `docs/SRS.md`, `docs/workflows.md`, `docs/architecture.md`, `docs/decisions.md` |
| Related architecture | [System architecture and Mermaid models](architecture.md) |
| Related delivery lifecycle | [RPM-aligned lifecycle](handoff/rpm-lifecycle.md) |

## 1. Introduction

### 1.1 Purpose

This SRS specifies the outcomes, system boundaries, actors, behaviors, constraints, quality attributes and acceptance conditions for the CBSUA Digital Helpdesk and Ticketing System. It is intended to support stakeholder validation, architecture, implementation, verification, release planning and handover.

Requirements are written to be individually identifiable and testable. A feature is not accepted merely because a screen or configuration exists; evidence must demonstrate the required behavior.

### 1.2 Product scope

The system provides a shared digital channel for submitting and tracking service requests, and a controlled workspace for authorized service personnel to receive, classify, queue, assign, process, communicate about and resolve tickets.

The initial release serves the ICT Office. The solution is designed to support later office onboarding without separate Helpdesk installations, but Registrar, Admissions and Cashier are not enabled in Phase 1.

### 1.3 In scope

- Customer/requester ticket submission and permitted tracking.
- Ticket reference, classification, priority and status.
- ICT office/team queue and assignment.
- Agent and manager workspaces and role-based actions.
- Customer-visible replies and internal comments.
- Information requests, reassignment, escalation, resolution and closure.
- Approved notifications and service targets.
- Queue monitoring and operational reporting.
- Staff account lifecycle and access administration.
- A controlled, testable procedure for onboarding additional offices.
- CBSUA branding and narrowly scoped institutional extensions where native configuration is insufficient.

### 1.4 Out of scope

Unless separately approved through change control, the system does not provide:

- A general-purpose CRM, sales or marketing automation.
- Student Information System, enrollment or admissions processing.
- Payment processing or cashier transaction processing.
- Registrar document-processing workflows.
- Physical walk-in token generation, counter displays or turn calling.
- A replacement ticket engine or a second Helpdesk product.
- Telephony/call-center operations merely because the Telephony app is a declared software dependency.

**Queueing definition:** Queueing means digital ticket queues and assignment states. It does not mean a physical service-counter queue.

### 1.5 Normative language

The terms **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **MAY** and **OPTIONAL**, when written in capitals, express requirement strength consistent with BCP 14 (RFC 2119 and RFC 8174).

### 1.6 References

- [Problem-Based-SRS Agent methodology](https://github.com/RafaelGorski/Problem-Based-SRS/blob/main/agents/problem-based-srs/AGENT.md) — business context → customer problems → software glance → customer needs → software vision → functional requirements; Mermaid UML diagrams and traceability validation.
- [Problem-Based-SRS project](https://github.com/RafaelGorski/Problem-Based-SRS) — Gorski & Stadzisz problem-first requirements method.
- [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) — requirements engineering and requirements specification guidance.
- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174) — normative keywords.
- [CBSUA Pilot](https://github.com/AgeReapor/cbsua-app-pilot) — local host, bench/site and app lifecycle.
- [CBSUA Frappe fork](https://github.com/AgeReapor/cbsua-app-frappe), [CBSUA Helpdesk fork](https://github.com/AgeReapor/cbsua-app-helpdesk), [CBSUA Telephony fork](https://github.com/AgeReapor/cbsua-app-telephony) — platform/product/dependency sources.

## 2. Business context (BC)

### BC-01 — Institutional context

CBSUA requires a consistent digital mechanism for receiving, tracking and coordinating service requests. The first operational service owner is the ICT Office. Additional offices may join later under explicit approval and access-control validation.

### BC-02 — Current situation

The project baseline anticipates that requests may arrive through fragmented communication channels and be difficult to track consistently. The exact current-state volumes, channels, processing times and baseline service performance have not yet been measured; they MUST be established during discovery rather than fabricated.

### BC-03 — Desired outcome

Provide one institutional Helpdesk platform where a requester can submit and follow a permitted request and where authorized staff can manage a visible, accountable ticket lifecycle.

### BC-04 — Business principles

| ID | Principle | Classification |
|---|---|---|
| BP-01 | ICT is the only operational destination in the first release. | Mandatory |
| BP-02 | Future offices remain disabled until their onboarding and authorization tests pass. | Mandatory |
| BP-03 | Use native Helpdesk capabilities before adding custom code. | Mandatory |
| BP-04 | A user must only access tickets and actions within their authorized scope. | Mandatory |
| BP-05 | Ticket activity must be traceable and support operational accountability. | Mandatory |
| BP-06 | Hosting operations belong to Pilot; ticket behavior belongs to Helpdesk and its CBSUA extension. | Mandatory |
| BP-07 | Physical walk-in queueing and unrelated institutional systems are separate scope decisions. | Mandatory |

### BC-05 — Success measures

The project SHALL measure, once baseline data and targets are approved:

- percentage of ICT requests captured as tickets;
- time from submission to first response;
- time from submission to resolution;
- number and age of unassigned tickets;
- tickets by category, priority and status;
- SLA attainment where the required timestamps and calendars are available;
- customer-visible update completeness;
- authorization test pass rate;
- successful backup restoration evidence.

Numerical service targets are intentionally TBD until the ICT service owner approves them.

## 3. Customer problems (CP — WHY)

Problem statements describe adverse conditions, not proposed features.

| ID | Customer problem | Impacted stakeholders | Classification |
|---|---|---|---|
| CP-01 | CBSUA requesters lack a consistently traceable way to submit and follow service requests across the initial ICT service. | Students, employees, other requesters | Obligation |
| CP-02 | ICT personnel lack a single, consistently visible work queue for incoming requests, ownership and progress. | ICT agents and managers | Obligation |
| CP-03 | Requesters and service personnel can lose context when clarifications, replies and work history are scattered across channels. | Requesters, agents | Expectation |
| CP-04 | Service owners cannot reliably assess workload, response and resolution performance without consistent ticket records and reporting. | ICT managers, administrators | Expectation |
| CP-05 | A shared multi-office platform can expose confidential tickets if office/team authorization is incomplete or inconsistently enforced. | All offices and requesters | Mandatory risk |
| CP-06 | A locally hosted platform becomes difficult to maintain if hosting lifecycle, framework, product and institution-specific code have unclear ownership. | ICT administrators and maintainers | Expectation |

These problems are derived from the existing project scope and architecture decisions. Their current-state magnitude and baseline metrics require stakeholder confirmation.

## 4. Software glance (SG — solution outline)

### 4.1 Positioning

The CBSUA Digital Helpdesk is a shared, browser-accessible ticketing service built on Frappe Helpdesk. It provides requester and staff experiences, ticket lifecycle management, controlled team queues and reporting. It is hosted locally through CBSUA Pilot.

### 4.2 Major capabilities

1. Requester intake and permitted ticket tracking.
2. Ticket classification and ICT routing.
3. ICT queue, assignment and workload management.
4. Ticket communication and work history.
5. Status lifecycle, resolution and closure.
6. Staff identity, roles and authorization.
7. Notifications and service targets.
8. Operational reporting.
9. Future office onboarding controls.
10. CBSUA-specific configuration and extension boundary.

### 4.3 System boundary

The system boundary and external actors are illustrated in [Architecture §2 — C4 context](architecture.md#2-c4-level-1-system-context). The hosting containers and logical components are in [Architecture §3–4](architecture.md#3-c4-level-2-container-view).

## 5. Customer needs (CN — WHAT)

Each need describes an outcome that the system must provide. Needs are linked to their originating customer problems.

| ID | Customer need | Parent problem(s) | Outcome |
|---|---|---|---|
| CN-01.1 | Requesters need a dependable way to submit an ICT service request and receive a unique reference. | CP-01 | Requests are captured and identifiable. |
| CN-01.2 | Requesters need to see only the status and communications they are authorized to access. | CP-01, CP-05 | Follow-up is useful without disclosing other tickets. |
| CN-02.1 | ICT staff need a shared view of new, unassigned and active ICT tickets. | CP-02 | Work is visible and can be prioritized. |
| CN-02.2 | ICT managers need to allocate and monitor work within their authority. | CP-02, CP-04 | Ownership and workload are clear. |
| CN-03.1 | Requesters and agents need ticket-related communication and history in one context. | CP-03 | Clarifications and decisions remain associated with the ticket. |
| CN-04.1 | ICT managers need reliable views of ticket volume, status and workload. | CP-04 | Operational decisions can use consistent records. |
| CN-04.2 | Service owners need response and resolution performance information where data and policy permit. | CP-04 | Service performance can be reviewed. |
| CN-05.1 | Each staff member needs access limited to their authorized role and office/team scope. | CP-05 | Cross-office disclosure and unauthorized actions are prevented. |
| CN-05.2 | Administrators need a controlled way to provision, disable and audit staff access. | CP-05 | Access lifecycle is manageable. |
| CN-06.1 | Maintainers need clear separation between hosting, framework, product and CBSUA-specific behavior. | CP-06 | Changes have an identifiable owner and upgrade path. |
| CN-06.2 | Service owners need a controlled way to add future offices without weakening existing access boundaries. | CP-05, CP-06 | Expansion is repeatable and safe. |

## 6. Software vision (SV — HOW at architectural level)

### 6.1 Architecture decisions

- Pilot manages local host, benches, sites, app acquisition and operations.
- Frappe provides framework services such as authentication, permissions, persistence and background processing.
- Helpdesk owns ticketing product capabilities and ticket records.
- Telephony is a declared Helpdesk dependency; its user-facing capabilities are not automatically in Phase 1 scope.
- The CBSUA extension contains only institution-specific behavior that cannot be met safely through native Helpdesk configuration.
- One shared site is the logical target for multi-office operation; final production topology remains a separate decision.
- ICT is the only active office destination in Phase 1.

### 6.2 Logical architecture and data model

The architecture document contains Mermaid UML views:
- C4 Level 1 — system context;
- C4 Level 2 — containers and runtime services;
- C4 Level 3 — logical components;
- use-case view of requester, agent, manager and administrator interactions;
- conceptual entity-relationship model;
- UML class/domain model;
- ticket state machine;
- ticket submission and processing sequence;
- office authorization decision flow.

See [System architecture and Mermaid models](architecture.md).

### 6.3 Domain model constraints

The conceptual entities are not claims about physical database tables. The selected Helpdesk revision's DocTypes and supported APIs are authoritative. Prefer native fields and relationships. Any custom Office/Service mapping, ticket field, DocType or hook must be justified by a requirement and validated against the pinned application revisions.

## 7. Functional requirements (FR)

**Priority:** Must = required for Phase 1; Should = desirable for Phase 1 subject to product capability and approval; Future = required only when an additional office is onboarded.  
**Verification:** Test = executable functional test; Inspection = configuration/code/document inspection; Demonstration = witnessed workflow; Analysis = measured or reviewed evidence.

### 7.1 Request intake and requester access

| ID | Priority | Requirement | Verification |
|---|---|---|---|
| FR-01 | Must | The system SHALL allow a requester to submit a ticket through the approved customer-facing channel. | Test |
| FR-02 | Must | The system SHALL record a subject, description, requester identity/contact, creation timestamp and configured required fields. | Test |
| FR-03 | Must | The system SHALL assign each ticket a unique, human-referenceable identifier. | Test |
| FR-04 | Must | The system SHALL support approved ticket classification and priority values. | Test |
| FR-05 | Must | The system SHALL restrict requester ticket views and updates to tickets the requester is authorized to access. | Negative test |
| FR-06 | Should | Authorized agents SHOULD be able to create tickets on behalf of requesters for approved assisted-intake channels. | Demonstration |
| FR-07 | Must | The system SHALL associate customer-visible communication with its ticket. | Test |

### 7.2 Office identification and routing

| ID | Priority | Requirement | Verification |
|---|---|---|---|
| FR-08 | Must | Each ticket SHALL be associated with one responsible office or service team. | Test |
| FR-09 | Must | During Phase 1, ICT SHALL be the only enabled customer-facing office destination. | Test/Inspection |
| FR-10 | Must | The logical design SHALL support future office onboarding within the shared Helpdesk product without requiring a separate ticketing installation per office. | Architecture inspection |
| FR-11 | Must | The system SHALL route each ticket to the configured responsible Phase 1 service team. | Test |
| FR-12 | Must | Authorized staff SHALL be able to assign a ticket to a team and, where supported, an individual agent. | Test |
| FR-13 | Must | Authorized managers SHALL be able to reassign or escalate tickets within their permitted scope. | Test |
| FR-14 | Future | After approval and onboarding, requesters SHALL be able to select from enabled office destinations only. | Test |

### 7.3 Queue and assignment management

| ID | Priority | Requirement | Verification |
|---|---|---|---|
| FR-15 | Must | Authorized ICT staff SHALL be able to view unassigned ICT tickets. | Test |
| FR-16 | Must | Agents SHALL be able to view tickets assigned to them and/or their authorized team, subject to access policy. | Test |
| FR-17 | Must | The system SHALL support authorized manual ticket assignment. | Test |
| FR-18 | Should | The system SHOULD support automatic assignment using a validated native Helpdesk capability. | Demonstration |
| FR-19 | Should | A workload-based or round-robin assignment strategy SHOULD be considered only after ICT approves its rules and the selected release supports it. | Analysis |
| FR-20 | Must | ICT managers SHALL be able to monitor pending and active tickets within their authorized scope. | Test |
| FR-21 | Must | Authorized staff SHALL be able to filter or view tickets by supported status, priority, team, assignee, category and age. | Test |

### 7.4 Ticket processing and resolution

| ID | Priority | Requirement | Verification |
|---|---|---|---|
| FR-22 | Must | Agents SHALL be able to view ticket details and requester information necessary to process an authorized request. | Test |
| FR-23 | Must | Agents SHALL be able to send customer-visible replies. | Test |
| FR-24 | Must | Agents SHALL be able to add internal comments that are not visible to requesters. | Negative test |
| FR-25 | Must | Agents SHALL be able to update ticket status and priority within their permissions. | Test |
| FR-26 | Must | Agents SHALL be able to request additional information from requesters. | Demonstration |
| FR-27 | Must | Agents SHALL be able to record a resolution and resolve a ticket. | Test |
| FR-28 | Must | The system SHALL support closure according to the approved ICT workflow. | Test |
| FR-29 | Should | The system SHOULD support reopening a ticket when permitted by the approved workflow. | Test |
| FR-30 | Must | Ticket conversation and status history SHALL remain associated with the ticket. | Test/Inspection |

### 7.5 Staff authentication and authorization

| ID | Priority | Requirement | Verification |
|---|---|---|---|
| FR-31 | Must | Staff SHALL authenticate before accessing agent functions. | Negative test |
| FR-32 | Must | Only authorized ICT personnel SHALL receive ICT agent access during Phase 1. | Inspection/Test |
| FR-33 | Must | Authorized administrators SHALL be able to invite, activate and deactivate staff accounts using supported platform functions. | Test |
| FR-34 | Must | Staff SHALL receive roles and team membership appropriate to their approved duties. | Inspection/Test |
| FR-35 | Must | Disabled staff accounts SHALL be unable to access agent functions. | Negative test |
| FR-36 | Must | Agents SHALL NOT access tickets outside their authorized scope. | Negative test |
| FR-37 | Must | Office managers SHALL NOT receive platform-wide administration rights unless explicitly approved. | Negative test |
| FR-38 | Future | Authorized staff from each new office SHALL be provisioned during that office's approved onboarding. | Test |

### 7.6 Service targets and notifications

| ID | Priority | Requirement | Verification |
|---|---|---|---|
| FR-39 | Must | The ICT service owner SHALL approve first-response and resolution targets before production use. | Approval record |
| FR-40 | Must | The system SHALL apply the approved service policy and working calendar using capabilities verified in the selected Helpdesk release. | Test |
| FR-41 | Must | Relevant agents SHALL be notified of new tickets and relevant assignment changes through approved configured channels. | Test |
| FR-42 | Must | Requesters SHALL receive configured notifications for approved ticket events. | Test |
| FR-43 | Must | Authorized staff SHALL be able to identify tickets approaching or exceeding service targets where supported by the selected release. | Demonstration |
| FR-44 | Future | Each additional office SHALL have separately approved service targets and working calendars where required. | Approval/Test |

### 7.7 Reporting and monitoring

| ID | Priority | Requirement | Verification |
|---|---|---|---|
| FR-45 | Must | ICT managers SHALL be able to monitor ticket counts by status within their authorized scope. | Test |
| FR-46 | Must | ICT managers SHALL be able to monitor unassigned and assigned workload. | Test |
| FR-47 | Must | Authorized users SHALL be able to review response and resolution performance where the required data is available. | Demonstration |
| FR-48 | Must | System administrators SHALL be able to monitor platform-wide ticket activity. | Test |
| FR-49 | Future | Reports SHALL support office-level filtering and approved consolidated cross-office reporting. | Test |

## 8. Non-functional requirements (NFR)

| ID | Quality attribute | Requirement | Verification |
|---|---|---|---|
| NFR-01 | Security | Production browser access SHALL use HTTPS. | Inspection |
| NFR-02 | Security | Staff access to agent functions SHALL require authentication. | Negative test |
| NFR-03 | Security | Ticket access SHALL enforce role, team and office authorization server-side. | Negative test |
| NFR-04 | Confidentiality | Office users SHALL NOT access another office's tickets unless explicitly authorized. | Cross-office test |
| NFR-05 | Recoverability | Ticket database records and associated file storage SHALL be covered by a coordinated backup and recovery procedure. | Restore test |
| NFR-06 | Maintainability | The platform SHALL support additional offices without replacing the ticketing product. | Architecture inspection |
| NFR-07 | Maintainability | Native Helpdesk configuration SHOULD be preferred over custom code when it meets the requirement. | Design review |
| NFR-08 | Compatibility | Customizations SHALL be version-controlled, documented and tested against the selected Frappe/Helpdesk revisions. | CI/release evidence |
| NFR-09 | Usability | Requester and agent interfaces SHALL be usable on commonly supported desktop and mobile browsers. | Compatibility test |
| NFR-10 | Auditability | Ticket-processing and administrative activities SHALL be auditable to the extent supported by the platform and configured logging. | Inspection |
| NFR-11 | Operability | Production operation SHALL include monitoring, backup, restore testing and documented operational ownership. | Readiness review |
| NFR-12 | Reproducibility | Each accepted release SHALL record immutable revisions of Pilot, Frappe, Helpdesk, Telephony and the CBSUA extension, plus relevant runtime versions. | Release manifest inspection |
| NFR-13 | Privacy | Collection, visibility, retention and disposal of requester data and attachments SHALL follow institutionally approved privacy and records policies. | Policy review |
| NFR-14 | Extensibility | CBSUA-specific code SHALL remain isolated from Pilot, Frappe and generic Helpdesk product responsibilities. | Architecture/code review |

Quantitative availability, response-time, throughput, retention and recovery-time objectives are TBD. They require service-owner approval and a measured operational baseline.

## 9. External interface requirements

### 9.1 User interfaces

- Requester portal: submit a request and view permitted ticket details/updates.
- Agent workspace: inspect, classify, assign, communicate about and resolve authorized tickets.
- Manager views: monitor team queue, workload and service performance within authorized scope.
- Administrator interfaces: manage users, roles, teams, configuration and platform/site operations according to separate privileges.

### 9.2 Software interfaces

- Frappe Helpdesk provides ticketing behavior and product interfaces.
- Frappe Framework provides authentication, permissions, persistence, jobs and other platform services.
- Pilot provides host/bench/site/app lifecycle operations and is not called as a ticket workflow engine.
- Telephony is a declared app dependency of the inspected Helpdesk fork; feature activation is a separate scope decision.
- Email integration is optional unless Phase 1 stakeholders approve email intake or notifications as a launch requirement.

Exact API names, DocTypes, field names and integration protocols MUST be validated against the pinned release set before implementation.

## 10. Data requirements and conceptual entities

The conceptual model is documented in [Architecture §5 — UML domain and ER model](architecture.md#5-domain-model-uml-and-entity-relationship-model).

At minimum, the logical domain includes:
- User and staff identity;
- Office/service team and team membership;
- Requester/customer/contact;
- Ticket;
- Ticket communication/comment;
- Assignment;
- Service policy/SLA;
- Attachment/reference to file storage;
- Ticket status/event history.

The model MUST preserve ticket ownership, requester association, team scope and audit/history relationships. Physical schema and native DocType mapping are implementation decisions subject to inspection of the selected Helpdesk revision.

## 11. Business workflows and state model

The intended ICT lifecycle is:

1. Requester submits an ICT request.
2. Helpdesk creates a ticket and reference.
3. Ticket enters the ICT team queue.
4. Authorized staff assign an agent.
5. Agent investigates and communicates with the requester.
6. If information is needed, the ticket waits for requester input and resumes when a response arrives.
7. Agent records the resolution.
8. The ticket is closed under the approved policy.

The conceptual lifecycle is in [Architecture §6 — Ticket lifecycle](architecture.md#6-ticket-lifecycle-uml-state-machine). Exact state labels and transitions MUST be reconciled with the selected Helpdesk release; diagram labels are conceptual, not claims about built-in status names.

## 12. Security and authorization requirements

The authorization model SHALL be enforced server-side. Hiding records in the user interface is insufficient.

The verification plan MUST include positive and negative tests for:
- ticket list and direct URL access;
- search and reports;
- customer-visible replies versus internal comments;
- attachments and file downloads;
- assignment, reassignment and escalation;
- exports and bulk operations;
- disabled accounts and revoked memberships;
- manager versus platform administrator privileges;
- future office boundaries once additional offices are onboarded.

A successful ICT-only test does not prove multi-office isolation. Future office onboarding requires cross-office tests with separate test identities and synthetic records.

## 13. Deployment and operational constraints

### 13.1 Target local hosting model

- Pilot: local host, bench/site lifecycle, app staging/validation and process/task orchestration.
- Frappe: framework runtime.
- Helpdesk: ticketing product.
- Telephony: declared Helpdesk dependency.
- CBSUA extension: institution-specific application behavior only.

### 13.2 Compatibility gate

The inspected Helpdesk fork metadata declares Frappe `>=17.0.0-dev,<18.0.0` and Telephony `>=0.0.1,<1.0.0`; the inspected Frappe fork declares Python `>=3.14,<3.15`. Historical Frappe 16 setup instructions are superseded for these inspected revisions.

The CBSUA extension MUST declare Pilot-compatible Frappe app dependencies using tested ranges. No full-stack compatibility claim is made until Pilot validation, clean site installation, migrations, asset build and smoke tests pass for immutable revisions.

### 13.3 Production readiness

Local hosting is not equivalent to production readiness. Production requires an approved topology, HTTPS, access restrictions, monitoring, coordinated backup, restore testing, operational ownership, escalation and a rollback plan.

## 14. Phase 1 acceptance criteria

Phase 1 is accepted only when all applicable Must requirements pass and the ICT service owner approves the resulting workflow.

| ID | Acceptance condition | Related requirements |
|---|---|---|
| AC-01 | A requester submits an ICT ticket through the approved channel and receives a unique reference. | FR-01–04 |
| AC-02 | The new ticket appears in the ICT queue and is associated with the correct team. | FR-08–12, FR-15 |
| AC-03 | An authorized ICT agent can view and process the ticket. | FR-16, FR-22 |
| AC-04 | Agent can send a requester-visible reply and a separate internal comment. | FR-23–24 |
| AC-05 | Agent can update permitted status, priority and assignment. | FR-12, FR-17, FR-25 |
| AC-06 | Agent can request information, record resolution and complete approved closure. | FR-26–30 |
| AC-07 | Requester can view only tickets allowed by the approved identity/access policy. | FR-05, NFR-03–04 |
| AC-08 | ICT manager can monitor queue and workload within scope. | FR-20–21, FR-45–47 |
| AC-09 | Non-ICT staff cannot access ICT agent functions without explicit authorization. | FR-32, NFR-03–04 |
| AC-10 | Staff invitation, activation and deactivation behavior is tested. | FR-33–35 |
| AC-11 | Approved SLA and notification behavior is demonstrated. | FR-39–43 |
| AC-12 | Backup and restore of database and file data is demonstrated. | NFR-05, NFR-11 |
| AC-13 | The release manifest records exact revisions and runtime versions. | NFR-08, NFR-12 |
| AC-14 | The ICT service owner accepts the workflow and operational runbook. | Governance gate |

## 15. Assumptions, constraints and open questions

| ID | Question / assumption | Owner / decision required | Blocking impact |
|---|---|---|---|
| OQ-01 | Will customers use authenticated accounts, anonymous submission with secure follow-up, or a mixed model? | Service owner + privacy representative | Requester access design |
| OQ-02 | Is email-to-ticket intake required for Phase 1, or is portal intake sufficient? | ICT service owner | Integration scope |
| OQ-03 | What ICT categories and subcategories are required? | ICT service owner | Intake configuration |
| OQ-04 | What priority definitions and response/resolution targets apply? | ICT service owner | SLA acceptance |
| OQ-05 | What status transitions, reopen and closure rules are required? | ICT service owner | Workflow acceptance |
| OQ-06 | Who may reassign, escalate, merge or close tickets? | ICT service owner | Role matrix |
| OQ-07 | What working calendars, holidays and shifts apply? | ICT service owner | SLA calculation |
| OQ-08 | What requester data and attachments may be collected, retained and disposed? | Privacy/records authority | Production approval |
| OQ-09 | Which exact Frappe, Helpdesk, Telephony and Pilot revisions will be pinned? | Technical lead | Compatibility gate |
| OQ-10 | Can native Helpdesk permissions provide complete team/office isolation? | Technical lead + security reviewer | Security release gate |
| OQ-11 | Is an explicit Office entity required, or is a team-to-office mapping sufficient? | Architect + ICT | Domain model |
| OQ-12 | Is physical walk-in token queueing a separate future project? | Sponsor | Scope boundary |
| OQ-13 | What production topology, backup schedule, RPO/RTO and monitoring are required? | Operations owner | Production readiness |
| OQ-14 | Must Telephony be installed on the site, and can its user-facing features remain unused? | Technical lead | Dependency/install plan |

## 16. Traceability and change control

The initial traceability chain is:

`CP → CN → FR/NFR → Architecture element → Test/Acceptance evidence`

See [Traceability matrix](traceability-matrix.md). Every new or changed requirement MUST have:
- a stable ID and rationale;
- a parent customer need and problem, or a documented constraint;
- a verification method and acceptance condition;
- an identified owner/approver;
- an impact assessment for architecture, data, security, compatibility and documentation.

Requirements changes are reviewed through the RPM-aligned progressive lifecycle. A requirement is not considered complete until its verification evidence is recorded.

## 17. Approval record

| Role | Name | Decision | Date |
|---|---|---|---|
| Project sponsor | TBD | Pending | TBD |
| ICT service owner | TBD | Pending | TBD |
| Technical lead | TBD | Pending | TBD |
| Privacy/security reviewer | TBD | Pending | TBD |

---
**End of specification.**
