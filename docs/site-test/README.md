# CBSUA Helpdesk clean Site test

This runbook creates a fresh Frappe Site for the `site-test` app branch. It is separate from the main project README because it covers an isolated installation and its verification lifecycle.

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

   If a local `site-test` branch already exists, switch to it instead of creating it again, then verify its commit against the remote branch. The starting branch commit for this runbook is `86af7f425428e573f195b390d8ee6fc56090655f`; use the current remote tip for later runs.

5. Ensure you have an authorized MariaDB administrator credential available at the interactive prompt. The existing Site’s database user has privileges only on its own database and cannot create a second Site database. Do not put a MariaDB password or the new Administrator password in shell history, a command argument, a checked-in file, or a screenshot. If Bench cannot authenticate to MariaDB, stop and arrange authorized database provisioning; do not reuse the old Site’s database or switch the test to an unsupported engine.

## Create the Frappe Site

Run the following from the Bench root. Bench will prompt interactively for the MariaDB root password (if it is not configured for socket authentication) and a new password for the test Site’s `Administrator` account:

```bash
bench new-site cbsua-helpdesk-site-test.localhost
```

Do not set `--set-default`: the existing development Site should remain the default. Do not pass passwords through command-line options.

Bench stores Site-specific configuration under:

```text
sites/cbsua-helpdesk-site-test.localhost/site_config.json
```

That file includes database credentials. Leave it local and untracked.

## Install the apps and migrate

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

Apply database changes with `migrate` before checking a website update. If `bench start` is already running, stop it with Ctrl+C after migration, then start it again from the Bench root:

```bash
bench start
```

Keep this command running in its terminal while checking the Site. If an updated Helpdesk frontend asset is part of the change, build the required assets before restarting:

```bash
bench build --app helpdesk --app cbsua_helpdesk
bench --site cbsua-helpdesk-site-test.localhost migrate
```

Then stop and restart `bench start` again. Open `http://cbsua-helpdesk-site-test.localhost:8000/helpdesk` and `http://cbsua-helpdesk-site-test.localhost:8000/desk`, sign in as the test Site’s Administrator, and hard-refresh after the server restart.

## Clean-install verification

Record the result for each check; do not mark a check complete solely because the migration command exited successfully.

### Installation and configuration

- [ ] `bench --site cbsua-helpdesk-site-test.localhost list-apps` lists the four expected apps.
- [ ] The System Manager workspace for CBSUA Helpdesk is present.
- [ ] The `CBSUA Service Office` DocType opens in Desk.
- [ ] ICT, Registrar, Admissions, and Cashier defaults exist; only ICT is active and intake-enabled.
- [ ] `HD Ticket.cbsua_service_office` exists and is read-only at permission level 7.
- [ ] The CBSUA logo and favicon asset URLs respond successfully.
- [ ] The `/helpdesk` and `/desk` pages render on the new Site.
- [ ] The existing `cbsua-helpdesk.localhost` Site still resolves to its original data.

### Routing and permissions

The clean install does not create an ICT Helpdesk Team, map one to ICT, or provision an agent roster. Do not map ICT to Product Experts or Billing and do not add fake users. Ticket intake is expected to fail closed until CBSUA approves and configures the correct Helpdesk Team and agents.

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

The `site-test` source branch is committed and pushed. The new Frappe Site has not yet been created in the current WSL bench because this session has no non-interactive MariaDB administrator credential; the development Site’s database user cannot provision another database. Do not report the clean-Site installation or app tests as passed until the procedure above is completed.
