import pandas as pd
import streamlit as st
from bll import gs_bll

def render_gs_page():
    st.header("Bảng điều khiển - Bộ phận Giám sát")
    st.subheader("Nhật ký thao tác hệ thống (Audit Trail)")

    db_username = st.session_state.get("db_username")
    db_password = st.session_state.get("db_password")
    
    if not db_username or not db_password:
        st.error("Phiên đăng nhập không hợp lệ")
        return

    try:
        logs = gs_bll.get_danh_sach_log(db_username, db_password)
    except Exception as exc:
        st.error(f"Lỗi tải danh sách log: {str(exc)}")
        return

    if not logs:
        st.info("Hiện không có log thao tác nào trong hệ thống.")
        return

    df = pd.DataFrame(logs)

    # Bộ lọc cơ bản
    col1, col2 = st.columns(2)
    with col1:
        action_filter = st.selectbox("Lọc theo thao tác", options=["Tất cả"] + list(df['ACTION_NAME'].unique()))
    with col2:
        user_filter = st.text_input("Tìm theo người dùng (DBUSERNAME)")

    # Áp dụng bộ lọc
    if action_filter != "Tất cả":
        df = df[df['ACTION_NAME'] == action_filter]
    if user_filter:
        df = df[df['DBUSERNAME'].str.contains(user_filter.upper(), na=False)]

    # Cảnh báo thao tác DELETE
    delete_count = len(df[df['ACTION_NAME'] == 'DELETE'])
    if delete_count > 0:
        st.warning(f"Cảnh báo: Có {delete_count} thao tác xóa (DELETE) được ghi nhận trong danh sách hiện tại.")

    st.dataframe(df, use_container_width=True)