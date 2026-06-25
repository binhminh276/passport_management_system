import streamlit as st
from ui import login_view, register_view, xt_view, xd_view, lt_view, gs_view

# Nhúng mã CSS tùy chỉnh.
def apply_custom_css():
    custom_css = """
    <style>
        /* Tùy chỉnh Button ở thanh Sidebar và các Button thông thường */
        .stButton > button {
            background-color: #0056b3;
            color: white;
            border-radius: 6px;
            border: 1px solid #0056b3;
            font-weight: 600;
            transition: all 0.2s ease-in-out;
        }
        .stButton > button:hover {
            background-color: #004494;
            border-color: #004494;
            color: white;
            transform: scale(1.02);
        }
        
        /* Tùy chỉnh Nút Submit bên trong Form (Đăng nhập, Đăng ký) dùng màu nhấn khác */
        .stFormSubmitButton > button {
            background-color: #0056b3; 
            color: white;
            border-radius: 6px;
            border: none;
            font-weight: bold;
            width: 100%;
        }
        .stFormSubmitButton > button:hover {
            background-color: #003d82;
            color: white;
        }

        /* Tùy chỉnh viền của các ô nhập liệu (Input) và Selectbox */
        div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
            border-radius: 6px;
            border: 1px solid #b3d4fc;
        }
        div[data-baseweb="input"] > div:focus-within, div[data-baseweb="select"] > div:focus-within {
            border-color: #0056b3;
            box-shadow: 0 0 0 1px #0056b3;
        }
        
        /* Tùy chỉnh các khối thông báo (success, error, warning) */
        .stAlert > div {
            border-radius: 8px;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# Quản lý trạng thái và điều hướng các trang giao diện của hệ thống.
def main():
    st.set_page_config(page_title="Hệ thống Quản lý Hộ chiếu", layout="wide")
    
    # Gọi hàm áp dụng CSS ngay sau khi khởi tạo trang
    apply_custom_css()

    if "current_page" not in st.session_state:
        st.session_state.current_page = "login"
    if "user_role" not in st.session_state:
        st.session_state.user_role = None

    st.sidebar.title("Menu Chức năng")
    
    if st.session_state.user_role is None:
        if st.sidebar.button("Đăng nhập Cán bộ"):
            st.session_state.current_page = "login"
            st.rerun()
        if st.sidebar.button("Đăng ký hộ chiếu"):
            st.session_state.current_page = "register"
            st.rerun()
    else:
        st.sidebar.write(f"Quyền hiện tại: {st.session_state.user_role}")
        if st.sidebar.button("Đăng xuất"):
            st.session_state.user_role = None
            st.session_state.current_page = "login"
            st.rerun()

    if st.session_state.current_page == "login":
        login_view.render_login_page()
    elif st.session_state.current_page == "register":
        register_view.render_register_page()
    elif st.session_state.current_page == "xt_dashboard" and st.session_state.user_role == "ROLE_XT":
        xt_view.render_xt_page()
    elif st.session_state.current_page == "xd_dashboard" and st.session_state.user_role == "ROLE_XD":
        xd_view.render_xd_page()
    elif st.session_state.current_page == "lt_dashboard" and st.session_state.user_role == "ROLE_LT":
        lt_view.render_lt_page()
    elif st.session_state.current_page == "gs_dashboard" and st.session_state.user_role == "ROLE_GS":
        gs_view.render_gs_page()
    else:
        st.error("Bạn không có quyền truy cập hoặc chưa đăng nhập.")

if __name__ == "__main__":
    main()