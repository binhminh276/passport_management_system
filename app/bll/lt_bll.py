# bll/lt_bll.py
from dal import lt_dal


def get_danh_sach_ho_so():
    """
    Lay danh sach ho so da duyet, dinh dang lai cho de hien thi tren UI.
    Tra ve list cac dict thay vi tuple tho.
    """
    rows = lt_dal.fetch_ho_so_da_duyet()
    ket_qua = []
    for row in rows:
        reg_id, noi_dung_de_nghi, co_quan_tiep_nhan, trang_thai, thoi_gian_tao = row
        ket_qua.append({
            "reg_id": reg_id,
            "noi_dung_de_nghi": noi_dung_de_nghi,
            "co_quan_tiep_nhan": co_quan_tiep_nhan,
            "trang_thai": trang_thai,
            "thoi_gian_tao": thoi_gian_tao
        })
    return ket_qua


def luu_tru_ho_so(reg_id):
    """
    Kiem tra dau vao truoc khi goi DAL.
    """
    if reg_id is None:
        raise ValueError("Thieu ma ho so (reg_id)")
    lt_dal.execute_luu_tru_ho_so(reg_id)