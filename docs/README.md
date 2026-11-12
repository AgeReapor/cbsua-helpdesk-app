# CBSUA Helpdesk Documentation

This folder contains the project requirements, architecture, workflows, implementation plan, and decision records for the CBSUA Ticketing and Queueing System.

## Project direction

The system is based on **Frappe Helpdesk**. The project is not a general-purpose CRM and will not build a separate ticket-management engine.

The deployment strategy is phased:

1. **Phase 1 — ICT Office:** establish the first production ticket intake, queue, assignment, processing, resolution, and reporting workflow.
2. **Future expansion — Registrar, Admissions, and Cashier:** add office-specific teams, categories, access policies, routing, service targets, and reporting to the same platform.

The platform should be multi-office capable in its design, while only ICT is enabled as an operational destination during Phase 1.

## Documents

| Document | Purpose |
|---|---|
| [Software Requirements Specification](SRS.md) | Scope, actors, functional and non-functional requirements, acceptance criteria |
| [Architecture](architecture.md) | System context, containers, components, conceptual data model, office routing |
| [Workflows](workflows.md) | Ticket lifecycle, intake, assignment, escalation, and office onboarding |
| [Implementation Roadmap](roadmap.md) | Work packages, phase gates, deliverables, and task breakdown |
| [Decision Log](decisions.md) | Architectural decisions, assumptions, and items requiring validation |
| [M0 Runbook](M0-runbook.md) | Local environment verification and acceptance checklist |
| [M1 Configuration and Branding](M1-configuration-and-branding.md) | Office catalogue, native Helpdesk branding, tests, and rollback |
| [Fresh Site test runbook](site-test/README.md) | WSL Bench setup, clean Site creation, local app deployment, localhost URLs, verification, and cleanup |
| [Frappe UI Integration](frappe-ui-integration.md) | Frappe UI compatibility findings, CBSUA design adaptation, Custom Actions guidance, and frontend verification plan |
| [Agent Skills Review](agent-skills.md) | Installed Frappe skills, risk findings, and project rules for using third-party agent guidance |

## Documentation conventions

- Requirement IDs use `FR-` for functional requirements and `NFR-` for non-functional requirements.
- Mermaid diagrams are maintained as source in Markdown code fences.
- Requirements marked **Proposed** require stakeholder confirmation.
- Requirements marked **Version validation required** must be checked against the selected Frappe Helpdesk release before implementation.
- GitHub Issues are the execution-level task tracker; these documents define the intended scope and acceptance criteria.

## Scope control

Any feature that introduces a separate walk-in token/number display queue, student information system integration, payment processing, enrollment processing, or general CRM functionality requires a separately approved scope change.
