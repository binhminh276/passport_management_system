from dal.db_connection import get_db_connection


class XtDal:
    def __init__(self, db_user, db_pass):
        self.db_user = db_user
        self.db_pass = db_pass

    def get_pending_requests(self):
        connection = None
        try:
            connection = get_db_connection(self.db_user, self.db_pass)
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT REG_ID, CCCD, HO_TEN, NGAY_SINH, GIOI_TINH,
                       THOI_GIAN_TAO, TRANG_THAI
                FROM PASSPORT_APP.PASSPORT_DATA
                WHERE TRANG_THAI = :1
                ORDER BY THOI_GIAN_TAO ASC, REG_ID ASC
                """,
                ["Da nop"],
            )
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        finally:
            if connection:
                connection.close()

    def get_request_details(self, reg_id):
        connection = None
        try:
            connection = get_db_connection(self.db_user, self.db_pass)
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT REG_ID, CCCD, HO_TEN, GIOI_TINH, NGAY_SINH,
                       SDT, EMAIL, NOI_DUNG_DE_NGHI, CO_QUAN_TIEP_NHAN,
                       ANH_CHAN_DUNG_PATH, TRANG_THAI, THOI_GIAN_TAO
                FROM PASSPORT_APP.PASSPORT_DATA
                WHERE REG_ID = :1
                """,
                [reg_id],
            )
            columns = [col[0] for col in cursor.description]
            row = cursor.fetchone()
            if row:
                return dict(zip(columns, row))
            return None
        finally:
            if connection:
                connection.close()

    def get_resident_data(self, cccd):
        connection = None
        try:
            connection = get_db_connection(self.db_user, self.db_pass)
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT CCCD, HO_TEN, NGAY_SINH, GIOI_TINH, DIA_CHI_THUONG_TRU
                FROM PASSPORT_APP.RESIDENT_DATA
                WHERE CCCD = :1
                """,
                [cccd],
            )
            columns = [col[0] for col in cursor.description]
            row = cursor.fetchone()
            if row:
                return dict(zip(columns, row))
            return None
        finally:
            if connection:
                connection.close()

    def mark_verified(self, reg_id):
        connection = None
        try:
            connection = get_db_connection(self.db_user, self.db_pass)
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT TRANG_THAI
                FROM PASSPORT_APP.PASSPORT_DATA
                WHERE REG_ID = :1
                FOR UPDATE
                """,
                [reg_id],
            )
            row = cursor.fetchone()
            if not row:
                raise ValueError("Không tìm thấy hồ sơ")

            old_status = row[0]
            if old_status != "Da nop":
                raise ValueError("Hồ sơ không ở trạng thái chờ xác thực")

            cursor.execute(
                """
                UPDATE PASSPORT_APP.PASSPORT_DATA
                SET TRANG_THAI = :1,
                    MAC_LABEL = CHAR_TO_LABEL('PASSPORT_MAC_POL', :2)
                WHERE REG_ID = :3
                """,
                ["Da xac thuc", "CONF:XD:TW", reg_id],
            )
            cursor.execute(
                """
                INSERT INTO PASSPORT_APP.PASSPORT_REQUEST_HISTORY (
                    REG_ID, TRANG_THAI_CU, TRANG_THAI_MOI, NGUOI_CAP_NHAT
                )
                VALUES (:1, :2, :3, USER)
                """,
                [reg_id, old_status, "Da xac thuc"],
            )
            connection.commit()
            return True
        except Exception:
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                connection.close()
