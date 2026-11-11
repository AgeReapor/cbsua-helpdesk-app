# CBSUA Helpdesk

CBSUA-specific extension app for the [Frappe Helpdesk](https://github.com/frappe/helpdesk) platform.

> **Current status: scaffold only.** This repository provides the installable Frappe app package and development/deployment guidance. It does not replace Frappe Helpdesk, add a custom ticket engine, or yet implement office routing, ticket workflows, or custom DocTypes.

## Project scope

- **Phase 1:** ICT Office only.
- **Future phases:** Registrar, Admissions, and Cashier, enabled only after office-specific configuration and access-isolation tests pass.
- **Queueing:** digital ticket queues and assignment only. Physical walk-in tokens, counter displays, and turn calling are outside this app's current scope.
- **Customization:** use native Frappe Helpdesk features first. Add CBSUA-specific code only for a verified requirement that cannot be met through supported configuration.

See [docs/](docs/README.md) for the SRS, architecture, workflows, decisions, and roadmap.

## Repository layout

```text
cbsua-helpdesk-app/
├── cbsua_helpdesk/
│   ├── __init__.py
│   ├── hooks.py
│   ├── modules.txt
│   ├── patches.txt
│   ├── config/
│   └── cbsua_helpdesk/
│       └── __init__.py
├── tests/
├── docs/
├── MANIFEST.in
├── setup.py
└── README.md
```

The package intentionally contains no custom ticket DocTypes or business logic yet. Keep new features small, documented, permission-aware, and covered by tests.

## Compatibility and version policy

Frappe Framework and Frappe Helpdesk must be installed at mutually compatible versions. Do not assume that the latest `develop` branches are a supported production combination.

Before implementation or deployment:

1. Select a supported Frappe Framework release/commit.
2. Select the matching Frappe Helpdesk release/commit.
3. Test this app against that exact pair.
4. Record the selected versions in the project deployment notes and pin them in the deployment build.
5. Upgrade the three components together only after regression tests pass.

The commands below use placeholders deliberately. Replace them with the approved compatible branch names or immutable commit references from the project's compatibility decision. The existence of a branch does not establish compatibility.

## Local development installation (Bench)

The recommended first target is a local Bench environment. Follow the official [Frappe installation guide](https://frappeframework.com/docs/user/en/installation) for operating-system packages and supported Python, Node.js, Redis, and MariaDB versions. Bench is the supported command-line tool for managing the development environment.

### 1. Prepare the machine

Install the prerequisites for the chosen Frappe release, including:

- Python and the required build tools
- Node.js and Yarn (for frontend asset builds)
- Redis
- MariaDB
- Git
- wkhtmltopdf only if required by the selected framework features/release

Use the versions specified by the selected Frappe release's installation documentation; do not substitute arbitrary system versions.

Install Bench using the method recommended by the official documentation. Verify it is available:

```bash
bench --version
```

### 2. Create a Bench with the selected Frappe branch

From the directory where you keep development environments:

```bash
bench init --frappe-branch <FRAPPE_BRANCH> frappe-bench
cd frappe-bench
```

Replace `<FRAPPE_BRANCH>` with the approved Frappe branch or tag (or initialize from a reviewed commit using the Bench-supported workflow).

### 3. Fetch Frappe Helpdesk and this CBSUA app

```bash
bench get-app --branch <HELPDESK_BRANCH> https://github.com/frappe/helpdesk
bench get-app --branch develop https://github.com/AgeReapor/cbsua-helpdesk-app
```

Replace `<HELPDESK_BRANCH>` with the Helpdesk branch/tag that has been validated against `<FRAPPE_BRANCH>`. This repository's `develop` branch is the development target; use a reviewed commit or release tag for a controlled deployment.

### 4. Create a local site and install the applications

```bash
bench new-site cbsua-helpdesk.localhost
bench --site cbsua-helpdesk.localhost install-app helpdesk
bench --site cbsua-helpdesk.localhost install-app cbsua_helpdesk
```

`bench new-site` prompts for the database administrator credentials and the new site's Administrator password. Install Helpdesk before the CBSUA extension.

### 5. Start the development server

```bash
bench start
```

Open the local site at the address printed by Bench (commonly `http://cbsua-helpdesk.localhost:8000`). Sign in using the Administrator account created for the site.

### 6. Verify the installation

Run these checks from the Bench directory:

```bash
bench --site cbsua-helpdesk.localhost list-apps
bench --site cbsua-helpdesk.localhost migrate
bench --site cbsua-helpdesk.localhost run-tests --app cbsua_helpdesk
```

Confirm that both `helpdesk` and `cbsua_helpdesk` appear in the installed-app list. The test command exercises the CBSUA app's basic import/installation smoke test. Also complete the Helpdesk UI and workflow checks in [docs/SRS.md](docs/SRS.md#8-phase-1-acceptance-criteria).

If the repository changes while the Bench is running, update the app source in the Bench's `apps/cbsua_helpdesk` checkout, then run:

```bash
bench --site cbsua-helpdesk.localhost migrate
```

Restart the development processes after Python or hook changes. Rebuild assets only when frontend assets are introduced.

## Installing into an existing Bench

If a compatible Bench and site already exist, fetch the app and install it:

```bash
cd /path/to/frappe-bench
bench get-app --branch develop https://github.com/AgeReapor/cbsua-helpdesk-app
bench --site <SITE_NAME> install-app cbsua_helpdesk
bench --site <SITE_NAME> list-apps
```

Ensure the site already has the compatible Frappe Helpdesk app installed. Do not install this extension into an unverified Frappe/Helpdesk version combination.

## Docker deployment (planned; not yet supplied by this scaffold)

Local Bench is the initial development and test environment. Docker is the intended packaging/deployment path after the compatible versions and local acceptance tests have been established.

The repository does **not** yet include a production Dockerfile or Compose stack. Do not treat the local Bench instructions as a production deployment recipe.

The planned Docker approach is:

1. Pin Frappe Framework, Frappe Helpdesk, and `cbsua_helpdesk` to reviewed tags or immutable commits.
2. Build a custom application image using the official [frappe_docker](https://github.com/frappe/frappe_docker) project as the deployment foundation. Include the Helpdesk and CBSUA app source in the image at build time.
3. Use the same immutable image for the relevant backend, websocket, worker, and scheduler services so every process runs the same app versions.
4. Keep MariaDB and Redis as separately managed services with persistent storage as appropriate. Persist site files and private/public attachments using the deployment's documented volume or storage configuration.
5. Provision the site and install apps through a controlled one-time site initialization/release process. Run migrations as an explicit deployment step, not independently in every service container.
6. Configure secrets through environment/secrets management; do not commit passwords, tokens, production site configuration, or private keys.
7. Back up and restore the database and site files together. Test restoration before production acceptance.
8. Promote the exact image tested in staging to production; do not rebuild an unpinned `develop` branch during deployment.

Useful references:

- [Frappe Docker repository and deployment documentation](https://github.com/frappe/frappe_docker)
- [Community guide: building a Docker image for a custom Frappe app](https://discuss.frappe.io/t/frappe-docker-custom-app-guide-create-docker-image-for-your-custom-frappe-app/151315)

The community guide is a useful implementation reference, not a substitute for validating the current official `frappe_docker` configuration. The final Dockerfile, image build arguments, app manifest, Compose services, site initialization, migration, backup, and upgrade procedures must be tested against the pinned Frappe release before they are documented as supported.

## Development conventions

- Keep ticket records, customer portal behavior, assignment, SLA, and ticket lifecycle in native Frappe Helpdesk unless a tested gap requires an extension.
- Do not activate Registrar, Admissions, or Cashier intake destinations during Phase 1.
- Treat office/team access isolation as a release gate. Test direct URLs, lists, search, reports, attachments, and conversations—not just menu visibility.
- Put custom DocTypes and fixtures in the app only when approved and required. Avoid copying native Helpdesk DocTypes.
- Add schema changes through Frappe's supported DocType, fixture, and patch mechanisms; never edit a live site's database manually as an application deployment strategy.
- Add automated tests for every custom hook, permission rule, patch, and workflow extension.
- Keep secrets and site-specific data out of Git.

## Useful Bench commands

Run from the Bench directory:

```bash
# Show installed applications
bench --site <SITE_NAME> list-apps

# Apply app migrations and schema changes
bench --site <SITE_NAME> migrate

# Run this app's tests
bench --site <SITE_NAME> run-tests --app cbsua_helpdesk

# Open an interactive console for a site
bench --site <SITE_NAME> console

# Export a site backup (include files when required)
bench --site <SITE_NAME> backup --with-files
```

Check `bench --help` and the documentation for the selected Bench/Frappe version if a command's options differ.

## Status

- [x] Installable Frappe app package scaffold
- [x] Basic app metadata and smoke test
- [x] Local Bench installation instructions
- [x] Planned Docker deployment approach and references
- [ ] Pin and verify the Frappe/Helpdesk compatibility matrix
- [ ] Add approved ICT-specific configuration/fixtures
- [ ] Prove ICT-only access boundaries with automated tests
- [ ] Build and test the Docker image and deployment stack
