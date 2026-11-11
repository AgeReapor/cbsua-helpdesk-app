# Frappe UI integration and CBSUA adaptation

**Status:** M1 implementation guidance; native branding defaults implemented, Vue theme integration documented for the next verified frontend patch.
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

The current public Frappe UI documentation and its agent skill describe the newer 1.x API and semantic token conventions. These are design guidance, not proof that every current API exists in Helpdesk's pinned release candidate. Before using any newer component or prop, verify it against the exact installed package in the local Bench checkout.

## 2. Native Helpdesk branding — implemented

Helpdesk `HD Settings` includes native fields `brand_name`, `brand_logo`, and `favicon`. Its public configuration method `helpdesk.api.config.get_config` returns these fields. The agent frontend's BrandLogo component uses the configured logo.

The CBSUA app's `after_migrate` routine now fills these values only when blank:
- `brand_name`: `CBSUA Helpdesk`
- `brand_logo`: `/assets/cbsua_helpdesk/images/cbsua-logo.png`
- `favicon`: `/assets/cbsua_helpdesk/images/cbsua-logo.png`

The PNG is app-owned and served from Frappe's public asset path. The migration deliberately preserves administrator-supplied values. It does not copy or modify the official source image.

This native configuration is the correct first branding layer for the agent app and supported Helpdesk surfaces. It does not recolor all Vue components.

## 3. CBSUA theme direction

The digital palette is sampled from the official seal supplied to the project. It is a project implementation palette, not a claim of formal approval by CBSUA's communications office.

| Project token | Value | UI role |
|---|---|---|
| `cbsua-green-950` | `#06452A` | Strong headings / rare dark brand surfaces |
| `cbsua-green-900` | `#0B5632` | Hover / pressed brand actions |
| `cbsua-green-800` | `#106031` | Primary institutional accent |
| `cbsua-green-700` | `#197342` | Supporting accent |
| `cbsua-gold-500` | `#ECE249` | Thin accent / active indicator |
| `cbsua-gold-100` | `#FBF8D5` | Limited highlight surface |
| `cbsua-ink` | `#173326` | Brand-specific dark text |

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

The CBSUA app currently registers `app_include_css` and `web_include_css`. Those hooks cover Frappe Desk and website pages; they are not a supported injection mechanism for the standalone Helpdesk Vue bundle at `/helpdesk`.

The supported M1 path is therefore:
1. Configure native Helpdesk branding through HD Settings (implemented).
2. Keep the institutional palette and design rules in this CBSUA app and project documentation.
3. For actual agent-UI recoloring, add a small, reviewed integration to the Helpdesk frontend's source entry stylesheet (currently `desk/src/index.css`) and rebuild Helpdesk assets.
4. Track that integration as a version-pinned patch or maintained fork with an explicit upstream rebase procedure. Do not edit generated files in `helpdesk/public/desk`, `sites/assets`, or `node_modules`.
5. Verify every selector/token against the exact pinned Frappe UI release. Do not copy a current-main token implementation into the older RC without inspection.

No upstream Helpdesk source patch is being claimed as committed by this document. The present repository owns the native settings defaults and the documentation only.

## 6. Custom Actions — use only for ticket-specific workflow gaps

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

## 7. Verification plan

### Native branding
- [ ] Run `bench migrate`.
- [ ] Confirm HD Settings contains the three CBSUA defaults if fields were previously blank.
- [ ] Confirm existing administrator values are preserved on a second migration.
- [ ] Confirm `/api/method/helpdesk.api.config.get_config` returns the configured values for an authenticated test site.
- [ ] Confirm the logo and favicon asset URLs return HTTP 200.
- [ ] Confirm the logo appears in the agent interface and relevant portal/login surfaces.

### UI theme integration (separate frontend patch)
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
- [Helpdesk version-16 Tailwind preset integration](https://github.com/frappe/helpdesk/blob/version-16/desk/tailwind.config.js)
- [Helpdesk native HD Settings schema](https://github.com/frappe/helpdesk/blob/version-16/helpdesk/helpdesk/doctype/hd_settings/hd_settings.json)
- [Helpdesk native config endpoint](https://github.com/frappe/helpdesk/blob/version-16/helpdesk/api/config.py)
- [Helpdesk BrandLogo component](https://github.com/frappe/helpdesk/blob/version-16/desk/src/components/BrandLogo.vue)
- [Frappe UI repository](https://github.com/frappe/frappe-ui)
- [Frappe UI LLM index](https://ui.frappe.io/llms.txt)
- [Frappe UI agent skill](https://github.com/frappe/frappe-ui/tree/main/skills/frappe-ui)
- [Frappe UI semantic token/design guidance](https://ui.frappe.io/docs/design-system/background-color)
