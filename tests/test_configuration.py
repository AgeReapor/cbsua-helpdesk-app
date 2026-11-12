"""Tests for the M1 CBSUA configuration foundation.

These tests cover safe office defaults and activation guardrails. They do not
claim that Helpdesk ticket-level isolation has been implemented or proven;
that is a separate release gate in the SRS.
"""

from unittest.mock import MagicMock, call, patch

import frappe
from frappe.tests.utils import FrappeTestCase

from cbsua_helpdesk.migrate import after_migrate
from cbsua_helpdesk.setup.install import ensure_default_branding

from cbsua_helpdesk.cbsua_helpdesk.doctype.cbsua_service_office.cbsua_service_office import (
    CBSUAServiceOffice,
)


class TestCBSUAConfiguration(FrappeTestCase):
    def test_cbsua_lifecycle_hooks_are_registered(self):
        """The installed app must expose both seed entry points to Frappe.

        This catches a packaging regression where migration helpers exist but
        hooks.py no longer registers them, leaving HD Settings blank forever.
        """
        self.assertIn(
            "cbsua_helpdesk.migrate.after_migrate",
            frappe.get_hooks("after_migrate", app_name="cbsua_helpdesk"),
        )
        self.assertIn(
            "cbsua_helpdesk.migrate.after_install",
            frappe.get_hooks("after_install", app_name="cbsua_helpdesk"),
        )

    def test_default_office_catalogue_is_seeded(self):
        """Migrations seed all offices; ICT is mapped with intake on, others stay off."""
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

    def test_branding_seed_populates_blank_fields(self):
        """The seed repairs blank native fields without requiring a reinstall."""
        settings = frappe.get_single("HD Settings")
        original = {
            fieldname: settings.get(fieldname)
            for fieldname in ("brand_name", "brand_logo", "favicon")
        }
        try:
            for fieldname in original:
                settings.set(fieldname, None)
            settings.save(ignore_permissions=True)

            ensure_default_branding()
            refreshed = frappe.get_single("HD Settings")
            self.assertEqual(refreshed.brand_name, "CBSUA Helpdesk")
            self.assertEqual(
                refreshed.brand_logo,
                "/assets/cbsua_helpdesk/images/cbsua-logo.png",
            )
            self.assertEqual(
                refreshed.favicon,
                "/assets/cbsua_helpdesk/images/cbsua-logo.png",
            )
        finally:
            restored = frappe.get_single("HD Settings")
            for fieldname, value in original.items():
                restored.set(fieldname, value)
            restored.save(ignore_permissions=True)

    def test_branding_seed_preserves_existing_admin_values(self):
        """A rerun must not overwrite branding deliberately set by an admin."""
        settings = frappe.get_single("HD Settings")
        original = {
            fieldname: settings.get(fieldname)
            for fieldname in ("brand_name", "brand_logo", "favicon")
        }
        try:
            settings.brand_name = "Existing approved brand"
            settings.brand_logo = "/files/approved-logo.png"
            settings.favicon = "/files/approved-favicon.png"
            settings.save(ignore_permissions=True)

            ensure_default_branding()
            refreshed = frappe.get_single("HD Settings")
            self.assertEqual(refreshed.brand_name, "Existing approved brand")
            self.assertEqual(refreshed.brand_logo, "/files/approved-logo.png")
            self.assertEqual(refreshed.favicon, "/files/approved-favicon.png")
        finally:
            restored = frappe.get_single("HD Settings")
            for fieldname, value in original.items():
                restored.set(fieldname, value)
            restored.save(ignore_permissions=True)

    def test_migration_seed_is_idempotent(self):
        """Repeated migration seeding preserves the same settings and offices."""
        office_codes = ("ICT", "REGISTRAR", "ADMISSIONS", "CASHIER")

        after_migrate()
        first_branding = frappe.get_single("HD Settings").as_dict()
        first_offices = {
            code: frappe.get_doc("CBSUA Service Office", code).as_dict()
            for code in office_codes
        }

        after_migrate()
        second_branding = frappe.get_single("HD Settings").as_dict()
        second_offices = {
            code: frappe.get_doc("CBSUA Service Office", code).as_dict()
            for code in office_codes
        }

        for fieldname in ("brand_name", "brand_logo", "favicon"):
            self.assertEqual(second_branding[fieldname], first_branding[fieldname])
        for code in office_codes:
            for fieldname in (
                "office_code",
                "office_name",
                "phase",
                "is_active",
                "allow_customer_intake",
            ):
                self.assertEqual(
                    second_offices[code][fieldname], first_offices[code][fieldname]
                )

    def test_branding_seed_logs_and_skips_when_settings_doctype_is_missing(self):
        """An absent Helpdesk app is diagnosed without calling its DocType APIs."""
        with (
            patch.object(frappe.db, "exists", return_value=False),
            patch.object(frappe, "logger") as logger_factory,
            patch.object(frappe, "get_meta") as get_meta,
            patch.object(frappe, "get_single") as get_single,
        ):
            ensure_default_branding()

        logger_factory.return_value.warning.assert_called_once_with(
            "HD Settings DocType is not installed; skipped CBSUA branding defaults."
        )
        get_meta.assert_not_called()
        get_single.assert_not_called()

    def test_branding_seed_logs_missing_fields_and_sets_available_fields(self):
        """Schema drift is logged while fields still present are populated."""
        metadata = MagicMock()
        metadata.get_valid_columns.return_value = ["brand_name"]
        settings = MagicMock()
        settings.get.return_value = None

        with (
            patch.object(frappe.db, "exists", return_value=True),
            patch.object(frappe, "get_meta", return_value=metadata),
            patch.object(frappe, "get_single", return_value=settings),
            patch.object(frappe, "logger") as logger_factory,
        ):
            ensure_default_branding()

        settings.set.assert_called_once_with("brand_name", "CBSUA Helpdesk")
        settings.save.assert_called_once_with(ignore_permissions=True)
        logger_factory.return_value.warning.assert_has_calls(
            [
                call("HD Settings is missing expected branding field: %s", "brand_logo"),
                call("HD Settings is missing expected branding field: %s", "favicon"),
            ]
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

    def test_ict_intake_requires_a_mapped_helpdesk_team(self):
        office = frappe.get_doc("CBSUA Service Office", "ICT")
        office.is_active = 1
        office.allow_customer_intake = 1
        office.helpdesk_team = None
        with self.assertRaises(frappe.ValidationError):
            office.validate()

    def test_controller_is_a_frappe_document_controller(self):
        self.assertTrue(issubclass(CBSUAServiceOffice, frappe.model.document.Document))
