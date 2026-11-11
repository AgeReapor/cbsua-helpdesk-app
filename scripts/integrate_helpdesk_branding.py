#!/usr/bin/env python3
"""Install the tracked CBSUA CSS link into the pinned Helpdesk v16 page shell.

Run from any directory with the Frappe Bench root as the first argument:
    python /path/to/cbsua-helpdesk-app/scripts/integrate_helpdesk_branding.py /path/to/frappe-bench

The source change is idempotent and intentionally limited to Helpdesk's
version-16 HTML shell. Re-run it after upgrading/replacing the Helpdesk app.
"""

from __future__ import annotations

import sys
from pathlib import Path


MARKER = "cbsua-helpdesk-theme"
LINK = (
    f'    <link rel="stylesheet" href="/assets/cbsua_helpdesk/css/'
    f'cbsua_helpdesk.css" data-theme-integration="{MARKER}" />\n'
)


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    bench = Path(sys.argv[1]).expanduser().resolve()
    target = bench / "apps/helpdesk/helpdesk/www/helpdesk/index.html"
    if not target.is_file():
        print(f"Helpdesk v16 page template not found: {target}", file=sys.stderr)
        return 1

    html = target.read_text(encoding="utf-8")
    if "</head>" not in html or "/assets/helpdesk/desk/assets/" not in html:
        print(
            "Unexpected Helpdesk page template; expected the v16 Vite shell. "
            "No file was changed.",
            file=sys.stderr,
        )
        return 1

    original = html
    html = html.replace("<title>Helpdesk</title>", "<title>CBSUA Helpdesk</title>", 1)
    html = html.replace(
        '<meta name="apple-mobile-web-app-title" content="Frappe Helpdesk" />',
        '<meta name="apple-mobile-web-app-title" content="CBSUA Helpdesk" />',
        1,
    )
    html = html.replace(
        'href="/assets/helpdesk/desk/manifest/apple-icon-180.png"',
        'href="/assets/cbsua_helpdesk/images/cbsua-logo.png?v=2"',
    )
    if MARKER not in html:
        html = html.replace("</head>", f"{LINK}</head>", 1)

    if html == original:
        print(f"CBSUA theme and favicon integration already current in {target}")
        return 0

    target.write_text(html, encoding="utf-8")
    print(f"Applied CBSUA theme, title, and favicon integration to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
