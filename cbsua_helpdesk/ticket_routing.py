"""Phase 1 routing from the active CBSUA office to native Helpdesk teams."""

import frappe
from frappe import _


def route_ticket_to_office(doc, method=None):
    """Stamp new tickets with the only active intake office and its HD Team.

    Existing tickets without an office remain untouched. When an office has a
    team mapping, later changes to the native Helpdesk team must match it.
    """
    if doc.is_new():
        offices = frappe.get_all(
            "CBSUA Service Office",
            filters={"is_active": 1, "allow_customer_intake": 1},
            fields=["name", "helpdesk_team"],
        )
        if len(offices) != 1:
            frappe.throw(
                _("Ticket intake requires exactly one active CBSUA service office.")
            )

        office = offices[0]
        if not office.helpdesk_team:
            frappe.throw(
                _(
                    "Configure a Helpdesk Team on the active CBSUA Service Office "
                    "before accepting tickets."
                )
            )
        if not frappe.db.exists("HD Team", office.helpdesk_team):
            frappe.throw(_("The Helpdesk Team configured for {0} does not exist.").format(office.name))
        if frappe.db.get_value("HD Team", office.helpdesk_team, "disabled"):
            frappe.throw(_("The Helpdesk Team configured for {0} is disabled.").format(office.name))

        doc.cbsua_service_office = office.name
        doc.agent_group = office.helpdesk_team
        return

    office_name = doc.get("cbsua_service_office")
    if not office_name and doc.get("agent_group"):
        office_name = frappe.db.get_value(
            "CBSUA Service Office", {"helpdesk_team": doc.agent_group}, "name"
        )
        if office_name:
            doc.cbsua_service_office = office_name

    if office_name:
        expected_team = frappe.db.get_value(
            "CBSUA Service Office", office_name, "helpdesk_team"
        )
        if not expected_team:
            frappe.throw(
                _("Configure a Helpdesk Team for {0} before updating its tickets.").format(
                    office_name
                )
            )
        if doc.get("agent_group") != expected_team:
            frappe.throw(
                _("Tickets for {0} must remain assigned to its configured Helpdesk Team.").format(
                    office_name
                )
            )
