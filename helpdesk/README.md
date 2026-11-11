# Frappe Helpdesk — local setup and M0 verification

This folder documents the upstream Frappe Helpdesk dependency used by CBSUA.
It is not a fork or a second ticketing implementation. The upstream source is
frappe/helpdesk; in a local Bench its checkout normally lives at apps/helpdesk.
The CBSUA extension is the separate cbsua_helpdesk app in this repository.

## 1. M0 purpose and boundary

M0 proves that the local platform is usable before CBSUA-specific ticket
configuration is added. It covers installation, site reachability, login,
frontend assets, agent/customer interfaces, and a minimal smoke test.

M0 is not the ICT MVP. It does not implement office routing, categories, SLA,
custom ticket DocTypes, or production security. Native Helpdesk remains the
ticket engine; CBSUA code is added only for a verified institutional gap.

## 2. Expected applications

From the Bench root (the directory containing apps/ and sites/), run:

~~~bash
bench --site cbsua-helpdesk.localhost list-apps
bench version
~~~

The site should list frappe, telephony, helpdesk, and cbsua_helpdesk.
Telephony is installed before Helpdesk as its declared dependency; CBSUA is
installed after Helpdesk because it extends that platform.

Record exact app versions and commit IDs. Branch labels such as version-16
and develop can move and are not immutable deployment evidence.

## 3. Start the local server

~~~bash
cd ~/frappe/frappe-bench
bench start
~~~

Keep the terminal open. Browse to:

| Interface | URL |
|---|---|
| Frappe login | http://cbsua-helpdesk.localhost:8000/login |
| Helpdesk v16 app (agent landing) | http://cbsua-helpdesk.localhost:8000/helpdesk |
| Customer tickets | http://cbsua-helpdesk.localhost:8000/helpdesk/my-tickets |
| Customer knowledge base | http://cbsua-helpdesk.localhost:8000/helpdesk/kb-public |

Helpdesk 16.1.0 serves its agent and customer route families from one Vue app
whose history base is `/helpdesk/`. The current v16 router sends unauthenticated
visitors to login, including routes marked for the customer portal. Do not
assume guest ticket intake or guest knowledge-base access; verify the approved
customer access policy separately. `/help` is the Studio portal route described
by the newer upstream `develop` branch, not this v16 baseline.

The hostname must resolve locally. If it does not, run from the Bench root:

~~~bash
bench --site cbsua-helpdesk.localhost add-to-hosts
~~~

## 4. Administrator login

Use the site-level built-in account:

- Username: Administrator
- Password: the site Administrator password created by bench new-site.

This is not the MariaDB administrator/root password. The login form may have
an email-oriented label; try the literal username Administrator.

If the site password has been lost, reset it from the Bench root. Bench
versions accept the new password as the command argument:

~~~bash
bench --site cbsua-helpdesk.localhost set-admin-password 'NEW_PASSWORD'
~~~

Replace the placeholder locally. Never commit or share a real password.
Command-line arguments may be stored in shell history or briefly visible to
local process inspection; handle the password securely. If syntax differs in
your installed Bench version, inspect bench help and the relevant command help.

If login still fails, record the non-secret error and verify the browser is
using the intended site hostname.

## 5. Diagnose broken styles or missing icons

Unstyled HTML, missing icons, or generic framework imagery often indicate
that CSS/JavaScript assets were not built or served correctly. Treat this as a
separate frontend delivery issue; it does not automatically mean app
installation failed.

Stop bench start with Ctrl+C. From the Bench root, rebuild relevant assets:

~~~bash
bench build --app frappe --app helpdesk
~~~

If the build fails, retain the complete error output. Do not claim the repair
succeeded. After a successful build, clear caches and restart:

~~~bash
bench --site cbsua-helpdesk.localhost clear-cache
bench --site cbsua-helpdesk.localhost clear-website-cache
bench start
~~~

Hard-refresh the browser and re-check /login, /helpdesk,
/helpdesk/my-tickets, and /helpdesk/kb-public.

### If assets still fail

1. Open browser Developer Tools > Network and enable Disable cache.
2. Reload the page and filter requests for CSS and JS.
3. Record the failed URL, HTTP status (for example 404/500), and response type.
4. Check Console for the first relevant loading/runtime error.
5. Correlate the failure with the terminal running bench start and build output.

Do not manually copy generated files into sites/assets or edit compiled bundles
to conceal a build error. Redact cookies, authorization headers, credentials,
and personal/ticket data from reports.

## 6. Run tests and migrations

From the Bench root:

~~~bash
bench --site cbsua-helpdesk.localhost run-tests --app cbsua_helpdesk
~~~

This tests the CBSUA app, not every Helpdesk workflow or office-level access
boundary. After reviewed app changes that require schema updates:

~~~bash
bench --site cbsua-helpdesk.localhost migrate
~~~

Back up before migrations on any environment containing data that matters.

## 7. M0 smoke-test checklist

- [ ] bench version completes and versions are recorded.
- [ ] list-apps shows Frappe, Telephony, Helpdesk, and CBSUA Helpdesk.
- [ ] Login page CSS/JS assets load successfully.
- [ ] Administrator can sign in.
- [ ] Helpdesk v16 app at /helpdesk renders.
- [ ] Customer ticket and knowledge-base routes under /helpdesk render for the intended user roles.
- [ ] A disposable test ticket can be created and viewed by an authorized agent.
- [ ] CBSUA app tests pass.
- [ ] Future office destinations are not enabled.
- [ ] No real institutional or personal data is used for this test.

Record date, OS, Bench version, app versions/commit IDs, results, and known
issues. Never record credentials. Installation alone is not proof of a working
MVP or correct authorization.

## 8. Read-only diagnostic helper

From the Bench root, run the script in this repository:

~~~bash
bash /path/to/cbsua-helpdesk-app/scripts/diagnose_m0.sh cbsua-helpdesk.localhost
~~~

It reports versions, installed apps, service status, and asset-directory
presence. It does not install packages, modify site configuration, build
assets, clear caches, restart services, or change database records. Review
output before sharing because it contains environment metadata.

## 9. Upstream references

- [Frappe Helpdesk repository and development setup](https://github.com/frappe/helpdesk)
- [Helpdesk compatibility matrix](https://github.com/frappe/helpdesk#compatibility-matrix)
- [Frappe installation guide](https://docs.frappe.io/framework/user/en/installation)
- [Bench documentation](https://docs.frappe.io/framework/user/en/bench)
- [Asset bundling documentation](https://docs.frappe.io/framework/user/en/basics/asset-bundling)

## 10. Handoff to M1

Once the checklist passes, M0 is verified for that local environment. M1 can
then establish the CBSUA configuration foundation. Later milestones handle
ICT intake, routing, authorization, ticket processing, and reporting.

Do not create a duplicate Ticket DocType or replace the native Helpdesk
lifecycle. Keep changes minimal, documented, tested, and compatible with the
pinned Frappe/Helpdesk versions.


## 11. M1 CBSUA extension

The M1 CBSUA extension and office catalogue are documented in
[M1-setup.md](M1-setup.md). This is a separate app from upstream Helpdesk.
Apply the migration and run the CBSUA app tests after updating the develop
branch. The office catalogue is metadata only; it does not route tickets or
grant office access. ICT is the only active office; future offices remain
disabled. CBSUA branding defaults are configured through Helpdesk HD Settings
using the official PNG logo. See [Frappe UI integration](../docs/frappe-ui-integration.md)
for the native branding mechanism, frontend theme boundary, and Custom Actions guidance.
