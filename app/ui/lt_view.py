# ui/lt_view.py
import streamlit as st
from bll import lt_bll


def render_lt_page():
    st.title("Màn hình lưu trữ hồ sơ hộ chiếu")
    st.caption("Danh sách hồ sơ đã xét duyệt, chờ chuyển sang trạng thái lưu trữ")

    try:
        danh_sach = lt_bll.get_danh_sach_ho_so()
    except Exception as e:
        st.error(str(e))
        return

    # Thanh thống kê tổng quan
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Tổng số hồ sơ chờ lưu trữ", len(danh_sach))
    with col_b:
        st.metric("Trạng thái áp dụng", "Đã duyệt")

    st.divider()

    if not danh_sach:
        st.info("Hiện không có hồ sơ nào cho lưu trữ.")
        return

    # Header của bảng (giả lập dạng table bằng columns)
    header = st.columns([1, 3, 3, 2, 2, 2])
    header[0].markdown("**Mã hồ sơ**")
    header[1].markdown("**Nội dung đề nghị**")
    header[2].markdown("**Cơ quan tiếp nhận**")
    header[3].markdown("**Trạng thái**")
    header[4].markdown("**Thời gian tạo**")
    header[5].markdown("**Hành động**")

    st.markdown("---")

    for ho_so in danh_sach:
        row = st.columns([1, 3, 3, 2, 2, 2])
        row[0].write(ho_so['reg_id'])
        row[1].write(ho_so['noi_dung_de_nghi'])
        row[2].write(ho_so['co_quan_tiep_nhan'])
        row[3].write(ho_so['trang_thai'])
        row[4].write(ho_so['thoi_gian_tao'].strftime("%d/%m/%Y %H:%M") if ho_so['thoi_gian_tao'] else "")

        with row[5]:
            if st.button("Lưu trữ", key=f"btn_luu_tru_{ho_so['reg_id']}", use_container_width=True):
                try:
                    lt_bll.luu_tru_ho_so(ho_so['reg_id'])
                    st.success(f"Đã lưu trữ hồ sơ {ho_so['reg_id']}")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

        st.markdown(
            "<hr style='margin:4px 0; border:none; border-top:1px solid #2b2b2b;'>",
            unsafe_allow_html=True
        )