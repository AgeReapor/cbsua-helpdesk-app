"""Tests for server-managed CBSUA ticket office routing."""

from unittest.mock import MagicMock, patch

import frappe
from frappe.tests.utils import FrappeTestCase

from cbsua_helpdesk.ticket_routing import route_ticket_to_office


class TestTicketRouting(FrappeTestCase):
    def test_new_ticket_is_stamped_with_the_active_office_and_team(self):
        doc = MagicMock()
        doc.is_new.return_value = True

        with (
            patch(
                "cbsua_helpdesk.ticket_routing.frappe.get_all",
                return_value=[
                    frappe._dict(name="ICT", helpdesk_team="CBSUA ICT Support")
                ],
            ),
            patch.object(frappe.db, "exists", return_value=True),
            patch.object(frappe.db, "get_value", return_value=0),
        ):
            route_ticket_to_office(doc)

        self.assertEqual(doc.cbsua_service_office, "ICT")
        self.assertEqual(doc.agent_group, "CBSUA ICT Support")

    def test_new_ticket_fails_closed_when_intake_is_disabled(self):
        doc = MagicMock()
        doc.is_new.return_value = True

        with (
            patch("cbsua_helpdesk.ticket_routing.frappe.get_all", return_value=[]),
            self.assertRaises(frappe.ValidationError),
        ):
            route_ticket_to_office(doc)

    def test_existing_ticket_cannot_change_its_office(self):
        doc = MagicMock()
        doc.is_new.return_value = False
        doc.name = "HD-TICKET-TEST"
        doc.get.side_effect = lambda key: {
            "cbsua_service_office": "CASHIER",
            "agent_group": "CBSUA ICT Support",
        }.get(key)
        saved = frappe._dict(
            cbsua_service_office="ICT", agent_group="CBSUA ICT Support"
        )

        with (
            patch.object(frappe.db, "get_value", return_value=saved),
            self.assertRaises(frappe.ValidationError),
        ):
            route_ticket_to_office(doc)

    def test_legacy_ticket_cannot_be_classified_by_a_client(self):
        doc = MagicMock()
        doc.is_new.return_value = False
        doc.name = "HD-TICKET-LEGACY"
        doc.get.side_effect = lambda key: {
            "cbsua_service_office": "ICT",
            "agent_group": "CBSUA ICT Support",
        }.get(key)
        saved = frappe._dict(cbsua_service_office=None, agent_group=None)

        with (
            patch.object(frappe.db, "get_value", return_value=saved),
            self.assertRaises(frappe.ValidationError),
        ):
            route_ticket_to_office(doc)

    def test_existing_ticket_cannot_be_moved_to_another_team(self):
        doc = MagicMock()
        doc.is_new.return_value = False
        doc.name = "HD-TICKET-ICT"
        doc.get.side_effect = lambda key: {
            "cbsua_service_office": "ICT",
            "agent_group": "Billing",
        }.get(key)
        saved = frappe._dict(
            cbsua_service_office="ICT", agent_group="CBSUA ICT Support"
        )

        with (
            patch.object(
                frappe.db,
                "get_value",
                side_effect=[saved, "CBSUA ICT Support"],
            ),
            self.assertRaises(frappe.ValidationError),
        ):
            route_ticket_to_office(doc)
