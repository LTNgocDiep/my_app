import frappe

def attendance_has_permission(doc, ptype, user):

    if "HR Manager" in frappe.get_roles(user):
        return True
    return False

def attendance_query(user):
    if not user: user = frappe.session.user

    if "HR Manager" in frappe.get_roles(user):
        return "" 

    return "1=0"