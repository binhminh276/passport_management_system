# bll/xd_bll.py
from dal import xd_dal

def get_danh_sach_ho_so(username):
    """Lấy danh sách hồ sơ Xét duyệt, định dạng lại cho UI."""
    rows = xd_dal.fetch_ho_so_xet_duyet(username)
    ket_qua = []
    for row in rows:
        reg_id, cccd, ho_ten, trang_thai, thoi_gian_tao = row
        ket_qua.append({
            "reg_id": reg_id,
            "cccd": cccd,
            "ho_ten": ho_ten,
            "trang_thai": trang_thai,
            "thoi_gian_tao": thoi_gian_tao
        })
    return ket_qua

def get_danh_sach_quy_dinh(username):
    """Lấy danh sách quy định pháp lý."""
    rows = xd_dal.fetch_quy_dinh(username)
    ket_qua = []
    for row in rows:
        quy_dinh_id, noi_dung = row
        ket_qua.append({
            "quy_dinh_id": quy_dinh_id,
            "noi_dung": noi_dung
        })
    return ket_qua

def xu_ly_ho_so(username, reg_id, old_status, action_type):
    """Xác định nhãn OLS và trạng thái mới dựa trên hành động."""
    if reg_id is None:
        raise ValueError("Thiếu mã hồ sơ (reg_id)")
        
    if action_type == "Duyệt":
        new_status = "Da duyet"
        new_mac_label = "CONF:XD:TW"
    elif action_type == "Từ chối":
        new_status = "Tu choi"
        new_mac_label = "CONF:XD:TW"
    elif action_type == "Lưu trữ":
        new_status = "Da luu tru"
        new_mac_label = "PUB:LT:TW"
    else:
        raise ValueError("Hành động không hợp lệ")

    xd_dal.execute_cap_nhat_ho_so(username, reg_id, old_status, new_status, new_mac_label)

def get_ten_tinh_quan_ly(username):
    """Gọi DAL lấy tên tỉnh quản lý."""
    return xd_dal.fetch_ten_tinh_quan_ly(username)

def get_lich_su_thao_tac(username):
    """Gọi DAL lấy lịch sử và định dạng lại cấu trúc dữ liệu."""
    rows = xd_dal.fetch_lich_su_thao_tac(username)
    ket_qua = []
    for row in rows:
        history_id, reg_id, trang_thai_cu, trang_thai_moi, thoi_gian_cap_nhat = row
        ket_qua.append({
            "history_id": history_id,
            "reg_id": reg_id,
            "trang_thai_cu": trang_thai_cu if trang_thai_cu else "N/A",
            "trang_thai_moi": trang_thai_moi,
            "thoi_gian_cap_nhat": thoi_gian_cap_nhat
        })
    return ket_qua

def get_chi_tiet_ho_so(username, reg_id):
    """Gọi DAL lấy chi tiết hồ sơ và định dạng lại."""
    row = xd_dal.fetch_chi_tiet_ho_so(username, reg_id)
    if not row:
        return None
        
    return {
        "reg_id": row[0],
        "cccd": row[1],
        "ho_ten": row[2] if row[2] else "Chưa cập nhật",
        "ngay_sinh": row[3].strftime("%d/%m/%Y") if row[3] else "N/A",
        "gioi_tinh": row[4] if row[4] else "N/A",
        "sdt": row[5] if row[5] else "N/A",
        "email": row[6] if row[6] else "N/A",
        "thoi_gian_tao": row[7].strftime("%d/%m/%Y %H:%M") if row[7] else "N/A",
        "trang_thai": row[8],
        # Thêm 3 trường mới
        "loai_yeu_cau": row[9] if len(row) > 9 and row[9] else "Không xác định",
        "anh_chan_dung": row[10] if len(row) > 10 and row[10] else None,
        "giay_to_dinh_kem": row[11] if len(row) > 11 and row[11] else None
    }
