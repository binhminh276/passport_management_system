import datetime
import hashlib
import re

from dal.user_dal import UserDal


class AuthBll:
    def __init__(self):
        self.user_dal = UserDal()
        self.default_password = "123"

    def hash_password(self, plain_text):
        return hashlib.sha256(plain_text.encode("utf-8")).hexdigest()

    def authenticate(self, username, password):
        clean_username = str(username or "").strip()
        password_hash = self.hash_password(password)
        db_role = self.user_dal.verify_login(clean_username, password_hash)

        role_pages = {
            "ROLE_CD": "register",
            "ROLE_XT": "xt_dashboard",
            "ROLE_XD": "xd_dashboard",
            "ROLE_LT": "lt_dashboard",
            "ROLE_GS": "admin_users",
        }
        if db_role in role_pages:
            return db_role, role_pages[db_role]
        return None

    def validate_registration(self, data):
        cccd = str(data.get("cccd") or "").strip()
        ho_ten = str(data.get("ho_ten") or "").strip()
        gioi_tinh = self.normalize_gender(data.get("gioi_tinh"))
        ngay_sinh = data.get("ngay_sinh")
        sdt = str(data.get("sdt") or "").strip()
        email = str(data.get("email") or "").strip()
        noi_dung = str(data.get("noi_dung_de_nghi") or "").strip()
        co_quan = str(data.get("co_quan_tiep_nhan") or "").strip()

        if len(cccd) != 12 or not cccd.isdigit():
            return False, "CCCD phải gồm đúng 12 chữ số"
        if not ho_ten:
            return False, "Họ tên không được để trống"
        if gioi_tinh not in {"Nam", "Nu"}:
            return False, "Giới tính chỉ nhận Nam hoặc Nu"
        if not isinstance(ngay_sinh, datetime.date):
            return False, "Ngày sinh phải có định dạng YYYY-MM-DD"
        if ngay_sinh > datetime.date.today():
            return False, "Ngày sinh không được lớn hơn ngày hiện tại"
        if len(sdt) < 10 or len(sdt) > 15 or not sdt.isdigit():
            return False, "Số điện thoại phải gồm 10 đến 15 chữ số"
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            return False, "Email không hợp lệ"
        if not noi_dung:
            return False, "Nội dung đề nghị không được để trống"
        if not co_quan:
            return False, "Cơ quan tiếp nhận không được để trống"
        return True, ""

    def register(self, data):
        data = self._normalize_registration_data(data)
        is_valid, message = self.validate_registration(data)
        if not is_valid:
            return False, message

        username = self.build_citizen_username(data["cccd"])
        raw_password = self.default_password
        password_hash = self.hash_password(raw_password)

        try:
            self.user_dal.create_account(username, raw_password, password_hash, "ROLE_CD")
            self.user_dal.register_passport(
                username,
                raw_password,
                data["cccd"],
                data["ho_ten"],
                data["gioi_tinh"],
                data["ngay_sinh"],
                data["sdt"],
                data["email"],
                data["noi_dung_de_nghi"],
                data["co_quan_tiep_nhan"],
                data["anh_chan_dung_path"],
            )
            return True, f"Gửi hồ sơ thành công. Tài khoản công dân: {username}, mật khẩu: {raw_password}"
        except Exception as exc:
            return False, str(exc)

    def submit_passport(self, data, db_user, db_password):
        data = self._normalize_registration_data(data)
        is_valid, message = self.validate_registration(data)
        if not is_valid:
            return False, message

        try:
            self.user_dal.register_passport(
                db_user,
                db_password,
                data["cccd"],
                data["ho_ten"],
                data["gioi_tinh"],
                data["ngay_sinh"],
                data["sdt"],
                data["email"],
                data["noi_dung_de_nghi"],
                data["co_quan_tiep_nhan"],
                data["anh_chan_dung_path"],
            )
            return True, "Gửi hồ sơ thành công"
        except Exception as exc:
            return False, str(exc)

    def create_employee_account(self, username, db_role):
        input_username = str(username or "").strip()
        clean_username = input_username.upper()
        clean_role = str(db_role or "").strip().upper()
        allowed_roles = {"ROLE_XT", "ROLE_XD", "ROLE_LT", "ROLE_GS"}

        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{2,29}", input_username):
            return False, "Tên đăng nhập phải bắt đầu bằng chữ và chỉ gồm chữ, số, dấu gạch dưới"
        if clean_role not in allowed_roles:
            return False, "Vai trò nhân viên không hợp lệ"

        raw_password = self.default_password
        password_hash = self.hash_password(raw_password)

        try:
            self.user_dal.create_account(clean_username, raw_password, password_hash, clean_role)
            return True, f"Tạo tài khoản thành công. Mật khẩu mặc định: {raw_password}"
        except Exception as exc:
            return False, str(exc)

    def build_citizen_username(self, cccd):
        return f"cd_{cccd}"

    def parse_date(self, value):
        try:
            return datetime.datetime.strptime(str(value).strip(), "%Y-%m-%d").date()
        except ValueError:
            return None

    def normalize_gender(self, value):
        normalized = str(value or "").strip().upper()
        if normalized in {"NAM", "MALE"}:
            return "Nam"
        if normalized in {"NU", "NỮ", "FEMALE"}:
            return "Nu"
        return str(value or "").strip()

    def _normalize_registration_data(self, data):
        return {
            **data,
            "cccd": str(data.get("cccd") or "").strip(),
            "ho_ten": str(data.get("ho_ten") or "").strip(),
            "gioi_tinh": self.normalize_gender(data.get("gioi_tinh")),
            "sdt": str(data.get("sdt") or "").strip(),
            "email": str(data.get("email") or "").strip(),
            "noi_dung_de_nghi": str(data.get("noi_dung_de_nghi") or "").strip(),
            "co_quan_tiep_nhan": str(data.get("co_quan_tiep_nhan") or "").strip(),
            "anh_chan_dung_path": str(data.get("anh_chan_dung_path") or "").strip() or None,
        }


class AuthPresenter:
    def __init__(self):
        self.auth_bll = AuthBll()

    def authenticate(self, username, password):
        return self.auth_bll.authenticate(username, password)

    def register(self, data):
        return self.auth_bll.register(data)

    def submit_passport(self, data, db_user, db_password):
        return self.auth_bll.submit_passport(data, db_user, db_password)

    def create_employee_account(self, username, db_role):
        return self.auth_bll.create_employee_account(username, db_role)

    def parse_date(self, value):
        return self.auth_bll.parse_date(value)
