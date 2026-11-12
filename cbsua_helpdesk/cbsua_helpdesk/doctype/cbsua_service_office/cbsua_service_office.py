"""CBSUA office catalogue validation."""
import frappe
from frappe.model.document import Document

class CBSUAServiceOffice(Document):
    def validate(self):
        self.validate_phase_gate()
        self.validate_intake_gate()
        self.validate_unique_team_mapping()

    def validate_phase_gate(self):
        if self.office_code != "ICT" and (self.is_active or self.allow_customer_intake):
            frappe.throw("Only the ICT office can be activated in Phase 1.")

    def validate_intake_gate(self):
        if self.allow_customer_intake and not self.is_active:
            frappe.throw("Customer intake cannot be enabled for an inactive office.")
        if self.allow_customer_intake:
            team = self.helpdesk_team
            if not team or not frappe.db.exists("HD Team", team):
                frappe.throw("Map an existing Helpdesk Team before enabling intake.")
            if frappe.db.get_value("HD Team", team, "disabled"):
                frappe.throw("The mapped Helpdesk Team is disabled.")

    def validate_unique_team_mapping(self):
        if not self.helpdesk_team:
            return
        duplicate = frappe.db.get_value("CBSUA Service Office", {"helpdesk_team": self.helpdesk_team, "name": ["!=", self.name]}, "name")
        if duplicate:
            frappe.throw(f"Helpdesk Team {self.helpdesk_team} is already mapped to {duplicate}.")
