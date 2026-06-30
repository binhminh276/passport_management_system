import streamlit as st

from bll.auth_bll import AuthPresenter


def render_form_style(max_width="1120px"):
    st.markdown(
        """
        <style>
        button[aria-label="Show password text"],
        button[aria-label="Hide password text"],
        div[data-testid="stAppDeployButton"],
        span[data-testid="stMainMenu"],
        header[data-testid="stHeader"] button:not([data-testid="stExpandSidebarButton"]) {
            display: none !important;
        }

        div[data-testid="InputInstructions"] {
            display: none !important;
        }

        .block-container {
            width: 100%;
            max-width: 100%;
            padding: clamp(1rem, 3.5vh, 2.25rem) clamp(1rem, 3vw, 3rem) 2rem;
        }

        .page-title {
            width: min(100%, __MAX_WIDTH__);
            margin: 0 auto 12px;
            color: #2f323a;
            font-size: clamp(28px, 2.4vw, 38px);
            font-weight: 700;
            line-height: 1.2;
        }

        div[data-testid="stForm"] {
            width: min(100%, __MAX_WIDTH__);
            margin: 0 auto;
            padding: clamp(16px, 2vw, 22px);
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            background: #ffffff;
            box-sizing: border-box;
        }

        div[data-testid="stForm"] label {
            color: #333842;
            font-size: 15px;
            font-weight: 600;
        }

        div[data-testid="stForm"] div[data-testid="stTextInput"],
        div[data-testid="stForm"] div[data-testid="stTextArea"] {
            margin-bottom: 8px;
        }

        div[data-testid="stForm"] div[data-testid="stTextInputRootElement"],
        div[data-testid="stForm"] textarea {
            border: 1px solid #d8dfe8 !important;
            border-radius: 6px !important;
            background: #ffffff !important;
            box-shadow: none !important;
        }

        div[data-testid="stForm"] div[data-testid="stTextInputRootElement"] {
            min-height: 44px;
        }

        div[data-testid="stForm"] textarea {
            min-height: 88px !important;
            resize: vertical;
        }

        div[data-testid="stForm"] input,
        div[data-testid="stForm"] textarea {
            color: #2f323a !important;
            background: #ffffff !important;
            font-size: 15px !important;
        }

        div[data-testid="stForm"] input::placeholder,
        div[data-testid="stForm"] textarea::placeholder {
            color: #8c94a3 !important;
            opacity: 1;
        }

        div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] button {
            min-width: 180px;
            height: 42px;
            border: 0;
            border-radius: 6px;
            background: #3157b7 !important;
            color: #ffffff !important;
            font-size: 15px;
            font-weight: 700;
        }

        div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] button:hover {
            background: #294ba2 !important;
            color: #ffffff !important;
        }

        @media (max-width: 900px) {
            .page-title {
                font-size: clamp(24px, 5vw, 30px);
            }

            div[data-testid="stForm"] {
                width: 100%;
                padding: 18px;
            }

            div[data-testid="stForm"] div[data-testid="stHorizontalBlock"] {
                flex-direction: column;
                gap: 0 !important;
            }

            div[data-testid="stForm"] div[data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
            }

            div[data-testid="stForm"] div[data-testid="stFormSubmitButton"],
            div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] button {
                width: 100% !important;
            }
        }
        </style>
        """.replace("__MAX_WIDTH__", max_width),
        unsafe_allow_html=True,
    )


def render_register_page():
    render_form_style("1120px")
    st.markdown('<div class="page-title">Tờ khai đề nghị cấp hộ chiếu</div>', unsafe_allow_html=True)

    with st.form(key="register_form"):
        col1, col2 = st.columns(2, gap="large")

        with col1:
            cccd = st.text_input("Số CCCD (*)", max_chars=12)
            ho_ten = st.text_input("Họ và tên (*)")
            gioi_tinh = st.text_input("Giới tính (*)", placeholder="Nam hoặc Nu")
            ngay_sinh_text = st.text_input("Ngày sinh (*)", placeholder="YYYY-MM-DD")

        with col2:
            sdt = st.text_input("Số điện thoại (*)")
            email = st.text_input("Email (*)")
            noi_dung = st.text_area("Nội dung đề nghị (*)")
            co_quan = st.text_input(
                "Cơ quan tiếp nhận (*)",
                value="Cục Quản lý xuất nhập cảnh",
            )

        anh_chan_dung_path = st.text_input("Đường dẫn ảnh chân dung 4x6")
        submit_btn = st.form_submit_button("Đồng ý và Tiếp tục")

        if submit_btn:
            auth_presenter = AuthPresenter()
            ngay_sinh = auth_presenter.parse_date(ngay_sinh_text)
            data = {
                "cccd": cccd,
                "ho_ten": ho_ten,
                "gioi_tinh": gioi_tinh,
                "ngay_sinh": ngay_sinh,
                "sdt": sdt,
                "email": email,
                "noi_dung_de_nghi": noi_dung,
                "co_quan_tiep_nhan": co_quan,
                "anh_chan_dung_path": anh_chan_dung_path,
            }

            if st.session_state.get("user_role") == "ROLE_CD":
                db_username = st.session_state.get("db_username")
                db_password = st.session_state.get("db_password")
                if not db_username or not db_password:
                    st.markdown("**Phiên đăng nhập không hợp lệ**")
                    return
                is_success, message = auth_presenter.submit_passport(data, db_username, db_password)
            else:
                is_success, message = auth_presenter.register(data)
            st.markdown(f"**{message}**")


def render_admin_user_page():
    render_form_style("640px")
    st.markdown('<div class="page-title">Cấp tài khoản nhân viên</div>', unsafe_allow_html=True)

    if st.session_state.get("user_role") != "ROLE_GS":
        st.markdown("**Bạn không có quyền truy cập chức năng này**")
        return

    with st.form(key="admin_create_user_form"):
        username = st.text_input("Tên đăng nhập nhân viên (*)")
        db_role = st.text_input("Vai trò (*)", placeholder="ROLE_XT, ROLE_XD, ROLE_LT hoặc ROLE_GS")
        submit_btn = st.form_submit_button("Tạo tài khoản")

        if submit_btn:
            auth_presenter = AuthPresenter()
            is_success, message = auth_presenter.create_employee_account(username, db_role)
            st.markdown(f"**{message}**")
