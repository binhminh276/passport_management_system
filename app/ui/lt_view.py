import pandas as pd
import streamlit as st
from bll import lt_bll


def render_lt_page():
    st.markdown(
        """
        <style>
        div[data-testid="stAppDeployButton"],
        span[data-testid="stMainMenu"],
        header[data-testid="stHeader"] button:not([data-testid="stExpandSidebarButton"]) {
            display: none !important;
        }

        .block-container {
            width: 100%;
            max-width: 1120px;
            padding: clamp(1.75rem, 5vh, 3.5rem) clamp(1rem, 3vw, 3rem) 2rem;
        }

        .lt-page-title {
            margin: 0 0 20px;
            color: #2f323a;
            font-size: clamp(28px, 2.4vw, 38px);
            font-weight: 700;
            line-height: 1.2;
        }

        .lt-section-title {
            margin: 22px 0 12px;
            color: #2f323a;
            font-size: clamp(22px, 1.8vw, 28px);
            font-weight: 700;
            line-height: 1.25;
        }

        section[data-testid="stMain"] div[data-testid="stTable"],
        section[data-testid="stMain"] div[data-testid="stDataFrame"] {
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            background: #ffffff;
            overflow: hidden;
        }

        section[data-testid="stMain"] div[data-testid="stTextInput"] label {
            color: #333842;
            font-size: 15px;
            font-weight: 600;
        }

        section[data-testid="stMain"] div[data-testid="stTextInputRootElement"] {
            min-height: 44px;
            border: 1px solid #d8dfe8 !important;
            border-radius: 6px !important;
            background: #ffffff !important;
            box-shadow: none !important;
        }

        section[data-testid="stMain"] div[data-testid="stButton"] button {
            min-width: 180px;
            height: 42px;
            border: 0;
            border-radius: 6px;
            background: #3157b7 !important;
            color: #ffffff !important;
            font-size: 15px;
            font-weight: 700;
        }

        section[data-testid="stMain"] div[data-testid="stButton"] button:hover {
            background: #294ba2 !important;
            color: #ffffff !important;
        }

        @media (max-width: 900px) {
            .lt-page-title { font-size: clamp(24px, 5vw, 30px); }
            .lt-section-title { font-size: clamp(20px, 4vw, 24px); }

            section[data-testid="stMain"] div[data-testid="stButton"],
            section[data-testid="stMain"] div[data-testid="stButton"] button {
                width: 100% !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="lt-page-title">Bảng điều khiển - Bộ phận Lưu trữ</div>', unsafe_allow_html=True)

    db_user = st.session_state.get("db_username")
    db_pass = st.session_state.get("db_password")
    current_username = st.session_state.get("username", "Unknown")

    if not db_user or not db_pass:
        st.markdown("**Phiên đăng nhập không hợp lệ. Vui lòng đăng nhập lại.**")
        return

    # ---------------------------------------------------------------
    # Tra cuu nhanh
    # ---------------------------------------------------------------
    st.markdown('<div class="lt-section-title">Tra cứu nhanh theo mã hồ sơ</div>', unsafe_allow_html=True)

    ma_ho_so_input = st.text_input("Nhập mã hồ so", key="search_input")
    if st.button("Tra cứu", key="btn_search"):
        try:
            reg_id = int(ma_ho_so_input)
            ket_qua = lt_bll.tra_cuu_ho_so(reg_id, db_user, db_pass)
            if ket_qua is None:
                st.markdown("**Không tìm thấy hồ sơ này.**")
            else:
                df_single = pd.DataFrame({
                    "Thong tin": [
                        "Ma ho so", "Trang thai", "Noi dung de nghi",
                        "Co quan tiep nhan", "Ma tinh thuong tru", "Thoi gian tao",
                    ],
                    "Gia tri": [
                        ket_qua["reg_id"], ket_qua["trang_thai"],
                        ket_qua["noi_dung_de_nghi"], ket_qua["co_quan_tiep_nhan"],
                        ket_qua["ma_tinh_thuong_tru"], ket_qua["thoi_gian_tao"],
                    ],
                })
                st.table(df_single)
        except ValueError:
            st.markdown("**Mã hồ sơ phải là số nguyên.**")

    st.divider()

    # ---------------------------------------------------------------
    # Tai danh sach
    # ---------------------------------------------------------------
    try:
        danh_sach = lt_bll.get_danh_sach_ho_so(db_user, db_pass)
    except Exception as e:
        st.markdown(f"**Lỗi hệ thống: {str(e)}**")
        return

    if not danh_sach:
        st.markdown("**Hiện không có hồ sơ thuộc tỉnh quản lý.**")
        return

    cho_xu_ly = [h for h in danh_sach if h["trang_thai"] == "Da luu tru"]
    da_hoan_thanh = [h for h in danh_sach if h["trang_thai"] == "Da hoan thanh"]

    ITEMS_PER_PAGE = 5

    # ---------------------------------------------------------------
    # Ho so cho hoan tat
    # ---------------------------------------------------------------
    st.markdown(f'<div class="lt-section-title">Hồ sơ hoàn tất chờ lưu trữ({len(cho_xu_ly)})</div>', unsafe_allow_html=True)

    if not cho_xu_ly:
        st.markdown("**Không có hồ sơ nào cần xử lý.**")
    else:
        df_cho_xu_ly = pd.DataFrame(cho_xu_ly)
        df_cho_xu_ly.columns = [
            "Ma ho so", "Noi dung de nghi", "Co quan tiep nhan",
            "Ma tinh", "Trang thai", "Thoi gian tao",
        ]
        st.dataframe(df_cho_xu_ly, use_container_width=True, hide_index=True)

        selected_reg_id = st.selectbox(
            "Chọn mã hồ sơ để hoàn tất lưu trữ:",
            options=[h["reg_id"] for h in cho_xu_ly],
            format_func=lambda x: f"Hồ sơ số: {x}",
        )

        if st.button(f"Xác nhận hoàn tất lưu {selected_reg_id}", type="primary"):
            try:
                lt_bll.hoan_tat_luu_tru(selected_reg_id, current_username, db_user, db_pass)
                st.markdown(f"**Đã hoàn tất lưu trữ hồ sơ {selected_reg_id}**")
                st.rerun()
            except Exception as e:
                st.markdown(f"**{str(e)}**")

    st.divider()

    # ---------------------------------------------------------------
    # Ho so da hoan thanh (phan trang)
    # ---------------------------------------------------------------
    st.markdown(f'<div class="lt-section-title">Hồ sơ đã hoàn thành</div>', unsafe_allow_html=True)

    if not da_hoan_thanh:
        st.markdown("**Chưa có hồ sơ.**")
    else:
        if "lt_page_num" not in st.session_state:
            st.session_state.lt_page_num = 1

        total_pages = (len(da_hoan_thanh) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
        if st.session_state.lt_page_num > total_pages:
            st.session_state.lt_page_num = total_pages

        start_idx = (st.session_state.lt_page_num - 1) * ITEMS_PER_PAGE
        page_data = da_hoan_thanh[start_idx:start_idx + ITEMS_PER_PAGE]

        df_da_hoan_thanh = pd.DataFrame(page_data)
        df_da_hoan_thanh.columns = [
            "Ma ho so", "Noi dung de nghi", "Co quan tiep nhan",
            "Ma tinh", "Trang thai", "Thoi gian tao",
        ]
        st.dataframe(df_da_hoan_thanh, use_container_width=True, hide_index=True)

        col_prev, col_info, col_next = st.columns([1, 2, 1])
        with col_prev:
            if st.button("Trang trước", disabled=(st.session_state.lt_page_num == 1), use_container_width=True):
                st.session_state.lt_page_num -= 1
                st.rerun()
        with col_info:
            st.markdown(
                f"<div style='text-align:center;line-height:38px;font-weight:bold;'>"
                f"Trang {st.session_state.lt_page_num} / {total_pages}</div>",
                unsafe_allow_html=True,
            )
        with col_next:
            if st.button("Trang sau", disabled=(st.session_state.lt_page_num == total_pages), use_container_width=True):
                st.session_state.lt_page_num += 1
                st.rerun()