import oracledb
from dal.db_connection import get_db_connection

def fetch_audit_logs(db_user, db_pass):
    connection = None
    try:
        connection = get_db_connection(db_user, db_pass)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT EVENT_TIMESTAMP, DBUSERNAME, ACTION_NAME, OBJECT_SCHEMA, OBJECT_NAME, SQL_TEXT
            FROM SEC_MGR.VW_AUDIT_GS
            ORDER BY EVENT_TIMESTAMP DESC
        """)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        
        ket_qua = []
        for row in rows:
            row_dict = dict(zip(columns, row))
            if row_dict.get('SQL_TEXT') is not None:
                row_dict['SQL_TEXT'] = str(row_dict['SQL_TEXT'])
            ket_qua.append(row_dict)
            
        cursor.close()
        return ket_qua
    except oracledb.DatabaseError as e:
        raise Exception(f"Lỗi truy vấn log giám sát: {str(e)}")
    finally:
        if connection is not None:
            connection.close()