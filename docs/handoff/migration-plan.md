# Documentation and Architecture Migration Plan

## 1. Objective

Transition from traditional Bench-centered setup documentation to a Pilot-first architecture and development contract without losing business requirements or scope controls.

This branch is a handoff baseline. It does not silently rewrite historical documents or claim code migration is complete.

## 2. Documentation treatment

| Existing material | Treatment | Reason |
|---|---|---|
| Root README local Bench instructions | Mark superseded and point to handoff docs in a follow-up change | Avoid competing setup methods |
| docs/architecture.md | Retain as historical baseline; supersede with handoff architecture | Preserve context while changing deployment boundary |
| docs/roadmap.md | Reconcile with RPM gates and Pilot workflow | Work packages remain useful; sequencing changes |
| docs/decisions.md | Carry forward valid decisions; supersede hosting/version decisions | Preserve decision history |
| docs/SRS.md | Retain as business requirements; validate with ICT owner | Hosting choice does not change service requirements |
| docs/workflows.md | Reconcile with actual Helpdesk version and native feature inventory | Avoid designing unsupported workflows |
| M0 runbook/scripts | Review every command; label Bench assumptions | Diagnostics may not apply to Pilot paths |

## 3. Technical work packages

### WP-A — Repository baseline
- [ ] Confirm access, default branch and owner for all four forks.
- [ ] Record exact commit SHAs for selected revisions.
- [ ] Review local changes before branch/merge operations.
- [ ] Identify upstream divergence and local patches.

### WP-B — Compatibility and Pilot validation
- [ ] Resolve Helpdesk metadata (Frappe 17 development range) versus old Frappe 16 docs.
- [ ] Confirm Pilot bench Python meets Frappe's Python 3.14 constraint.
- [ ] Add required pyproject.toml to CBSUA extension with tested ranges.
- [ ] Confirm Telephony dependency behavior and installation scope.
- [ ] Run Pilot app validation and retain resolver output.
- [ ] Pin all app commits for a reproducible test set.

### WP-C — Clean local environment
- [ ] Install CBSUA Pilot using documented process.
- [ ] Create clean development bench and test site.
- [ ] Add apps through Pilot CLI/Admin UI.
- [ ] Install apps on the site through Pilot.
- [ ] Run migrations/builds through supported tasks.
- [ ] Record setup duration, prerequisites and limitations.

### WP-D — Business feature mapping
- [ ] Review SRS and Phase 1 ICT acceptance criteria.
- [ ] Inventory native Helpdesk features at pinned revision.
- [ ] Map requirements to native config, CBSUA extension, dependency or out-of-scope.
- [ ] Obtain ICT owner approval for categories, priority, workflow and customer access.
- [ ] Keep future offices inactive.

### WP-E — Authorization and quality
- [ ] Define personas and test fixtures.
- [ ] Test direct URL, list, search, reports, attachments, comments, assignment and export.
- [ ] Test customer visibility and requester identity.
- [ ] Test migrations, assets, jobs and notifications.
- [ ] Perform database + file backup and restore.
- [ ] Conduct ICT user acceptance.

### WP-F — Handover and release
- [ ] Publish developer/admin runbooks based on validated Pilot commands.
- [ ] Publish release manifest with immutable SHAs.
- [ ] Record operational owners, backup schedule, monitoring and escalation.
- [ ] Obtain approval to promote tested release.
- [ ] Archive previous Bench workflow as historical guidance.

## 4. Migration sequencing

1. Documentation first: establish architecture, boundaries, risks and decisions.
2. Compatibility second: no workflow configuration until app set installs cleanly.
3. Platform third: reproduce Pilot from a clean host.
4. Business mapping fourth: validate native Helpdesk capabilities before custom code.
5. Extension fifth: implement only confirmed gaps in CBSUA app.
6. Acceptance sixth: prove ICT workflow, security and recovery.
7. Expansion last: onboard another office only after separate approval.

## 5. Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Helpdesk metadata targets Frappe 17 while old docs target 16 | Install failure/unsupported runtime | Treat exact metadata and resolver output as G1 |
| CBSUA extension lacks Pilot dependency metadata | Pilot rejects app or cannot validate | Add metadata with tested ranges |
| Legacy Bench commands used alongside Pilot | Configuration drift | Make Pilot the single operator interface |
| Customization duplicates Helpdesk features | Upgrade burden | Native-feature inventory and ADR |
| Team membership mistaken for full isolation | Unauthorized disclosure | Server-side negative authorization tests |
| Moving branch heads | Non-reproducible builds | Immutable SHAs and release manifests |
| Local success mistaken for production readiness | Operational/data risk | Separate environment gates and recovery tests |

## 6. Handoff acceptance checklist

- [ ] Incoming team accepts repository boundaries.
- [ ] Compatible revision set is recorded.
- [ ] Pilot validation passes, including CBSUA metadata.
- [ ] Clean Pilot-managed local environment is reproduced.
- [ ] Legacy setup instructions are clearly superseded.
- [ ] ICT SRS/workflows are reviewed against actual Helpdesk.
- [ ] Security and recovery evidence is produced.
- [ ] Owners and gate approvers are identified.
