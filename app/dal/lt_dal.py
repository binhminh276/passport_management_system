# dal/lt_dal.py
import oracledb
from dal.db_connection import get_db_connection

LT_USERNAME = "USER_LT"
LT_PASSWORD = "123"


def fetch_ho_so_da_duyet():
    """Truy van danh sach ho so da duyet thong qua view VW_PASSPORT_LT."""
    connection = None
    try:
        connection = get_db_connection(LT_USERNAME, LT_PASSWORD)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT REG_ID, NOI_DUNG_DE_NGHI, CO_QUAN_TIEP_NHAN, TRANG_THAI, THOI_GIAN_TAO
            FROM PASSPORT_APP.VW_PASSPORT_LT
            ORDER BY REG_ID
        """)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except oracledb.DatabaseError as e:
        raise Exception(f"Loi truy van danh sach ho so: {str(e)}")
    finally:
        if connection is not None:
            connection.close()


def execute_luu_tru_ho_so(reg_id):
    """Goi procedure PROC_LUU_TRU_HO_SO de cap nhat trang thai."""
    connection = None
    try:
        connection = get_db_connection(LT_USERNAME, LT_PASSWORD)
        cursor = connection.cursor()
        cursor.callproc(
            "PASSPORT_APP.PROC_LUU_TRU_HO_SO",
            [reg_id, LT_USERNAME]
        )
        connection.commit()
        cursor.close()
    except oracledb.DatabaseError as e:
        raise Exception(f"Loi khi luu tru ho so {reg_id}: {str(e)}")
    finally:
        if connection is not None:
            connection.close()