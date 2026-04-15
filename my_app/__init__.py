__version__ = "0.0.1"

import frappe

def apply_monkey_patch():
    import erpnext.projects.doctype.task.task as erpnext_task
    from my_app.overrides.task_utils import set_tasks_as_overdue_custom
    erpnext_task.set_tasks_as_overdue = set_tasks_as_overdue_custom

apply_monkey_patch()