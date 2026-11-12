# MVP-1 implementation status

## Implemented in this branch
- CBSUA Service Office catalogue with ICT, Registrar, Admissions, and Cashier seed definitions.
- ICT is the only active Phase 1 office; intake defaults off until an enabled native Helpdesk Team is mapped.
- Future offices cannot be activated during Phase 1.
- New native HD Tickets receive server-managed office and mapped team values from the sole intake-enabled office.
- Existing CBSUA ticket classification and office-team assignment are protected from ordinary edits.
- Additional list-query and document checks scope CBSUA-tagged agent tickets to mapped-team membership; untagged records defer to native Helpdesk permissions.
- HD Settings brand name is filled only when blank. Existing logo/favicon values are preserved.
- Provisional CBSUA palette CSS for Frappe Desk and regular website surfaces.

## Not yet accepted / outstanding
1. Provision the approved ICT Helpdesk Team and roster on the target Site.
2. Confirm the installed Helpdesk v16 DocType fields and team child-table schema before migration.
3. Run clean-site install, migration, and app tests on pinned Frappe 16 / Helpdesk 16.
4. Verify list, direct document, REST/RPC, search, reports, exports, assignments, comments, attachments, and administrator exceptions using separate accounts.
5. Resolve customer identity/intake policy (SRS OQ-01/OQ-02), office visibility, ICT categories, priorities, status/closure, working calendar, retention, and data handling.
6. Add the approved official CBSUA logo before setting logo/favicon defaults. The supplied upload set did not contain the binary asset.
7. Integrate the standalone Helpdesk Vue shell only after checking the exact pinned v16 template in the Bench checkout. Desk CSS hooks do not style the /helpdesk/ SPA automatically.
8. Add integration tests against the installed Helpdesk app. Current tests cover configuration invariants only.

## Safety constraints
- Do not enable ICT intake until the approved team exists and identity policy is signed off.
- Do not map ICT to Product Experts or Billing as a shortcut.
- Do not enable Registrar, Admissions, or Cashier.
- Office catalogue flags are not authorization controls by themselves.
- The list query hook alone is not complete access isolation proof.
