#!/usr/bin/env bash
#
# CBSUA Helpdesk — M0 local environment diagnostic
#
# PURPOSE: Collect a non-secret snapshot of a local Frappe Bench installation.
# SAFETY: READ-ONLY. Does not install, edit, build, clear caches, restart, or
# mutate the database. Run from the Bench root (the folder with apps/ and sites/).
#
# USAGE:
#   bash /path/to/cbsua-helpdesk-app/scripts/diagnose_m0.sh cbsua-helpdesk.localhost
#
# Review output before sharing: hostnames, paths, and software versions are
# environment metadata. Never share passwords, tokens, cookies, or private data.
set -u

SITE="${1:-}"
if [[ -z "$SITE" ]]; then
  echo "Usage: $0 <site-name>"
  exit 2
fi
if [[ ! -d "apps" || ! -d "sites" ]]; then
  echo "ERROR: Run from the Bench root (must contain apps/ and sites/)."
  exit 2
fi

section() { printf '\n\n===== %s =====\n' "$1"; }
check() {
  local label="$1"; shift
  printf '\n--- %s ---\n' "$label"
  if command -v "$1" >/dev/null 2>&1; then
    "$@" 2>&1 || echo "[command returned a non-zero status]"
  else
    echo "[not installed or not on PATH: $1]"
  fi
}

section "Diagnostic context"
printf 'Date: '; date -Is 2>/dev/null || date
printf 'Bench root: %s\nTarget site: %s\nMode: read-only\n' "$PWD" "$SITE"

section "Bench and application versions"
check "Bench CLI" bench --version
check "Application versions" bench version
check "Installed apps on target site" bench --site "$SITE" list-apps

section "Runtime and service-client versions"
check "Python" python3 --version
check "Node.js" node --version
check "npm" npm --version
check "Yarn" yarn --version
check "MariaDB client" mariadb --version
check "Redis client" redis-cli --version

section "Local service status"
if command -v systemctl >/dev/null 2>&1; then
  for service in mariadb redis-server; do
    printf '\n--- %s ---\n' "$service"
    systemctl is-active "$service" 2>&1 || true
  done
else
  echo "systemctl unavailable; inspect services with the operating-system tools."
fi

section "Expected site and application directories"
for path in "sites/$SITE" apps/frappe apps/telephony apps/helpdesk apps/cbsua_helpdesk; do
  [[ -d "$path" ]] && echo "[present] $path" || echo "[missing] $path"
done

section "Frontend asset directory presence"
if [[ -d sites/assets ]]; then
  for app in frappe helpdesk; do
    [[ -d "sites/assets/$app" ]] && echo "[present] sites/assets/$app" || echo "[missing] sites/assets/$app"
  done
else
  echo "[missing] sites/assets"
fi

section "Manual follow-up"
cat <<'EOF'
1. Open /login, /helpdesk, and /help in a browser.
2. Sign in with the site Administrator username and site password.
3. If styles fail, inspect Developer Tools > Network for failed CSS/JS requests.
4. Record request URL, HTTP status, response type, first console error, and build output.
5. Never share passwords, cookies, authorization headers, or private ticket data.
EOF

section "Complete"
echo "No files, services, caches, database records, or app settings were changed."
