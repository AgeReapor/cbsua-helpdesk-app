"""Additional team-scope checks for CBSUA-tagged tickets."""
import frappe

def hd_ticket_query(user):
    """Limit tagged-ticket list queries to teams the current agent belongs to."""
    user = user or frappe.session.user
    if user == "Administrator":
        return None
    escaped_user = frappe.db.escape(user)
    table = "`tabHD Ticket`"
    return (
        f"(({table}.cbsua_service_office IS NULL OR {table}.cbsua_service_office = '') "
        f"OR ({table}.agent_group IN (SELECT parent FROM `tabHD Team Member` WHERE user = {escaped_user})))"
    )

def hd_ticket_has_permission(doc, user=None, permission_type=None):
    """Apply team membership to tagged tickets; defer untagged tickets to Helpdesk."""
    user = user or frappe.session.user
    if user == "Administrator" or not doc.cbsua_service_office:
        return True
    if not frappe.db.exists("HD Agent", {"user": user}):
        return False
    return bool(frappe.db.exists("HD Team Member", {"parent": doc.agent_group, "user": user}))
