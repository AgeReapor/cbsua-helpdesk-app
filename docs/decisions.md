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


## ADR-009 — Keep CBSUA configuration and branding in the extension app

**Status:** Accepted for M1

**Decision:** Implement the CBSUA office catalogue and institutional visual layer in
the cbsua_helpdesk app using Frappe hooks and app-owned assets. Do not make
untracked or manual edits to the installed upstream Helpdesk checkout.

**Rationale:** Keeps the upstream Helpdesk upgrade path intact and gives CBSUA
a version-controlled extension boundary.

**Consequences:** CSS overrides must remain conservative and be checked against
the pinned Helpdesk release. Changes to the Helpdesk Vue interface require a
separately tracked, version-pinned frontend patch or maintained fork with
regression tests and an explicit rebuild procedure.

## ADR-010 — Office catalogue activation is not authorization

**Status:** Accepted for M1

**Decision:** Maintain a CBSUA Service Office metadata catalogue with ICT active
and intake-enabled; Registrar, Admissions, and Cashier remain inactive and
intake-disabled. The catalogue does not provision Helpdesk Teams or grant
ticket permissions.

**Rationale:** Office onboarding and ticket access isolation are separate
concerns. A configuration flag must not be mistaken for an authorization rule.

**Consequences:** Ticket routing and office-scoped permissions remain pending.
Future offices cannot be activated until onboarding and isolation tests pass.


## ADR-011 — Reuse Helpdesk's existing Frappe UI stack

**Status:** Accepted for M1

**Decision:** Adapt the Frappe UI version already pinned by Helpdesk `version-16`. Do not add a second copy of the package or upgrade it as part of CBSUA branding.

**Rationale:** Source inspection confirms Helpdesk's Vue frontend already imports Frappe UI, uses its Tailwind preset, and uses Frappe Framework UI components. Reuse reduces dependency duplication and upgrade risk.

**Consequences:** New frontend components must be checked against the exact installed `frappe-ui@1.0.0-rc.1` API rather than assuming current-main docs apply. A full theme change requires a tracked source-level integration in the Helpdesk frontend build. Do not edit generated assets or node_modules.

## ADR-012 — Use native HD Settings for Helpdesk brand identity

**Status:** Accepted; implementation committed

**Decision:** Set `brand_name`, `brand_logo`, and `favicon` in Helpdesk's singleton HD Settings only when the values are blank.

**Rationale:** Helpdesk's config endpoint exposes these fields and its Vue BrandLogo component consumes the configured logo. This is the native integration point, unlike general Frappe Desk CSS hooks.

**Consequences:** Administrator-configured values are preserved. The migration is additive and does not force branding values on subsequent runs.

## ADR-013 — Keep Custom Actions scoped to documented ticket workflows

**Status:** Accepted

**Decision:** Use Helpdesk HD Form Script / Custom Actions only for ticket-page actions that map to an approved SRS requirement and cannot be met through native configuration. Do not use them for global navigation or branding.

**Rationale:** Custom Actions are contextual Form Scripts with different supported functions on agent, customer, and new-ticket views. A client-side button is not an authorization boundary.

**Consequences:** Any consequential action requires server-side permission validation, explicit customer-portal exposure review, and authorized/unauthorized tests. No custom action is introduced until a concrete workflow gap is approved.
