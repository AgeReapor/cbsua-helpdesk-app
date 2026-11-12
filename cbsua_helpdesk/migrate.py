"""CBSUA migration lifecycle helpers.

The after_install/after_migrate hooks seed the office catalogue, branding
defaults, workspace, the office field on HD Ticket, and the ICT Phase 1
bootstrap (team, mapping, provisional categories, queue views). Every step is
additive and idempotent, so administrator edits are preserved.
"""

from cbsua_helpdesk.setup.ict import provision_ict
from cbsua_helpdesk.setup.install import (
    ensure_default_branding,
    ensure_default_offices,
    ensure_default_workspace,
    ensure_ticket_office_field,
)


def seed_baseline():
    """Run every idempotent seed step in dependency order."""
    ensure_default_offices()
    ensure_ticket_office_field()
    provision_ict()
    ensure_default_branding()
    ensure_default_workspace()


def after_install():
    """Seed baseline configuration immediately after a fresh app install."""
    seed_baseline()


def after_migrate():
    """Reconcile missing baseline configuration after every site migration."""
    seed_baseline()
