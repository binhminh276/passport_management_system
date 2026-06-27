import pandas as pd
import streamlit as st

from bll.xt_bll import XtBll


def render_xt_page():
    st.markdown(
        """
        <style>
        div[data-testid="stAppDeployButton"],
        span[data-testid="stMainMenu"],
        header[data-testid="stHeader"] button:not([data-testid="stExpandSidebarButton"]) {
            display: none !important;
        }

        @media (max-width: 900px) {
            section[data-testid="stSidebar"][aria-expanded="true"] ~ div section[data-testid="stMain"] .block-container,
            section[data-testid="stSidebar"][aria-expanded="true"] ~ section[data-testid="stMain"] .block-container {
                margin-left: 300px !important;
                width: calc(100vw - 300px) !important;
                max-width: calc(100vw - 300px) !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.header("Bảng điều khiển - Bộ phận Xác thực")
    st.subheader("Danh sách hồ sơ chờ xác thực")

    db_username = st.session_state.get("db_username")
    db_password = st.session_state.get("db_password")
    if not db_username or not db_password:
        st.markdown("**Phiên đăng nhập không hợp lệ**")
        return

    xt_bll = XtBll(db_username, db_password)
    try:
        pending_list = xt_bll.get_pending_list()
    except Exception as exc:
        st.markdown(f"**Lỗi tải danh sách hồ sơ: {str(exc)}**")
        return

    if not pending_list:
        st.markdown("**Không có hồ sơ chờ xác thực**")
        return

    st.table(pd.DataFrame(pending_list))
    st.divider()
    st.subheader("Kiểm tra hồ sơ")

    valid_ids = {str(item["REG_ID"]) for item in pending_list}
    default_id = str(pending_list[0]["REG_ID"])
    reg_id_text = st.text_input("Nhập mã hồ sơ cần kiểm tra", value=default_id)

    if not reg_id_text.strip().isdigit() or reg_id_text.strip() not in valid_ids:
        st.markdown("**Mã hồ sơ không nằm trong danh sách chờ xác thực**")
        return

    reg_id = int(reg_id_text.strip())
    try:
        ho_so = xt_bll.get_detail(reg_id)
        is_match, result_data = xt_bll.verify_resident_data(reg_id)
    except Exception as exc:
        st.markdown(f"**Lỗi xác thực hồ sơ: {str(exc)}**")
        return

    col1, col2 = st.columns(2)
    with col1:
        st.write("Thông tin hồ sơ nộp")
        st.table(pd.DataFrame([ho_so]))
    with col2:
        st.write("Dữ liệu dân cư")
        if is_match:
            st.markdown("**Kết quả: dữ liệu khớp**")
            st.table(pd.DataFrame([result_data]))
        else:
            if isinstance(result_data, dict):
                st.markdown(f"**Kết quả: {result_data.get('message', 'dữ liệu không khớp')}**")
                resident_data = result_data.get("resident_data")
                if resident_data:
                    st.table(pd.DataFrame([resident_data]))
            else:
                st.markdown(f"**Kết quả: {result_data}**")

    if st.button("Xác thực thành công", disabled=not is_match):
        try:
            is_success, message = xt_bll.mark_verified(reg_id)
            st.markdown(f"**{message}**")
            if is_success:
                st.rerun()
        except Exception as exc:
            st.markdown(f"**Lỗi cập nhật hồ sơ: {str(exc)}**")
