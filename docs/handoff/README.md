# CBSUA Helpdesk — Architectural Handoff

**Status:** Architecture baseline for incoming team review  
**Prepared:** 2026-11-12  
**Target hosting model:** CBSUA Pilot local hosting

## Executive direction

The previous repository is no longer the owner of hosting, bench lifecycle, framework source, or Helpdesk source. It is the intended home for CBSUA-specific application behavior and the integration contract for the Pilot stack.

The target separation is:

1. **cbsua-app-pilot** — local host, bench/site lifecycle, app acquisition and validation, process orchestration, Admin UI and CLI.
2. **cbsua-app-frappe** — framework runtime and platform services.
3. **cbsua-app-helpdesk** — upstream Helpdesk product and ticketing workflows.
4. **cbsua-app-telephony** — Helpdesk dependency and telephony integration capability.
5. **cbsua-helpdesk-app** — CBSUA-owned extension/configuration only; no hosting or framework responsibilities.

Pilot is not a replacement ticketing application. Frappe is not the product workflow. Helpdesk is not the infrastructure manager. Telephony is not the core ticketing system.

## Start here

| Document | Purpose |
|---|---|
| [Target architecture](architecture.md) | Pilot hosting boundaries, deployment layers and data/control flows |\n| [Software Requirements Specification](../SRS.md) | Problem-first institutional requirements, acceptance criteria and open decisions |\n| [C4 and UML architecture](../architecture.md) | Restored C4 views, ERD, UML domain model, lifecycle and sequence diagrams |\n| [Requirements traceability](../traceability-matrix.md) | CP → CN → FR/NFR → architecture → verification mapping |
| [Repository responsibilities](repository-responsibilities.md) | Ownership, allowed changes, dependency direction |
| [Compatibility and dependencies](compatibility-and-dependencies.md) | Observed metadata, compatibility blockers, version policy |
| [Local development and release](local-development-and-release.md) | Pilot-first developer workflow and promotion model |
| [RPM lifecycle](rpm-lifecycle.md) | Result, Purpose, Massive Action Plan and progressive gates |
| [Migration plan](migration-plan.md) | What to retain, retire, validate and deliver |
| [Decision register](decision-register.md) | Accepted decisions and unresolved decisions |
| [Research notes](research-notes.md) | Repository inspection, upstream references and caveats |

## Project outcome

Deliver an institutionally usable, ICT-first digital helpdesk on the Pilot-managed Frappe platform, with a controlled path for office onboarding later. Keep native Helpdesk capabilities as the default; add CBSUA code only for verified gaps. Do not activate Registrar, Admissions, or Cashier intake until office-specific authorization tests and stakeholder approval pass.

## Important findings

- The previous README documents a traditional Bench-managed setup and a Frappe 16 / Helpdesk 16 pairing. That is historical guidance for the superseded hosting model.
- The inspected CBSUA Helpdesk fork's project metadata declares Frappe >=17.0.0-dev,<18.0.0 and Telephony >=0.0.1,<1.0.0. This conflicts with the older README's Frappe 16 recommendation.
- The inspected CBSUA Frappe fork requires Python >=3.14,<3.15.
- The inspected CBSUA Helpdesk extension repository did not return a pyproject.toml on main or develop. Pilot's current app-dependency policy requires a valid Frappe dependency declaration for every app except Frappe itself. Treat the custom app as not Pilot-installable until this is added and validated.
- The four CBSUA fork repositories currently expose develop as their only branch in the inspected branch listings. This is not a release strategy; immutable commit pins and tested release tags still need to be established.

These are repository observations at preparation date, not proof that a complete local installation has passed.

## Scope and non-claims

This handoff is architecture and documentation. It does not claim to have installed Pilot, completed dependency resolution, installed the extension on a site, implemented ICT workflows, or completed functional/security/recovery/UAT testing.

Use the gates in [RPM lifecycle](rpm-lifecycle.md) and [Migration plan](migration-plan.md) to turn assumptions into evidence.
