__version__ = "0.0.1"

import frappe

def apply_monkey_patch():
    import erpnext.projects.doctype.task.task as erpnext_task
    from my_app.overrides.task import set_tasks_as_overdue_custom
    erpnext_task.set_tasks_as_overdue = set_tasks_as_overdue_custom

apply_monkey_patch()




from my_app.overrides.attendance_report import patch_monthly_attendance_sheet

patch_monthly_attendance_sheet()




