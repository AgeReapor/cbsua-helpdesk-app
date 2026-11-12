# Repository Responsibilities and Ownership

## 1. Repository map

| Repository | Inspected branch | Responsibility | Must not own |
|---|---|---|---|
| [cbsua-app-pilot](https://github.com/AgeReapor/cbsua-app-pilot) | develop | Local host, bench/site lifecycle, app acquisition/validation, process/task orchestration, Admin UI/CLI | Ticket workflow or office policy |
| [cbsua-app-frappe](https://github.com/AgeReapor/cbsua-app-frappe) | develop | Framework runtime and platform services | CBSUA business rules or Helpdesk product logic |
| [cbsua-app-helpdesk](https://github.com/AgeReapor/cbsua-app-helpdesk) | develop | Ticketing product and Helpdesk experience | Host orchestration or CBSUA office policies |
| [cbsua-app-telephony](https://github.com/AgeReapor/cbsua-app-telephony) | develop | Telephony integration app required by Helpdesk metadata | Ticketing system-of-record responsibilities |
| [cbsua-helpdesk-app](https://github.com/AgeReapor/cbsua-helpdesk-app/tree/handoff) | handoff | CBSUA extension, requirements, ADRs, tests and integration docs | Hosting, framework or upstream product forks |

Branch names are observed listings as of 2026-11-12, not a release or compatibility guarantee.

## 2. Change ownership

### Pilot
Changes belong here when they affect host, bench, sites, apps, processes, tasks or Admin UI. Keep CLI/API surfaces thin and delegate behavior to Pilot core objects.

### Frappe
Changes belong here only for genuine framework-level fixes or platform capabilities intended for framework scope. CBSUA ticket policies do not qualify.

### Helpdesk
Generic product defects and capabilities belong here when suitable for the wider Helpdesk product, not just one institution.

### Telephony
Changes belong here for telephony app integration behavior, provider support or defects. Its dependency status does not imply that CBSUA must enable calling features in Phase 1.

### CBSUA extension
Preferred home for institution-specific customizations, subject to requirement approval:
- CBSUA-specific configuration and fixtures;
- approved custom fields or DocTypes not covered natively;
- institution-specific hooks and validation;
- office onboarding configuration and permission tests;
- CBSUA reports and narrowly scoped integrations.

Every custom feature needs a requirement ID, reason native configuration is insufficient, supported version range, tests, migration/rollback notes and owner.

## 3. Dependency and integration contract

- CBSUA extension depends on supported Frappe and Helpdesk interfaces.
- Helpdesk declares its Frappe and Telephony dependencies in app metadata.
- Pilot validates app metadata and shared-environment package resolution.
- Avoid circular imports or runtime dependency from Frappe/Helpdesk back into CBSUA extension.
- Do not add CBSUA ticket policy to Pilot merely because Pilot orchestrates the stack.
- Site configuration does not replace server-side authorization.

## 4. Change-location decision test

1. Host, bench, site, app or process lifecycle? **Pilot.**
2. Framework-wide platform capability or bug? **Frappe.**
3. Generic ticketing capability? **Helpdesk.**
4. Telephony provider/integration? **Telephony.**
5. Institution-specific requirement not met by supported configuration? **CBSUA extension.**
6. Requirement unapproved or layer unclear? Record an ADR/issue before implementation.

## 5. Change and review policy

- Pin source revisions for all platform repositories.
- Do not use moving branch heads for acceptance/production releases.
- Submit changes to the narrowest responsible repository.
- Review cross-repository changes as one coordinated release set.
- Keep CBSUA extension independently testable against a declared matrix.
- Preserve upstream attribution and licenses; do not copy upstream code as a shortcut.
