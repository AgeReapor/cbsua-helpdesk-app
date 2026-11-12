"""Server-managed office classification and routing for native HD Tickets."""
import frappe

def before_validate(doc, method=None):
    """Stamp new tickets from the sole enabled intake office; protect classification."""
    if doc.is_new():
        office = get_intake_office()
        doc.cbsua_service_office = office.name
        doc.agent_group = office.helpdesk_team
        return
    previous = frappe.db.get_value("HD Ticket", doc.name, ["cbsua_service_office", "agent_group"], as_dict=True)
    if not previous:
        return
    if doc.cbsua_service_office != previous.cbsua_service_office:
        frappe.throw("Service office is managed by CBSUA Helpdesk and cannot be changed.")
    if previous.cbsua_service_office:
        office = frappe.get_doc("CBSUA Service Office", previous.cbsua_service_office)
        if not office.is_active or not office.helpdesk_team:
            frappe.throw("The ticket's CBSUA office mapping is no longer active.")
        if doc.agent_group != previous.agent_group:
            frappe.throw("The office team assignment cannot be changed directly.")
        if previous.agent_group != office.helpdesk_team:
            frappe.throw("The ticket's office/team mapping has changed; contact an administrator.")

def get_intake_office():
    offices = frappe.get_list("CBSUA Service Office", filters={"is_active": 1, "allow_customer_intake": 1}, fields=["name", "helpdesk_team"], limit_page_length=2)
    if len(offices) != 1:
        frappe.throw("CBSUA ticket intake is unavailable: exactly one office must be enabled.")
    office = offices[0]
    team = office.helpdesk_team
    if not team or not frappe.db.exists("HD Team", team):
        frappe.throw("CBSUA ticket intake is unavailable: configure the ICT Helpdesk Team.")
    if frappe.db.get_value("HD Team", team, "disabled"):
        frappe.throw("CBSUA ticket intake is unavailable: the ICT Helpdesk Team is disabled.")
    return office
