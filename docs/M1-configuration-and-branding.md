# M1 — CBSUA configuration foundation and branding

**Status:** Initial implementation committed; local migration and visual review required.  
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
| cbsua_helpdesk/public/images/cbsua-brand-mark.svg | Temporary compact app icon; not a substitute for the official seal |
| tests/test_configuration.py | Safe-default and activation-gate tests |

CBSUA Service Office is configuration metadata only. It is not a Helpdesk Team, ticket, assignment rule, route, or permission boundary.

## 3. Office catalogue defaults

| Code | Phase | Active | Customer intake |
|---|---|---:|---:|
| ICT | Phase 1 | Yes | Yes |
| REGISTRAR | Future | No | No |
| ADMISSIONS | Future | No | No |
| CASHIER | Future | No | No |

The controller rejects activation of a non-ICT office and rejects customer intake for inactive offices. This is a configuration guard, not a replacement for Frappe permissions.

The migration seed is additive and idempotent. Existing records are not silently overwritten on later migrations. Review and correct manually changed records explicitly.

## 4. Branding palette

The palette is sampled from the supplied CBSUA seal and translated into usable digital interface colors:

| Token | Value | Intended use |
|---|---|---|
| Deep green | #06452A | Strong headings / darkest institutional surface |
| Primary green | #106031 | Primary actions, links, brand accents |
| Supporting green | #197342 | Hover/focus and secondary emphasis |
| Seal gold | #ECE249 | Thin accents and small highlights |
| Soft gold | #FBF8D5 | Subtle highlight surface |
| Ink | #173326 | Main text |

Gold is not used as small text on white because contrast is insufficient. The stylesheet avoids changing every component or hardcoding typography across the Helpdesk Vue application. Confirm final typography, official logo usage, and exact rules with CBSUA PIO.

### Public website observations

The public CBSUA homepage currently uses the institutional tagline “Education for Sustainable Human Development” and includes an Online Services section. The university's About Us navigation also provides a dedicated “Seal, Coat of Arms, and Hymn” reference page. These are useful identity and information-architecture references for a future customer portal: institutional naming, recognizable seal usage, clear service entry points, and accessible information hierarchy. This M1 implementation uses the seal's green/gold colors and CBSUA naming, but does not copy website layout or claim to have scraped/downloaded every website asset. See [CBSUA homepage](https://cbsua.edu.ph/) and [About Us / Board of Regents navigation](https://cbsua.edu.ph/about-us/board-of-regents/).

### Framework integration reference

The Desk and portal stylesheet is registered using Frappe's documented `app_include_css` and `web_include_css` hooks. The navbar mark uses the documented `brand_html` hook. See [Frappe Hooks documentation](https://docs.frappe.io/framework/user/en/python-api/hooks).

### Logo asset status

The uploaded full-resolution seal is available in the project conversation, but the GitHub file-writing connector accepts UTF-8 text and has no binary upload operation. The official PNG has therefore not been committed as a binary file in this change. The SVG in public/images is a clearly documented temporary icon treatment, not the supplied official seal. Replace it with the approved seal once a binary asset can be added through a Git-capable local checkout or supported upload flow. Preserve the attribution supplied with the image.

## 5. Installation and verification

From the Frappe Bench root:

~~~bash
bench --site cbsua-helpdesk.localhost migrate
bench build --app cbsua_helpdesk
bench --site cbsua-helpdesk.localhost clear-cache
bench --site cbsua-helpdesk.localhost clear-website-cache
bench start
~~~

Run tests:

~~~bash
bench --site cbsua-helpdesk.localhost run-tests --app cbsua_helpdesk
~~~

After migration, inspect CBSUA Service Office in Desk. Confirm ICT is active with intake enabled and all future offices are inactive with intake disabled. Attempting to activate a future office should produce a validation error.

Inspect the browser Network panel for cbsua_brand.css and review Desk/portal at desktop and mobile widths. If the asset is not requested, review hooks and rebuild/cache.

## 6. Rollback

1. Back up the local site before migration if it contains data that matters.
2. To remove branding only, remove app_include_css and web_include_css entries from hooks.py, then migrate/clear cache/build.
3. Do not delete office catalogue records after later configuration references them.
4. Production rollback requires a reviewed backup and code release; do not manually drop DocType tables.

## 7. Not implemented in M1

HD Team provisioning and membership; ticket office field/routing/automatic assignment; office-scoped permission_query_conditions or has_permission overrides; customer identity policy (OQ-01); ICT categories, SLA, calendars, notifications, and reports; future office activation. These omissions are deliberate. Prove ticket access isolation before onboarding additional offices or entering real institutional ticket data.
