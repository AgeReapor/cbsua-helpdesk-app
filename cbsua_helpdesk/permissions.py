"""Office-aware permission checks layered over native Helpdesk permissions."""

from __future__ import annotations

import frappe
from helpdesk.utils import is_agent


def _is_platform_admin(user: str) -> bool:
    return user == "Administrator" or "System Manager" in frappe.get_roles(user)


def _allowed_office_teams(user: str) -> list[str]:
    memberships = frappe.get_all("HD Team Member", filters={"user": user}, pluck="parent")
    if not memberships:
        return []
    teams = frappe.get_all(
        "HD Team",
        filters={"name": ["in", memberships], "disabled": 0},
        pluck="name",
    )
    if not teams:
        return []
    mapped = frappe.get_all(
        "CBSUA Service Office",
        filters={"helpdesk_team": ["in", teams]},
        pluck="helpdesk_team",
    )
    return sorted(set(mapped))


def get_hd_ticket_query_conditions(user: str | None = None) -> str:
    """Keep CBSUA-tagged tickets inside their mapped team for agent queries.

    Unmarked legacy/non-CBSUA tickets remain under native Helpdesk rules.
    """
    user = user or frappe.session.user
    if _is_platform_admin(user) or not is_agent(user):
        return ""

    allowed_teams = _allowed_office_teams(user)
    legacy = "(`tabHD Ticket`.cbsua_service_office IS NULL OR `tabHD Ticket`.cbsua_service_office = '')"
    if not allowed_teams:
        return legacy

    team_values = ", ".join(frappe.db.escape(team) for team in allowed_teams)
    return (
        f"({legacy} OR (`tabHD Ticket`.agent_group IN ({team_values}) "
        f"AND `tabHD Ticket`.cbsua_service_office IN ("
        "SELECT `name` FROM `tabCBSUA Service Office` "
        f"WHERE `helpdesk_team` IN ({team_values})))"
    )


def has_hd_ticket_permission(
    doc, user: str | None = None, ptype: str | None = None, debug: bool = False
) -> bool:
    """Apply the office check while leaving Helpdesk's native check in place.

    Frappe v16 combines controller permission hooks and denies when any returns
    false. Return true for tickets outside the CBSUA scope so Helpdesk's own
    ticket policy can decide those requests.
    """
    user = user or frappe.session.user
    if _is_platform_admin(user):
        return True
    office_name = doc.get("cbsua_service_office")
    if not office_name:
        return True
    if not is_agent(user):
        # Helpdesk's native check decides customer/requester access.
        return True

    team = frappe.db.get_value(
        "CBSUA Service Office", office_name, "helpdesk_team"
    )
    if not team or doc.get("agent_group") != team:
        return False
    if frappe.db.get_value("HD Team", team, "disabled"):
        return False
    return bool(
        frappe.db.exists("HD Team Member", {"parent": team, "user": user})
    )
