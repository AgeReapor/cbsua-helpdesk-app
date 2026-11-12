# RPM-Aligned Progressive Project Lifecycle

## 1. Planning model

Tony Robbins' Rapid Planning Method (RPM) separates:
- **Result:** the observable outcome the team commits to deliver;
- **Purpose:** why the outcome matters;
- **Massive Action Plan (MAP):** a flexible set of actions and options that can achieve the result.

The MAP is a menu of actions that can be adjusted as evidence arrives, not merely a fixed checklist. The lifecycle below translates outcome-first planning into progressive engineering gates. This is a project adaptation, not a claim that RPM itself prescribes a software-development methodology.

## 2. Project RPM

### Result

Deliver a maintainable, locally hosted CBSUA Helpdesk platform managed by Pilot, with a tested ICT-first ticket lifecycle and a documented path for controlled office onboarding.

Evidence:
- reproducible Pilot-managed development environment;
- dependency-compatible and pinned application set;
- operational ICT intake, queue, assignment, processing and resolution;
- verified role and office data isolation;
- documented operational ownership, recovery and release practices.

### Purpose

Provide a dependable service channel for CBSUA constituents and a manageable work queue for institutional service teams, while reducing duplicated infrastructure work and avoiding unnecessary divergence from maintained Frappe products.

### Massive Action Plan

1. Establish repository ownership and retire obsolete hosting assumptions.
2. Resolve Frappe/Helpdesk/Python compatibility discrepancy.
3. Add Pilot-compliant dependency metadata to CBSUA extension.
4. Produce reproducible Pilot-managed local bench and test site.
5. Inventory native Helpdesk features against approved ICT requirements.
6. Configure ICT intake, queue, roles, notifications and reporting.
7. Prove authorization boundaries with negative tests.
8. Complete user acceptance, backup/restore and operational handover.
9. Create a repeatable onboarding template for future offices after approval.

The team may add, reorder or replace actions when technical or stakeholder evidence changes the best route to the Result.

## 3. Progressive lifecycle gates

| Gate | Result / exit evidence | Purpose | Core MAP actions |
|---|---|---|---|
| G0 — Reframe and discover | Ownership map, current-state inventory, scope and assumptions accepted | Stop work against obsolete architecture | Inspect forks, docs, branches and metadata |
| G1 — Compatibility proof | Pilot + Frappe + Helpdesk + Telephony + CBSUA set passes dependency validation | Avoid investing in a stack that cannot install | Resolve versions, Python runtime, metadata and package conflicts |
| G2 — Local platform proof | Clean Pilot-managed bench/site is reproducible | Establish one repeatable development path | Install Pilot, create bench/site, add apps, install, migrate, smoke test |
| G3 — ICT design proof | ICT requirements and native feature mapping approved | Build the right workflow before coding | Confirm categories, fields, priority, intake, identity, roles, SLA and reports |
| G4 — ICT service proof | End-to-end ICT journey and authorization tests pass | Make the initial service trustworthy | Configure native features, add justified extensions, test positive/negative cases |
| G5 — Acceptance and readiness | ICT owner accepts; recovery and operations evidence complete | Ensure support beyond a developer workstation | UAT, training, backup/restore, monitoring, runbooks and release package |
| G6 — Controlled expansion | Next office approved and passes onboarding checks | Expand without weakening existing boundaries | Configure office/team, policy, queues, reports and regression tests |

A gate is not passed by a document alone. It requires evidence from actual selected revisions and target environment.

## 4. Definition of Done

1. Result and linked requirement IDs are explicit.
2. Purpose and user impact are understood by the responsible stakeholder.
3. Implementation is in the correct repository/layer.
4. Source revisions and dependency constraints are recorded.
5. Relevant tests and negative security tests pass.
6. Migration, backup and rollback implications are documented.
7. Documentation is updated.
8. A named reviewer or service owner accepts the result.

## 5. Progress measures

Track outcomes, not only task counts:
- time to reproduce a clean local environment;
- number of unpinned dependencies (target zero for acceptance releases);
- unresolved compatibility errors (target zero at G1);
- approved ICT requirements with passing tests;
- cross-office authorization test pass rate (100% for defined cases);
- successful backup restore evidence;
- unresolved critical/high-risk defects;
- ICT service-owner acceptance.

Do not set service-level targets until the responsible office approves them.

## 6. Governance cadence

- Review the Result and current gate at each planning/review session.
- Keep the MAP flexible; remove actions that no longer contribute to the Result.
- Record scope, compatibility and security decisions in the decision register.
- Reassess gate evidence after any platform revision change.
- Do not mark progress complete solely because code merged or an app appears in the bench.
