"""CBSUA migration lifecycle helpers.

The after_migrate hook seeds the small Service Office catalogue. Seeding is
idempotent and additive; it does not modify existing records, create Helpdesk
Teams, configure routes, or change ticket permissions.
"""

from cbsua_helpdesk.setup.install import (
    ensure_default_branding,
    ensure_default_offices,
    ensure_default_workspace,
)


def after_install():
    """Seed baseline configuration immediately after a fresh app install.

    Helpdesk is installed before this extension, so HD Settings is available.
    """
    ensure_default_offices()
    ensure_default_branding()
    ensure_default_workspace()


def after_migrate():
    """Reconcile missing baseline configuration after every site migration.

    Both routines are idempotent and preserve administrator-configured values.
    """
    ensure_default_offices()
    ensure_default_branding()
    ensure_default_workspace()
