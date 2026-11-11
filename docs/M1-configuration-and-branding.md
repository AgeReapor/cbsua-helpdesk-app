# M1 — CBSUA configuration foundation and branding

**Status:** Native HD Settings branding, repeatable office seeding, a System Manager Workspace, and a version-pinned Helpdesk v16 theme entry are implemented in app source. Palette values follow the supplied design-system proposal and remain provisional pending official brand validation.

**Branch:** develop  
**Scope:** Institutional identity, office catalogue metadata, and safe Phase 1 defaults.

## 1. Requirements basis

Aligned requirements and decisions: FR-09 (ICT-only Phase 1 destination), FR-10 (reusable office model), NFR-06 through NFR-08 (extensibility, minimal custom code, documented/testing), and ADR-001/003/004. The native Frappe Helpdesk ticket engine remains authoritative.

M1 does not complete ticket routing, agent/team authorization, customer intake, or cross-office isolation. These remain separate requirements and must be implemented and tested before operational use.

## 2. Components

| Path | Responsibility |
|---|---|
| cbsua_helpdesk/cbsua_helpdesk/doctype/cbsua_service_office/ | Office catalogue DocType and validation controller |
| cbsua_helpdesk/setup/install.py | Idempotent creation of baseline office records |
| cbsua_helpdesk/migrate.py | Additive seed routine after migration |
| cbsua_helpdesk/public/css/cbsua_brand.css | Conservative institutional palette overrides |
| cbsua_helpdesk/public/css/cbsua_helpdesk.css | Semantic-token overrides for the Helpdesk Vue app |
| cbsua_helpdesk/public/images/cbsua-logo.png | Official CBSUA logo asset supplied to the project |
| cbsua_helpdesk/cbsua_helpdesk/workspace/cbsua_helpdesk/cbsua_helpdesk.json | System Manager Workspace linking to CBSUA Service Office |
| scripts/integrate_helpdesk_branding.py | Idempotent integration of the stylesheet in the pinned Helpdesk v16 page shell |
| tests/test_configuration.py | Hook registration, branding defaults/preservation, repeatable migration seeding, missing-schema diagnostics, and office activation-gate tests |

CBSUA Service Office is configuration metadata only. It is not a Helpdesk Team, ticket, assignment rule, route, or permission boundary.

## 3. Office catalogue defaults

| Code | Phase | Active | Customer intake |
|---|---|---:|---:|
| ICT | Phase 1 | Yes | Yes |
| REGISTRAR | Future | No | No |
| ADMISSIONS | Future | No | No |
| CASHIER | Future | No | No |

The controller rejects activation of a non-ICT office and rejects customer intake for inactive offices. This is a configuration guard, not a replacement for Frappe permissions.

The install and migration hooks both invoke the idempotent seed routine. In `hooks.py`, `after_migrate` and `after_install` are declared as dotted Python paths, matching Frappe's documented hook contract. It validates the live HD Settings schema and writes diagnostic messages to the site log if the DocType or expected fields are unavailable. The migration seed is additive and idempotent. Existing records are not silently overwritten on later migrations. Review and correct manually changed records explicitly.

The Frappe app tests cover hook discovery, repeatable office/branding seeds, and safe handling of missing Helpdesk settings fields. The WSL site has now been migrated from the current app source; the CBSUA Workspace, its System Manager role, office link, and theme stylesheet response were verified in the local site. Full browser visual/accessibility review remains outstanding.

### Resolved WSL hook mismatch — 2026-11-11

Earlier inspection found the WSL app at `0e6e718` without lifecycle hook declarations. The developer later updated the checkout; it is now at the current app source and migration output confirms the `after_migrate` hook runs. The logo asset was linked by `bench build --app cbsua_helpdesk`. A tracked theme integration script now patches the pinned Helpdesk v16 HTML shell so the app-owned Vue CSS loads.

The Workspace is seeded additively from the app-owned definition file; migrations do not overwrite an existing administrator-edited Workspace. References: [Frappe hooks documentation](https://docs.frappe.io/framework/user/en/python-api/hooks) and [Frappe v16 migration source](https://github.com/frappe/frappe/blob/version-16/frappe/migrate.py).

## 4. Branding palette

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

## 5. Installation and verification

From the Frappe Bench root:

~~~bash
bench --site cbsua-helpdesk.localhost migrate
bench build --app helpdesk --app cbsua_helpdesk
python /path/to/cbsua-helpdesk-app/scripts/integrate_helpdesk_branding.py /path/to/frappe-bench
bench --site cbsua-helpdesk.localhost clear-cache
bench --site cbsua-helpdesk.localhost clear-website-cache
bench start
~~~

Run tests:

~~~bash
bench --site cbsua-helpdesk.localhost run-tests --app cbsua_helpdesk
~~~

After migration, open the **CBSUA Helpdesk** Workspace from the Desk sidebar and select **CBSUA Service Office**. The workspace is restricted to System Manager. Confirm ICT is active with intake enabled and all future offices are inactive with intake disabled. Attempting to activate a future office should produce a validation error.

Inspect the Helpdesk config response and verify the logo/favicon URLs return HTTP 200. Confirm the agent interface displays the configured logo and the CBSUA theme stylesheet loads after Helpdesk's compiled stylesheet. Re-run the integration script after replacing or upgrading the Helpdesk v16 app, then rebuild and clear caches. It refuses unexpected page templates without changing them.

## 6. Rollback

1. Back up the local site before migration if it contains data that matters.
2. To remove the native Helpdesk branding defaults, clear or replace the HD Settings fields manually. To remove Desk/website styles, remove the corresponding hooks from hooks.py, then rebuild and clear caches. The migration does not force values back after an administrator changes them.
3. Do not delete office catalogue records after later configuration references them.
4. Production rollback requires a reviewed backup and code release; do not manually drop DocType tables.

## 7. Frappe UI and Custom Actions

Helpdesk `version-16` already uses Frappe UI. CBSUA adapts the existing UI rather than adding another frontend dependency. The app-owned stylesheet and guarded template integration provide the first visual theme layer; Helpdesk Custom Actions are ticket-page Form Scripts, not global theme hooks. Add them only for a specific approved ticket workflow gap and include server-side authorization checks. See [frappe-ui-integration.md](frappe-ui-integration.md).

## 8. Not implemented in M1

HD Team provisioning and membership; ticket office field/routing/automatic assignment; office-scoped permission_query_conditions or has_permission overrides; customer identity policy (OQ-01); ICT categories, SLA, calendars, notifications, and reports; future office activation. These omissions are deliberate. Prove ticket access isolation before onboarding additional offices or entering real institutional ticket data.
