import streamlit as st

# Hiển thị biểu mẫu đăng ký cấp hộ chiếu lần đầu cho công dân.
def render_register_page():
    st.header("Tờ khai đề nghị cấp hộ chiếu")
    
    with st.form(key="register_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            cccd = st.text_input("Số CCCD (*)")
            ho_ten = st.text_input("Họ và tên (*)")
            gioi_tinh = st.selectbox("Giới tính (*)", ["Nam", "Nữ"])
            ngay_sinh = st.date_input("Ngày sinh (*)")
            
        with col2:
            sdt = st.text_input("Số điện thoại (*)")
            email = st.text_input("Email (*)")
            noi_dung = st.selectbox("Nội dung đề nghị (*)", ["Cấp hộ chiếu lần đầu", "Cấp lại hộ chiếu do bị mất"])
            co_quan = st.selectbox("Cơ quan tiếp nhận (*)", ["Cục Quản lý xuất nhập cảnh tại Hà Nội", "Cục Quản lý xuất nhập cảnh tại TP. Hồ Chí Minh"])
            
        anh_chan_dung = st.file_uploader("Tải ảnh chân dung 4x6 nền trắng", type=["jpg", "jpeg"])
        
        submit_btn = st.form_submit_button("Đồng ý và Tiếp tục")
        
        if submit_btn:
            if not cccd or not ho_ten or not sdt:
                st.warning("Vui lòng nhập đầy đủ thông tin bắt buộc (*)")
            else:
                st.success("Gửi hồ sơ thành công. Mã hồ sơ của bạn đang được xử lý.")