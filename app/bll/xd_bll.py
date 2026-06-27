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
