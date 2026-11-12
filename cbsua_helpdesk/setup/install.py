"""Idempotent M1 setup for CBSUA Helpdesk."""
import frappe

OFFICES = (
    {"office_code": "ICT", "office_name": "Information and Communications Technology Office", "phase": "Phase 1", "is_active": 1, "allow_customer_intake": 0},
    {"office_code": "REGISTRAR", "office_name": "Registrar", "phase": "Future", "is_active": 0, "allow_customer_intake": 0},
    {"office_code": "ADMISSIONS", "office_name": "Admissions", "phase": "Future", "is_active": 0, "allow_customer_intake": 0},
    {"office_code": "CASHIER", "office_name": "Cashier", "phase": "Future", "is_active": 0, "allow_customer_intake": 0},
)

def after_install():
    seed_configuration()

def after_migrate():
    seed_configuration()

def seed_configuration():
    """Create missing office catalogue rows and safe native branding defaults."""
    if not frappe.db.exists("DocType", "CBSUA Service Office"):
        frappe.logger("cbsua_helpdesk").warning("CBSUA Service Office DocType is unavailable; skipping office seed.")
        return
    for values in OFFICES:
        if not frappe.db.exists("CBSUA Service Office", values["office_code"]):
            frappe.get_doc({"doctype": "CBSUA Service Office", **values}).insert(ignore_permissions=True)
    if frappe.db.exists("DocType", "HD Settings"):
        meta = frappe.get_meta("HD Settings")
        if meta.issingle and "brand_name" in {field.fieldname for field in meta.fields}:
            if not frappe.db.get_single_value("HD Settings", "brand_name"):
                frappe.db.set_single_value("HD Settings", "brand_name", "CBSUA Helpdesk")
    frappe.clear_cache(doctype="CBSUA Service Office")
