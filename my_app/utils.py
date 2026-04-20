import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def sync_task_status_options():
    try:

        if not frappe.db.exists("DocType", "Task"):
            print("--- THÔNG BÁO: Site này không có DocType 'Task'. Bỏ qua script. ---")
            return

        ordered_statuses = [
            "Open",
            "Working",
            "QA Pending",
            "QA Reviewing",
            "QA Feedback",
            "QA Approved",
            "Delivered",
            "Client Feedback",
            "Overdue",
            "Completed",
            "Cancelled",
            "Closed"
        ]
        
        new_options_string = "\n".join(ordered_statuses)

        meta = frappe.get_meta("Task")
        field = meta.get_field("status")
        
        if not field:
            print("Lỗi: Không tìm thấy trường 'status' trong Task")
            return

        current_options = (field.options or "").strip()

        if current_options != new_options_string:

            make_property_setter(
                doctype="Task", 
                fieldname="status", 
                property="options", 
                value=new_options_string, 
                property_type="Small Text"
            )

            frappe.db.commit()
            frappe.clear_cache(doctype="Task")
            print("--- success---")
        else:
            print("--- unsuccessful ---")
            
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Lỗi khi chạy sync_task_status_options")
        print(f"Đã xảy ra lỗi hệ thống: {e}")
