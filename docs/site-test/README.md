# CBSUA Helpdesk clean Site test

This runbook covers setup, local deployment, localhost access, verification, and cleanup for the `site-test` Frappe Site. It is separate from the main project README because it documents this isolated test environment rather than the main development Site or a production deployment.

## What the test isolates

There are two separate things called a “site” in this workflow:

- The Git branch `site-test` selects the CBSUA app source revision.
- The Frappe Site `cbsua-helpdesk-site-test.localhost` gets its own database and its own site directory under the Bench `sites/` folder.

The Site directory is created by Bench at `<bench>/sites/cbsua-helpdesk-site-test.localhost`. Keep credentials and local site data there; do not add that runtime directory or its `site_config.json` to the app repository. This runbook belongs in the repository at `docs/site-test/README.md`, so it can be reviewed and committed without putting documentation beside private site configuration.

The test uses the bench’s existing MariaDB service and its installed Frappe, Telephony, and Helpdesk versions. Frappe’s [Create a Site guide](https://docs.frappe.io/framework/user/en/tutorial/create-a-site) describes the site creation and app installation commands. For this v16 bench, use the configured MariaDB backend; do not use SQLite as a shortcut for a clean Helpdesk install. See the [Frappe installation requirements](https://docs.frappe.io/framework/user/en/installation).

## Names and locations

| Purpose | Value |
|---|---|
| Bench root | `/home/kadinarudess/frappe/frappe-bench` on the current WSL workstation; use your actual Bench root elsewhere |
| App checkout | `<bench>/apps/cbsua_helpdesk` |
| App branch | `site-test` |
| Test Site name | `cbsua-helpdesk-site-test.localhost` |
| Runtime Site directory | `<bench>/sites/cbsua-helpdesk-site-test.localhost` |
| Existing development Site | `cbsua-helpdesk.localhost` |

The app branch and Frappe Site are separate: checking out `site-test` changes app source in the Bench, while the Site name selects its database and configuration. Both Sites can be served by the same local Bench on port `8000`; use the matching hostname in the browser so Frappe routes to the intended Site.

The test Site must have a different database from the development Site. Do not copy the existing Site’s database or configuration into the test.

## Prerequisites

1. Use the Frappe Bench that already contains compatible checkouts of `frappe`, `telephony`, `helpdesk`, and `cbsua_helpdesk`.
2. Confirm the current development Site is listed and the four apps are available:

   ```bash
   bench version
   bench --site cbsua-helpdesk.localhost list-apps
   git -C apps/cbsua_helpdesk status --short --branch
   git -C apps/cbsua_helpdesk rev-parse HEAD
   ```

3. Check the app checkout for local edits before switching branches. If it has local work, preserve it first; do not use `git reset --hard` or `git clean`:

   ```bash
   git -C apps/cbsua_helpdesk stash push -u -m 'before site-test branch checkout'
   ```

   The stash keeps tracked and untracked app changes available for later review. This step does not apply to the separate Helpdesk checkout; leave unrelated Helpdesk working-tree changes alone.

4. Fetch and check out the committed branch. Replace `upstream` with the remote name shown by `git -C apps/cbsua_helpdesk remote -v` if needed. In the current WSL app checkout, the remote is named `upstream`.

   ```bash
   git -C apps/cbsua_helpdesk fetch upstream +refs/heads/site-test:refs/remotes/upstream/site-test
   git -C apps/cbsua_helpdesk switch -c site-test refs/remotes/upstream/site-test
   git -C apps/cbsua_helpdesk status --short --branch
   git -C apps/cbsua_helpdesk log -1 --oneline
   ```

   If a local `site-test` branch already exists, switch to it instead of creating it again, then verify its commit against the remote branch. The initial branch commit was `86af7f425428e573f195b390d8ee6fc56090655f`; the implementation run recorded below used commit `7a2b99e`. Use the current remote tip for later runs.

5. Ensure you have an authorized MariaDB administrator credential available at Bench's interactive prompt. The existing Site’s database user may have privileges only on its own database and cannot create another Site database. Do not put a MariaDB password or the new Administrator password in shell history, a command argument, a checked-in file, or a screenshot. If Bench cannot authenticate to MariaDB, arrange authorized database provisioning; do not reuse the old Site’s database or switch the test to an unsupported engine.

## Create the Frappe Site

Run this once from the Bench root when creating a fresh test Site. The current WSL test Site has already been created, so do not repeat this command against it. Bench will prompt for MariaDB authentication (unless the configured database account uses socket authentication) and a new password for the test Site’s `Administrator` account:

```bash
bench new-site cbsua-helpdesk-site-test.localhost
```

Do not set `--set-default`: the existing development Site should remain the default. Do not pass passwords through command-line options.

Bench stores Site-specific configuration under:

```text
sites/cbsua-helpdesk-site-test.localhost/site_config.json
```

That file includes database credentials. Leave it local and untracked.

## Deploy source updates to the local test Site

For first-time installation, use the one-time install procedure below. For an existing Site, do not reinstall apps. To deploy a reviewed `site-test` source update to this local Site, run from the Bench root:

```bash
git -C apps/cbsua_helpdesk status --short --branch
git -C apps/cbsua_helpdesk fetch upstream
git -C apps/cbsua_helpdesk switch site-test
git -C apps/cbsua_helpdesk pull --ff-only upstream site-test
bench build --app helpdesk --app cbsua_helpdesk
bench --site cbsua-helpdesk-site-test.localhost migrate
bench --site cbsua-helpdesk-site-test.localhost clear-cache
bench --site cbsua-helpdesk-site-test.localhost clear-website-cache
```

Review the app working tree before fetching or switching. Preserve local edits rather than resetting or cleaning them. If the checkout uses a remote name other than `upstream`, substitute its configured remote. The build step refreshes bundled frontend and public assets; migration applies DocType and fixture changes to this Site's database. Follow a separate build procedure for changed assets owned by other apps or for a changed Helpdesk template.

This procedure deploys code to a local development/test Site only. It is not a production deployment procedure: `bench start` is a development server, and this repo does not provide the production infrastructure, TLS, process supervision, backup/restore, monitoring, or release automation needed for production.

## Install the apps and migrate (first time only)

Install the dependencies in order so the log clearly records each app:

```bash
bench --site cbsua-helpdesk-site-test.localhost install-app telephony
bench --site cbsua-helpdesk-site-test.localhost install-app helpdesk
bench --site cbsua-helpdesk-site-test.localhost install-app cbsua_helpdesk
bench --site cbsua-helpdesk-site-test.localhost migrate
bench --site cbsua-helpdesk-site-test.localhost list-apps
```

Expected installed apps: `frappe`, `telephony`, `helpdesk`, and `cbsua_helpdesk`. Record the output and the commit IDs of all four app checkouts. A successful `new-site` alone does not verify that the CBSUA app installs or migrates.

## Start or restart the Bench before browser checks

After the build, migration, and cache clearing are complete, restart the development server before checking a website update. If `bench start` is already running, stop it with Ctrl+C, then start it from the Bench root:

```bash
bench start
```

Keep this command running in its terminal while checking the Site. Do not close the terminal while using the local test Site.

## Localhost access

With `bench start` running in the WSL Bench root, open these URLs from the Windows or WSL browser:

| Purpose | URL |
|---|---|
| Helpdesk portal | [http://cbsua-helpdesk-site-test.localhost:8000/helpdesk](http://cbsua-helpdesk-site-test.localhost:8000/helpdesk) |
| Frappe Desk | [http://cbsua-helpdesk-site-test.localhost:8000/desk](http://cbsua-helpdesk-site-test.localhost:8000/desk) |
| Login | [http://cbsua-helpdesk-site-test.localhost:8000/login](http://cbsua-helpdesk-site-test.localhost:8000/login) |
| Customer tickets | [http://cbsua-helpdesk-site-test.localhost:8000/helpdesk/my-tickets](http://cbsua-helpdesk-site-test.localhost:8000/helpdesk/my-tickets) |

Sign in with the `Administrator` account created for this Site when checking Desk configuration. Use separate customer and agent test accounts for portal and access-control checks. The Administrator credentials are Site-specific; they are not the credentials for `cbsua-helpdesk.localhost`.

From WSL, a quick HTTP check is:

```bash
curl -I http://cbsua-helpdesk-site-test.localhost:8000/helpdesk
```

If the `.localhost` name does not resolve in the browser, first confirm the server is running and the request reaches port `8000`. From WSL, test Frappe's hostname-based Site routing directly with:

```bash
curl -I -H 'Host: cbsua-helpdesk-site-test.localhost' http://127.0.0.1:8000/helpdesk
```

The `Host` header is essential when testing by IP because the Bench may contain more than one Site. If the WSL request works but the Windows browser cannot resolve the name, configure the host's local name resolution for `cbsua-helpdesk-site-test.localhost` to loopback using the host's normal administrator-managed process. Do not change the Bench's default Site to work around a hostname problem.

After the page loads, hard-refresh the browser and verify the CBSUA theme, logo, and favicon. Use the browser Network panel or `curl -I` on the asset URL to distinguish a stale browser cache from a missing asset. A successful `/desk` response alone does not verify customer login, agent access, or office isolation.

## Clean-install verification

Record the result for each check; do not mark a check complete solely because the migration command exited successfully.

### Installation and configuration

- [ ] `bench --site cbsua-helpdesk-site-test.localhost list-apps` lists the four expected apps.
- [ ] The System Manager workspace for CBSUA Helpdesk is present.
- [ ] The `CBSUA Service Office` DocType opens in Desk.
- [ ] ICT, Registrar, Admissions, and Cashier defaults exist; ICT alone is active, and intake is initially disabled until a test/approved Helpdesk Team is mapped.
- [ ] `HD Ticket.cbsua_service_office` exists, is read-only in Desk, and is assigned by server logic.
- [ ] The CBSUA logo and favicon asset URLs respond successfully.
- [ ] The `/helpdesk` and `/desk` pages render on the new Site.
- [ ] The existing `cbsua-helpdesk.localhost` Site still resolves to its original data.

### Routing and permissions

The clean install does not create an ICT Helpdesk Team, map one to ICT, or provision an agent roster. For an isolated functional routing check, configure a clearly test-only native team in the fresh Site:

1. In Desk, create `HD Team` named `CBSUA ICT Support (site-test)`. Leave its roster empty, keep `ignore_restrictions` off, and do not reuse Product Experts or Billing.
2. Open **CBSUA Helpdesk → CBSUA Service Office**, edit ICT, set **Helpdesk Team** to the test team, and enable **Allow Customer Intake**.
3. Save. The app should reject enabling intake without a mapped, enabled team. New ticket creation should stamp ICT and the test team server-side.
4. Try changing or clearing `cbsua_service_office` on an existing ticket through a direct API request; the server should reject it. An unclassified legacy ticket must stay unclassified.

This empty test team verifies configuration and routing only. It does not prove that agents can process tickets or that office isolation works. For access-control evidence, use separately approved non-admin test accounts and mapped teams; do not count Administrator access as an isolation test.

Treat office isolation as unverified until separate agent accounts are used to test list view, direct document access, search, reports, comments, attachments, assignment, and reassignment against tickets from multiple offices. A successful app test suite is not proof of end-to-end authorization.

### Run the existing app tests

The requested clean-Site experiment includes running the app’s existing tests after the app has been installed and migrated:

```bash
bench --site cbsua-helpdesk-site-test.localhost run-tests --app cbsua_helpdesk
```

Save the pass/fail summary and relevant failure traceback without credentials, private ticket content, or personal data. Do not add tests as part of this runbook unless the implementation scope calls for it.

## Record the run

For each run, capture the following in a separate result note or the task report:

```text
Date and timezone:
Bench path:
Site name:
Frappe version and commit:
Telephony commit:
Helpdesk version and commit:
CBSUA app branch and commit:
Site creation result:
Install and migration result:
Browser smoke-check result:
Existing CBSUA app test result:
Outstanding configuration or authorization gaps:
```

Do not record passwords or database connection strings. Keep screenshots free of private ticket data.

## Cleanup

Keep the test Site for review unless it is no longer needed. Removing a Site is destructive: `bench drop-site cbsua-helpdesk-site-test.localhost` deletes its database and Site files. Back up anything needed and confirm the exact target before running that command. Do not drop or overwrite `cbsua-helpdesk.localhost` as part of this test.

## Current attempt

The `site-test` branch is committed and pushed. The fresh Site `cbsua-helpdesk-site-test.localhost` was created in the WSL Bench at `/home/kadinarudess/frappe/frappe-bench`; `telephony`, `helpdesk`, and `cbsua_helpdesk` were installed, assets were built, and migration completed. The app branch was at commit `7a2b99e` during the recorded implementation run.

The test command `bench --site cbsua-helpdesk-site-test.localhost run-tests --app cbsua_helpdesk` was invoked and exited with status 0, but the captured output did not include a test count or pass/fail summary. Treat the test result as **unverified** until the test log shows a completed passing run. The live browser check and ICT team/intake configuration are also pending; do not mark the visual, routing, or authorization checks above complete based on installation and migration alone. Re-run the checks from the Bench root using the instructions in this guide, then record the verified results and dependency commits here.
