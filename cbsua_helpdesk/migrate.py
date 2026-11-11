"""CBSUA migration lifecycle helpers.

The after_migrate hook seeds missing Service Office records and branding
defaults, creates the app-owned office field on HD Ticket, and seeds the
workspace. It does not provision Helpdesk Teams or users.
"""

from cbsua_helpdesk.setup.install import (
    ensure_default_branding,
    ensure_default_offices,
    ensure_default_workspace,
    ensure_ticket_office_field,
)


def after_install():
    """Seed baseline configuration immediately after a fresh app install.

    Helpdesk is installed before this extension, so HD Settings is available.
    """
    ensure_default_offices()
    ensure_default_branding()
    ensure_default_workspace()
    ensure_ticket_office_field()


def after_migrate():
    """Reconcile missing baseline configuration after every site migration.

    Both routines are idempotent and preserve administrator-configured values.
    """
    ensure_default_offices()
    ensure_default_branding()
    ensure_default_workspace()
    ensure_ticket_office_field()
