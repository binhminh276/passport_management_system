import pandas as pd
import streamlit as st
from bll import lt_bll


def render_lt_page():
    st.title("Lưu trữ hồ sơ hộ chiếu")

    db_user = st.session_state.get("db_username")
    db_pass = st.session_state.get("db_password")
    current_username = st.session_state.get("username", "Unknown")

    if not db_user or not db_pass:
        st.error(
            "Không tìm thấy thông tin phiên đăng nhập hệ thống. Vui lòng đăng nhập lại."
        )
        return

    st.subheader("Tra cứu nhanh theo mã hồ sơ")
    ma_ho_so_input = st.text_input("Nhập mã hồ sơ (REG_ID)", key="search_input")

    if st.button("Tra cứu", key="btn_search"):
        try:
            reg_id = int(ma_ho_so_input)
            ket_qua = lt_bll.tra_cuu_ho_so(reg_id, db_user, db_pass)
            if ket_qua is None:
                st.warning("Không tìm thấy hồ sơ này trong phạm vi được xem.")
            else:
                df_single = pd.DataFrame(
                    {
                        "Thông tin": [
                            "Mã hồ sơ",
                            "Trạng thái",
                            "Nội dung đề nghị",
                            "Cơ quan tiếp nhận",
                            "Mã tỉnh thường trú",
                            "Thời gian tạo",
                        ],
                        "Giá trị": [
                            ket_qua["reg_id"],
                            ket_qua["trang_thai"],
                            ket_qua["noi_dung_de_nghi"],
                            ket_qua["co_quan_tiep_nhan"],
                            ket_qua["ma_tinh_thuong_tru"],
                            ket_qua["thoi_gian_tao"],
                        ],
                    }
                )
                st.table(df_single)
        except ValueError:
            st.error("Mã hồ sơ phải là số nguyên")

    st.divider()

    try:
        danh_sach = lt_bll.get_danh_sach_ho_so(db_user, db_pass)
    except Exception as e:
        st.error(f"Lỗi hệ thống: {str(e)}")
        return

    if not danh_sach:
        st.info("Hiện không có hồ sơ nào thuộc tỉnh bạn quản lý.")
        return

    cho_xu_ly = [h for h in danh_sach if h["trang_thai"] == "Da luu tru"]
    da_hoan_thanh = [h for h in danh_sach if h["trang_thai"] == "Da hoan thanh"]

    ITEMS_PER_PAGE = 5

    st.subheader(f"Hồ sơ chờ hoàn tất lưu trữ ({len(cho_xu_ly)})")

    if not cho_xu_ly:
        st.write("Không có hồ sơ nào cần xử lý.")
    else:
        df_cho_xu_ly = pd.DataFrame(cho_xu_ly)
        df_cho_xu_ly.columns = [
            "Mã hồ sơ",
            "Nội dung đề nghị",
            "Cơ quan tiếp nhận",
            "Mã tỉnh",
            "Trạng thái",
            "Thời gian tạo",
        ]

        st.dataframe(df_cho_xu_ly, use_container_width=True, hide_index=True)

        selected_reg_id = st.selectbox(
            "Chọn Mã hồ sơ để tiến hành hoàn tất lưu trữ:",
            options=[h["reg_id"] for h in cho_xu_ly],
            format_func=lambda x: f"Hồ sơ số: {x}",
        )

        if st.button(
            f"Xác nhận hoàn tất lưu trữ hồ sơ {selected_reg_id}",
            type="primary",
        ):
            try:
                lt_bll.hoan_tat_luu_tru(
                    selected_reg_id, current_username, db_user, db_pass
                )
                st.success(f"Đã hoàn tất lưu trữ hồ sơ {selected_reg_id}")
                st.rerun()
            except Exception as e:
                st.error(str(e))

    st.divider()

    st.subheader(f"Hồ sơ đã hoàn thành ({len(da_hoan_thanh)})")

    if not da_hoan_thanh:
        st.write("Chua có hồ sơ nào hoàn thành.")
    else:
        if "lt_page_num" not in st.session_state:
            st.session_state.lt_page_num = 1

        total_items = len(da_hoan_thanh)
        total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

        if st.session_state.lt_page_num > total_pages:
            st.session_state.lt_page_num = total_pages

        start_idx = (st.session_state.lt_page_num - 1) * ITEMS_PER_PAGE
        end_idx = start_idx + ITEMS_PER_PAGE
        page_data = da_hoan_thanh[start_idx:end_idx]

        df_da_hoan_thanh = pd.DataFrame(page_data)
        df_da_hoan_thanh.columns = [
            "Mã hồ sơ",
            "Nội dung đề nghị",
            "Cơ quan tiếp nhận",
            "Mã tỉnh",
            "Trạng thái",
            "Thời gian tạo",
        ]

        st.dataframe(
            df_da_hoan_thanh, use_container_width=True, hide_index=True
        )

        col_prev, col_info, col_next = st.columns([1, 2, 1])

        with col_prev:
            if st.button(
                "Trang trước",
                disabled=(st.session_state.lt_page_num == 1),
                use_container_width=True,
            ):
                st.session_state.lt_page_num -= 1
                st.rerun()

        with col_info:
            st.markdown(
                f"<div style='text-align: center; line-height: 38px; font-weight: bold;'>"
                f"Trang {st.session_state.lt_page_num} / {total_pages}"
                f"</div>",
                unsafe_allow_html=True,
            )

        with col_next:
            if st.button(
                "Trang sau",
                disabled=(st.session_state.lt_page_num == total_pages),
                use_container_width=True,
            ):
                st.session_state.lt_page_num += 1
                st.rerun()