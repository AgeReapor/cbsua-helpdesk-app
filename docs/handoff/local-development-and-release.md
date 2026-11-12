# Pilot-First Local Development and Release Workflow

## 1. Operating principle

Pilot is the supported operator interface for the local environment. Do not recreate a parallel Bench lifecycle with separate instructions for initializing benches, starting processes, cloning apps, creating sites and managing services.

Use the CBSUA Pilot fork's README, CLI help and Admin UI as the command contract. The official Pilot project describes a local runner, Admin UI, CLI, app acquisition, site management and task-based operations. The CBSUA fork may differ; verify exact behavior against its checked-out revision.

## 2. First-time local host setup

1. Review requirements and installation instructions in [cbsua-app-pilot](https://github.com/AgeReapor/cbsua-app-pilot).
2. Confirm host OS support, Python host runtime, Node.js, database prerequisites and permissions.
3. Install the CBSUA Pilot fork using its documented installer source.
4. Launch Pilot and complete its setup wizard.
5. Create a dedicated development bench through Pilot.
6. Configure the Frappe source repository/revision selected by the compatibility decision.
7. Start local services through Pilot and verify Admin UI reachability.
8. Record host and bench configuration without committing secrets.

The current fork README identifies this installer source:

~~~sh
curl -fsSL https://raw.githubusercontent.com/AgeReapor/cbsua-app-pilot/develop/install.sh | bash
~~~

Review the script and source-trust policy before executing it on an institutional computer. This handoff does not execute it.

## 3. Add platform applications to the bench

Use the Pilot CLI/Admin UI workflow to add the selected repositories:
- Frappe Framework;
- Telephony;
- Frappe Helpdesk;
- CBSUA Helpdesk extension.

The fork README documents the general CLI pattern: pilot -b <bench> get-app <repo>. Confirm exact syntax against the checked-out CBSUA Pilot revision.

**Adding app source to a bench and installing an app on a site are separate operations.** Pilot dependency validation must accept the full app set before site installation. Verify Telephony installation state explicitly; do not assume dependency installation behavior without checking the selected Pilot version.

## 4. Create and configure a development site

1. Create a local test site using Pilot Admin UI or documented CLI.
2. Install required apps on that site using Pilot's supported site app-install workflow.
3. Confirm installed-app list contains the expected framework, Helpdesk, Telephony and CBSUA app entries.
4. Apply migrations/build assets through supported Pilot tasks/CLI.
5. Configure only approved Phase 1 ICT teams, categories, roles and portal behavior.
6. Use synthetic test identities and data.

Do not reuse the previous README's direct bench new-site/get-app/install-app/start or direct git pull instructions as the canonical Pilot workflow.

## 5. Developing the CBSUA extension

- Work in the CBSUA extension repository, not inside vendored Helpdesk/Frappe source, unless a genuine upstream fix is required.
- Use Pilot-supported app development/workspace features if available in the selected fork.
- Keep pyproject.toml, hooks, DocTypes, fixtures, patches and tests aligned with Pilot validation.
- Add only behavior linked to an approved requirement.
- Verify migrations on a disposable site before a shared development site.
- Never edit generated assets or installed app copies as source of truth.

## 6. Local validation checklist

- [ ] Pilot CLI/Admin UI report the expected bench.
- [ ] Frappe, Helpdesk, Telephony and CBSUA revisions are recorded.
- [ ] Pilot dependency validation passes for all apps.
- [ ] Site is reachable through Pilot-managed local runner.
- [ ] Intended apps are installed on the site.
- [ ] Migrations complete without error.
- [ ] Helpdesk agent and customer portals load.
- [ ] A synthetic ICT ticket can be created, assigned, replied to and resolved.
- [ ] Cross-role and cross-office negative authorization tests pass.
- [ ] Workers and scheduler are healthy.
- [ ] Logs contain no unresolved startup, migration or asset errors.

## 7. Promotion model

~~~mermaid
flowchart LR
  Dev["Local development bench"]
  Review["Code review + dependency validation"]
  QA["Integration / acceptance site"]
  Gate["RPM release gate"]
  Prod["Approved deployment target"]
  Dev --> Review --> QA --> Gate --> Prod
~~~

A promotion package must include immutable app SHAs, exact Pilot/runtime versions, dependency-resolution evidence, migration/build/test results, requirement traceability, site configuration changes, backup/restore evidence, rollback procedure, release owner and approval.

## 8. Updating and rollback

- Update app sources through Pilot's app update workflow.
- Validate revisions and dependencies before site migration.
- Back up database and files together before schema-changing updates.
- Apply migrations through Pilot's supported task path.
- Run smoke and authorization tests after update.
- Stop promotion and restore the last known-good release if validation fails.

Do not manually change installed app source folders, run unconstrained package installers, or update one repository independently when compatibility is affected.
