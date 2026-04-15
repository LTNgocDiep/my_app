import frappe
from frappe.utils import getdate, today

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