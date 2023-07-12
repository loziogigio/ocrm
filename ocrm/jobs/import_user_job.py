import frappe
from ocrm.controller.user import import_users_from_external_db

def import_users_from_external_db_job():
    try:
        frappe.enqueue(import_users_from_external_db, queue='long', timeout=30, event='daily_user_import', limit=5)
        frappe.log_error(message="User import job has been queued.", title="User Import")
    except Exception as e:
        frappe.log_error(message=f"An error occurred while queuing the user import job: {str(e)}", title="User Import Error")
