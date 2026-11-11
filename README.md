# CBSUA Helpdesk

CBSUA-specific extension app for [Frappe Helpdesk](https://github.com/frappe/helpdesk).

> **Current status:** starter scaffold. This repository contains the installable CBSUA Frappe app and the instructions to set up a complete local development environment. The app does not replace Frappe Helpdesk and does not yet add custom ticket workflows or office-routing logic.

## 1. What you are installing

The complete system consists of three Frappe applications:

| Application | What it does | Source |
|---|---|---|
| Frappe Framework | The platform that runs the site, database-backed apps, users, and permissions | [frappe/frappe](https://github.com/frappe/frappe) |
| Frappe Helpdesk | The actual ticketing system, including agent and customer interfaces | [frappe/helpdesk](https://github.com/frappe/helpdesk) |
| CBSUA Helpdesk | This repository; reserved for CBSUA-specific configuration and extensions | [AgeReapor/cbsua-helpdesk-app](https://github.com/AgeReapor/cbsua-helpdesk-app) |

Frappe applications are installed into a **site**. A **Bench** is the local development environment that holds the framework, applications, and one or more sites. You do not need to know Git branch terminology to follow the recommended setup below; the exact choices are already made for you.

### Project scope

- **Phase 1:** ICT Office only.
- **Future phases:** Registrar, Admissions, and Cashier, only after their onboarding and access-isolation tests pass.
- **Queueing:** digital ticket queues and assignment only. Physical walk-in tokens, counter displays, and turn calling are not part of this implementation.
- **Customization:** use native Frappe Helpdesk features first. Add CBSUA code only for a verified requirement that cannot be met safely through configuration.

## 2. Recommended version choices

For a new environment, use the supported **Frappe 16** release line. The Frappe Helpdesk project publishes matching release lines. A branch is simply the named version line of a source repository.

| Component | Select this branch | Why |
|---|---|---|
| Frappe Framework | `version-16` | Supported Frappe 16 release line |
| Frappe Helpdesk | `version-16` | Matches Frappe Framework `version-16` |
| CBSUA Helpdesk | `develop` | This project scaffold currently lives on this repository branch |
| Telephony dependency | Default branch selected by Bench | Required by Frappe Helpdesk; fetched separately below |

**Do not choose `develop` for Frappe Framework or Frappe Helpdesk for the normal setup.** Those are moving development branches and must be used together only for deliberate experimental work. The Helpdesk project's published compatibility matrix is:

| Frappe Helpdesk branch | Matching Frappe Framework branch |
|---|---|
| `version-15` | `version-15` |
| `version-16` | `version-16` |
| `develop` | `develop` |

The current Helpdesk `version-16` application metadata requires Frappe 16 and declares Telephony as an app dependency. The commands in this guide install Telephony before Helpdesk.

> **Compatibility status:** The version-16 pair is the recommended baseline for this setup, but the CBSUA app scaffold has not yet been certified by a completed installation and test run. Follow the verification steps before treating the environment as ready for use.

References: [Frappe supported versions](https://frappe.io/support-versions) · [Helpdesk compatibility matrix](https://github.com/frappe/helpdesk#compatibility-matrix).

## 3. Local development setup (recommended first)

These instructions are written for a clean **Ubuntu 24.04 or newer** computer. Use a normal user account for Bench commands; use `sudo` only for operating-system package installation and database setup.

Windows users should use Ubuntu through WSL2 rather than trying to run the Frappe server directly in Windows. macOS is also supported, but its prerequisite installation commands differ; follow the official installation guide linked below.

### Step 1 — Install system packages

Open a terminal and run:

```bash
sudo apt update
sudo apt install -y git curl build-essential pkg-config \
  redis-server mariadb-server mariadb-client libmariadb-dev
```

Start the database and Redis services:

```bash
sudo systemctl enable --now mariadb
sudo systemctl enable --now redis-server
```

Secure/configure MariaDB using the system's MariaDB setup utility if required:

```bash
sudo mariadb-secure-installation
```

Keep the MariaDB administrator credentials available. The `bench new-site` command will ask for the database administrator password when it needs it.

**Important version check:** Frappe's current installation guide specifies MariaDB 11.8 for Frappe 16/develop. Some Ubuntu package sources may provide an older MariaDB release. Check before continuing:

```bash
mariadb --version
```

If the installed version is not 11.8, install MariaDB 11.8 using the official MariaDB repository instructions for your Ubuntu release. Do not continue with an unverified database version.

### Step 2 — Install Node.js 24 and Yarn

Frappe 16 uses Node.js 24 and Yarn 1.x for frontend dependencies. Install Node.js with NVM:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
```

Close and reopen the terminal. Then run:

```bash
nvm install 24
nvm use 24
npm install --global yarn
```

Check the installed versions:

```bash
node --version
npm --version
yarn --version
```

### Step 3 — Install Python 3.14 and Bench

Frappe's current installation guide recommends Python 3.14 for Frappe 16/develop. Install it with `uv`, then install the Bench command-line tool:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close and reopen the terminal if the installer asks you to update your PATH. Then run:

```bash
uv python install 3.14
uv tool install frappe-bench
```

Verify that Bench is available:

```bash
bench --version
uv python find 3.14
```

### Step 4 — Create the Bench and install the three applications

Choose a folder where you want the development environment to live. The following commands create a folder named `frappe-bench` in your home directory.

Copy and run the commands in order:

```bash
mkdir -p ~/frappe
cd ~/frappe

# Create a Bench using the Frappe 16 framework branch.
bench init --frappe-branch version-16 --python "$(uv python find 3.14)" frappe-bench

cd frappe-bench

# Install the Helpdesk app's required Telephony dependency.
bench get-app https://github.com/frappe/telephony

# Install Frappe Helpdesk from its matching Frappe 16 branch.
bench get-app --branch version-16 https://github.com/frappe/helpdesk

# Install the CBSUA extension from this project's develop branch.
bench get-app --branch develop https://github.com/AgeReapor/cbsua-helpdesk-app
```

**What those commands mean:**

- `bench init` creates the environment and downloads Frappe Framework.
- `bench get-app` downloads an application into the Bench. It does not yet install the application on a site.
- `version-16` keeps Frappe Framework and Helpdesk on their matching supported release line.
- `develop` is used only for the CBSUA repository because that is where this scaffold is currently maintained.

If a command fails, stop and resolve that error before continuing. Do not work around dependency or version errors by switching one of the Frappe components to an unrelated branch.

### Step 5 — Create your local CBSUA Helpdesk site

Still inside the `frappe-bench` folder, run:

```bash
bench new-site cbsua-helpdesk.localhost
```

Bench will ask for the MariaDB administrator password and then ask you to create the site's **Administrator** password. This site Administrator password is separate from the MariaDB password. Save it securely; it is needed to sign in to the local site.

Add the local site name to your computer's hosts file:

```bash
bench --site cbsua-helpdesk.localhost add-to-hosts
```

If your operating system requests permission, approve the hosts-file update.

### Step 6 — Install the applications on the site

Install the applications in this order:

```bash
bench --site cbsua-helpdesk.localhost install-app telephony
bench --site cbsua-helpdesk.localhost install-app helpdesk
bench --site cbsua-helpdesk.localhost install-app cbsua_helpdesk
```

The order matters: Telephony is a Helpdesk dependency, and the CBSUA app extends the Helpdesk platform.

### Step 7 — Build Helpdesk assets

Build the Helpdesk frontend assets:

```bash
bench build --app helpdesk
```

The CBSUA scaffold currently has no custom frontend assets, so it does not need a separate frontend build step.

### Step 8 — Start the local server

From the `frappe-bench` folder, run:

```bash
bench start
```

Keep this terminal window open while using the application. Open the following URL in your browser:

- **Helpdesk agent interface:** [http://cbsua-helpdesk.localhost:8000/helpdesk](http://cbsua-helpdesk.localhost:8000/helpdesk)
- **Customer portal:** [http://cbsua-helpdesk.localhost:8000/help](http://cbsua-helpdesk.localhost:8000/help)

Sign in to the agent interface with:

- **Username:** `Administrator`
- **Password:** the site Administrator password you created in Step 5.

Do not use a default/demo password for a shared or internet-accessible environment.

## 4. Verify that the installation works

Open a second terminal window. Move into the Bench folder:

```bash
cd ~/frappe/frappe-bench
```

Confirm that all three applications are installed on the site:

```bash
bench --site cbsua-helpdesk.localhost list-apps
```

The list must include:

- `frappe`
- `telephony`
- `helpdesk`
- `cbsua_helpdesk`

Run the CBSUA app tests:

```bash
bench --site cbsua-helpdesk.localhost run-tests --app cbsua_helpdesk
```

Apply migrations when app code or DocTypes change:

```bash
bench --site cbsua-helpdesk.localhost migrate
```

### Phase 1 smoke-test checklist

Before calling the local environment ready, confirm:

- [ ] The site opens at the local Helpdesk URL.
- [ ] An Administrator can sign in.
- [ ] The Helpdesk agent interface loads without a frontend/build error.
- [ ] The customer portal loads.
- [ ] `list-apps` shows Frappe, Telephony, Helpdesk, and CBSUA Helpdesk.
- [ ] The CBSUA app test command completes successfully.
- [ ] A test ticket can be created and viewed in Helpdesk.
- [ ] No Registrar, Admissions, or Cashier intake destinations are enabled.
- [ ] ICT-only access restrictions are tested before any real institutional data is entered.

The scaffold currently contains no CBSUA ticket workflow or office-routing customizations. A successful app installation is not, by itself, proof that the Phase 1 business workflow or access boundaries are complete.

## 5. Updating the local environment

Run these commands from `~/frappe/frappe-bench`.

To update the CBSUA app source from its Git remote:

```bash
cd apps/cbsua_helpdesk
git pull
cd ../..
```

Then apply migrations and restart Bench:

```bash
bench --site cbsua-helpdesk.localhost migrate
```

Stop the running `bench start` process with `Ctrl+C`, then start it again:

```bash
bench start
```

For a controlled test or deployment, prefer a reviewed commit rather than automatically pulling the latest development code.

Useful commands:

```bash
# Show installed applications
bench --site cbsua-helpdesk.localhost list-apps

# Run CBSUA app tests
bench --site cbsua-helpdesk.localhost run-tests --app cbsua_helpdesk

# Apply migrations
bench --site cbsua-helpdesk.localhost migrate

# Open the site console
bench --site cbsua-helpdesk.localhost console

# Back up the database and site files
bench --site cbsua-helpdesk.localhost backup --with-files
```

## 6. Docker deployment (next stage — not yet implemented)

**Docker deployment is planned, but this repository does not yet contain a custom Docker image, Dockerfile, or production Compose configuration.** Do not treat the local Bench setup above as a production deployment procedure.

The intended Docker approach is to build one immutable image containing the exact tested versions of Frappe Framework, Frappe Helpdesk, Telephony, and CBSUA Helpdesk, then run that image using the official Frappe Docker deployment structure.

The deployment implementation must:

1. Pin all application repositories to reviewed release tags or immutable commit IDs.
2. Build the custom image with the official [Frappe Docker build process](https://frappe.github.io/frappe_docker/02-setup/02-build-setup.html), using its supported custom-app manifest (`apps.json`).
3. Include the same application versions in the backend, websocket, worker, and scheduler services.
4. Keep database and Redis services separate from the application image.
5. Persist site data and uploaded files using the supported storage/volume configuration.
6. Install the apps and run migrations through a controlled site initialization/release procedure.
7. Supply secrets through environment or secrets management, never by committing credentials.
8. Test database and file backups, restore, upgrades, and rollback before production use.

References:

- [Official Frappe Docker documentation](https://frappe.github.io/frappe_docker/)
- [Official custom image build guide](https://frappe.github.io/frappe_docker/02-setup/02-build-setup.html)
- [Official automated builds and deployment guide](https://github.com/frappe/frappe_docker/blob/main/docs/11-how-to/06-automated-builds-and-deployment.md)
- [Community guide for custom Frappe app images](https://discuss.frappe.io/t/frappe-docker-custom-app-guide-create-docker-image-for-your-custom-frappe-app/151315)

The community guide is supplementary. The official Frappe Docker documentation is the primary reference for the image and Compose implementation.

## 7. Troubleshooting

### `bench: command not found`

Close and reopen the terminal so the `uv` tool directory is added to PATH. Then check:

```bash
uv tool list
bench --version
```

### MariaDB version or login error

Check the installed database version and service status:

```bash
mariadb --version
sudo systemctl status mariadb
```

Confirm that the database administrator password entered during `bench new-site` is correct. Do not paste passwords into chat, issue trackers, or committed files.

### Redis is not running

```bash
sudo systemctl status redis-server
sudo systemctl start redis-server
```

### Helpdesk page or assets do not load

From the Bench directory, rebuild Helpdesk assets and restart the development server:

```bash
bench build --app helpdesk
```

### App is not listed after installation

Run the installation command again and read the complete error output:

```bash
bench --site cbsua-helpdesk.localhost install-app cbsua_helpdesk
```

Do not manually insert app records into the database to work around an installation failure.

## 8. Official references

- [Frappe Framework installation guide](https://docs.frappe.io/framework/user/en/installation) — supported operating systems, prerequisites, Python/Node/database versions, and Bench installation.
- [Frappe Framework introduction](https://docs.frappe.io/framework/user/en/introduction) — framework concepts and documentation navigation.
- [Frappe Framework: Create an app](https://docs.frappe.io/framework/user/en/tutorial/create-an-app) — custom Frappe app structure.
- [Frappe Helpdesk repository](https://github.com/frappe/helpdesk) — Helpdesk setup instructions and compatibility matrix.
- [Frappe supported versions](https://frappe.io/support-versions) — current supported and development release lines.
- [Frappe Docker](https://github.com/frappe/frappe_docker) — container build and deployment reference.

## 9. Current project status

- [x] Installable CBSUA Frappe app scaffold
- [x] Beginner-oriented local installation instructions
- [x] Explicit Frappe/Helpdesk branch selection for the recommended setup
- [x] Local verification and troubleshooting instructions
- [x] Docker deployment approach and official references
- [ ] Complete a clean Frappe 16 + Helpdesk 16 + CBSUA installation test
- [ ] Record exact tested commit IDs for every application
- [ ] Configure and test the Phase 1 ICT workflow
- [ ] Prove office-level access isolation
- [ ] Build and test the Docker image and deployment stack


## 10. M1 — CBSUA configuration and branding foundation

The initial M1 implementation adds a CBSUA Service Office catalogue, safe
Phase 1 defaults, and conservative institutional styling. Read
[docs/M1-configuration-and-branding.md](docs/M1-configuration-and-branding.md)
for the implementation boundary, palette rationale, logo asset status,
migration steps, tests, and rollback. The Helpdesk integration instructions
are in [helpdesk/M1-setup.md](helpdesk/M1-setup.md).

After pulling the develop branch, run `bench migrate`, build the CBSUA app
assets, clear caches, and run the app tests. M1 does not yet implement ticket
routing, HD Team provisioning, or office-level ticket isolation. ICT is the
only active office record; Registrar, Admissions, and Cashier remain disabled.

## 11. M0 local baseline — current implementation

M0 is the first engineering milestone: verify that the local Frappe/Helpdesk
stack is healthy before implementing CBSUA-specific workflows. It is a
verification milestone, not a claim that the ICT MVP or production deployment
is complete.

Start with these repository resources:

- [Helpdesk setup and M0 verification guide](helpdesk/README.md) — agent and
  customer URLs, Administrator login, frontend asset troubleshooting, tests,
  and the local smoke-test checklist.
- [M0 runbook](docs/M0-runbook.md) — diagnostic procedure, acceptance criteria,
  and explicit scope boundaries.
- [Read-only diagnostic script](scripts/diagnose_m0.sh) — checks versions,
  installed apps, local service status, expected directories, and asset
  directory presence from the Bench root.

Example diagnostic invocation (run from the Bench root):

```bash
bash /path/to/cbsua-helpdesk-app/scripts/diagnose_m0.sh cbsua-helpdesk.localhost
```

The script does not modify the environment. Its output is diagnostic evidence,
not an automated pass/fail certification. Browser asset delivery must still
be checked in Developer Tools, and the M0 smoke-test checklist must be
completed on the actual local machine.

**M0 status:** documentation and a read-only diagnostic helper are committed.
The local environment has not been independently inspected or tested by this
repository change. Mark M0 verified only after the acceptance checklist in
[docs/M0-runbook.md](docs/M0-runbook.md) passes and the results are recorded.


For requirements, architecture, workflows, decisions, and implementation planning, see [the project documentation](docs/README.md).
