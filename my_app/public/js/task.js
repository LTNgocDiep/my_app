frappe.ui.form.on("Task", {
    refresh(frm) {
        const is_projects_user = frappe.user.has_role("GS Projects User");
        const is_project_manager = frappe.user.has_role("GS Project Manager");

        if (is_projects_user && !is_project_manager) {
            const editable_fields = ["status", "description"];

            (frm.meta.fields || []).forEach(df => {
                if (!df.fieldname) return;

                // bỏ qua section/tab/column break
                if (
                    ["Section Break", "Column Break", "Tab Break", "HTML", "Button"].includes(df.fieldtype)
                ) {
                    return;
                }

                if (editable_fields.includes(df.fieldname)) {
                    frm.set_df_property(df.fieldname, "read_only", 0);
                } else {
                    frm.set_df_property(df.fieldname, "read_only", 1);
                }
            });

            frm.refresh_fields();
        }
    }
});