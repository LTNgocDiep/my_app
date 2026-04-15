import frappe
from frappe import _
from erpnext.projects.doctype.task.task import Task

class CustomTask(Task):
    def validate(self):
        super(CustomTask, self).validate()

        if self.is_new():
            return

        old_doc = self.get_doc_before_save()
        if not old_doc:
            return
            
        old_status = old_doc.status
        new_status = self.status

        if old_status == new_status:
            return

        user_roles = frappe.get_roles(frappe.session.user)
        
        is_manager = "GS Project Manager" in user_roles
        is_user = "GS Projects User" in user_roles

        if is_manager or "Administrator" in user_roles:
            return

        if is_user:

            allowed_2way_statuses = ["Open", "Working", "QA Pending"]
            
            if old_status in allowed_2way_statuses and new_status in allowed_2way_statuses:
                return

            if old_status == "QA Feedback" and new_status == "Working":
                return

            frappe.throw(
                _("Action denied: Cannot change status from {0} to {1}. ").format(old_status, new_status)
            )
