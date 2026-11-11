"""Smoke tests for the CBSUA Helpdesk app."""

import cbsua_helpdesk
from frappe.tests.utils import FrappeTestCase


class TestCBSUAHelpdeskApp(FrappeTestCase):
    def test_app_package_imports(self):
        self.assertEqual(cbsua_helpdesk.__version__, "0.1.0")
