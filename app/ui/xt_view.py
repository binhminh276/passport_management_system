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

        .block-container {
            width: 100%;
            max-width: 1120px;
            padding: clamp(1.75rem, 5vh, 3.5rem) clamp(1rem, 3vw, 3rem) 2rem;
        }

        .xt-page-title {
            margin: 0 0 20px;
            color: #2f323a;
            font-size: clamp(28px, 2.4vw, 38px);
            font-weight: 700;
            line-height: 1.2;
        }

        .xt-section-title {
            margin: 22px 0 12px;
            color: #2f323a;
            font-size: clamp(22px, 1.8vw, 28px);
            font-weight: 700;
            line-height: 1.25;
        }

        .xt-card-title {
            margin: 4px 0 10px;
            color: #333842;
            font-size: 16px;
            font-weight: 700;
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
            .xt-page-title {
                font-size: clamp(24px, 5vw, 30px);
            }

            .xt-section-title {
                font-size: clamp(20px, 4vw, 24px);
            }

            section[data-testid="stMain"] div[data-testid="stHorizontalBlock"] {
                flex-direction: column;
                gap: 0 !important;
            }

            section[data-testid="stMain"] div[data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
            }

            section[data-testid="stMain"] div[data-testid="stButton"],
            section[data-testid="stMain"] div[data-testid="stButton"] button {
                width: 100% !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="xt-page-title">Bảng điều khiển - Bộ phận Xác thực</div>', unsafe_allow_html=True)
    st.markdown('<div class="xt-section-title">Danh sách hồ sơ chờ xác thực</div>', unsafe_allow_html=True)

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
    st.markdown('<div class="xt-section-title">Kiểm tra hồ sơ</div>', unsafe_allow_html=True)

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
        st.markdown('<div class="xt-card-title">Thông tin hồ sơ nộp</div>', unsafe_allow_html=True)
        st.table(pd.DataFrame([ho_so]))
    with col2:
        st.markdown('<div class="xt-card-title">Dữ liệu dân cư</div>', unsafe_allow_html=True)
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
