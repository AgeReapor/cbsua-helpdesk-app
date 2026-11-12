"""Tests for the ICT Phase 1 bootstrap, routing, and team-scoped access."""

import frappe
from frappe.tests.utils import FrappeTestCase

from cbsua_helpdesk.permissions import (
    get_hd_ticket_query_conditions,
    has_hd_ticket_permission,
)
from cbsua_helpdesk.setup.ict import (
    ICT_OFFICE,
    ICT_TEAM_NAME,
    ICT_TICKET_TYPES,
    ICT_VIEWS,
    add_ict_staff,
    provision_ict,
)
from cbsua_helpdesk.test_utils import make_team, make_ticket, make_user


class TestICTBootstrap(FrappeTestCase):
    def test_ict_team_is_mapped_and_intake_enabled(self):
        office = frappe.get_doc("CBSUA Service Office", ICT_OFFICE)
        self.assertEqual(office.helpdesk_team, ICT_TEAM_NAME)
        self.assertTrue(office.allow_customer_intake)

    def test_future_offices_stay_disabled(self):
        for code in ("REGISTRAR", "ADMISSIONS", "CASHIER"):
            office = frappe.get_doc("CBSUA Service Office", code)
            self.assertEqual((office.is_active, office.allow_customer_intake), (0, 0))

    def test_provisional_ticket_types_exist(self):
        for name, _description in ICT_TICKET_TYPES:
            self.assertTrue(frappe.db.exists("HD Ticket Type", name), name)

    def test_queue_views_exist_and_are_public(self):
        for view in ICT_VIEWS:
            name = frappe.db.get_value(
                "HD View", {"label": view["label"], "dt": "HD Ticket"}, "name"
            )
            self.assertTrue(name, view["label"])
            self.assertEqual(frappe.db.get_value("HD View", name, "public"), 1)

    def test_provisioning_is_idempotent(self):
        counts = lambda: (
            frappe.db.count("HD Team", {"team_name": ICT_TEAM_NAME}),
            frappe.db.count("HD View", {"label": ["like", "ICT %"]}),
            frappe.db.count("HD Ticket Type", {"name": ["in", [t for t, _ in ICT_TICKET_TYPES]]}),
        )
        before = counts()
        provision_ict()
        self.assertEqual(counts(), before)

    def test_add_ict_staff_joins_team_and_is_repeatable(self):
        email = "ict.agent@example.com"
        make_user(email)
        add_ict_staff(email)
        add_ict_staff(email)
        members = frappe.get_all("HD Team Member", filters={"parent": ICT_TEAM_NAME, "user": email})
        self.assertEqual(len(members), 1)
        self.assertTrue(frappe.db.exists("HD Agent", email))

    def test_add_ict_staff_rejects_unknown_user(self):
        with self.assertRaises(frappe.ValidationError):
            add_ict_staff("nobody@example.com")


class TestICTRoutingAndAccess(FrappeTestCase):
    def test_new_ticket_is_stamped_for_ict(self):
        ticket = make_ticket("Wi-Fi down in the library")
        self.assertEqual(ticket.cbsua_service_office, ICT_OFFICE)
        self.assertEqual(ticket.agent_group, ICT_TEAM_NAME)

    def test_ict_member_can_open_ticket_and_outsider_cannot(self):
        ticket = make_ticket("Printer jam")
        ict_user = "ict.reader@example.com"
        other_user = "other.team@example.com"
        make_user(ict_user, ("Agent",))
        make_user(other_user, ("Agent",))
        add_ict_staff(ict_user)
        other_team = make_team("CBSUA Test Other Team")
        other_team.append("users", {"user": other_user})
        other_team.save(ignore_permissions=True)

        self.assertTrue(has_hd_ticket_permission(ticket, ict_user))
        self.assertFalse(has_hd_ticket_permission(ticket, other_user))

    def test_outsider_list_query_excludes_cbsua_tickets(self):
        other_user = "other.list@example.com"
        make_user(other_user, ("Agent",))
        condition = get_hd_ticket_query_conditions(other_user)
        self.assertIn("cbsua_service_office IS NULL", condition)
        self.assertNotIn("agent_group IN", condition)

    def test_client_cannot_change_ticket_office(self):
        ticket = make_ticket("Account locked")
        ticket.cbsua_service_office = "CASHIER"
        with self.assertRaises(frappe.ValidationError):
            ticket.save(ignore_permissions=True)
