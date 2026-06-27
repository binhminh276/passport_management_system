import re

from dal.db_connection import get_db_connection


class UserDal:
    def __init__(self):
        self.guest_db_user = "APP_GUEST"
        self.db_pass = "123"

    def verify_login(self, username, password_hash):
        connection = None
        try:
            connection = get_db_connection(self.guest_db_user, self.db_pass)
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT DB_ROLE
                FROM PASSPORT_APP.APP_USERS
                WHERE UPPER(USERNAME) = UPPER(:1)
                  AND LOWER(PASSWORD_HASH) = LOWER(:2)
                  AND IS_ACTIVE = 1
                """,
                [username, password_hash],
            )
            row = cursor.fetchone()
            if not row:
                return None
            return row[0]
        finally:
            if connection:
                connection.close()

    def create_account(self, username, raw_password, password_hash, db_role):
        connection = None
        try:
            connection = get_db_connection(self.guest_db_user, self.db_pass)
            cursor = connection.cursor()
            cursor.callproc(
                "SEC_MGR.PROC_TAO_TAI_KHOAN",
                [username, raw_password, password_hash, db_role],
            )
            connection.commit()
            return True
        finally:
            if connection:
                connection.close()

    def register_passport(
        self,
        db_user,
        db_password,
        cccd,
        ho_ten,
        gioi_tinh,
        ngay_sinh,
        sdt,
        email,
        noi_dung_de_nghi,
        co_quan_tiep_nhan,
        anh_chan_dung_path,
    ):
        connection = None
        try:
            connection = self._get_user_connection(db_user, db_password)
            cursor = connection.cursor()
            cursor.callproc(
                "PASSPORT_APP.PROC_TAO_HO_SO",
                [
                    cccd,
                    ho_ten,
                    gioi_tinh,
                    ngay_sinh,
                    sdt,
                    email,
                    noi_dung_de_nghi,
                    co_quan_tiep_nhan,
                    anh_chan_dung_path,
                ],
            )
            connection.commit()
            return True
        finally:
            if connection:
                connection.close()

    def _get_user_connection(self, db_user, db_password):
        try:
            return get_db_connection(db_user, db_password)
        except Exception as original_exception:
            clean_user = str(db_user or "").strip()
            if re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{2,29}", clean_user):
                try:
                    return get_db_connection(f'"{clean_user}"', db_password)
                except Exception:
                    pass
            raise original_exception
