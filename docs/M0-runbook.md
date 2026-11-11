# M0 — Local Helpdesk baseline runbook

**Status:** Execution guide; verification evidence must be supplied by the developer.  
**Target:** Local Frappe + Telephony + Helpdesk + CBSUA Helpdesk site.  
**Scope:** Installation baseline, login, frontend assets, and minimum smoke test.

## 1. Objective

M0 establishes a known-good local environment before CBSUA-specific ticket
configuration begins. Successful app download and installation are necessary
but insufficient: the site must render, authenticate an administrator, load
the agent/customer interfaces, and pass CBSUA app tests.

M0 is not the ICT MVP and is not a production-readiness claim.

## 2. Capture baseline facts

From the Bench root:

~~~bash
bench --version
bench version
bench --site cbsua-helpdesk.localhost list-apps
~~~

Record OS release, Python, Node, Yarn, MariaDB, Redis, Bench, and exact
versions/commit IDs for all installed apps. Branch names are moving references,
not immutable release evidence. Never record passwords, tokens, cookies,
database dumps, or private ticket content.

## 3. Login diagnosis

The built-in site administrator username is Administrator. Its password is
the site password entered during bench new-site, not the MariaDB root password.
Even if the login form's label mentions email, try the literal username.

If the password is lost, reset it from the Bench root using the installed
Bench command syntax:

~~~bash
bench --site cbsua-helpdesk.localhost set-admin-password 'NEW_PASSWORD'
~~~

Do not put a real password in repository docs, screenshots, or shared logs.
Command-line arguments may persist in shell history or be visible to local
process inspection; handle the new password securely. If syntax differs,
inspect the installed Bench help rather than guessing.

If authentication still fails, capture the non-secret error and verify the
browser is pointed at the correct site.

## 4. Frontend asset diagnosis

Treat broken styling as a frontend asset delivery/build problem until evidence
points elsewhere. Stop bench start first. From the Bench root:

~~~bash
bench build --app frappe --app helpdesk
bench --site cbsua-helpdesk.localhost clear-cache
bench --site cbsua-helpdesk.localhost clear-website-cache
bench start
~~~

Hard-refresh and test /login, /helpdesk, and /help. If styling remains broken,
inspect Developer Tools > Network and Console. Record the first failed CSS/JS
request, status, response type, first relevant console error, build output,
and corresponding server-terminal error. Never patch generated bundles or
manually populate sites/assets as a workaround.

## 5. Diagnostic helper

The repository script scripts/diagnose_m0.sh is read-only. Run it from the
Bench root:

~~~bash
bash /path/to/cbsua-helpdesk-app/scripts/diagnose_m0.sh cbsua-helpdesk.localhost
~~~

It checks command versions, installed apps, service status, expected folders,
and asset directory presence. It does not mutate the environment. Review
output before sharing because it contains host and software metadata.

## 6. Verification procedure

1. Confirm Bench and application versions.
2. Confirm all expected apps are installed on the intended site.
3. Start Bench and load the login page.
4. Sign in as Administrator.
5. Load the agent workspace and customer portal.
6. Confirm CSS/JS requests succeed in browser Developer Tools.
7. Create one disposable test ticket and inspect it as an authorized agent.
8. Run the CBSUA app test command.
9. Confirm future office destinations remain disabled.
10. Record results and unresolved defects without secrets.

## 7. Acceptance criteria

M0 is verified only when each item has evidence:

- [ ] All expected apps are installed on the intended site.
- [ ] The local hostname resolves and the site responds.
- [ ] Administrator authentication succeeds.
- [ ] Login and Helpdesk assets load without unexplained failures.
- [ ] Agent workspace and customer portal render.
- [ ] A disposable test ticket can be created and inspected.
- [ ] CBSUA app tests pass.
- [ ] Future office intake destinations remain disabled.
- [ ] Versions, results, and known issues are recorded without secrets.

If any criterion fails, mark M0 blocked or partially verified. Do not proceed
on the assumption that installation alone proves the baseline is working.

## 8. Explicitly out of scope

M0 does not configure ICT categories, intake, assignment, office routing,
custom roles, office-level ticket isolation, customer identity policy, SLA,
escalation, notifications, reports, production HTTPS, email delivery,
backup/restore acceptance, or Docker. Those require later milestones and
separate acceptance tests.
