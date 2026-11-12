# CBSUA Helpdesk

**This repository is transitioning to a Pilot-managed architecture.** The former Bench-centered setup instructions below this README are superseded for the target local-hosting workflow.

## Start with the architectural handoff

Read **[docs/handoff/README.md](docs/handoff/README.md)** first. It documents:

- the target architecture and responsibilities of Pilot, Frappe, Helpdesk, Telephony and the CBSUA extension;
- the dependency and compatibility blockers found in the current fork metadata;
- the Pilot-first local development and release model;
- the RPM-Aligned Progressive Project Lifecycle (Result, Purpose, Massive Action Plan);
- migration work packages, decisions, risks and research references.

## Repository purpose

This repository is intended to own **CBSUA-specific Helpdesk extensions** only. It must not become a second hosting manager, Frappe Framework fork, or generic Helpdesk product fork.

Use native Helpdesk capabilities first. Add CBSUA-specific code only for an approved institutional requirement that cannot be met safely through configuration.

## Important compatibility warning

The historical setup instructions in the previous README recommended Frappe 16 / Helpdesk 16. The inspected CBSUA Helpdesk fork metadata currently declares Frappe `>=17.0.0-dev,<18.0.0` and Telephony `>=0.0.1,<1.0.0`; the inspected Frappe fork requires Python `>=3.14,<3.15`. The CBSUA extension also needs Pilot-compatible dependency metadata before it can pass Pilot validation.

**Do not treat the old Bench instructions or Frappe 16 pairing as the current installation procedure.** No compatible full-stack install has been certified by this documentation handoff. See [Compatibility and Dependency Policy](docs/handoff/compatibility-and-dependencies.md).

## Business scope carried forward

- Phase 1 operational office: ICT only.
- Future offices: Registrar, Admissions and Cashier, subject to separate onboarding approval and access-isolation tests.
- Queueing: digital ticket queues and assignment only.
- Physical walk-in token display/calling, payment processing, SIS integration, enrollment processing and general CRM features remain out of scope unless separately approved.

## Documentation

- [Handoff index](docs/handoff/README.md)
- [Project documentation index](docs/README.md)
- [Existing SRS](docs/SRS.md)
- [Existing workflows](docs/workflows.md)
- [Existing decision history](docs/decisions.md)

## Handoff status

The `handoff` branch contains the architectural documentation baseline. It does not claim that Pilot was installed, dependency validation passed, business workflows were implemented, or security/acceptance testing was completed. Those are explicit follow-on gates in the handoff plan.
