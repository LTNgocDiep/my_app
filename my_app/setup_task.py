import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def update_task_fields():

    frappe.db.delete("Property Setter", {
        "doc_type": "Task",
        "field_name": "color",
        "property": "hidden"
    })

    make_property_setter(
        doctype="Task",
        fieldname="color",
        property="permlevel",
        value=1,
        property_type="Int"
    )

    if not frappe.db.exists("Custom DocPerm", {"parent": "Task", "role": "GS Project Manager", "permlevel": 1}):
        frappe.get_doc({
            "doctype": "Custom DocPerm",
            "parent": "Task",
            "parenttype": "DocType",
            "parentfield": "permissions",
            "role": "GS Project Manager",
            "permlevel": 1,
            "read": 1,
            "write": 1
        }).insert()

    fieldname_to_remove = "custom_test" 
    
    if frappe.db.exists("Custom Field", {"dt": "Task", "fieldname": fieldname_to_remove}):
        frappe.get_doc("Custom Field", {"dt": "Task", "fieldname": fieldname_to_remove}).delete()
        print(f"Deleted! ")

    frappe.db.commit()