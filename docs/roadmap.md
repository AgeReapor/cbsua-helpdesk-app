# Implementation Roadmap and Task Breakdown

## 1. Delivery strategy

Deliver a complete, usable ICT ticketing service before onboarding other offices. Build reusable multi-office configuration patterns, but do not implement speculative office workflows during Phase 1.

## 2. Work packages

| ID | Work package | Deliverable | Exit condition |
|---|---|---|---|
| WP-01 | Version and environment baseline | Pinned Frappe/Helpdesk versions; development and test environments | Clean install and compatibility recorded |
| WP-02 | Stakeholder requirements | Approved ICT categories, fields, priorities, workflow, customer access policy | ICT owner signs off |
| WP-03 | Helpdesk configuration | CBSUA native HD Settings branding, portal settings, ticket templates and fields | Configuration reviewed |
| WP-03a | Frappe UI adaptation | Version-pinned CBSUA theme integration using Helpdesk's existing Frappe UI stack | Agent and portal visual/accessibility tests pass; no duplicate UI dependency |
| WP-04 | ICT queue and routing | ICT team, queue views, assignment configuration | Test tickets route correctly |
| WP-05 | Identity and permissions | Admin, manager, agent setup and access policy | Permission tests pass |
| WP-06 | Ticket processing | Reply, internal comment, status, resolution and closure configuration | End-to-end workflow passes |
| WP-07 | SLA and notifications | Approved ICT targets, calendars, and notification configuration | SLA/notification tests pass |
| WP-08 | Reporting | ICT queue and performance views | ICT manager accepts reports |
| WP-09 | Quality assurance | Functional, security, usability, recovery, and UAT evidence | Acceptance criteria pass |
| WP-10 | Production deployment | Production release, backup/restore procedure, runbook, training | ICT production handover |
| WP-11 | Office expansion template | Repeatable office onboarding checklist and configuration guide | Ready for next office approval |

## 3. Suggested GitHub issue breakdown

Create issues from these work packages and link them to requirement IDs in `SRS.md`.

### Foundation
- [ ] Confirm supported Frappe Framework / Helpdesk version pair.
- [ ] Establish development, test, and production environment strategy.
- [ ] Document installation and upgrade procedure.

### ICT requirements and configuration
- [ ] Conduct ICT service-owner workshop.
- [ ] Approve ticket categories, subcategories, and required fields.
- [ ] Approve priority definitions and ticket lifecycle.
- [ ] Approve customer portal authentication and submission policy.
- [ ] Configure CBSUA native HD Settings branding and customer portal.
- [ ] Integrate CBSUA theme tokens into the pinned Helpdesk Vue frontend using the existing Frappe UI dependency.
- [ ] Verify agent and customer interfaces in light/dark themes and responsive layouts.
- [ ] Evaluate ticket-page Custom Actions only against an approved SRS workflow gap.
- [ ] Configure ICT team and queue views.
- [ ] Configure manual assignment and evaluate automatic assignment.
- [ ] Configure staff roles, invitations, and deactivation.
- [ ] Verify office/team ticket isolation.
- [ ] Configure SLA, working hours, and notifications.
- [ ] Configure ICT reports and workload views.

### Validation and handover
- [ ] Build requirement-linked test cases.
- [ ] Perform end-to-end functional testing.
- [ ] Perform role and ticket access-control testing.
- [ ] Perform backup and restore test.
- [ ] Conduct ICT user acceptance testing.
- [ ] Prepare administrator and agent guides.
- [ ] Deploy and hand over Phase 1.

### Expansion readiness
- [ ] Document office onboarding procedure.
- [ ] Define the Registrar onboarding backlog after approval.
- [ ] Define Admissions onboarding backlog after approval.
- [ ] Define Cashier onboarding backlog after approval.

## 4. Phase gates

### Gate 0 — Technical feasibility
- Compatible versions selected.
- Clean installation completed.
- Native Helpdesk feature inventory documented.
- Permission-isolation proof of concept completed.

### Gate 1 — ICT design approval
- ICT categories and fields approved.
- Ticket lifecycle and priority definitions approved.
- Customer access policy approved.
- SLA and notification requirements approved.

### Gate 2 — ICT configuration complete
- Ticket intake, queue, assignment, and processing configured.
- Staff roles and permissions configured.
- Reporting and notifications configured.

### Gate 3 — ICT acceptance
- All Phase 1 acceptance criteria in the SRS pass.
- Access-control and recovery tests pass.
- ICT owner signs off.

### Gate 4 — Production handover
- Production environment operational.
- Backup, restore, monitoring, and support ownership documented.
- Staff training and runbooks delivered.

## 5. Definition of Done

A work item is done only when:

1. Its scope and linked requirement IDs are clear.
2. Configuration or code is committed to the repository.
3. Relevant tests are documented and pass.
4. Access-control impact is reviewed where applicable.
5. Documentation is updated.
6. The designated reviewer or stakeholder accepts the result.

## 6. Office onboarding checklist

- [ ] Office owner and service scope approved.
- [ ] Ticket categories and required fields approved.
- [ ] Team and staff list approved.
- [ ] Roles and permissions tested.
- [ ] Queue and routing configured.
- [ ] SLA and working calendar approved.
- [ ] Notifications and reports configured.
- [ ] Cross-office isolation tests pass.
- [ ] Office acceptance testing completed.
- [ ] Office destination activated.
