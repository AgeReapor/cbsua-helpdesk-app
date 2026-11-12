"""CBSUA test helpers. Keep factories here, not inline in test files."""

import frappe


def make_user(email: str, roles: tuple[str, ...] = ()):
    """Create (or fetch) an enabled test User with the given roles."""
    if frappe.db.exists("User", email):
        return frappe.get_doc("User", email)
    user = frappe.get_doc(
        {
            "doctype": "User",
            "email": email,
            "first_name": email.split("@")[0],
            "send_welcome_email": 0,
            "enabled": 1,
        }
    )
    user.insert(ignore_permissions=True)
    if roles:
        user.add_roles(*roles)
    return user


def make_team(team_name: str):
    """Create (or fetch) a native HD Team that is not mapped to any office."""
    if frappe.db.exists("HD Team", team_name):
        return frappe.get_doc("HD Team", team_name)
    return frappe.get_doc({"doctype": "HD Team", "team_name": team_name}).insert(
        ignore_permissions=True
    )


def make_ticket(subject: str = "CBSUA test ticket", raised_by: str = "requester@example.com"):
    """Insert a native HD Ticket through the normal controller; routing stamps it."""
    make_user(raised_by)
    return frappe.get_doc(
        {
            "doctype": "HD Ticket",
            "subject": subject,
            "description": "Disposable test ticket.",
            "raised_by": raised_by,
        }
    ).insert(ignore_permissions=True)
