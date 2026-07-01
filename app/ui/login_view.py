import streamlit as st

from bll.auth_bll import AuthPresenter


def render_login_page():
    st.markdown(
        """
        <style>
        button[aria-label="Show password text"],
        button[aria-label="Hide password text"] {
            display: none !important;
            width: 0 !important;
            min-width: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        div[data-testid="InputInstructions"] {
            display: none !important;
        }

        div[data-testid="stAppDeployButton"],
        div[data-testid="stToolbar"],
        div[data-testid="stStatusWidget"],
        div[data-testid="stDecoration"],
        span[data-testid="stMainMenu"],
        header[data-testid="stHeader"] button:not([data-testid="stExpandSidebarButton"]) {
            display: none !important;
        }

        .block-container {
            width: 100%;
            max-width: 100%;
            padding: clamp(1.5rem, 5vh, 3rem) clamp(1rem, 4vw, 4rem) 1.5rem;
        }

        section[data-testid="stSidebar"] div[data-testid="stElementContainer"],
        section[data-testid="stSidebar"] div[data-testid="stButton"] {
            width: 100% !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stButton"] button {
            width: 100% !important;
            min-height: 44px;
            border-radius: 6px;
            font-weight: 700;
            justify-content: center;
        }

        div[data-testid="stForm"] {
            width: min(100%, 520px);
            margin: 0 auto;
            padding: clamp(26px, 3vw, 36px);
            border: 1px solid #e6e6e6;
            border-radius: 8px;
            background: #ffffff;
            box-shadow: 0 10px 26px rgba(0, 0, 0, 0.07);
            box-sizing: border-box;
        }

        .login-title {
            margin: 0 0 24px;
            color: #333333;
            font-size: clamp(28px, 3vw, 34px);
            font-weight: 700;
            line-height: 1.2;
        }

        div[data-testid="stForm"] div[data-testid="stTextInput"] {
            margin-bottom: 16px;
            width: 100%;
        }

        div[data-testid="stForm"] div[data-testid="stTextInputRootElement"] {
            min-height: 52px;
            border: 1px solid #d8d8d8 !important;
            border-radius: 6px !important;
            background: #ffffff !important;
            box-shadow: none !important;
        }

        div[data-testid="stForm"] div[data-baseweb="base-input"] {
            width: 100%;
            background: #ffffff !important;
        }

        div[data-testid="stForm"] div[data-baseweb="input"] input {
            color: #333333;
            background: #ffffff !important;
            font-size: 16px;
        }

        div[data-testid="stForm"] div[data-baseweb="input"] input::placeholder {
            color: #a9a9a9;
            opacity: 1;
        }

        div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] {
            width: 100% !important;
            align-self: stretch !important;
            display: block !important;
        }

        div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] button {
            display: flex !important;
            align-items: center;
            justify-content: center;
            height: 52px;
            margin-top: 10px;
            border: 0;
            border-radius: 6px;
            background: #c9342c !important;
            color: #ffffff !important;
            font-size: 16px;
            font-weight: 700;
            width: 100% !important;
        }

        div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] button:hover {
            background: #b92f28 !important;
            color: #ffffff !important;
        }

        .login-message {
            margin-top: 18px;
            color: #b92f28;
            font-weight: 600;
        }

        @media (max-width: 760px) {
            .block-container {
                padding: 1.5rem 1rem 1rem;
            }

            div[data-testid="stForm"] {
                width: 100%;
                padding: 26px 20px;
                box-shadow: none;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.form(key="login_form"):
        st.markdown('<div class="login-title">Đăng nhập</div>', unsafe_allow_html=True)
        username = st.text_input(
            "Tên đăng nhập",
            placeholder="Tên đăng nhập",
            label_visibility="collapsed",
        )
        password = st.text_input(
            "Mật khẩu",
            placeholder="Mật khẩu",
            type="password",
            label_visibility="collapsed",
        )
        submit_btn = st.form_submit_button("Đăng nhập", use_container_width=True)

        if submit_btn:
            if not username.strip() or not password:
                st.markdown('<div class="login-message">Vui lòng nhập đầy đủ thông tin</div>', unsafe_allow_html=True)
                return

            auth_presenter = AuthPresenter()
            try:
                result = auth_presenter.authenticate(username, password)
            except Exception as exc:
                st.markdown(f'<div class="login-message">Lỗi kết nối cơ sở dữ liệu: {str(exc)}</div>', unsafe_allow_html=True)
                return

            if result:
                db_role, target_page = result
                clean_username = username.strip()
                st.session_state.user_role = db_role
                st.session_state.current_page = target_page
                st.session_state.username = clean_username
                st.session_state.db_username = clean_username
                st.session_state.db_password = password
                st.rerun()
            else:
                st.markdown('<div class="login-message">Sai tên đăng nhập hoặc mật khẩu</div>', unsafe_allow_html=True)
