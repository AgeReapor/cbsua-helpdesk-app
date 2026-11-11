# Helpdesk dependency — M1 integration notes

This folder describes the upstream Helpdesk integration boundary. CBSUA code belongs in the separate cbsua_helpdesk app; do not patch the upstream apps/helpdesk checkout for institutional branding or office configuration.

## Apply M1 locally

From the Bench root:

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

The CBSUA Service Office DocType is a CBSUA metadata catalogue. It does not create native Helpdesk teams or modify ticket permissions. After migration, confirm ICT is the only active office and only ICT intake is enabled. Registrar, Admissions, and Cashier remain disabled.

## Branding integration boundary

The CBSUA app uses Frappe's documented app_include_css and web_include_css hooks to add a restrained palette to Desk and portal pages. The CSS does not modify upstream source files. The Helpdesk agent interface is a Vue application; CSS variables and framework-level selectors are deliberately conservative. A full replacement of Vue component branding requires a separate version-pinned frontend integration and visual regression tests, not broad CSS overrides.

The supplied official PNG is referenced by Frappe branding hooks. The standalone Helpdesk Vue agent interface still requires a separate frontend integration. See docs/M1-configuration-and-branding.md for asset status, palette rationale, verification, and rollback.

## Important limitations

- This change does not configure ticket intake or office routing.
- This change does not provision HD Teams, agents, or managers.
- This change does not prove office-level ticket isolation.
- Future office records must not be activated before their onboarding gate.
- Do not use real tickets or personal information as test fixtures.
