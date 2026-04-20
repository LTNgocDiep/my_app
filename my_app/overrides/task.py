import frappe
from frappe import _
from frappe.utils import getdate, today
from erpnext.projects.doctype.task.task import Task
from hrms.hr.report.monthly_attendance_sheet.monthly_attendance_sheet import execute as original_execute

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

            status_2way = ["Open", "Working", "QA Pending"]
            
            if old_status in status_2way and new_status in status_2way:
                return

            feedback_status = ["QA Feedback", "Client Feedback"]
            
            if old_status in feedback_status and new_status == "Working":
                return

            frappe.throw(
                _("Action denied: Cannot change status from {0} to {1}. ").format(old_status, new_status)
            )

def set_tasks_as_overdue_custom():

    tasks = frappe.get_all(
        "Task",
        filters={"status": ["not in", ["Cancelled", "Completed"]]},
        fields=["name", "status", "review_date"],
    )
    
    for task in tasks:

        if task.status == "QA Pending": 
            if task.review_date and getdate(task.review_date) > getdate(today()):
                continue
        
        try:
            task_doc = frappe.get_doc("Task", task.name)
            task_doc.update_status()
        except Exception:
            frappe.log_error(f"Error updating task {task.name}", "Overdue Task Update")


import frappe
from frappe import _

ALLOWED_FIELDS = {"status", "description"}

SYSTEM_FIELDS = {
    "name",
    "owner",
    "creation",
    "modified",
    "modified_by",
    "docstatus",
    "idx",
    "_user_tags",
    "_comments",
    "_assign",
    "_liked_by",
}


def validate_task_restricted_edit(doc, method=None):
    user = frappe.session.user

    if user == "Guest":
        return

    roles = frappe.get_roles(user)

    # Chỉ áp dụng cho user thường
    if not ("GS Projects User" in roles and "GS Project Manager" not in roles):
        return

    # Nếu là doc mới thì có thể bỏ qua, hoặc chặn luôn tùy bạn
    if doc.is_new():
        return

    old_doc = doc.get_doc_before_save()
    if not old_doc:
        return

    changed_disallowed_fields = []

    for df in doc.meta.fields:
        fieldname = df.fieldname

        if not fieldname:
            continue

        if fieldname in SYSTEM_FIELDS:
            continue

        # bỏ qua field layout
        if df.fieldtype in ("Section Break", "Column Break", "Tab Break", "HTML", "Button"):
            continue

        old_value = old_doc.get(fieldname)
        new_value = doc.get(fieldname)

        if old_value != new_value and fieldname not in ALLOWED_FIELDS:
            changed_disallowed_fields.append(fieldname)

    if changed_disallowed_fields:
        frappe.throw(
            _(
                "Bạn chỉ được phép chỉnh sửa các trường: {0}. "
                "Các trường không được phép sửa: {1}"
            ).format(
                ", ".join(sorted(ALLOWED_FIELDS)),
                ", ".join(changed_disallowed_fields)
            )
        )