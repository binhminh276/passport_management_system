from dal import lt_dal

def get_danh_sach_ho_so(db_user, db_password):
    rows = lt_dal.fetch_danh_sach_ho_so(db_user, db_password)
    return [{
        "reg_id": r[0],
        "noi_dung_de_nghi": r[1],
        "co_quan_tiep_nhan": r[2],
        "ma_tinh_thuong_tru": r[3],
        "trang_thai": r[4],
        "thoi_gian_tao": r[5]
    } for r in rows]


def tra_cuu_ho_so(reg_id, db_user, db_password):
    if reg_id is None or reg_id <= 0:
        raise ValueError("Ma ho so khong hop le")
    row = lt_dal.tra_cuu_ho_so(reg_id, db_user, db_password)
    if row is None:
        return None
    return {
        "reg_id": row[0],
        "noi_dung_de_nghi": row[1],
        "co_quan_tiep_nhan": row[2],
        "ma_tinh_thuong_tru": row[3],
        "trang_thai": row[4],
        "thoi_gian_tao": row[5]
    }


def hoan_tat_luu_tru(reg_id, nguoi_dung_hien_tai, db_user, db_password):
    if reg_id is None:
        raise ValueError("Thieu ma ho so")
    lt_dal.hoan_tat_luu_tru(reg_id, nguoi_dung_hien_tai, db_user, db_password)