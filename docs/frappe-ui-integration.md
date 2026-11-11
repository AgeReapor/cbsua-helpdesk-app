# Frappe UI integration and CBSUA adaptation

**Status:** M1 implementation; native branding defaults, app-owned Vue theme tokens, and a version-guarded v16 page-shell integration are implemented.
**Target:** Frappe Framework 16 + Frappe Helpdesk `version-16` + the Helpdesk frontend dependency set resolved by that branch.
**Owner:** `cbsua_helpdesk` extension.

## 1. Executive decision

Use the Frappe UI components and design language already used by the selected Helpdesk frontend. Do not add a second UI framework, install a second copy of `frappe-ui`, or upgrade its version as part of CBSUA branding.

Inspection of the upstream Helpdesk `version-16` frontend confirms:
- Vue 3.5.x and Tailwind CSS 3.4.x are used.
- `frappe-ui` is pinned to `1.0.0-rc.1` in `desk/package.json`.
- `@framework/ui` is linked to the Frappe app's `frappe/ui` source.
- `desk/tailwind.config.js` imports the Frappe UI Tailwind preset and includes the framework UI source paths.
- `desk/src/main.js` installs `FrappeUI` and imports the application's `index.css`.
- `BrandLogo.vue` reads the Helpdesk config store and renders `config.brandLogo`, falling back to the Helpdesk logo.

The supplied [Frappe Custom UI App reference](https://github.com/janakvaghela542/Frappe-Custom-UI-App) demonstrates conventional Frappe Desk hooks, public JS/CSS assets, and a custom settings DocType. Its README describes role-based Desk UI controls and ListView actions. Those are useful patterns for Desk-only extensions, but its hooks do not inject styles into Helpdesk's standalone Vue `/helpdesk` application. We will not install it as a dependency or copy its global overrides; we will keep CBSUA-specific extensions small and scoped.

The current public Frappe UI documentation and its agent skill describe the newer 1.x API and semantic token conventions. These are design guidance, not proof that every current API exists in Helpdesk's pinned release candidate. Before using any newer component or prop, verify it against the exact installed package in the local Bench checkout.

## 2. Native Helpdesk branding — implemented

Helpdesk `HD Settings` includes native fields `brand_name`, `brand_logo`, and `favicon`. Its public configuration method `helpdesk.api.config.get_config` returns these fields. The agent frontend's BrandLogo component uses the configured logo.

The CBSUA app fills these values only when blank, through both its `after_install` and `after_migrate` lifecycle hooks. The migration helper checks the live DocType schema, logs missing fields or skipped setup, and logs which defaults it applied. The fields are `Attach Image`/`Data` values in Helpdesk v16; the logo paths below are public app asset URLs:
- `brand_name`: `CBSUA Helpdesk`
- `brand_logo`: `/assets/cbsua_helpdesk/images/cbsua-logo.png`
- `favicon`: `/assets/cbsua_helpdesk/images/cbsua-logo.png`

The PNG is app-owned and served from Frappe's public asset path. The migration deliberately preserves administrator-supplied values. It does not copy or modify the official source image.

This native configuration is the correct first branding layer for the agent app and supported Helpdesk surfaces. It does not recolor all Vue components.

## 3. CBSUA theme direction

The current implementation follows the supplied CBSUA Digital Design System v0.1.0 proposal. The palette remains provisional pending validation by CBSUA's communications office; it is not claimed as an approved institutional standard.

| Project token | Value | UI role |
|---|---|---|
| `brand.primary` | `#174B35` | Primary actions and links |
| `brand.primary-hover` | `#103B2A` | Hover state |
| `brand.primary-subtle` | `#EAF2ED` | Selected and subtle surfaces |
| `brand.accent` | `#C6A04A` | Restrained secondary emphasis |
| `brand.accent-subtle` | `#F6F0E1` | Warm highlight surface |
| `neutral.50` | `#F8FAF8` | Application background |
| `neutral.200` | `#DDE4DE` | Borders and separators |
| `neutral.800` | `#29382F` | Primary text |

### Visual rules

1. Keep most workspace surfaces neutral. Green is an accent, not a page-wide fill.
2. Use one clear primary action per page; secondary actions remain quiet.
3. Gold is decorative/highlight-only where contrast is insufficient for text.
4. Do not recolor ticket status badges indiscriminately. Status colors carry meaning and must remain distinguishable.
5. Preserve Frappe UI focus indicators, keyboard behavior, and component states.
6. Use semantic surface/ink/outline tokens for neutral UI, not fixed gray palette classes.
7. Test both light and dark themes; avoid assuming that a light-mode override is safe in dark mode.

## 4. Frappe UI conventions to follow

The current `https://ui.frappe.io/llms.txt` index and upstream `skills/frappe-ui` guidance establish these conventions for new UI work:

- Prefer existing Frappe UI components over hand-rolled buttons, inputs, dialogs, dropdowns, and other controls.
- Use semantic classes such as `bg-surface-base`, `text-ink-gray-8`, and `border-outline-gray-1`; avoid hardcoded Tailwind gray classes.
- Component color is expressed through `variant` and `theme`, not invented `intent` or `severity` props.
- Inputs use their documented labeling contract; labels must not be replaced by placeholders.
- Overlays use `v-model:open`; input controls use `v-model`.
- Use `useCall`, `useList`, `useDoc`, `useDoctype`, and `useNewDoc` for new Frappe data access when supported by the installed version. Do not introduce raw `fetch`/Axios calls for Frappe endpoints in new components.
- Icons use the documented `lucide-<kebab-case-name>` CSS class / icon string convention. Do not import individual icon Vue components unless the installed app's build explicitly requires it.
- Style component internals through documented `data-slot` / `data-state` hooks only when needed; do not depend on undocumented class injection props.
- Keep exactly one root `FrappeUIProvider` where the application architecture requires it. Do not add a second provider around Helpdesk.

**Version caveat:** Helpdesk currently pins `frappe-ui@1.0.0-rc.1`. The live llms index describes the current published library and may document APIs added after that RC. Use the installed source and package export map as the authority for implementation on this branch.

## 5. Safe integration boundary

The CBSUA app registers `app_include_css` and `web_include_css` for Frappe Desk and normal website pages. Helpdesk's `/helpdesk` page uses a standalone HTML shell and does not load those hooks. Its theme stylesheet, CBSUA page title, browser favicon, and Apple touch icon are therefore integrated by the tracked script through guarded, idempotent edits to `apps/helpdesk/helpdesk/www/helpdesk/index.html`.

Apply the integration after migration and asset build:

```bash
python /path/to/cbsua-helpdesk-app/scripts/integrate_helpdesk_branding.py /path/to/frappe-bench
```

The stylesheet overrides the installed Frappe UI semantic tokens for light surfaces, sidebar, blue action/selection colors, text, outlines, and focus rings. It preserves functional status colors and the dark theme. The brand mark in the sidebar is fitted with contained proportions and a restrained gold keyline; the original asset is unchanged. Re-run the integration script after Helpdesk updates. It checks for the v16 shell and exits without editing if the expected template shape is absent. Never edit generated bundles, `sites/assets`, or `node_modules` for this integration.

The Helpdesk template itself remains an upstream checkout file; the patch script and stylesheet are versioned in the CBSUA app repository so the change can be reapplied and reviewed after upgrades.

### Where to put custom styles

Use the stylesheet that matches the surface being changed:

| Surface | File / mechanism | Use it for |
|---|---|---|
| Frappe Desk and regular website pages | `cbsua_helpdesk/public/css/cbsua_brand.css` via `app_include_css` / `web_include_css` | CBSUA Frappe Desk and standard website chrome |
| Helpdesk agent and customer Vue app at `/helpdesk` | `cbsua_helpdesk/public/css/cbsua_helpdesk.css` loaded by `scripts/integrate_helpdesk_branding.py` | Frappe UI semantic tokens and stable shell-level CBSUA identity |

Keep the Helpdesk stylesheet app-owned and limited to documented semantic tokens or stable, inspected shell selectors. Add new design values as named CBSUA custom properties at the top of that file, then map the corresponding Frappe UI semantic tokens. Preserve Helpdesk status colors, component behavior, and the framework's dark palette. Avoid selectors tied to generated Vite hashes, utility-class combinations that can change between builds, and broad `!important` rules. Do not put Helpdesk Vue rules into `cbsua_brand.css`: its hooks are not present in the standalone Helpdesk shell.

The integration script also replaces Helpdesk's hard-coded document title and favicon/touch-icon URLs. The logo URL carries a version query so browsers refresh a previously cached favicon. After changing app CSS or images, run `bench build --app cbsua_helpdesk`; after replacing or upgrading Helpdesk, run the integration script again and confirm it recognizes the v16 template. Clear site caches and hard-refresh the browser. An unsupported template is left untouched and requires reviewing/revising the tracked script before deployment.

## 6. Studio compatibility boundary

The Helpdesk `develop` branch now documents its customer portal as a Frappe Studio standard app. That implementation is not the same source layout as the selected Helpdesk `version-16` installation. The local project baseline is Frappe 16.56.0 and Helpdesk 16.1.0 on `version-16`; therefore the `develop/studio/` README is an architectural reference, not an implementation instruction for this deployment.

The installed Helpdesk 16.1.0 source confirms that the v16 agent and customer route families use one Vue app with history base `/helpdesk/`. Customer routes include `/helpdesk/my-tickets`, `/helpdesk/my-tickets/:ticketId`, `/helpdesk/kb-public`, `/helpdesk/kb-public/:categoryId`, and `/helpdesk/kb-public/articles/:articleId`. The v16 router redirects unauthenticated visitors to login, including on its customer portal routes. The standalone `/help` route below belongs to the newer Studio portal architecture and must not be presented as the v16 route.

The upstream `develop` Studio README describes:
- JSON page block trees with TypeScript setup scripts and reusable Vue components.
- Source-controlled pages under `studio/helpdesk/`, synchronized into Studio DocTypes during migration.
- A separate Studio frontend development loop (`watch-studio`) and production build.
- A customer portal at `/help`; this is the Studio-based `develop` route. In the selected v16 source, customer and agent route families share the `/helpdesk/` Vue app.

Do not copy Studio page JSON, scripts, or components into this CBSUA app or upgrade Helpdesk solely to obtain Studio without a separate compatibility and migration plan. For the current v16 baseline, configure the existing Helpdesk portal using the supported settings and native features. If a future approved upgrade adopts the Studio-based portal, keep CBSUA branding in source-controlled Studio app assets/components and test guest, customer, and agent access separately.

Reference: [Helpdesk develop Studio README](https://github.com/frappe/helpdesk/blob/develop/studio/README.md).
## 7. Custom Actions — use only for ticket-specific workflow gaps

The official Helpdesk Custom Actions documentation describes Form Scripts attached to `HD Ticket` using `HD Form Script`. A script returns an `actions` array and receives ticket context such as `doc`, `updateField`, `call`, `router`, `$dialog`, and `createToast`. Scripts can be enabled for agent ticket views, customer ticket views, or new-ticket pages, with function support varying by page.

This is a useful native extension point for a future, approved ICT ticket action. It is not a global branding hook and should not be used to add app navigation, global buttons, or theme CSS.

Before creating a custom action:
- Identify the exact SRS requirement and user role.
- Check whether a native Helpdesk setting or workflow already covers it.
- Use server-side validation and permission checks for any consequential operation; a hidden button is not authorization.
- Avoid embedding secrets or trusting arbitrary client-provided ticket identifiers.
- Document customer-portal exposure separately.
- Add a test for authorized and unauthorized users.

No custom ticket action is added in this M1 change because the current SRS does not identify a specific additional ticket-page action that cannot be met by native Helpdesk functionality.

## 7. Verification status

### Native branding
- [ ] Confirm the CBSUA app is installed on the site (`bench --site cbsua-helpdesk.localhost list-apps`).
- [ ] Confirm Frappe resolves the CBSUA lifecycle hooks (`bench --site cbsua-helpdesk.localhost console`, then inspect `frappe.get_hooks('after_migrate', app_name='cbsua_helpdesk')`).
- [ ] Run `bench migrate` and inspect the site log for the `cbsua_helpdesk` branding messages if values remain blank.
- [ ] Confirm HD Settings contains the three CBSUA defaults if fields were previously blank.
- [ ] Confirm existing administrator values are preserved on a second migration.
- [ ] Confirm `/api/method/helpdesk.api.config.get_config` returns the configured values for an authenticated test site.
- [ ] Confirm the logo and favicon asset URLs return HTTP 200.
- [ ] Complete browser review of the logo and theme on agent, customer, and login surfaces.

### UI theme integration
- [ ] Pin exact Helpdesk and Frappe UI commits/versions.
- [ ] Add only source-level CSS imports/overrides; never edit generated bundles.
- [ ] Run the Helpdesk frontend production build.
- [ ] Review agent navigation, ticket list, ticket detail, forms, dialogs, dropdowns, and status badges.
- [ ] Review customer portal and new-ticket screens.
- [ ] Test light and dark mode, keyboard focus, reduced viewport, and contrast.
- [ ] Run existing Helpdesk tests and a ticket create/reply/status smoke test.

### M1 configuration
- [ ] Run CBSUA app tests.
- [ ] Confirm ICT remains the only active office and only ICT intake is enabled.
- [ ] Confirm future offices remain disabled.
- [ ] Do not infer ticket isolation from the office catalogue flags.

## 8. Local application instructions

From the Bench root:

~~~bash
bench --site cbsua-helpdesk.localhost migrate
bench build --app helpdesk --app cbsua_helpdesk
bench --site cbsua-helpdesk.localhost clear-cache
bench --site cbsua-helpdesk.localhost clear-website-cache
bench --site cbsua-helpdesk.localhost run-tests --app cbsua_helpdesk
~~~

Then restart `bench start` and hard-refresh the browser. If HD Settings already had non-empty branding values, the migration intentionally leaves them unchanged; review or set them manually if required.

## 9. Upstream references

- [Frappe Helpdesk Custom Actions](https://docs.frappe.io/helpdesk/custom-actions)
- [Helpdesk version-16 frontend package](https://github.com/frappe/helpdesk/blob/version-16/desk/package.json)
- [Helpdesk version-16 frontend entry](https://github.com/frappe/helpdesk/blob/version-16/desk/src/main.js)
- [Helpdesk version-16 frontend routes](https://github.com/frappe/helpdesk/blob/version-16/desk/src/router/index.ts)
- [Helpdesk version-16 app page](https://github.com/frappe/helpdesk/blob/version-16/helpdesk/www/helpdesk/index.py)
- [Helpdesk version-16 Tailwind preset integration](https://github.com/frappe/helpdesk/blob/version-16/desk/tailwind.config.js)
- [Helpdesk native HD Settings schema](https://github.com/frappe/helpdesk/blob/version-16/helpdesk/helpdesk/doctype/hd_settings/hd_settings.json)
- [Helpdesk native config endpoint](https://github.com/frappe/helpdesk/blob/version-16/helpdesk/api/config.py)
- [Helpdesk BrandLogo component](https://github.com/frappe/helpdesk/blob/version-16/desk/src/components/BrandLogo.vue)
- [Frappe UI repository](https://github.com/frappe/frappe-ui)
- [Frappe UI LLM index](https://ui.frappe.io/llms.txt)
- [Frappe UI agent skill](https://github.com/frappe/frappe-ui/tree/main/skills/frappe-ui)
- [Frappe UI semantic token/design guidance](https://ui.frappe.io/docs/design-system/background-color)
