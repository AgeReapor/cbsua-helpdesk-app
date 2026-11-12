"""Configuration invariant tests."""
import unittest
from cbsua_helpdesk.setup.install import OFFICES

class TestOfficeConfiguration(unittest.TestCase):
    def test_only_ict_is_phase_one_active(self):
        self.assertEqual([o["office_code"] for o in OFFICES if o["is_active"]], ["ICT"])

    def test_intake_is_disabled_until_team_mapping(self):
        self.assertTrue(all(not o["allow_customer_intake"] for o in OFFICES))

    def test_future_offices_remain_disabled(self):
        future = [o for o in OFFICES if o["phase"] == "Future"]
        self.assertEqual({o["office_code"] for o in future}, {"REGISTRAR", "ADMISSIONS", "CASHIER"})
        self.assertTrue(all(not o["is_active"] for o in future))
