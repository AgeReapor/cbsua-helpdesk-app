# CBSUA Helpdesk Frappe app

This directory is the installable Python/Frappe application package for CBSUA-specific Helpdesk configuration. The repository root is the developer/deployment guide; this README documents the interior app package and its extension contracts.

## 1. Responsibility and boundaries

`cbsua_helpdesk` extends the installed Frappe Helpdesk app. It is not a replacement ticket engine.

This app currently owns:
- The `CBSUA Service Office` configuration DocType.
- Safe, additive seed defaults for ICT, Registrar, Admissions, and Cashier.
- The Phase 1 guard that permits only ICT to be active/intake-enabled.
- A protected `cbsua_service_office` custom field on native `HD Ticket`.
- Fail-closed routing of new tickets to the single active office's mapped native Helpdesk Team.
- Additional office-aware list and direct-document checks for CBSUA-tagged tickets.
- Native Helpdesk branding defaults in the `HD Settings` singleton, filled only when those fields are blank.
- CBSUA-owned public image and CSS assets.
- A System Manager Workspace linking to the office catalogue DocType.
- A tracked Helpdesk v16 page-shell integration for the CBSUA Vue theme stylesheet.
- Migration integration and app-level tests.

This app does **not** currently own:
- HD Ticket records or ticket lifecycle; those remain native Helpdesk responsibilities.
- HD Team creation, agent provisioning, or assignment rules.
- Customer identity/access policy, ticket categories, priorities, SLA, notifications, or reports.
- Proven office-level isolation; the new hooks require end-to-end validation before operational use.
- A separate Vue frontend or a second UI component library.

Frappe Helpdesk remains authoritative for tickets, teams, agents, customer portal, native ticket policy, and agent/customer frontend. CBSUA adds a narrow office restriction for CBSUA-tagged tickets.

## 2. Package layout

| Path | Responsibility |
|---|---|
| `hooks.py` | App metadata, Desk/website asset hooks, logo references, routing event, and permission hook registration |
| `migrate.py` | Small migration lifecycle entry point |
| `setup/install.py` | Idempotent office seeding, non-destructive HD Settings branding, and HD Ticket custom-field creation |
| `cbsua_helpdesk/doctype/cbsua_service_office/` | Office catalogue schema and controller validation |
| `permissions.py` | CBSUA-scoped list and document access checks layered with Helpdesk's native policy |
| `ticket_routing.py` | Fail-closed mapping of new tickets to the active office's native Helpdesk Team |
| `public/images/cbsua-logo.png` | Official CBSUA logo supplied for the project |
| `public/css/cbsua_brand.css` | Conservative Frappe Desk and website styles |
| `public/css/cbsua_helpdesk.css` | Provisional design-system token overrides for Helpdesk Vue |
| `cbsua_helpdesk/workspace/cbsua_helpdesk/` | Standard System Manager Workspace with office catalogue shortcut |
| `../scripts/integrate_helpdesk_branding.py` | Guarded, repeatable Helpdesk v16 stylesheet integration |
| `../tests/` | Frappe app tests for office defaults, branding, lifecycle registration, repeatability, and schema drift |

Keep comments in internal files current when changing behavior. Every migration should be safe to run more than once and must not silently overwrite an administrator's configured settings.

## 3. Office catalogue and Phase 1 guard

The migration seeds the following records when they do not already exist:

| Code | Phase | Active | Customer intake |
|---|---|---:|---:|
| ICT | Phase 1 | Yes | Yes |
| REGISTRAR | Future | No | No |
| ADMISSIONS | Future | No | No |
| CASHIER | Future | No | No |

Existing records are not overwritten during migration. The DocType controller rejects activating a non-ICT office and rejects intake for an inactive office. A native Helpdesk Team can map to only one office; mapped teams must exist and be enabled.

These flags are catalogue/routing configuration, not ticket authorization. The app does not create a team or provision its users. New ticket creation requires exactly one active intake office with a mapped, enabled native Helpdesk Team. The current site has no ICT team mapping; configure the approved ICT team and roster before trying ticket intake. Do not map ICT to the existing Product Experts or Billing teams. The route hook stamps the office/team and the office permission hooks add CBSUA-specific list and direct-document checks. Native Helpdesk checks continue to apply to tickets outside CBSUA scope. Treat the authorization implementation as unverified until the test cases in `docs/architecture.md` and the SRS pass.

## 4. Native Helpdesk branding defaults

The app's `after_install` and `after_migrate` hooks call `ensure_default_branding()`. Both are registered in `hooks.py` as dotted Python paths (the documented Frappe convention); `after_migrate` is a single dotted path, not a custom list declaration. It fills blank `HD Settings` fields only:

| HD Settings field | Default |
|---|---|
| `brand_name` | `CBSUA Helpdesk` |
| `brand_logo` | `/assets/cbsua_helpdesk/images/cbsua-logo.png` |
| `favicon` | `/assets/cbsua_helpdesk/images/cbsua-logo.png` |

In Helpdesk v16, `brand_logo` and `favicon` are `Attach Image` fields and `brand_name` is a `Data` field. The public app asset URLs below are stored as their values. Helpdesk's `helpdesk.api.config.get_config` endpoint exposes these settings and the Vue `BrandLogo.vue` component consumes the configured logo. The seed checks the live DocType schema, logs skipped/missing fields, and preserves any non-empty values selected by an administrator. If the fields remain blank after migration, verify the app is installed and that `frappe.get_hooks('after_migrate', app_name='cbsua_helpdesk')` includes the CBSUA migration method; then inspect the site log for `cbsua_helpdesk` messages.

To change branding manually, open Helpdesk's **HD Settings → Branding** and select or enter the appropriate asset path according to the installed Helpdesk field behavior. If an administrator changes the settings, later migrations will not force the defaults back.

## 5. Frappe UI integration boundary

Helpdesk `version-16` already uses Vue 3, Tailwind CSS, and `frappe-ui@1.0.0-rc.1`, with a Tailwind preset and framework UI source integration. Do not install another copy of Frappe UI in this app and do not upgrade the pinned dependency as part of this branding work.

The current `app_include_css` and `web_include_css` hooks apply to Frappe Desk and website pages. Helpdesk's standalone `/helpdesk` shell does not load them; run the tracked integration script to include the app-owned Vue theme stylesheet.

The theme integration is documented in [Frappe UI integration](../docs/frappe-ui-integration.md). Re-run the guarded script after upgrading Helpdesk. Do not edit `node_modules`, generated `helpdesk/public/desk` bundles, or `sites/assets` by hand.

Follow the Frappe UI conventions after checking the installed package version: prefer library components, semantic `surface`/`ink`/`outline` tokens, documented component props, and Frappe data composables where supported. Current-main documentation can be newer than Helpdesk's pinned release candidate.

## 6. Helpdesk Custom Actions boundary

Helpdesk Custom Actions are ticket-page Form Scripts configured through `HD Form Script`. They are useful only for a concrete ticket-specific action that maps to an approved SRS requirement and is not already supported natively.

They are not a global theme, navbar, or app-wide navigation extension point. A client-side action button is not authorization: any consequential operation must enforce user and ticket permissions on the server. Review agent, customer portal, and new-ticket exposure independently.

No custom action is seeded by this app at this stage. See [official Custom Actions documentation](https://docs.frappe.io/helpdesk/custom-actions) and [project integration notes](../docs/frappe-ui-integration.md).

## 7. Local development and verification

Run commands from the Frappe Bench root, not from this app directory:

```bash
# Apply DocType changes, office seeds, and blank-only branding defaults.
bench --site cbsua-helpdesk.localhost migrate

# Build the upstream Helpdesk frontend and CBSUA app assets.
bench build --app helpdesk --app cbsua_helpdesk

# Clear site caches.
bench --site cbsua-helpdesk.localhost clear-cache
bench --site cbsua-helpdesk.localhost clear-website-cache

# Run the CBSUA app test suite.
bench --site cbsua-helpdesk.localhost run-tests --app cbsua_helpdesk
```

Then restart `bench start` and hard-refresh the browser.

### Expected checks

- [ ] `CBSUA Service Office` contains the four expected records.
- [ ] ICT is active and intake-enabled.
- [ ] Registrar, Admissions, and Cashier remain inactive and intake-disabled.
- [ ] `HD Settings` has the CBSUA brand defaults if those fields were blank before migration.
- [ ] A pre-existing non-empty HD Settings value survives a subsequent migration.
- [ ] Tests cover repeated migration seeding and log/skip behavior for a missing DocType or branding field.
- [ ] The configured logo and favicon asset paths return HTTP 200.
- [ ] The Helpdesk frontend displays the configured brand logo.
- [ ] The CBSUA app test suite passes.
- [ ] No test has been misrepresented as proof of office-level ticket isolation.

Local runtime verification is environment-specific. A successful GitHub commit does not mean the user's local Bench migration, frontend build, or tests have already run.

## 8. Reference evaluation

The [Frappe Custom UI App](https://github.com/janakvaghela542/Frappe-Custom-UI-App) is a useful example of a conventional Frappe extension: app hooks, public assets, and a custom settings DocType. Its documented features target Frappe Desk (role-based field visibility, ListView actions, and reusable Desk UI extensions). It is not a direct theme plugin for Helpdesk's standalone Vue agent app, so CBSUA does not add it as a dependency. We will use scoped patterns only where they fit the actual surface being customized.

## 9. Related documentation

- [Project documentation index](../docs/README.md)
- [M1 configuration and branding](../docs/M1-configuration-and-branding.md)
- [Frappe UI integration and CBSUA adaptation](../docs/frappe-ui-integration.md)
- [SRS](../docs/SRS.md)
- [Architecture](../docs/architecture.md)
- [Implementation roadmap](../docs/roadmap.md)
- [Helpdesk dependency notes](../helpdesk/README.md)
