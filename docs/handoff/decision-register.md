# Architecture Decision Register

This register supersedes hosting/deployment assumptions only where stated. Existing business scope decisions remain in force unless stakeholders approve a change.

## ADR-H01 — Pilot is the local hosting and orchestration layer

**Status:** Accepted as target architecture  
**Decision:** Use cbsua-app-pilot as supported local host, bench/site manager and operator interface.  
**Rationale:** Avoid maintaining a parallel Bench lifecycle and reuse Pilot's CLI, Admin UI, app validation and task operations.  
**Consequences:** Local setup, app acquisition, site lifecycle and service operations use Pilot terminology. Legacy Bench instructions are historical only.

## ADR-H02 — Separate framework, product and institutional code

**Status:** Accepted  
**Decision:** Frappe remains framework; Helpdesk remains ticketing product; Telephony remains dependency; CBSUA app remains institutional extension.  
**Rationale:** Reduce fork coupling and make ownership explicit.  
**Consequences:** Changes go to the narrowest responsible repository.

## ADR-H03 — Native Helpdesk configuration before custom code

**Status:** Carried forward / accepted  
**Decision:** Prefer native Helpdesk features and supported Frappe configuration.  
**Rationale:** Lower upgrade risk and smaller maintenance surface.  
**Consequences:** Every custom feature requires a documented native-feature gap and tests.

## ADR-H04 — ICT is the only enabled office initially

**Status:** Carried forward / accepted  
**Decision:** Phase 1 activates ICT only. Registrar, Admissions and Cashier remain future targets.  
**Rationale:** Limit initial delivery and unapproved data access paths.  
**Consequences:** Future destinations remain disabled until approval and isolation tests pass.

## ADR-H05 — Office-level authorization is a release gate

**Status:** Carried forward / implementation evidence pending  
**Decision:** Users must not access tickets outside their authorized office/team scope except explicitly privileged administrators.  
**Rationale:** Tickets may contain confidential institutional/personal information.  
**Consequences:** Test list, direct URL, search, report, attachment, comment, assignment and export paths.

## ADR-H06 — Reconcile Frappe/Helpdesk version metadata

**Status:** Open / blocking  
**Decision required:** Select an exact compatible revision set.  
**Evidence:** Inspected Helpdesk fork metadata requires Frappe >=17.0.0-dev,<18.0.0; old project docs recommend Frappe 16.  
**Consequence:** No environment is declared compatible until Pilot validation and smoke tests pass.

## ADR-H07 — CBSUA extension must satisfy Pilot validation

**Status:** Open / blocking  
**Decision required:** Add and validate pyproject.toml with supported Frappe and Helpdesk ranges.  
**Evidence:** No pyproject.toml found on inspected main/develop; Pilot requires declaration for non-Frappe apps.  
**Consequence:** Treat extension as not yet Pilot-installable.

## ADR-H08 — Telephony is a declared dependency, not automatically a Phase 1 feature

**Status:** Open  
**Decision required:** Confirm whether Telephony must be installed on the site and whether features remain disabled for Phase 1.  
**Rationale:** Helpdesk metadata declares dependency, but ticketing scope does not itself require calling.  
**Consequence:** Do not bypass declared dependencies; clarify feature activation separately.

## ADR-H09 — Production topology is not yet approved

**Status:** Open  
**Decision required:** Define production site/bench/host topology, backup, domain, TLS, monitoring and operational ownership.  
**Consequence:** Local Pilot hosting is not a production deployment decision.

## ADR-H10 — Digital ticket queue only

**Status:** Carried forward / accepted  
**Decision:** Queueing means digital ticket queues and assignment. Physical walk-in token displays, turn calling, payment processing, SIS integrations and unrelated CRM remain out of scope absent approval.
