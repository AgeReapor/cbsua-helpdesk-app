"""Tests for the M1 CBSUA configuration foundation.

These tests intentionally cover only the office catalogue's safe defaults and
activation guard. They do not claim that Helpdesk ticket-level isolation has
been implemented or proven; that is a separate release gate in the SRS.
"""

import frappe
from frappe.tests.utils import FrappeTestCase

from cbsua_helpdesk.cbsua_helpdesk.doctype.cbsua_service_office.cbsua_service_office import (
    CBSUAServiceOffice,
)


class TestCBSUAConfiguration(FrappeTestCase):
    def test_default_office_catalogue_is_seeded(self):
        """Migrations seed all four offices while exposing only ICT intake."""
        expected = {
            "ICT": (1, 1),
            "REGISTRAR": (0, 0),
            "ADMISSIONS": (0, 0),
            "CASHIER": (0, 0),
        }
        for code, flags in expected.items():
            office = frappe.get_doc("CBSUA Service Office", code)
            self.assertEqual((office.is_active, office.allow_customer_intake), flags)

    def test_helpdesk_branding_defaults_are_configured(self):
        """Native HD Settings expose the official logo to the Helpdesk Vue app."""
        settings = frappe.get_single("HD Settings")
        self.assertEqual(settings.brand_name, "CBSUA Helpdesk")
        self.assertEqual(
            settings.brand_logo,
            "/assets/cbsua_helpdesk/images/cbsua-logo.png",
        )
        self.assertEqual(
            settings.favicon,
            "/assets/cbsua_helpdesk/images/cbsua-logo.png",
        )

    def test_future_office_cannot_be_activated_in_m1(self):
        """Registrar, Admissions, and Cashier require a later reviewed release."""
        office = frappe.get_doc("CBSUA Service Office", "REGISTRAR")
        office.is_active = 1
        with self.assertRaises(frappe.ValidationError):
            office.validate()

    def test_future_office_cannot_enable_customer_intake(self):
        office = frappe.get_doc("CBSUA Service Office", "ADMISSIONS")
        office.allow_customer_intake = 1
        with self.assertRaises(frappe.ValidationError):
            office.validate()

    def test_inactive_office_cannot_accept_intake(self):
        office = frappe.get_doc("CBSUA Service Office", "ICT")
        office.is_active = 0
        office.allow_customer_intake = 1
        with self.assertRaises(frappe.ValidationError):
            office.validate()

    def test_controller_is_a_frappe_document_controller(self):
        self.assertTrue(issubclass(CBSUAServiceOffice, frappe.model.document.Document))
