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

The CBSUA app uses Frappe's Desk and website hooks only for those surfaces. The standalone `/helpdesk/` agent application is a Vue/Vite frontend and does not automatically load these hooks. Helpdesk `version-16` already uses `frappe-ui`; CBSUA should adapt that existing dependency rather than add a duplicate. The CBSUA migration now fills blank HD Settings brand fields (`brand_name`, `brand_logo`, `favicon`) with the official logo asset path.

The official PNG is referenced by native HD Settings defaults as well as Frappe branding metadata. This should display the logo in the Helpdesk surfaces that consume the native config. Full green/gold component theming still needs a version-pinned source stylesheet integration. See [Frappe UI integration](../docs/frappe-ui-integration.md) and [M1 configuration](../docs/M1-configuration-and-branding.md).

## Custom Actions

Helpdesk Custom Actions are ticket-specific Form Scripts configured through HD Form Script. They are not a global navigation or branding extension point. Add one only when an approved SRS workflow gap requires it, and always enforce permissions on the server side. See the official [Custom Actions documentation](https://docs.frappe.io/helpdesk/custom-actions) and the integration decision in `../docs/frappe-ui-integration.md`.

## Important limitations

- This change does not configure ticket intake or office routing.
- This change does not provision HD Teams, agents, or managers.
- This change does not prove office-level ticket isolation.
- Future office records must not be activated before their onboarding gate.
- Do not use real tickets or personal information as test fixtures.
