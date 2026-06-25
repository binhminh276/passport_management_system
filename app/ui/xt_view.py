import streamlit as st
import pandas as pd

# Giao diện bảng điều khiển dành riêng cho bộ phận Xác thực.
def render_xt_page():
    st.header("Bảng điều khiển - Bộ phận Xác thực")
    st.subheader("Danh sách hồ sơ chờ xác thực")
    
    mock_data = {
        "Mã Hồ Sơ": [1, 6, 9],
        "CCCD": ["079203000001", "079203000006", "079203000009"],
        "Họ Tên": ["Nguyễn Văn A", "Vũ Thị F", "Bùi Văn I"],
        "Trạng Thái": ["Đã nộp", "Đã nộp", "Đã nộp"]
    }
    df = pd.DataFrame(mock_data)
    
    st.dataframe(df, use_container_width=True)
    
    st.divider()
    
    st.subheader("Thao tác hồ sơ")
    with st.form("action_form"):
        ma_ho_so = st.number_input("Nhập Mã Hồ Sơ cần xử lý", min_value=1, step=1)
        ket_qua = st.selectbox("Kết quả xác thực", ["Hợp lệ", "Từ chối"])
        submit_action = st.form_submit_button("Cập nhật trạng thái")
        
        if submit_action:
            st.success("Cập nhật hồ sơ thành công")