import pandas as pd
import streamlit as st
from bll import gs_bll

def render_gs_page():
    # Ham render giao dien giam sat he thong
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
            background: #111827 !important;
        }

        section[data-testid="stSidebar"] * {
            color: #e5e7eb !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stElementContainer"],
        section[data-testid="stSidebar"] div[data-testid="stButton"] {
            width: 100% !important;
        }

        .gs-hero {
            border-radius: 8px;
            padding: 18px 20px;
            margin-bottom: 12px;
            background: linear-gradient(135deg, #233b87 0%, #4268e8 100%);
            color: #ffffff;
        }

        .gs-hero-title {
            margin: 0;
            font-size: clamp(22px, 2.3vw, 30px);
            font-weight: 800;
            line-height: 1.2;
        }

        .gs-hero-subtitle {
            margin: 8px 0 0;
            font-size: 15px;
            font-weight: 600;
            color: #dbeafe;
        }

        .gs-stat-card {
            min-height: 70px;
            padding: 13px 14px;
            border: 1px solid #2b3654;
            border-radius: 8px;
            background: #151c2f;
            color: #f8fafc;
            box-sizing: border-box;
        }

        .gs-stat-card strong {
            display: block;
            margin-bottom: 8px;
            color: #cbd5e1;
            font-size: 12px;
            letter-spacing: .02em;
            text-transform: uppercase;
        }

        .gs-stat-card span {
            color: #ffffff;
            font-size: 18px;
            font-weight: 800;
        }

        .gs-panel-title {
            margin: 14px 0 8px;
            color: #f8fafc;
            font-size: 18px;
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

        section[data-testid="stMain"] div[data-testid="stTextInput"] label,
        section[data-testid="stMain"] div[data-testid="stSelectbox"] label {
            color: #cbd5e1;
            font-size: 14px;
            font-weight: 700;
        }

        section[data-testid="stMain"] div[data-testid="stTextInputRootElement"],
        section[data-testid="stMain"] div[data-baseweb="input"],
        section[data-testid="stMain"] div[data-baseweb="input"] > div {
            min-height: 42px;
            border: 1px solid #2f7af0 !important;
            border-radius: 6px !important;
            background-color: #111827 !important;
            box-shadow: none !important;
        }

        section[data-testid="stMain"] input {
            color: #f8fafc !important;
            background-color: #111827 !important;
            -webkit-text-fill-color: #f8fafc !important;
        }
        
        section[data-testid="stMain"] div[data-testid="stSelectbox"] > div[data-baseweb="select"],
        section[data-testid="stMain"] div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            min-height: 42px;
            border: 1px solid #2f7af0 !important;
            border-radius: 6px !important;
            background-color: #111827 !important;
        }

        section[data-testid="stMain"] div[data-testid="stSelectbox"] div[data-baseweb="select"] * {
            color: #f8fafc !important;
            background-color: transparent !important;
        }

        @media (max-width: 900px) {
            .block-container {
                padding: 10px 12px 16px;
            }

            .gs-hero {
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

    try:
        logs = gs_bll.get_danh_sach_log(db_username, db_password)
    except Exception as exc:
        st.markdown(f"**Lỗi tải danh sách log: {str(exc)}**")
        return

    st.markdown(
        """
        <div class="gs-hero">
            <div class="gs-hero-title">Bộ phận Giám sát</div>
            <div class="gs-hero-subtitle">Nhật ký thao tác hệ thống (Audit Trail)</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    total_logs = len(logs) if logs else 0
    stat_col1, stat_col2, stat_col3 = st.columns(3, gap="small")
    stat_col1.markdown('<div class="gs-stat-card"><strong>Tình trạng</strong><span>Đang hoạt động</span></div>', unsafe_allow_html=True)
    stat_col2.markdown(f'<div class="gs-stat-card"><strong>Cán bộ</strong><span>{db_username}</span></div>', unsafe_allow_html=True)
    stat_col3.markdown(f'<div class="gs-stat-card"><strong>Tổng số nhật ký</strong><span>{total_logs}</span></div>', unsafe_allow_html=True)

    if not logs:
        st.markdown("**Hiện không có log thao tác nào trong hệ thống.**")
        return

    df = pd.DataFrame(logs)

    st.markdown('<div class="gs-panel-title">Bộ lọc tra cứu</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        action_filter = st.selectbox("Lọc theo thao tác", options=["Tất cả"] + list(df['ACTION_NAME'].unique()))
    with col2:
        user_filter = st.text_input("Tìm theo người dùng (DBUSERNAME)")

    if action_filter != "Tất cả":
        df = df[df['ACTION_NAME'] == action_filter]
    if user_filter:
        df = df[df['DBUSERNAME'].str.contains(user_filter.upper(), na=False)]

    delete_count = len(df[df['ACTION_NAME'] == 'DELETE'])
    if delete_count > 0:
        st.markdown(
            f'<div style="color: #ef4444; font-weight: bold; margin-bottom: 16px; background: #450a0a; padding: 12px; border-radius: 6px; border: 1px solid #7f1d1d;">'
            f'Cảnh báo: Có {delete_count} thao tác xóa (DELETE) được ghi nhận trong danh sách hiện tại.'
            f'</div>', 
            unsafe_allow_html=True
        )

    st.markdown('<div class="gs-panel-title">Danh sách nhật ký hệ thống</div>', unsafe_allow_html=True)
    table_height = min(600, 78 + len(df) * 38)
    st.dataframe(df, use_container_width=True, hide_index=True, height=table_height)