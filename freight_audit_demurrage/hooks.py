# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "freight_audit_demurrage"
app_title = "Frappe Freight Audit Container Demurrage"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Freight Audit Container Demurrage - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/freight_audit_demurrage/css/freight_audit_demurrage.bundle.css"
app_include_js = "/assets/freight_audit_demurrage/js/freight_audit_demurrage.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Frappe Freight Audit Container Demurrage Entry": {
        "validate": "freight_audit_demurrage.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "freight_audit_demurrage.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "freight_audit_demurrage.tasks.hourly_sync"
    ],
    "daily": [
        "freight_audit_demurrage.tasks.daily_reconciliation"
    ],
    "weekly": [
        "freight_audit_demurrage.tasks.weekly_digest"
    ]
}
