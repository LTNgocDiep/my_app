import frappe

def patch_monthly_attendance_sheet():
    from hrms.hr.report.monthly_attendance_sheet import monthly_attendance_sheet as original_report

    # # tránh patch nhiều lần
    # if getattr(original_report, "_my_app_patched", False):
    #     return

    original_execute = original_report.execute

    def custom_execute(filters=None):
        result = original_execute(filters)

        # thường report trả về:
        # (columns, data)
        # hoặc (columns, data, message, chart, report_summary, skip_total_rows)
        if not result:
            return result

        columns = result[0]
        data = result[1] if len(result) > 1 else []

        filtered_columns = []
        removed_indexes = []

        for idx, col in enumerate(columns):
            fieldname = None
            label = None

            if isinstance(col, dict):
                fieldname = col.get("fieldname")
                label = col.get("label")
            elif isinstance(col, str):
                # dạng string kiểu "Label:Type:Width"
                label = col.split(":")[0].strip()

            if fieldname == "unmarked_days" or str(label).strip() == "Unmarked Days":
                removed_indexes.append(idx)
                continue

            filtered_columns.append(col)

        filtered_data = []

        for row in data or []:
            if isinstance(row, dict):
                row.pop("unmarked_days", None)
                filtered_data.append(row)
            elif isinstance(row, (list, tuple)):
                new_row = [v for i, v in enumerate(row) if i not in removed_indexes]
                filtered_data.append(new_row)
            else:
                filtered_data.append(row)

        result = list(result)
        result[0] = filtered_columns
        result[1] = filtered_data

        return tuple(result)

    original_report.execute = custom_execute
    # original_report._my_app_patched = True