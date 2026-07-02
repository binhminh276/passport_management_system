import oracledb
from dal.db_connection import get_db_connection


def fetch_danh_sach_ho_so(db_user, db_pass):
    connection = None
    try:
        connection = get_db_connection(db_user, db_pass)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT REG_ID, NOI_DUNG_DE_NGHI, CO_QUAN_TIEP_NHAN, MA_TINH_THUONG_TRU, TRANG_THAI, THOI_GIAN_TAO
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


def tra_cuu_ho_so(reg_id, db_user, db_pass):
    connection = None
    try:
        connection = get_db_connection(db_user, db_pass)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT REG_ID, NOI_DUNG_DE_NGHI, CO_QUAN_TIEP_NHAN, MA_TINH_THUONG_TRU, TRANG_THAI, THOI_GIAN_TAO
            FROM PASSPORT_APP.VW_PASSPORT_LT
            WHERE REG_ID = :reg_id
        """, reg_id=reg_id)
        row = cursor.fetchone()
        cursor.close()
        return row
    except oracledb.DatabaseError as e:
        raise Exception(f"Loi tra cuu ho so {reg_id}: {str(e)}")
    finally:
        if connection is not None:
            connection.close()


def hoan_tat_luu_tru(reg_id, nguoi_cap_nhat, db_user, db_pass):
    connection = None
    try:
        connection = get_db_connection(db_user, db_pass)
        cursor = connection.cursor()
        cursor.callproc("PASSPORT_APP.PROC_HOAN_TAT_LUU_TRU", [reg_id, nguoi_cap_nhat])
        connection.commit()
        cursor.close()
    except oracledb.DatabaseError as e:
        if connection is not None:
            connection.rollback()
        raise Exception(f"Loi khi hoan tat luu tru ho so {reg_id}: {str(e)}")
    finally:
        if connection is not None:
            connection.close()