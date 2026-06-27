# dal/xd_dal.py
import oracledb
from dal.db_connection import get_db_connection

def fetch_ho_so_xet_duyet(username):
    """Truy vấn danh sách hồ sơ thuộc quyền quản lý của Xét duyệt."""
    connection = None
    try:
        connection = get_db_connection(username, "123")
        cursor = connection.cursor()
        cursor.execute("""
            SELECT REG_ID, CCCD, HO_TEN, TRANG_THAI, THOI_GIAN_TAO
            FROM PASSPORT_APP.PASSPORT_DATA
            WHERE TRANG_THAI IN ('Da xac thuc', 'Da duyet', 'Tu choi')
            ORDER BY REG_ID
        """)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except oracledb.DatabaseError as e:
        raise Exception(f"Lỗi truy vấn hồ sơ xét duyệt: {str(e)}")
    finally:
        if connection is not None:
            connection.close()

def fetch_quy_dinh(username):
    """Truy vấn danh mục quy định để đối chiếu."""
    connection = None
    try:
        connection = get_db_connection(username, "123")
        cursor = connection.cursor()
        cursor.execute("SELECT QUY_DINH_ID, NOI_DUNG FROM PASSPORT_APP.REGULATIONS ORDER BY QUY_DINH_ID")
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except oracledb.DatabaseError as e:
        raise Exception(f"Lỗi truy vấn quy định: {str(e)}")
    finally:
        if connection is not None:
            connection.close()

def execute_cap_nhat_ho_so(username, reg_id, old_status, new_status, new_mac_label):
    """Cập nhật trạng thái, dán nhãn OLS và ghi log lịch sử trong cùng 1 phiên."""
    connection = None
    try:
        connection = get_db_connection(username, "123")
        cursor = connection.cursor()
        
        # 1. Cập nhật trạng thái và nhãn OLS
        cursor.execute("""
            UPDATE PASSPORT_APP.PASSPORT_DATA 
            SET TRANG_THAI = :new_status,
                MAC_LABEL = CHAR_TO_LABEL('PASSPORT_MAC_POL', :new_mac_label)
            WHERE REG_ID = :reg_id
        """, new_status=new_status, new_mac_label=new_mac_label, reg_id=reg_id)
        
        # 2. Ghi log lịch sử
        cursor.execute("""
            INSERT INTO PASSPORT_APP.PASSPORT_REQUEST_HISTORY 
            (REG_ID, TRANG_THAI_CU, TRANG_THAI_MOI, NGUOI_CAP_NHAT) 
            VALUES (:reg_id, :old_status, :new_status, :username)
        """, reg_id=reg_id, old_status=old_status, new_status=new_status, username=username)
        
        connection.commit()
        cursor.close()
    except oracledb.DatabaseError as e:
        raise Exception(f"Lỗi khi cập nhật hồ sơ {reg_id}: {str(e)}")
    finally:
        if connection is not None:
            connection.close()
