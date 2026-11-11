"""Frappe hooks for the CBSUA Helpdesk extension.

Helpdesk remains the owner of ticket lifecycle, native team permissions, agent
UI, and customer workflow. CBSUA adds office metadata and narrowly scoped
routing and permission checks for tickets linked to CBSUA Service Offices.
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

# App-scoped CSS is not loaded by the /helpdesk Vue application; this hook
# intentionally styles only Frappe Desk. See the frontend integration notes.
web_include_css = ["/assets/cbsua_helpdesk/css/cbsua_brand.css"]

# Used by Frappe app metadata surfaces and the standard website navbar.
# The supplied official seal is used here; the standalone Helpdesk Vue frontend
# requires its own version-pinned integration for in-app logo replacement.
app_logo_url = "/assets/cbsua_helpdesk/images/cbsua-logo.png"
brand_html = (
    '<a class="navbar-brand" href="/" aria-label="CBSUA Helpdesk">'
    '<img src="/assets/cbsua_helpdesk/images/cbsua-logo.png" '
    'alt="" style="height:28px;width:28px;margin-right:8px;">'
    '<span>CBSUA Helpdesk</span></a>'
)

# Additive, repeatable catalogue seed. This runs after DocTypes are synced by
# migrate, so the Service Office table exists before records are inserted.
# Frappe's documented migration hook contract is a dotted Python path.
# Frappe normalizes this into the list returned by frappe.get_hooks().
after_migrate = "cbsua_helpdesk.migrate.after_migrate"

# Helpdesk is installed before this extension, so HD Settings exists here.
after_install = "cbsua_helpdesk.migrate.after_install"

# Route new Helpdesk tickets through the active CBSUA office-to-team mapping.
# The Helpdesk ticket engine and its native team/assignment permissions remain
# authoritative; this hook only stamps the office and selected team.
doc_events = {
    "HD Ticket": {
        "before_validate": "cbsua_helpdesk.ticket_routing.route_ticket_to_office",
    }
}

# Restrict only CBSUA-tagged tickets. Non-CBSUA Helpdesk tickets continue to
# follow their existing Helpdesk permissions and team rules.
permission_query_conditions = {
    "HD Ticket": "cbsua_helpdesk.permissions.get_hd_ticket_query_conditions",
}
has_permission = {
    "HD Ticket": "cbsua_helpdesk.permissions.has_hd_ticket_permission",
}
