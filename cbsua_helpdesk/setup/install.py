"""Safe, repeatable setup for the CBSUA configuration foundation.

The seed routine creates the four office catalogue records required by the
SRS. It is deliberately additive: it never overwrites an existing office
record, so an administrator's later edits are not silently reverted by
bench migrate. The Service Office controller separately prevents activation
of future offices until a later, reviewed onboarding implementation changes
that guard.
"""

import frappe


DEFAULT_OFFICES = (
    {
        "office_code": "ICT",
        "office_name": "ICT Office",
        "phase": "Phase 1",
        "is_active": 1,
        "allow_customer_intake": 1,
        "description": "Initial operational office for Phase 1.",
    },
    {
        "office_code": "REGISTRAR",
        "office_name": "Registrar",
        "phase": "Future",
        "is_active": 0,
        "allow_customer_intake": 0,
        "description": "Reserved for a separately approved future onboarding phase.",
    },
    {
        "office_code": "ADMISSIONS",
        "office_name": "Admissions",
        "phase": "Future",
        "is_active": 0,
        "allow_customer_intake": 0,
        "description": "Reserved for a separately approved future onboarding phase.",
    },
    {
        "office_code": "CASHIER",
        "office_name": "Cashier",
        "phase": "Future",
        "is_active": 0,
        "allow_customer_intake": 0,
        "description": "Reserved for a separately approved future onboarding phase.",
    },
)


def ensure_default_offices():
    """Create missing office catalogue rows without changing existing rows.

    This method is safe to call repeatedly from after_migrate. It does not
    create Helpdesk Teams, users, assignments, routes, or customer-facing
    forms. The office catalogue is configuration metadata only at this stage.
    """
    for office in DEFAULT_OFFICES:
        if frappe.db.exists("CBSUA Service Office", office["office_code"]):
            continue

        frappe.get_doc(
            {
                "doctype": "CBSUA Service Office",
                **office,
            }
        ).insert(ignore_permissions=True)
