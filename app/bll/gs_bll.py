from dal import gs_dal

def get_danh_sach_log(db_user, db_pass):
    rows = gs_dal.fetch_audit_logs(db_user, db_pass)
    for row in rows:
        if row.get('EVENT_TIMESTAMP'):
            row['EVENT_TIMESTAMP'] = row['EVENT_TIMESTAMP'].strftime("%d/%m/%Y %H:%M:%S")
    return rows