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
        if not offices:
            frappe.throw(
                _(
                    "CBSUA ticket intake is disabled. Map an enabled Helpdesk Team "
                    "to ICT, then enable customer intake."
                )
            )
        if len(offices) > 1:
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

    # Do not trust the submitted office field, even though the Desk control is
    # read-only. Client scripts and REST callers can still send arbitrary data.
    # Preserve legacy tickets as unclassified; an explicit migration policy is
    # required before any backfill or cross-office transfer is supported.
    saved = frappe.db.get_value(
        "HD Ticket",
        doc.name,
        ["cbsua_service_office", "agent_group"],
        as_dict=True,
    )
    saved_office = (saved.cbsua_service_office or "") if saved else ""
    submitted_office = doc.get("cbsua_service_office") or ""

    if not saved_office:
        if submitted_office:
            frappe.throw(
                _("CBSUA Service Office is assigned by the server and cannot be set manually.")
            )
        return

    if submitted_office != saved_office:
        frappe.throw(
            _("CBSUA Service Office is assigned by the server and cannot be changed manually.")
        )

    expected_team = frappe.db.get_value(
        "CBSUA Service Office", saved_office, "helpdesk_team"
    )
    if not expected_team:
        frappe.throw(
            _("Configure a Helpdesk Team for {0} before updating its tickets.").format(
                saved_office
            )
        )
    if doc.get("agent_group") != expected_team:
        frappe.throw(
            _("Tickets for {0} must remain assigned to its configured Helpdesk Team.").format(
                saved_office
            )
        )
