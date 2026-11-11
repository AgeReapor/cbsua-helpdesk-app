"""Safe, repeatable setup for the CBSUA configuration foundation.

The seed routine creates the four office catalogue records required by the
SRS. It is deliberately additive: it never overwrites an existing office
record, so an administrator's later edits are not silently reverted by
bench migrate. The Service Office controller separately prevents activation
of future offices until a later, reviewed onboarding implementation changes
that guard.
"""

import json
from pathlib import Path

import frappe


# Helpdesk's own HD Settings drives the Vue agent/customer app branding.
# Use the app-served image path so the official logo is available without
# duplicating the PNG into Frappe's private File storage. These are defaults:
# never overwrite an administrator's explicitly configured brand values.
DEFAULT_BRANDING = {
    "brand_name": "CBSUA Helpdesk",
    "brand_logo": "/assets/cbsua_helpdesk/images/cbsua-logo.png",
    "favicon": "/assets/cbsua_helpdesk/images/cbsua-logo.png",
}


DEFAULT_OFFICES = (
    {
        "office_code": "ICT",
        "office_name": "ICT Office",
        "phase": "Phase 1",
        "is_active": 1,
        "allow_customer_intake": 1,
        "description": "Initial operational office for Phase 1.",
    },
    {
        "office_code": "REGISTRAR",
        "office_name": "Registrar",
        "phase": "Future",
        "is_active": 0,
        "allow_customer_intake": 0,
        "description": "Reserved for a separately approved future onboarding phase.",
    },
    {
        "office_code": "ADMISSIONS",
        "office_name": "Admissions",
        "phase": "Future",
        "is_active": 0,
        "allow_customer_intake": 0,
        "description": "Reserved for a separately approved future onboarding phase.",
    },
    {
        "office_code": "CASHIER",
        "office_name": "Cashier",
        "phase": "Future",
        "is_active": 0,
        "allow_customer_intake": 0,
        "description": "Reserved for a separately approved future onboarding phase.",
    },
)


def ensure_default_offices():
    """Create missing office catalogue rows without changing existing rows.

    This method is safe to call repeatedly from after_migrate. It does not
    create Helpdesk Teams, users, assignments, routes, or customer-facing
    forms. The office catalogue is configuration metadata only at this stage.
    """
    for office in DEFAULT_OFFICES:
        if frappe.db.exists("CBSUA Service Office", office["office_code"]):
            continue

        frappe.get_doc(
            {
                "doctype": "CBSUA Service Office",
                **office,
            }
        ).insert(ignore_permissions=True)



def ensure_default_workspace():
    """Create the CBSUA Desk workspace once from its app-owned definition."""
    workspace_name = "CBSUA Helpdesk"
    if frappe.db.exists("Workspace", workspace_name):
        return

    workspace_file = (
        Path(__file__).resolve().parent.parent
        / "cbsua_helpdesk"
        / "workspace"
        / "cbsua_helpdesk"
        / "cbsua_helpdesk.json"
    )
    if not workspace_file.is_file():
        frappe.logger("cbsua_helpdesk").warning(
            "CBSUA Helpdesk Workspace definition is missing: %s", workspace_file
        )
        return

    workspace = json.loads(workspace_file.read_text(encoding="utf-8"))
    frappe.get_doc(workspace).insert(ignore_permissions=True)


def ensure_default_branding():
    """Set Helpdesk's native brand fields only when they are still blank.

    Helpdesk's public config endpoint reads these HD Settings fields and its
    Vue BrandLogo component consumes brand_logo. Using the native settings is
    safer than attempting to inject Desk CSS into the standalone Vue app.
    Administrators remain free to replace any value later.
    """
    if not frappe.db.exists("DocType", "HD Settings"):
        # Keep installation tolerant of app ordering mistakes; the normal
        # installation order installs Helpdesk before this extension.
        frappe.logger("cbsua_helpdesk").warning(
            "HD Settings DocType is not installed; skipped CBSUA branding defaults."
        )
        return

    # HD Settings is a Single DocType in Helpdesk v16. Check the live schema
    # before writing so an upstream field rename is visible in the site log.
    available_fields = set(frappe.get_meta("HD Settings").get_valid_columns())
    settings = frappe.get_single("HD Settings")
    changed_fields = []
    for fieldname, value in DEFAULT_BRANDING.items():
        if fieldname not in available_fields:
            frappe.logger("cbsua_helpdesk").warning(
                "HD Settings is missing expected branding field: %s", fieldname
            )
            continue
        if not settings.get(fieldname):
            settings.set(fieldname, value)
            changed_fields.append(fieldname)

    if changed_fields:
        settings.save(ignore_permissions=True)
        frappe.logger("cbsua_helpdesk").info(
            "Applied default CBSUA HD Settings branding fields: %s",
            ", ".join(changed_fields),
        )
    else:
        frappe.logger("cbsua_helpdesk").info(
            "CBSUA HD Settings branding defaults already populated or unavailable."
        )
