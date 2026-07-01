import re
from pathlib import Path

import streamlit as st

from bll.auth_bll import AuthPresenter


UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads"


def save_uploaded_portrait(uploaded_file, cccd):
    if uploaded_file is None:
        return ""

    suffix = Path(uploaded_file.name).suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png"}:
        raise ValueError("Ảnh chân dung chỉ nhận file JPG, JPEG hoặc PNG")

    clean_cccd = re.sub(r"[^0-9]", "", cccd or "")
    if len(clean_cccd) == 12:
        file_name = f"avatar_{clean_cccd}{suffix}"
    else:
        stem = re.sub(r"[^A-Za-z0-9_]", "_", Path(uploaded_file.name).stem).strip("_") or "avatar"
        file_name = f"{stem}{suffix}"

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file_path = UPLOAD_DIR / file_name
    file_path.write_bytes(uploaded_file.getbuffer())
    return f"/uploads/{file_name}"


def render_form_style(max_width="1120px"):
    st.markdown(
        """
        <style>
        button[aria-label="Show password text"],
        button[aria-label="Hide password text"],
        div[data-testid="stAppDeployButton"],
        div[data-testid="stToolbar"],
        div[data-testid="stStatusWidget"],
        div[data-testid="stDecoration"],
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
            padding: clamp(0.75rem, 2.5vh, 1.5rem) clamp(1rem, 3vw, 2.25rem) 1.5rem;
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

        .page-title {
            width: min(100%, __MAX_WIDTH__);
            margin: 0 auto 10px;
            color: #2f323a;
            font-size: clamp(26px, 2.2vw, 34px);
            font-weight: 700;
            line-height: 1.2;
        }

        div[data-testid="stForm"] {
            width: min(100%, __MAX_WIDTH__);
            margin: 0 auto;
            padding: clamp(16px, 1.8vw, 20px);
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            background: #ffffff;
            box-sizing: border-box;
            box-shadow: 0 8px 22px rgba(15, 23, 42, 0.04);
        }

        div[data-testid="stForm"] label {
            color: #333842;
            font-size: 15px;
            font-weight: 600;
        }

        div[data-testid="stForm"] div[data-testid="stTextInput"],
        div[data-testid="stForm"] div[data-testid="stTextArea"],
        div[data-testid="stForm"] div[data-testid="stFileUploader"] {
            margin-bottom: 6px;
        }

        div[data-testid="stForm"] div[data-testid="stTextInputRootElement"],
        div[data-testid="stForm"] textarea,
        div[data-testid="stForm"] section[data-testid="stFileUploaderDropzone"] {
            border: 1px solid #d8dfe8 !important;
            border-radius: 6px !important;
            background: #ffffff !important;
            box-shadow: none !important;
        }

        div[data-testid="stForm"] div[data-testid="stTextInputRootElement"] {
            min-height: 42px;
        }

        div[data-testid="stForm"] textarea {
            min-height: 82px !important;
            resize: vertical;
        }

        div[data-testid="stForm"] section[data-testid="stFileUploaderDropzone"] {
            min-height: 44px;
            padding: 8px 12px;
        }

        div[data-testid="stForm"] div[data-testid="stFileUploader"] svg,
        div[data-testid="stForm"] div[data-testid="stFileUploader"] [data-testid="stIconMaterial"] {
            display: none !important;
        }

        div[data-testid="stForm"] input,
        div[data-testid="stForm"] textarea,
        div[data-testid="stForm"] div[data-testid="stFileUploader"] {
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
            min-width: 220px;
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
    render_form_style("1180px")
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

        img_col1, img_col2 = st.columns(2, gap="large")
        with img_col1:
            uploaded_portrait = st.file_uploader(
                "Chọn ảnh chân dung 4x6",
                type=["jpg", "jpeg", "png"],
            )
        selected_portrait_path = ""
        if uploaded_portrait is not None:
            suffix = Path(uploaded_portrait.name).suffix.lower()
            clean_cccd = re.sub(r"[^0-9]", "", cccd or "")
            if len(clean_cccd) == 12:
                selected_portrait_path = f"/uploads/avatar_{clean_cccd}{suffix}"
            else:
                stem = re.sub(r"[^A-Za-z0-9_]", "_", Path(uploaded_portrait.name).stem).strip("_") or "avatar"
                selected_portrait_path = f"/uploads/{stem}{suffix}"
        with img_col2:
            anh_chan_dung_path = st.text_input(
                "Đường dẫn ảnh chân dung 4x6",
                value=selected_portrait_path,
            )
        submit_btn = st.form_submit_button("Đồng ý và Tiếp tục")

        if submit_btn:
            auth_presenter = AuthPresenter()
            if uploaded_portrait is not None:
                try:
                    anh_chan_dung_path = save_uploaded_portrait(uploaded_portrait, cccd)
                except ValueError as exc:
                    st.markdown(f"**{str(exc)}**")
                    return
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
    render_form_style("840px")
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
