"""ICT Phase 1 bootstrap for the CBSUA Helpdesk MVP.

Everything here is additive and idempotent: it only creates what is missing and
never overwrites an administrator's later edits. It uses native Helpdesk
records (HD Team, HD Ticket Type, HD View, HD Agent) and adds no duplicates.

The ticket categories are PROVISIONAL defaults pending ICT approval (OQ-03).
SLA targets and calendars stay on Helpdesk's native default until OQ-04/07.
"""

import json

import frappe

ICT_OFFICE = "ICT"
ICT_TEAM_NAME = "CBSUA ICT Support"

# Provisional ICT categories (OQ-03). Rename or disable them in Helpdesk later.
ICT_TICKET_TYPES = (
    ("Network & Internet", "Wi-Fi, LAN, internet access, and connectivity problems."),
    ("Account & Password", "Account access, password resets, and permissions."),
    ("Hardware & Equipment", "Computers, printers, peripherals, and repairs."),
    ("Software & Systems", "Software installation, errors, and licensing."),
    ("Email & Collaboration", "Institutional email, calendars, and shared tools."),
    ("Information System Request", "Requests for information system support or changes."),
    ("Other ICT Request", "Any ICT request that fits no other category."),
)

_VIEW_COLUMNS = [
    {"label": "ID", "type": "Int", "key": "name", "width": "5rem"},
    {"label": "Subject", "type": "Data", "key": "subject", "width": "25rem"},
    {"label": "Status", "type": "Select", "key": "status", "width": "8rem"},
    {"label": "Priority", "type": "Link", "options": "HD Ticket Priority", "key": "priority", "width": "8rem"},
    {"label": "Type", "type": "Link", "options": "HD Ticket Type", "key": "ticket_type", "width": "12rem"},
    {"label": "Assigned To", "type": "MultipleAvatar", "key": "_assign", "width": "8rem"},
    {"label": "First response", "type": "Datetime", "key": "response_by", "width": "8rem"},
    {"label": "Resolution", "type": "Datetime", "key": "resolution_by", "width": "8rem"},
    {"label": "Created", "type": "Datetime", "key": "creation", "width": "8rem"},
]
_VIEW_ROWS = [
    "name", "subject", "status", "priority", "ticket_type", "agent_group",
    "contact", "agreement_status", "response_by", "resolution_by", "customer",
    "modified", "creation", "_assign", "owner",
]

# FR-15, FR-16, FR-20, FR-21, FR-43: shared ICT queue views.
ICT_VIEWS = (
    {
        "label": "ICT Unassigned Queue",
        "icon": "inbox",
        "order_by": "creation asc",
        "filters": {
            "cbsua_service_office": ICT_OFFICE,
            "status_category": "Open",
            "_assign": ["is", "not set"],
        },
    },
    {
        "label": "ICT My Tickets",
        "icon": "user-check",
        "order_by": "modified desc",
        "filters": {
            "cbsua_service_office": ICT_OFFICE,
            "status_category": "Open",
            "_assign": ["LIKE", "%@me%"],
        },
    },
    {
        "label": "ICT All Open Tickets",
        "icon": "ticket",
        "order_by": "creation desc",
        "filters": {"cbsua_service_office": ICT_OFFICE, "status_category": "Open"},
    },
    {
        "label": "ICT SLA At Risk",
        "icon": "clock-alert",
        "order_by": "response_by asc",
        "filters": {
            "cbsua_service_office": ICT_OFFICE,
            "status_category": "Open",
            "agreement_status": ["in", "First Response Due,Resolution Due,Failed"],
        },
    },
)


def ensure_ict_team():
    """Create the native ICT Helpdesk Team (and its assignment rule) once."""
    if frappe.db.exists("HD Team", ICT_TEAM_NAME):
        return
    if not frappe.db.exists("DocType", "HD Team"):
        frappe.logger("cbsua_helpdesk").warning("HD Team is missing; skipped ICT team.")
        return
    frappe.get_doc({"doctype": "HD Team", "team_name": ICT_TEAM_NAME}).insert(
        ignore_permissions=True
    )


def ensure_ict_office_mapping():
    """Map the ICT office to its team and enable intake, only on first setup.

    An administrator who later unmaps the team or disables intake is respected:
    nothing happens once a team is mapped or if the office is inactive.
    """
    if not frappe.db.exists("CBSUA Service Office", ICT_OFFICE):
        return
    office = frappe.get_doc("CBSUA Service Office", ICT_OFFICE)
    if office.helpdesk_team or not office.is_active:
        return
    if not frappe.db.exists("HD Team", ICT_TEAM_NAME):
        return
    if frappe.db.get_value("HD Team", ICT_TEAM_NAME, "disabled"):
        return
    office.helpdesk_team = ICT_TEAM_NAME
    office.allow_customer_intake = 1
    office.save(ignore_permissions=True)


def ensure_ict_ticket_types():
    """Create the provisional ICT categories that do not exist yet."""
    if not frappe.db.exists("DocType", "HD Ticket Type"):
        return
    for name, description in ICT_TICKET_TYPES:
        if frappe.db.exists("HD Ticket Type", name):
            continue
        ticket_type = frappe.new_doc("HD Ticket Type")
        ticket_type.name = name
        ticket_type.description = description
        ticket_type.is_system = 0
        ticket_type.insert(ignore_permissions=True)


def ensure_ict_views():
    """Create the public ICT queue views once, matched by label."""
    if not frappe.db.exists("DocType", "HD View"):
        return
    for view in ICT_VIEWS:
        if frappe.db.exists("HD View", {"label": view["label"], "dt": "HD Ticket"}):
            continue
        frappe.get_doc(
            {
                "doctype": "HD View",
                "dt": "HD Ticket",
                "type": "list",
                "route_name": "TicketsAgent",
                "user": "Administrator",
                "public": 1,
                "pinned": 0,
                "is_default": 0,
                "is_standard": 0,
                "is_customer_portal": 0,
                "load_default_columns": 0,
                "label": view["label"],
                "icon": view["icon"],
                "order_by": view["order_by"],
                "filters": json.dumps(view["filters"]),
                "columns": json.dumps(_VIEW_COLUMNS),
                "rows": json.dumps(_VIEW_ROWS),
            }
        ).insert(ignore_permissions=True)


def provision_ict():
    """Run the full ICT bootstrap in dependency order."""
    ensure_ict_team()
    ensure_ict_office_mapping()
    ensure_ict_ticket_types()
    ensure_ict_views()


def add_ict_staff(email: str, manager: bool = False):
    """Onboard an existing user as an ICT agent (or manager) on the ICT team.

    Run explicitly, e.g.:
    bench --site SITE execute cbsua_helpdesk.setup.ict.add_ict_staff \\
        --kwargs '{"email": "agent@cbsua.edu.ph", "manager": 1}'
    """
    if not frappe.db.exists("User", email):
        frappe.throw(f"User {email} does not exist. Invite the user first.")
    if not frappe.db.exists("HD Team", ICT_TEAM_NAME):
        frappe.throw("The ICT team does not exist. Run provision_ict first.")

    if not frappe.db.exists("HD Agent", email):
        frappe.get_doc({"doctype": "HD Agent", "user": email}).insert(
            ignore_permissions=True
        )
    if manager:
        frappe.get_doc("User", email).add_roles("Agent Manager")

    team = frappe.get_doc("HD Team", ICT_TEAM_NAME)
    if email not in {member.user for member in team.users}:
        team.append("users", {"user": email})
        team.save(ignore_permissions=True)
