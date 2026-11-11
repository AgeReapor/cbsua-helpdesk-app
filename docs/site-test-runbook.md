# Fresh Frappe Site test runbook

**Purpose:** Verify that the CBSUA Helpdesk app installs and migrates on a clean Frappe Site without relying on existing-site data.
**Status:** Repeatable local test procedure; a completed run is recorded separately from the existing development site.

Frappe Sites have separate databases and site-specific configuration. A new Site is a useful install test, while a Git branch isolates the app source; they solve different parts of the test setup. See the official [Create a Site](https://docs.frappe.io/framework/user/en/tutorial/create-a-site) guide.

## 1. Preconditions

- Work from the Frappe Bench root.
- Confirm the Bench has compatible `frappe`, `telephony`, `helpdesk`, and `cbsua_helpdesk` apps checked out.
- Record `bench version` and the app commit IDs for the run.
- Keep the new Site name distinct from the existing development Site. The suggested name is `cbsua-helpdesk-site-test.localhost`.
- Choose a new local Administrator password at the interactive prompt. Do not put it in shell history, source control, or this document.

The application repository is tested on a Git branch named `site-test`; create it from the committed implementation before checking it out in the Bench app checkout. Do not commit site configuration, database content, credentials, or backups.

## 2. Create and install the test Site

From the Bench root, create the Site. Bench asks for MariaDB root credentials and a new Site Administrator password:

~~~bash
bench new-site cbsua-helpdesk-site-test.localhost
~~~

Install the apps in dependency order. Helpdesk requires Telephony; explicitly installing it first makes the dependency visible in the run log:

~~~bash
bench --site cbsua-helpdesk-site-test.localhost install-app telephony
bench --site cbsua-helpdesk-site-test.localhost install-app helpdesk
bench --site cbsua-helpdesk-site-test.localhost install-app cbsua_helpdesk
bench --site cbsua-helpdesk-site-test.localhost migrate
~~~

Check the installed app list:

~~~bash
bench --site cbsua-helpdesk-site-test.localhost list-apps
~~~

Expected: `frappe`, `telephony`, `helpdesk`, and `cbsua_helpdesk`. Frappe is installed when `bench new-site` creates the Site.

## 3. Verify the clean install

If Bench is already running, stop it with Ctrl+C and restart it after migration:

~~~bash
bench start
~~~

Open `http://cbsua-helpdesk-site-test.localhost:8000/desk` and log in as Administrator. Verify:

- The CBSUA Helpdesk Workspace and `CBSUA Service Office` DocType are present.
- ICT, Registrar, Admissions, and Cashier catalogue rows exist; only ICT is active/intake-enabled.
- ICT has no team mapping until an approved ICT Helpdesk Team and roster are configured. New ticket creation should fail closed until then.
- `HD Ticket.cbsua_service_office` exists and is read-only at permission level 7.
- CBSUA logo and favicon paths load; Helpdesk customer/agent views render.
- The existing `cbsua-helpdesk.localhost` database and its configuration remain unchanged.

After the smoke checks, run the app's existing test suite against the new Site:

~~~bash
bench --site cbsua-helpdesk-site-test.localhost run-tests --app cbsua_helpdesk
~~~

Record the date, app commits, migration output, test results, and screenshots or logs that contain no credentials or private ticket data. Do not call the office permission implementation proven until dedicated list, direct-access, search, report, comment, attachment, and reassignment cases pass with separate team accounts.

## 4. Reset and cleanup

Use a new Site name for another independent run. Do not point this runbook at production data. Removing a Site is destructive: `bench drop-site` deletes its database and site files, so use it only when the test Site is no longer needed and its owner has approved removal.
