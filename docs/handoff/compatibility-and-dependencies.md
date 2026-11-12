# Compatibility and Dependency Policy

**Observation date:** 2026-11-12

## 1. Observed metadata

| Repository/app | Inspected metadata | Observed constraint |
|---|---|---|
| cbsua-app-frappe / frappe | pyproject.toml | Python >=3.14,<3.15 |
| cbsua-app-helpdesk / helpdesk | pyproject.toml | Frappe >=17.0.0-dev,<18.0.0; Telephony >=0.0.1,<1.0.0; Python >=3.14 |
| cbsua-app-telephony / telephony | pyproject.toml | Frappe >=14.101.0,<=17.0.0-dev; Python >=3.10 |
| cbsua-helpdesk-app / cbsua_helpdesk | pyproject.toml | Not found on inspected main or develop; must be added before Pilot validation |

These are declarations, not a successful resolver run. Exact installed versions, commit SHAs and full dependency resolution are not certified.

## 2. Compatibility discrepancy — release blocker

The old CBSUA Helpdesk README recommends Frappe 16 and Helpdesk 16. The inspected Helpdesk fork metadata instead declares:

~~~toml
[tool.bench.frappe-dependencies]
frappe = ">=17.0.0-dev,<18.0.0"
telephony = ">=0.0.1,<1.0.0"
~~~

The Frappe fork metadata declares Python >=3.14,<3.15. Therefore, the previous Frappe 16 instructions are obsolete for the currently inspected fork revisions. Do not install Frappe 16 merely because the old README says so.

The Helpdesk README's compatibility matrix is generic/upstream guidance. The CBSUA fork's current pyproject.toml is the authoritative declaration for that exact revision. Resolve the discrepancy by aligning fork revisions/metadata to a deliberately selected compatible release set, or by updating docs and metadata to the selected Frappe 17-compatible set.

Do not loosen dependency declarations just to force Pilot to accept an app.

## 3. Pilot app validation requirements

The inspected CBSUA Pilot fork's App Dependencies guide states:
- every app except Frappe must declare a [tool.bench.frappe-dependencies] table in pyproject.toml;
- each Frappe app dependency must use a real version range;
- Pilot validates compatibility and package resolution before admitting an app;
- all apps share one Python environment, so package conflicts must be resolved;
- install, update and branch-switch paths apply validation.

The CBSUA extension therefore needs a valid project metadata file before Pilot installation. At minimum, after selecting and testing target versions, declare supported Frappe and Helpdesk ranges. Do not invent final ranges before checking imports and supported APIs.

Illustrative shape only; values are placeholders, not approved pins:

~~~toml
[project]
name = "cbsua_helpdesk"
requires-python = ">=3.14,<3.15"

[tool.bench.frappe-dependencies]
frappe = "REPLACE_WITH_TESTED_RANGE"
helpdesk = "REPLACE_WITH_TESTED_RANGE"
~~~

Confirm the app's import name and packaging conventions. If Pilot expects a specific dependency key/name, follow the selected Pilot implementation.

## 4. Dependency resolution policy

1. Select Frappe, Helpdesk and Telephony revisions together.
2. Read each pyproject.toml at the exact commit SHA.
3. Confirm Python/system requirements against the Pilot bench runtime.
4. Add CBSUA extension metadata with honest tested ranges.
5. Run Pilot validation/install and retain resolver output.
6. Record app SHAs and package resolution evidence.
7. Run migrations, asset build, app tests and end-to-end smoke tests.
8. Repeat validation on every update and before release.

Because all apps share one environment, package conflicts are compatibility failures. Do not solve them with ad-hoc pip installs inside the managed bench.

## 5. Release manifest

Record for each tested environment/release:
- Pilot, Frappe, Helpdesk, Telephony and CBSUA extension URLs, refs and immutable commit SHAs;
- exact Python and Node.js versions;
- database engine/version and Redis/runtime details;
- site installed-app list and versions;
- Pilot validation result, test runs and acceptance evidence.

No production or acceptance release should be identified only by moving branch names such as develop.

## 6. Open compatibility questions

- Does the selected Pilot revision create benches with Python required by the Frappe fork?
- Is Helpdesk intentionally targeting Frappe 17 development, or should it be aligned to a stable release?
- What exact dependency range should CBSUA extension declare for Helpdesk?
- Must Telephony be installed on the site, and can its features remain unused in Phase 1?
- Are all system packages and frontend build requirements covered by Pilot?
- Is extension metadata absent on all maintained branches, or only inspected main/develop?

Resolve these before the first repeatable local installation.
