import pandas as pd
import streamlit as st

from bll.xt_bll import XtBll


def _to_key_value_rows(data):
    return pd.DataFrame(
        {
            "THONG_TIN": list(data.keys()),
            "GIA_TRI": ["" if value is None else str(value) for value in data.values()],
        }
    )


def render_xt_page():
    st.markdown(
        """
        <style>
        div[data-testid="stAppDeployButton"],
        div[data-testid="stToolbar"],
        div[data-testid="stStatusWidget"],
        div[data-testid="stDecoration"],
        span[data-testid="stMainMenu"],
        header[data-testid="stHeader"] button:not([data-testid="stExpandSidebarButton"]) {
            display: none !important;
        }

        .stApp {
            background: #0b1020;
        }

        header[data-testid="stHeader"] {
            background: #0b1020;
        }

        .block-container {
            width: 100%;
            max-width: 1240px;
            padding: 12px 16px 18px;
        }

        section[data-testid="stSidebar"] {
            background: #111827;
        }

        section[data-testid="stSidebar"] * {
            color: #e5e7eb !important;
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

        .xt-hero {
            border-radius: 8px;
            padding: 18px 20px;
            margin-bottom: 12px;
            background: linear-gradient(135deg, #233b87 0%, #4268e8 100%);
            color: #ffffff;
        }

        .xt-hero-title {
            margin: 0;
            font-size: clamp(22px, 2.3vw, 30px);
            font-weight: 800;
            line-height: 1.2;
        }

        .xt-hero-subtitle {
            margin: 8px 0 0;
            font-size: 15px;
            font-weight: 600;
            color: #dbeafe;
        }

        .xt-stat-card {
            min-height: 70px;
            padding: 13px 14px;
            border: 1px solid #2b3654;
            border-radius: 8px;
            background: #151c2f;
            color: #f8fafc;
            box-sizing: border-box;
        }

        .xt-stat-card strong {
            display: block;
            margin-bottom: 8px;
            color: #cbd5e1;
            font-size: 12px;
            letter-spacing: .02em;
            text-transform: uppercase;
        }

        .xt-stat-card span {
            color: #ffffff;
            font-size: 18px;
            font-weight: 800;
        }

        .xt-panel-title {
            margin: 14px 0 8px;
            color: #f8fafc;
            font-size: 18px;
            font-weight: 800;
        }

        .xt-card-title {
            margin: 8px 0 8px;
            color: #f8fafc;
            font-size: 15px;
            font-weight: 800;
        }

        section[data-testid="stMain"] div[data-testid="stTable"],
        section[data-testid="stMain"] div[data-testid="stDataFrame"] {
            border: 1px solid #2b3654;
            border-radius: 8px;
            background: #ffffff;
            overflow: hidden;
        }

        section[data-testid="stMain"] div[data-testid="stTable"] *,
        section[data-testid="stMain"] div[data-testid="stDataFrame"] * {
            color: #111827;
        }

        section[data-testid="stMain"] div[data-testid="stMarkdown"] {
            color: #e5e7eb;
        }

        section[data-testid="stMain"] div[data-testid="stTextInput"] label {
            color: #cbd5e1;
            font-size: 14px;
            font-weight: 700;
        }

        section[data-testid="stMain"] div[data-testid="stTextInputRootElement"] {
            min-height: 42px;
            border: 1px solid #2f7af0 !important;
            border-radius: 6px !important;
            background: #111827 !important;
            box-shadow: none !important;
        }

        section[data-testid="stMain"] input {
            color: #f8fafc !important;
            background: #111827 !important;
        }

        section[data-testid="stMain"] div[data-testid="stButton"] button {
            width: 100%;
            min-height: 42px;
            border: 0;
            border-radius: 6px;
            background: #4f9f57 !important;
            color: #ffffff !important;
            font-size: 14px;
            font-weight: 800;
        }

        section[data-testid="stMain"] div[data-testid="stButton"] button:hover {
            background: #438c4b !important;
            color: #ffffff !important;
        }

        section[data-testid="stMain"] div[data-testid="stButton"] button:disabled,
        section[data-testid="stMain"] div[data-testid="stButton"] button:disabled:hover {
            background: #334155 !important;
            color: #94a3b8 !important;
            opacity: 1 !important;
        }

        @media (max-width: 900px) {
            .block-container {
                padding: 10px 12px 16px;
            }

            .xt-hero {
                padding: 16px;
            }

            section[data-testid="stMain"] div[data-testid="stHorizontalBlock"] {
                flex-direction: column;
                gap: 0 !important;
            }

            section[data-testid="stMain"] div[data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
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

    st.markdown(
        """
        <div class="xt-hero">
            <div class="xt-hero-title">Bộ phận Xác thực</div>
            <div class="xt-hero-subtitle">Kiểm tra hồ sơ với dữ liệu dân cư trước khi chuyển xét duyệt</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    stat_col1, stat_col2, stat_col3 = st.columns(3, gap="small")
    stat_col1.markdown('<div class="xt-stat-card"><strong>Tình trạng</strong><span>Đang hoạt động</span></div>', unsafe_allow_html=True)
    stat_col2.markdown(f'<div class="xt-stat-card"><strong>Cán bộ</strong><span>{db_username}</span></div>', unsafe_allow_html=True)
    stat_col3.markdown(f'<div class="xt-stat-card"><strong>Hồ sơ chờ xác thực</strong><span>{len(pending_list)}</span></div>', unsafe_allow_html=True)

    if not pending_list:
        st.markdown("**Không có hồ sơ chờ xác thực**")
        return

    valid_ids = {str(item["REG_ID"]) for item in pending_list}
    default_id = str(pending_list[0]["REG_ID"])
    left_col, right_col = st.columns([0.36, 0.64], gap="medium")
    with left_col:
        st.markdown('<div class="xt-panel-title">Danh sách hồ sơ</div>', unsafe_allow_html=True)
        pending_df = pd.DataFrame(pending_list)
        visible_columns = [col for col in ["REG_ID", "CCCD", "HO_TEN", "TRANG_THAI"] if col in pending_df.columns]
        table_height = min(420, 78 + len(pending_list) * 38)
        st.dataframe(pending_df[visible_columns], use_container_width=True, hide_index=True, height=table_height)

    with right_col:
        st.markdown('<div class="xt-panel-title">Kiểm tra hồ sơ</div>', unsafe_allow_html=True)
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

        col1, col2 = st.columns(2, gap="medium")
        with col1:
            st.markdown('<div class="xt-card-title">Thông tin hồ sơ nộp</div>', unsafe_allow_html=True)
            st.dataframe(_to_key_value_rows(ho_so), use_container_width=True, hide_index=True, height=260)
        with col2:
            st.markdown('<div class="xt-card-title">Dữ liệu dân cư</div>', unsafe_allow_html=True)
            if is_match:
                st.markdown("**Kết quả: dữ liệu khớp**")
                st.dataframe(_to_key_value_rows(result_data), use_container_width=True, hide_index=True, height=220)
            else:
                if isinstance(result_data, dict):
                    st.markdown(f"**Kết quả: {result_data.get('message', 'dữ liệu không khớp')}**")
                    resident_data = result_data.get("resident_data")
                    if resident_data:
                        st.dataframe(_to_key_value_rows(resident_data), use_container_width=True, hide_index=True, height=220)
                else:
                    st.markdown(f"**Kết quả: {result_data}**")

        if st.button("Xác thực thành công", disabled=not is_match, use_container_width=True):
            try:
                is_success, message = xt_bll.mark_verified(reg_id)
                st.markdown(f"**{message}**")
                if is_success:
                    st.rerun()
            except Exception as exc:
                st.markdown(f"**Lỗi cập nhật hồ sơ: {str(exc)}**")
