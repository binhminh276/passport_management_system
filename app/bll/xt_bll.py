import datetime

from dal.xt_dal import XtDal


class XtBll:
    def __init__(self, db_user, db_pass):
        self.xt_dal = XtDal(db_user, db_pass)

    def get_pending_list(self):
        return self.xt_dal.get_pending_requests()

    def get_detail(self, reg_id):
        return self.xt_dal.get_request_details(reg_id)

    def verify_resident_data(self, reg_id):
        ho_so = self.xt_dal.get_request_details(reg_id)
        if not ho_so:
            return False, "Không tìm thấy hồ sơ"
        if ho_so.get("TRANG_THAI") != "Da nop":
            return False, "Hồ sơ không ở trạng thái chờ xác thực"

        dan_cu = self.xt_dal.get_resident_data(ho_so.get("CCCD"))
        if not dan_cu:
            return False, "Không tìm thấy dữ liệu trong CSDL dân cư"

        sai_khac = []
        if self._normalize_text(ho_so.get("HO_TEN")) != self._normalize_text(dan_cu.get("HO_TEN")):
            sai_khac.append("họ tên")
        if self._normalize_date(ho_so.get("NGAY_SINH")) != self._normalize_date(dan_cu.get("NGAY_SINH")):
            sai_khac.append("ngày sinh")
        if self._normalize_gender(ho_so.get("GIOI_TINH")) != self._normalize_gender(dan_cu.get("GIOI_TINH")):
            sai_khac.append("giới tính")

        if sai_khac:
            return False, {
                "message": "Không khớp " + ", ".join(sai_khac),
                "resident_data": dan_cu,
            }
        return True, dan_cu

    def mark_verified(self, reg_id):
        is_match, result_data = self.verify_resident_data(reg_id)
        if not is_match:
            if isinstance(result_data, dict):
                return False, result_data.get("message", "Dữ liệu không khớp")
            return False, result_data
        self.xt_dal.mark_verified(reg_id)
        return True, "Đã chuyển hồ sơ sang trạng thái Da xac thuc"

    def _normalize_text(self, value):
        return " ".join(str(value or "").strip().upper().split())

    def _normalize_date(self, value):
        if isinstance(value, datetime.datetime):
            return value.date()
        if isinstance(value, datetime.date):
            return value
        return value

    def _normalize_gender(self, value):
        normalized = self._normalize_text(value)
        if normalized == "NAM":
            return "NAM"
        if normalized in {"NU", "NỮ"}:
            return "NU"
        return normalized
