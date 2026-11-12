# M1 — CBSUA configuration foundation and branding

**Status (MVP build):** The ICT bootstrap is implemented: on install/migrate the app creates the native `CBSUA ICT Support` team, maps it to ICT, enables ICT intake, and seeds provisional ICT categories and queue views. These defaults are provisional and not tested on a live Site yet. Earlier status: native HD Settings branding, repeatable office seeding, a System Manager Workspace, and a version-pinned Helpdesk v16 theme entry are implemented. The app also contains office-to-team routing and scoped ticket permission hooks. ICT intake stays disabled until an enabled native Helpdesk Team is mapped. The team mapping and roster are not configured, and routing/isolation have not passed end-to-end verification; M1 is not operationally accepted. Palette values follow the supplied design-system proposal and remain provisional pending official brand validation.

**Scope:** Institutional identity, office catalogue metadata, and safe Phase 1 defaults.

## 1. Requirements basis

Aligned requirements and decisions: FR-08 through FR-12 (office association, ICT-only Phase 1, reusable office mapping, and team routing), NFR-03/04/06/07/08, and ADR-001/003/004/005/010. The native Frappe Helpdesk ticket engine remains authoritative.

The implementation covers the office catalogue, an office link on native tickets, fail-closed routing to a mapped native team, and an additional team membership check for CBSUA tickets. This is a source-level implementation, not proof of authorization correctness. Team provisioning, customer identity policy, ticket lifecycle choices, and end-to-end isolation validation remain open before operational use.

## 2. Components

| Path | Responsibility |
|---|---|
| cbsua_helpdesk/cbsua_helpdesk/doctype/cbsua_service_office/ | Office catalogue DocType and validation controller |
| cbsua_helpdesk/setup/install.py | Idempotent office records, native branding defaults, and the CBSUA Service Office custom field on HD Ticket |
| cbsua_helpdesk/migrate.py | Additive seed routine after migration |
| cbsua_helpdesk/ticket_routing.py | Server-side office and native HD Team stamping/consistency checks |
| cbsua_helpdesk/permissions.py | Additional list-query and document permission checks for CBSUA-tagged tickets |
| cbsua_helpdesk/public/css/cbsua_brand.css | Conservative institutional palette overrides |
| cbsua_helpdesk/public/css/cbsua_helpdesk.css | Semantic-token overrides for the Helpdesk Vue app |
| cbsua_helpdesk/public/images/cbsua-logo.png | Official CBSUA logo asset supplied to the project |
| cbsua_helpdesk/cbsua_helpdesk/workspace/cbsua_helpdesk/cbsua_helpdesk.json | System Manager Workspace linking to CBSUA Service Office |
| scripts/integrate_helpdesk_branding.py | Idempotent integration of the stylesheet in the pinned Helpdesk v16 page shell |
| tests/test_configuration.py and tests/test_ticket_routing.py | Hook registration, branding defaults/preservation, repeatable migration seeding, office activation-gate tests, server stamping, and rejection of client-side office/team changes |

`CBSUA Service Office` is the one CBSUA-specific entity defined clearly enough in the current SRS to model as a custom DocType. It maps an office code to a native Helpdesk Team. Tickets, teams, agents, customers, ticket types, priorities, and service-level agreements continue to use native Helpdesk DocTypes; do not create duplicate CBSUA versions of them. Ticket categories, required fields, priorities, and SLA targets remain pending ICT decisions (OQ-03/OQ-04/OQ-07).

## 3. Office catalogue defaults

| Code | Phase | Active | Customer intake |
|---|---|---:|---:|
| ICT | Phase 1 | Yes | Yes, after the ICT bootstrap maps `CBSUA ICT Support` |
| REGISTRAR | Future | No | No |
| ADMISSIONS | Future | No | No |
| CASHIER | Future | No | No |

The controller rejects activation of a non-ICT office, rejects customer intake for an inactive office, and requires an existing enabled native Helpdesk Team before ICT intake can be enabled. A new installation seeds ICT as active, then the ICT bootstrap maps the native ICT team and enables intake; an administrator may change either afterwards. This is a configuration guard, not a replacement for Frappe permissions.


## 3a. ICT MVP bootstrap (`cbsua_helpdesk/setup/ict.py`)

Runs from `after_install` and `after_migrate`; every step is additive and idempotent.

| Step | Result | Requirement |
|---|---|---|
| `ensure_ict_team` | Native HD Team `CBSUA ICT Support` (Helpdesk also creates its assignment rule) | FR-12, FR-18 |
| `ensure_ict_office_mapping` | Maps ICT to that team and enables intake, only while no team is mapped; later admin changes are respected | FR-09, FR-11 |
| `ensure_ict_ticket_types` | Provisional categories: Network & Internet, Account & Password, Hardware & Equipment, Software & Systems, Email & Collaboration, Information System Request, Other ICT Request | FR-04 (OQ-03 pending) |
| `ensure_ict_views` | Public HD Views: ICT Unassigned Queue, ICT My Tickets, ICT All Open Tickets, ICT SLA At Risk | FR-15, FR-16, FR-20, FR-21, FR-43 |

Onboard staff explicitly (not automatic, no credentials stored):

~~~bash
bench --site cbsua-helpdesk.localhost execute cbsua_helpdesk.setup.ict.add_ict_staff \
  --kwargs '{"email": "agent@cbsua.edu.ph", "manager": 0}'
~~~

The user must already exist (invite via Helpdesk). Set `"manager": 1` to also grant Agent Manager. SLA targets and calendars remain on Helpdesk's native default until OQ-04/OQ-07 are decided.

## 4. Ticket association and routing

The migration adds a read-only `cbsua_service_office` Link field to native `HD Ticket` at permission level 7. In the current Helpdesk permission model, level 7 is readable by customers and agents; the field's Helpdesk ticket-template visibility is a separate UI setting. The institution must decide whether the responsible office may be shown to customers. If it is internal, change the field to agent-only level 8 and grant that level only to approved agent roles. The server-side `before_validate` hook assigns new tickets to the only active office with customer intake enabled and stamps its mapped native `HD Team` into `agent_group`. The field is server-managed on both create and update: clients cannot classify an untagged legacy ticket or change the office on a CBSUA-tagged ticket through the API. A CBSUA ticket also cannot be saved after its team mapping is removed or changed. A Helpdesk Team can map to only one CBSUA Service Office.

Ticket creation fails closed unless exactly one intake-enabled office exists and its team mapping points to an existing, enabled Helpdesk Team. The current site has no ICT Helpdesk Team, so the seeded ICT office cannot accept tickets until an administrator creates the ICT team, provisions its approved agents, maps it in **CBSUA Helpdesk → CBSUA Service Office**, and confirms the office/team configuration. Do not point ICT at the existing Product Experts or Billing teams.

For list queries, the CBSUA permission hook narrows CBSUA-tagged tickets to a mapped team the agent belongs to. For direct document access it denies agents who are not members of the ticket's mapped team. Tickets outside the CBSUA field remain governed by Helpdesk. The hook returns `True` for those unaffected tickets so the installed Helpdesk controller hook still makes the native decision; in Frappe's controller permission chain, a single false result denies access. Both native and CBSUA list-query hooks are applied. These rules still need tests for list, direct URL, search, report, assignment, comments, and attachments before this is called isolation proof.

This uses Frappe's [DocType](https://docs.frappe.io/framework/user/en/tutorial/create-a-doctype), [controller methods](https://docs.frappe.io/framework/user/en/tutorial/controller-methods), and [hooks](https://docs.frappe.io/framework/user/en/python-api/hooks) extension points, and Helpdesk's native [team restriction settings](https://docs.frappe.io/helpdesk/settings) model. See ADR-014 for the compatibility rationale.

The install and migration hooks both invoke the idempotent seed routine. In `hooks.py`, `after_migrate` and `after_install` are declared as dotted Python paths, matching Frappe's documented hook contract. It validates the live HD Settings schema and writes diagnostic messages to the site log if the DocType or expected fields are unavailable. The migration seed is additive and idempotent. Existing records are not silently overwritten on later migrations. Review and correct manually changed records explicitly.

The Frappe app tests cover hook discovery, repeatable office/branding seeds, safe handling of missing Helpdesk settings fields, server-side routing, and rejection of client-side office changes. The prior development Site verified the Workspace, System Manager role, office link, and theme stylesheet response against an earlier source revision. The current routing guard changes remain pending clean-Site migration and verification. Full browser visual/accessibility review remains outstanding.

### Resolved WSL hook mismatch — 2026-11-11

Earlier inspection found the WSL app at `0e6e718` without lifecycle hook declarations. The developer later updated the checkout; it is now at the current app source and migration output confirms the `after_migrate` hook runs. The logo asset was linked by `bench build --app cbsua_helpdesk`. A tracked theme integration script now patches the pinned Helpdesk v16 HTML shell so the app-owned Vue CSS loads.

The Workspace is seeded additively from the app-owned definition file; migrations do not overwrite an existing administrator-edited Workspace. References: [Frappe hooks documentation](https://docs.frappe.io/framework/user/en/python-api/hooks) and [Frappe v16 migration source](https://github.com/frappe/frappe/blob/version-16/frappe/migrate.py).

## 5. Branding palette

The earlier scaffold palette was sampled from the supplied CBSUA seal. The supplied CBSUA Digital Design System v0.1.0 now proposes the following semantic palette for application UI. These values are provisional and must not be presented as institutionally approved until checked against official brand guidance:

| Token | Value | Intended use |
|---|---|---|
| Deep green | #174B35 | Primary actions, links, brand emphasis |
| Hover green | #103B2A | Hover state for primary actions |
| Pale green | #EAF2ED | Selected and subtle surfaces |
| Harvest accent | #C6A04A | Restrained secondary emphasis |
| Pale harvest | #F6F0E1 | Warm subtle surface |
| Main text | #29382F | Primary text |

The theme overrides Frappe UI semantic surface, text, outline, and link tokens while preserving status colors and the framework's dark theme. Gold is reserved for restrained accents, not small text on white. Confirm final typography, official logo usage, exact colors, and contrast with CBSUA PIO before treating them as approved brand rules.

### Public website observations

The public CBSUA homepage currently uses the institutional tagline “Education for Sustainable Human Development” and includes an Online Services section. The university's About Us navigation also provides a dedicated “Seal, Coat of Arms, and Hymn” reference page. These are useful identity and information-architecture references for a future customer portal: institutional naming, recognizable seal usage, clear service entry points, and accessible information hierarchy. This M1 implementation uses the seal's green/gold colors and CBSUA naming, but does not copy website layout or claim to have scraped/downloaded every website asset. See [CBSUA homepage](https://cbsua.edu.ph/) and [About Us / Board of Regents navigation](https://cbsua.edu.ph/about-us/board-of-regents/).

### Framework and Helpdesk integration reference

The CBSUA app registers standard Desk and website assets through hooks. Helpdesk 16.1.0 serves its agent and customer route families from the same Vue/Vite app under `/helpdesk/`; that route shell does not render the normal website head, so those hooks do not load CSS there. The tracked integration script inserts a stylesheet link into the pinned Helpdesk v16 HTML shell. Helpdesk already uses `frappe-ui`; the app adds no duplicate UI dependency. Native branding is configured through HD Settings (`brand_name`, `brand_logo`, `favicon`) and read by Helpdesk's config endpoint and `BrandLogo.vue`. See [Frappe UI integration notes](frappe-ui-integration.md) for the source paths and upgrade procedure.

### Logo asset status

The official `cbsua-logo.png` is stored at `cbsua_helpdesk/public/images/cbsua-logo.png`. Frappe app metadata, website branding hooks, and the new HD Settings defaults reference this asset. The migration only fills empty HD Settings fields and preserves administrator choices. The Helpdesk Vue app reads its logo from the native config response. A full theme/color integration still requires a source-level, version-pinned stylesheet patch; see [Frappe UI integration](frappe-ui-integration.md). Preserve the supplied logo as-is.

## 6. Installation and verification

From the Frappe Bench root:

~~~bash
bench --site cbsua-helpdesk.localhost migrate
bench build --app helpdesk --app cbsua_helpdesk
python /path/to/cbsua-helpdesk-app/scripts/integrate_helpdesk_branding.py /path/to/frappe-bench
bench --site cbsua-helpdesk.localhost clear-cache
bench --site cbsua-helpdesk.localhost clear-website-cache
# Stop the existing `bench start` process with Ctrl+C, then start it again.
bench start
~~~

Run tests:

~~~bash
bench --site cbsua-helpdesk.localhost run-tests --app cbsua_helpdesk
~~~

After migration, open the **CBSUA Helpdesk** Workspace from the Desk sidebar and select **CBSUA Service Office**. The workspace is restricted to System Manager. Confirm ICT is active with intake disabled and all future offices inactive with intake disabled. After an approved ICT team exists, map it to ICT and enable intake. Attempting to enable intake without an enabled team or activate a future office should produce a validation error.

Inspect the Helpdesk config response and verify the logo/favicon URLs return HTTP 200. Confirm the agent interface displays the configured logo and the CBSUA theme stylesheet loads after Helpdesk's compiled stylesheet. Re-run the integration script after replacing or upgrading the Helpdesk v16 app, then rebuild and clear caches. It refuses unexpected page templates without changing them.

## 7. Rollback

1. Back up the local site before migration if it contains data that matters.
2. To remove the native Helpdesk branding defaults, clear or replace the HD Settings fields manually. To remove Desk/website styles, remove the corresponding hooks from hooks.py, then rebuild and clear caches. The migration does not force values back after an administrator changes them.
3. Do not delete office catalogue records after later configuration references them.
4. Production rollback requires a reviewed backup and code release; do not manually drop DocType tables.

## 8. Frappe UI and Custom Actions

Helpdesk `version-16` already uses Frappe UI. CBSUA adapts the existing UI rather than adding another frontend dependency. The app-owned stylesheet and guarded template integration provide the first visual theme layer; Helpdesk Custom Actions are ticket-page Form Scripts, not global theme hooks. Add them only for a specific approved ticket workflow gap and include server-side authorization checks. See [frappe-ui-integration.md](frappe-ui-integration.md).

## 9. Remaining M1 work and exclusions

Not complete: ICT team and agent provisioning; routing configuration on the site; customer identity policy (OQ-01); intake channel decision (OQ-02); ICT categories (OQ-03); priorities and service targets (OQ-04); status and closure rules (OQ-05); role matrix (OQ-06); working calendar (OQ-07); data/attachment and retention policy (OQ-08); and full access-isolation evidence (OQ-10). Automatic assignment, notifications, reporting, and future-office onboarding are also not configured. Do not treat the current hooks as production-ready authorization proof.
