# CBSUA Helpdesk Documentation

This folder contains the project requirements, architecture, workflows, implementation plan, and decision records for the CBSUA Ticketing and Queueing System.

## Project direction

The system is based on **Frappe Helpdesk**. The project is not a general-purpose CRM and will not build a separate ticket-management engine.

The deployment strategy is phased:

1. **Phase 1 — ICT Office:** establish the first production ticket intake, queue, assignment, processing, resolution, and reporting workflow.
2. **Future expansion — Registrar, Admissions, and Cashier:** add office-specific teams, categories, access policies, routing, service targets, and reporting to the same platform.

The platform should be multi-office capable in its design, while only ICT is enabled as an operational destination during Phase 1.

## Architecture handoff

The hosting architecture has transitioned to the CBSUA Pilot stack. The previous Bench-centered setup is historical and is not the target local workflow. Start with the [Pilot architectural handoff](handoff/README.md), including its compatibility blockers and progressive RPM gates.

## Documents

| Document | Purpose |
|---|---|
| [Software Requirements Specification](SRS.md) | Scope, actors, functional and non-functional requirements, acceptance criteria |
| [Architecture](architecture.md) | C4 context/containers/components, UML domain model, ERD, state machine, sequence and authorization diagrams |
| [Workflows](workflows.md) | Ticket lifecycle, intake, assignment, escalation, and office onboarding |
| [Implementation Roadmap](roadmap.md) | Work packages, phase gates, deliverables, and task breakdown |
| [Decision Log](decisions.md) | Architectural decisions, assumptions, and items requiring validation |\n| [Traceability Matrix](traceability-matrix.md) | Customer problems → needs → requirements → architecture → verification evidence |

## Requirements engineering approach\n\nThe SRS follows the Problem-Based-SRS progression: Business Context → Customer Problems (WHY) → Software Glance → Customer Needs (WHAT) → Software Vision → Functional/Non-functional Requirements (HOW). Each requirement has a stable identifier and verification method. See the [SRS](SRS.md) and [Traceability Matrix](traceability-matrix.md). Architecture visuals are maintained as Mermaid source in [architecture.md](architecture.md).\n\n## Documentation conventions

- Requirement IDs use `FR-` for functional requirements and `NFR-` for non-functional requirements.
- Mermaid diagrams are maintained as source in Markdown code fences.
- Requirements marked **Proposed** require stakeholder confirmation.
- Requirements marked **Version validation required** must be checked against the selected Frappe Helpdesk release before implementation.
- GitHub Issues are the execution-level task tracker; these documents define the intended scope and acceptance criteria.

## Scope control

Any feature that introduces a separate walk-in token/number display queue, student information system integration, payment processing, enrollment processing, or general CRM functionality requires a separately approved scope change.
