"""Controller for the CBSUA Service Office configuration DocType.

This DocType is a small institutional office catalogue, not a ticket or team
model. It does not replace Helpdesk's HD Team, HD Ticket, or assignment logic.

M1 safety rule: only ICT can be enabled or exposed for customer intake. Future
offices are seeded as disabled records and attempts to activate them are
rejected until a later onboarding milestone explicitly changes this guard
alongside permission-isolation tests and documented approval.
"""

import frappe
from frappe import _
from frappe.model.document import Document


class CBSUAServiceOffice(Document):
    """Validate CBSUA office metadata and preserve the Phase 1 activation gate."""

    def validate(self):
        self.office_code = (self.office_code or "").strip().upper()
        if not self.office_code:
            frappe.throw(_("Office Code is required."))

        # Customer intake cannot be enabled for an inactive catalogue record.
        if self.allow_customer_intake and not self.is_active:
            frappe.throw(_("Customer intake cannot be enabled for an inactive office."))

        # Phase 1 is intentionally hard-gated to ICT. This is not a permission
        # boundary for tickets; it is a configuration guard against accidentally
        # exposing a future office before its onboarding work is approved.
        if self.office_code != "ICT" and (self.is_active or self.allow_customer_intake):
            frappe.throw(
                _("Only ICT may be activated in M1. Future offices require an approved onboarding release.")
            )

        if self.helpdesk_team:
            duplicate = frappe.db.exists(
                "CBSUA Service Office",
                {"helpdesk_team": self.helpdesk_team, "name": ["!=", self.name]},
            )
            if duplicate:
                frappe.throw(
                    _("A Helpdesk Team can be mapped to only one CBSUA Service Office.")
                )

            if not frappe.db.exists("HD Team", self.helpdesk_team):
                frappe.throw(_("Select an existing Helpdesk Team."))
            if frappe.db.get_value("HD Team", self.helpdesk_team, "disabled"):
                frappe.throw(_("The mapped Helpdesk Team must be enabled."))
