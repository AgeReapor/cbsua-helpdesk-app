"""Frappe hooks for the CBSUA Helpdesk extension."""
app_name = "cbsua_helpdesk"
app_title = "CBSUA Helpdesk"
app_publisher = "CBSUA"
app_description = "CBSUA-specific extensions for Frappe Helpdesk."
app_email = ""
app_license = "Proprietary"

after_install = "cbsua_helpdesk.setup.install.after_install"
after_migrate = "cbsua_helpdesk.setup.install.after_migrate"

app_include_css = ["/assets/cbsua_helpdesk/css/cbsua_brand.css"]
web_include_css = ["/assets/cbsua_helpdesk/css/cbsua_brand.css"]

doc_events = {
    "HD Ticket": {
        "before_validate": "cbsua_helpdesk.ticket_routing.before_validate",
    }
}

permission_query_conditions = {
    "HD Ticket": "cbsua_helpdesk.permissions.hd_ticket_query",
}
has_permission = {
    "HD Ticket": "cbsua_helpdesk.permissions.hd_ticket_has_permission",
}
