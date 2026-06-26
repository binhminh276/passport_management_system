import streamlit as st

def render_login_page():
    st.header("Đăng nhập hệ thống Quản lý Hộ chiếu")
    
    with st.form(key="login_form"):
        username = st.text_input("Tên đăng nhập")
        password = st.text_input("Mật khẩu", type="password")
        submit_btn = st.form_submit_button("Đăng nhập")

        if submit_btn:
            if username == "xt_nv01" and password == "123":
                st.session_state.user_role = "ROLE_XT"
                st.session_state.current_page = "xt_dashboard"
                st.rerun()
            elif username == "lt_nv01" and password == "123":
                st.session_state.user_role = "ROLE_LT"
                st.session_state.current_page = "lt_dashboard"
                st.rerun()
            else:
                st.error("Sai tên đăng nhập hoặc mật khẩu")