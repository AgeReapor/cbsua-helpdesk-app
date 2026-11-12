# Research Notes and Source Register

**Research date:** 2026-11-12  
**Scope:** CBSUA forks, Pilot architecture/documentation and RPM planning references.

## 1. Repositories inspected

| Repository | Inspected files/metadata | Key observation |
|---|---|---|
| [AgeReapor/cbsua-app-pilot](https://github.com/AgeReapor/cbsua-app-pilot) | README, docs/architecture.md, docs/app-dependencies.md, docs/configuration.md | Pilot-managed benches/sites, CLI/Admin UI, app staging and validation, dependency policy |
| [AgeReapor/cbsua-app-frappe](https://github.com/AgeReapor/cbsua-app-frappe) | pyproject.toml | Python >=3.14,<3.15 on inspected develop |
| [AgeReapor/cbsua-app-helpdesk](https://github.com/AgeReapor/cbsua-app-helpdesk) | README, pyproject.toml | Helpdesk product; metadata targets Frappe 17 development range and Telephony |
| [AgeReapor/cbsua-app-telephony](https://github.com/AgeReapor/cbsua-app-telephony) | README, pyproject.toml | Telephony app; metadata allows Frappe through 17.0.0-dev |
| [AgeReapor/cbsua-helpdesk-app](https://github.com/AgeReapor/cbsua-helpdesk-app) | README, docs index, architecture, roadmap, decisions, SRS | Existing docs describe Bench-centered Frappe 16 setup; extension pyproject not found on inspected main/develop |

## 2. Pilot architecture findings

The CBSUA Pilot fork's architecture guide describes these domain objects:
- Server owns host-level concerns.
- Bench owns bench config, apps, sites, runtime and production setup.
- Site owns site apps, domains, backups, restore and related operations.
- App owns repository acquisition, dependencies, validation and revision management.
- CLI and Admin API delegate to the same core objects.
- Long-running operations use observable tasks.
- App installation stages and validates apps before admitting them to the active app directory.

The app dependency guide describes one shared Python environment. Every app except Frappe must declare a [tool.bench.frappe-dependencies] table in pyproject.toml; Pilot validates compatibility and package resolution during install/update/branch-switch operations.

The missing CBSUA extension metadata is therefore an installation blocker, not merely documentation cleanup.

## 3. Version evidence and caveats

- Helpdesk fork README includes a compatibility matrix showing version-16 paired with version-16 and develop paired with develop.
- Exact inspected Helpdesk fork pyproject.toml says Frappe >=17.0.0-dev,<18.0.0.
- Exact inspected Frappe fork pyproject.toml requires Python >=3.14,<3.15.
- Exact inspected Telephony fork metadata accepts Frappe >=14.101.0,<=17.0.0-dev.
- CBSUA Pilot README says Frappe v16 or later and host CLI requires Python 3.11+; benches use their own Python environment. Confirm exact fork bench runtime is 3.14-compatible.

Metadata is evidence of declared intent, not proof that repositories install and run together. Resolver run and clean-site tests are mandatory.

## 4. RPM references

RPM distinguishes Result (what outcome is wanted), Purpose (why it matters) and Massive Action Plan (flexible actions to achieve it). This handoff applies those distinctions to engineering gates and outcomes; it does not reproduce the source workbook or claim the software lifecycle is itself part of Tony Robbins' method.

## 5. External references

- [Frappe Pilot upstream repository](https://github.com/frappe/pilot) — upstream project purpose, supported platform, local runner, CLI/Admin UI and configuration.
- [Pilot architecture guide](https://github.com/frappe/pilot/blob/develop/docs/architecture.md) — object model, app validation, control flow and state layout.
- [Pilot app dependencies guide](https://github.com/frappe/pilot/blob/develop/docs/app-dependencies.md) — dependency declarations, shared environment and validation.
- [Pilot commands guide](https://github.com/frappe/pilot/blob/develop/docs/commands.md) — command responsibilities and app/site lifecycle.
- [CBSUA Pilot fork](https://github.com/AgeReapor/cbsua-app-pilot) — actual fork selected for local use.
- [CBSUA Frappe fork](https://github.com/AgeReapor/cbsua-app-frappe) — framework source and Python metadata.
- [CBSUA Helpdesk fork](https://github.com/AgeReapor/cbsua-app-helpdesk) — Helpdesk source and compatibility metadata.
- [CBSUA Telephony fork](https://github.com/AgeReapor/cbsua-app-telephony) — Telephony source and dependency metadata.
- [Tony Robbins — requested Rapid Planning Method article](https://www.tonyrobbins.com/blog/tony-robbins-rapid-planning-method-rpm) — user-provided reference; verify current redirect/availability when revisiting.
- [Tony Robbins — RPM Planner FAQs](https://go.tonyrobbins.com/hubfs/PDF/WP-Files/RPM-Planner-FAQs-min.pdf) — explains the Result/Purpose distinction and describes the MAP as a flexible menu of actions.
- [Tony Robbins — Stop reacting and start owning your day](https://www.tonyrobbins.com/blog/stop-reacting-and-start-owning-your-day) — current official article summarizing the three RPM questions.
- [Tony Robbins — Rapid Planning Method](https://www.tonyrobbins.com/events/rapid-planning-method) — official RPM overview.

## 6. Limitations

- Repository inspection used GitHub file and branch metadata; no local Pilot host was provisioned.
- No install, resolver, migration, unit test, browser smoke test or backup/restore test was run.
- Selected documentation and metadata were inspected; this is not a full source-code audit.
- Fork contents can change. Revalidate claims against immutable SHAs before implementation/release.
- The requested Tony Robbins URL may redirect; the planner FAQ PDF was used as an additional primary-source explanation.
