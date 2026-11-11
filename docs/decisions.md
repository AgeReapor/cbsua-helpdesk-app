# Architecture Decision Log

This log records decisions and decisions still requiring validation. Update it when a stakeholder or technical decision changes the baseline.

## ADR-001 — Use Frappe Helpdesk as the ticketing foundation

**Status:** Accepted

**Decision:** Use Frappe Helpdesk as the primary ticketing application. Do not build a separate ticket-management engine or treat Frappe CRM as the ticketing foundation.

**Rationale:** The project scope is ticket intake, queueing, assignment, communication, resolution, and service reporting. Using the dedicated Helpdesk application avoids duplicating its core capabilities.

**Consequences:** CBSUA work should focus on configuration, branding, office structure, access control, and narrowly scoped extensions.

## ADR-002 — One shared deployment with phased office onboarding

**Status:** Accepted

**Decision:** Use one shared Helpdesk deployment for CBSUA offices. Start with ICT; onboard Registrar, Admissions, and Cashier in later phases.

**Rationale:** A shared platform provides consistent ticket handling and reduces duplicated administration.

**Consequences:** Office/team isolation must be proven before production and re-tested for each new office.

## ADR-003 — ICT is the only active destination in Phase 1

**Status:** Accepted

**Decision:** Only ICT is exposed as an operational destination during the initial release.

**Rationale:** Keeps the initial delivery focused and limits unapproved service workflows.

**Consequences:** Future office teams may be prepared in documentation, but their intake destinations remain disabled until their onboarding gate is passed.

## ADR-004 — Native Helpdesk capabilities before custom development

**Status:** Accepted

**Decision:** Prefer native Helpdesk configuration and Frappe Framework facilities. Develop a CBSUA-specific extension only when a verified requirement cannot be met safely through configuration.

**Rationale:** Reduces maintenance burden and upgrade risk.

**Consequences:** Every proposed customization requires a documented gap, implementation rationale, tests, and version compatibility review.

## ADR-005 — Office-level ticket authorization must be validated

**Status:** Accepted as a requirement; implementation pending

**Decision:** Agents and managers must be restricted to their authorized office/team scope, except explicitly authorized platform administrators.

**Rationale:** Tickets may contain sensitive student, employee, or institutional information.

**Validation:** Test list views, direct URLs, search, reports, attachments, comments, assignment, and manager functions using separate office accounts. Do not assume that team assignment alone guarantees complete data isolation.

## ADR-006 — Pin compatible Frappe and Helpdesk versions

**Status:** Pending

**Decision required:** Select and pin a supported Frappe Framework / Helpdesk version pair before development.

**Validation:** Review the official Helpdesk compatibility guidance and perform a clean installation in the project environment.

## ADR-007 — Customer authentication and anonymous ticket policy

**Status:** Pending

**Decision required:** Choose authenticated customer access, anonymous submission with secure follow-up, or a mixed model.

**Validation:** Evaluate privacy, identity verification, customer convenience, and ticket confidentiality.

## ADR-008 — Digital ticket queue only in current scope

**Status:** Accepted

**Decision:** Queueing refers to digital ticket queues and assignment. Physical walk-in token management, counter displays, and turn calling are excluded unless separately approved.

**Rationale:** These capabilities represent a distinct operational system and should not silently expand the current project.
