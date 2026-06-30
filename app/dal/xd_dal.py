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
        
        # 1. GHI LOG LỊCH SỬ TRƯỚC (ĐẢO LÊN TRÊN)
        # Lúc này hồ sơ vẫn mang nhãn cũ (CONF:XD:TW) nên cán bộ vẫn nhìn thấy bản ghi cha
        cursor.execute("""
            INSERT INTO PASSPORT_APP.PASSPORT_REQUEST_HISTORY 
            (REG_ID, TRANG_THAI_CU, TRANG_THAI_MOI, NGUOI_CAP_NHAT) 
            VALUES (:reg_id, :old_status, :new_status, :username)
        """, reg_id=reg_id, old_status=old_status, new_status=new_status, username=username)

        # 2. CẬP NHẬT TRẠNG THÁI VÀ NHÃN OLS SAU (ĐƯA XUỐNG DƯỚI)
        # Chạy xong lệnh này là hồ sơ sẽ tàng hình khỏi bộ phận Xét duyệt để chuyển qua Lưu trữ
        cursor.execute("""
            UPDATE PASSPORT_APP.PASSPORT_DATA 
            SET TRANG_THAI = :new_status,
                MAC_LABEL = CHAR_TO_LABEL('PASSPORT_MAC_POL', :new_mac_label)
            WHERE REG_ID = :reg_id
        """, new_status=new_status, new_mac_label=new_mac_label, reg_id=reg_id)
        
        connection.commit()
        cursor.close()
    except oracledb.DatabaseError as e:
        raise Exception(f"Lỗi khi cập nhật hồ sơ {reg_id}: {str(e)}")
    finally:
        if connection is not None:
            connection.close()
            
def fetch_ten_tinh_quan_ly(username):
    """Lấy tên tỉnh quản lý của cán bộ bằng cách JOIN bảng APP_USERS và TINH_THANH."""
    connection = None
    try:
        connection = get_db_connection(username, "123")
        cursor = connection.cursor()
        cursor.execute("""
            SELECT t.TEN_TINH 
            FROM PASSPORT_APP.APP_USERS u
            JOIN PASSPORT_APP.TINH_THANH t ON u.MA_TINH_QUAN_LY = t.MA_TINH
            WHERE UPPER(u.USERNAME) = UPPER(:username)
        """, username=username)
        row = cursor.fetchone()
        cursor.close()
        return row[0] if row else "Không xác định"
    except oracledb.DatabaseError as e:
        raise Exception(f"Lỗi truy vấn thông tin tỉnh: {str(e)}")
    finally:
        if connection is not None:
            connection.close()

def fetch_lich_su_thao_tac(username):
    """Truy vấn lịch sử thao tác """
    connection = None
    try:
        connection = get_db_connection(username, "123")
        cursor = connection.cursor()
        cursor.execute("""
            SELECT HISTORY_ID, REG_ID, TRANG_THAI_CU, TRANG_THAI_MOI, THOI_GIAN_CAP_NHAT
            FROM PASSPORT_APP.PASSPORT_REQUEST_HISTORY
            ORDER BY THOI_GIAN_CAP_NHAT DESC
        """)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except oracledb.DatabaseError as e:
        raise Exception(f"Lỗi truy vấn lịch sử: {str(e)}")
    finally:
        if connection is not None:
            connection.close()
def fetch_chi_tiet_ho_so(username, reg_id):
    """Truy vấn toàn bộ thông tin chi tiết của 1 hồ sơ cụ thể."""
    connection = None
    try:
        connection = get_db_connection(username, "123")
        cursor = connection.cursor()
        # Lấy thêm các trường thông tin cá nhân
        cursor.execute("""
            SELECT REG_ID, CCCD, HO_TEN, NGAY_SINH, GIOI_TINH, SDT, EMAIL, THOI_GIAN_TAO, TRANG_THAI,
                   NOI_DUNG_DE_NGHI, ANH_CHAN_DUNG_PATH, HO_SO_DINH_KEM_PATH
            FROM PASSPORT_APP.PASSPORT_DATA
            WHERE REG_ID = :reg_id
        """, reg_id=reg_id)
        row = cursor.fetchone()
        cursor.close()
        return row
    except oracledb.DatabaseError as e:
        raise Exception(f"Lỗi truy vấn chi tiết hồ sơ: {str(e)}")
    finally:
        if connection is not None:
            connection.close()
