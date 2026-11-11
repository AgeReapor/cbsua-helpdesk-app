# CBSUA Helpdesk Frappe app

This directory is the installable Python/Frappe application package for CBSUA-specific Helpdesk configuration. The repository root is the developer/deployment guide; this README documents the interior app package and its extension contracts.

## 1. Responsibility and boundaries

`cbsua_helpdesk` extends the installed Frappe Helpdesk app. It is not a replacement ticket engine.

This app currently owns:
- The `CBSUA Service Office` configuration DocType.
- Safe, additive seed defaults for ICT, Registrar, Admissions, and Cashier.
- The Phase 1 guard that permits only ICT to be active/intake-enabled.
- Native Helpdesk branding defaults in the `HD Settings` singleton, filled only when those fields are blank.
- CBSUA-owned public image and CSS assets.
- Migration integration and app-level tests.

This app does **not** currently own:
- HD Ticket records or ticket lifecycle.
- HD Team creation, agent provisioning, assignment rules, or routing.
- Office-level ticket permission enforcement or isolation.
- Ticket categories, SLAs, notification workflows, reports, or production deployment.
- A separate Vue frontend or a second UI component library.

Frappe Helpdesk remains authoritative for tickets, teams, agents, customer portal, ticket permissions, and agent/customer frontend.

## 2. Package layout

| Path | Responsibility |
|---|---|
| `hooks.py` | App metadata, Desk/website asset hooks, logo references, and `after_migrate` registration |
| `migrate.py` | Small migration lifecycle entry point |
| `setup/install.py` | Idempotent office seeding and non-destructive HD Settings brand defaults |
| `cbsua_helpdesk/doctype/cbsua_service_office/` | Office catalogue schema and controller validation |
| `public/images/cbsua-logo.png` | Official CBSUA logo supplied for the project |
| `public/css/cbsua_brand.css` | Conservative Frappe Desk and website styles; not injected into the Helpdesk Vue app |
| `../tests/` | Frappe app tests for office defaults and branding configuration |

Keep comments in internal files current when changing behavior. Every migration should be safe to run more than once and must not silently overwrite an administrator's configured settings.

## 3. Office catalogue and Phase 1 guard

The migration seeds the following records when they do not already exist:

| Code | Phase | Active | Customer intake |
|---|---|---:|---:|
| ICT | Phase 1 | Yes | Yes |
| REGISTRAR | Future | No | No |
| ADMISSIONS | Future | No | No |
| CASHIER | Future | No | No |

Existing records are not overwritten during migration. The DocType controller rejects activating a non-ICT office and rejects intake for an inactive office.

These fields are catalogue metadata only. They do not create Helpdesk Teams, route tickets, or enforce access control. Never treat `is_active` or `allow_customer_intake` as ticket authorization. Office routing and ticket-level isolation require their own server-side implementation and tests before any future office is onboarded.

## 4. Native Helpdesk branding defaults

The app's `after_migrate` hook calls `ensure_default_branding()`. It fills blank `HD Settings` fields only:

| HD Settings field | Default |
|---|---|
| `brand_name` | `CBSUA Helpdesk` |
| `brand_logo` | `/assets/cbsua_helpdesk/images/cbsua-logo.png` |
| `favicon` | `/assets/cbsua_helpdesk/images/cbsua-logo.png` |

Helpdesk's `helpdesk.api.config.get_config` endpoint exposes these settings and the Vue `BrandLogo.vue` component consumes the configured logo. The migration preserves any non-empty values selected by an administrator.

To change branding manually, open Helpdesk's **HD Settings → Branding** and select or enter the appropriate asset path according to the installed Helpdesk field behavior. If an administrator changes the settings, later migrations will not force the defaults back.

## 5. Frappe UI integration boundary

Helpdesk `version-16` already uses Vue 3, Tailwind CSS, and `frappe-ui@1.0.0-rc.1`, with a Tailwind preset and framework UI source integration. Do not install another copy of Frappe UI in this app and do not upgrade the pinned dependency as part of this branding work.

The current `app_include_css` and `web_include_css` hooks apply to Frappe Desk and website pages. They do not automatically style the standalone Helpdesk Vue frontend at `/helpdesk`.

The full theme adaptation is documented in [Frappe UI integration](../docs/frappe-ui-integration.md). Any future agent UI theme work must be integrated into the version-pinned Helpdesk frontend source and rebuilt. Do not edit `node_modules`, generated `helpdesk/public/desk` bundles, or `sites/assets` by hand.

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
- [ ] The configured logo and favicon asset paths return HTTP 200.
- [ ] The Helpdesk frontend displays the configured brand logo.
- [ ] The CBSUA app test suite passes.
- [ ] No test has been misrepresented as proof of office-level ticket isolation.

Local runtime verification is environment-specific. A successful GitHub commit does not mean the user's local Bench migration, frontend build, or tests have already run.

## 8. Related documentation

- [Project documentation index](../docs/README.md)
- [M1 configuration and branding](../docs/M1-configuration-and-branding.md)
- [Frappe UI integration and CBSUA adaptation](../docs/frappe-ui-integration.md)
- [SRS](../docs/SRS.md)
- [Architecture](../docs/architecture.md)
- [Implementation roadmap](../docs/roadmap.md)
- [Helpdesk dependency notes](../helpdesk/README.md)
