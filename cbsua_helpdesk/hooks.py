"""Frappe hooks for the CBSUA Helpdesk extension.

The hooks in this file are intentionally additive. Frappe Helpdesk remains the
owner of ticket lifecycle, ticket permissions, agent UI, and customer workflow.
CBSUA contributes institutional metadata and conservative brand assets only.
"""

app_name = "cbsua_helpdesk"
app_title = "CBSUA Helpdesk"
app_publisher = "Central Bicol State University of Agriculture"
app_description = "CBSUA-branded service desk configuration and extensions."
app_email = ""
app_license = "Proprietary"
app_icon = "octicon octicon-life-buoy"
app_color = "#106031"

# Frappe's documented Desk and Portal asset hooks. Keep both CSS files in this
# app so upgrades to the upstream Helpdesk checkout do not overwrite them.
app_include_css = ["/assets/cbsua_helpdesk/css/cbsua_brand.css"]
web_include_css = ["/assets/cbsua_helpdesk/css/cbsua_brand.css"]

# Used by Frappe app metadata surfaces and the standard website navbar.
# This SVG is a temporary compact mark, not a replacement for the official
# full university seal. See docs/M1-configuration-and-branding.md.
app_logo_url = "/assets/cbsua_helpdesk/images/cbsua-brand-mark.svg"
brand_html = (
    '<a class="navbar-brand" href="/" aria-label="CBSUA Helpdesk">'
    '<img src="/assets/cbsua_helpdesk/images/cbsua-brand-mark.svg" '
    'alt="" style="height:28px;width:28px;margin-right:8px;">'
    '<span>CBSUA Helpdesk</span></a>'
)

# Additive, repeatable catalogue seed. This runs after DocTypes are synced by
# migrate, so the Service Office table exists before records are inserted.
after_migrate = "cbsua_helpdesk.migrate.after_migrate"
