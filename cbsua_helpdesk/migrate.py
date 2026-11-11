"""CBSUA migration lifecycle helpers.

The after_migrate hook seeds the small Service Office catalogue. Seeding is
idempotent and additive; it does not modify existing records, create Helpdesk
Teams, configure routes, or change ticket permissions.
"""

from cbsua_helpdesk.setup.install import ensure_default_offices


def after_migrate():
    """Ensure baseline office metadata exists after DocTypes are synchronized."""
    ensure_default_offices()
