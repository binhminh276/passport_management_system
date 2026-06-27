import streamlit as st
from bll import xd_bll


def render_xd_page():

    st.markdown("""
<style>

/* ===========================
   GLOBAL
=========================== */

.stApp{
    background:#F4F7FB;
}

.main .block-container{
    max-width:98%;
    padding-top:25px;
    padding-left:35px;
    padding-right:35px;
}

h1,h2,h3,h4{
    color:#1B365D;
}

/* ===========================
   HEADER
=========================== */

.dashboard-header{

    background:linear-gradient(135deg,#0A3D62,#1565C0);

    border-radius:18px;

    padding:28px 35px;

    color:white;

    margin-bottom:28px;

    box-shadow:0 10px 25px rgba(0,0,0,.18);

}

.dashboard-header h1{

    margin:0;

    font-size:32px;

    font-weight:700;

    letter-spacing:.5px;

}

.dashboard-header h3{

    margin-top:12px;

    font-weight:500;

}

.dashboard-header p{

    margin-top:10px;

    opacity:.92;

    font-size:15px;

}

/* ===========================
   METRIC
=========================== */

div[data-testid="metric-container"]{

    background:white;

    border:1px solid #E5EAF2;

    border-radius:15px;

    padding:20px;

    box-shadow:0 4px 15px rgba(0,0,0,.06);

}

div[data-testid="metric-container"]:hover{

    transform:translateY(-2px);

    transition:.2s;

}

/* ===========================
   SEARCH
=========================== */

.stTextInput input{

    border-radius:10px;

}

div[data-baseweb="select"]{

    border-radius:10px;

}

/* ===========================
   CARD
=========================== */

.card{

    background:white;

    border-radius:16px;

    padding:22px;

    margin-bottom:18px;

    border:1px solid #E5EAF2;

    box-shadow:0 5px 14px rgba(0,0,0,.06);

}

.card:hover{

    box-shadow:0 10px 22px rgba(0,0,0,.12);

}

/* ===========================
   BUTTON
=========================== */

.stButton>button{

    width:100%;

    border:none;

    border-radius:10px;

    background:#1565C0;

    color:white;

    font-weight:600;

    height:42px;

}

.stButton>button:hover{

    background:#0D47A1;

    color:white;

}

/* ===========================
   EXPANDER
=========================== */

div[data-testid="stExpander"]{

    border-radius:12px;

    border:1px solid #E4E9F2;

}

/* ===========================
   STATUS BADGE
=========================== */

.badge{

    display:inline-block;

    padding:6px 16px;

    border-radius:30px;

    color:white;

    font-size:13px;

    font-weight:600;

    text-align:center;

}

</style>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="dashboard-header">

<h1>CỤC QUẢN LÝ XUẤT NHẬP CẢNH</h1>

<h3>Hệ thống Dịch vụ công Quốc gia</h3>

<p>
Phân hệ xét duyệt hồ sơ hộ chiếu điện tử
</p>

</div>
""", unsafe_allow_html=True)

    # ===========================
    # KIỂM TRA QUYỀN
    # ===========================

    if st.session_state.get("user_role") != "ROLE_XD":
        st.error("Truy cập bị từ chối. Tài khoản không có quyền sử dụng phân hệ Xét duyệt.")
        return

    current_user = st.session_state.get("username", "xd_nv01")

    try:

        danh_sach = xd_bll.get_danh_sach_ho_so(current_user)

        quy_dinh = xd_bll.get_danh_sach_quy_dinh(current_user)

    except Exception as e:

        st.error(str(e))

        return
        # =====================================================
    # DASHBOARD
    # =====================================================

    st.subheader("Thông tin phiên làm việc")

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric(
            label="Hồ sơ chờ xét duyệt",
            value=len(danh_sach)
        )

    with metric2:
        st.metric(
            label="Cán bộ đăng nhập",
            value=current_user.upper()
        )

    with metric3:
        st.metric(
            label="Tổng quy định",
            value=len(quy_dinh)
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # THANH TÌM KIẾM
    # =====================================================

    search_col, filter_col = st.columns([3, 1])

    with search_col:
        keyword = st.text_input(
            "Tìm kiếm hồ sơ",
            placeholder="Nhập mã hồ sơ, CCCD hoặc họ tên..."
        )

    with filter_col:
        filter_status = st.selectbox(
            "Trạng thái",
            [
                "Tất cả",
                "Dang xac thuc",
                "Da duyet",
                "Tu choi"
            ]
        )

    # =====================================================
    # LỌC DỮ LIỆU
    # =====================================================

    if keyword:

        keyword = keyword.lower().strip()

        danh_sach = [
            hs for hs in danh_sach
            if
            keyword in str(hs["reg_id"]).lower()
            or keyword in hs["cccd"].lower()
            or keyword in hs["ho_ten"].lower()
        ]

    if filter_status != "Tất cả":

        danh_sach = [
            hs for hs in danh_sach
            if hs["trang_thai"] == filter_status
        ]

    st.divider()

    # =====================================================
    # QUY ĐỊNH
    # =====================================================

    st.subheader("Danh mục tiêu chuẩn đối chiếu hồ sơ")
        # =====================================================
    # DANH MỤC QUY ĐỊNH
    # =====================================================

    with st.expander("Xem danh mục quy định áp dụng", expanded=False):

        if quy_dinh:

            for qd in quy_dinh:

                st.markdown(
                    f"""
<div style="
background:#F8FAFD;
border-left:5px solid #1565C0;
padding:12px 16px;
margin-bottom:10px;
border-radius:8px;
">

<b>Điều khoản {qd['quy_dinh_id']}</b>

<br>

{qd['noi_dung']}

</div>
""",
                    unsafe_allow_html=True
                )

        else:

            st.info("Không có dữ liệu quy định.")

    st.divider()

    # =====================================================
    # DANH SÁCH HỒ SƠ
    # =====================================================

    st.subheader("Danh sách hồ sơ chờ xét duyệt")

    st.caption("Các hồ sơ đã hoàn thành bước xác thực và đang chờ cán bộ xét duyệt.")

    if not danh_sach:

        st.info("Hiện không có hồ sơ nào phù hợp.")

        return

    # =====================================================
    # HIỂN THỊ TỪNG HỒ SƠ
    # =====================================================

    for ho_so in danh_sach:

        status = ho_so["trang_thai"]

        if status == "Dang xac thuc":
            badge_color = "#F39C12"
        elif status == "Da duyet":
            badge_color = "#27AE60"
        elif status == "Tu choi":
            badge_color = "#E74C3C"
        else:
            badge_color = "#7F8C8D"

        with st.container(border=True):

            left, right = st.columns([6, 1])

            with left:

                st.subheader(f"Hồ sơ: {ho_so['reg_id']}")

                st.write(f"**Họ và tên:** {ho_so['ho_ten']}")

                st.write(f"**CCCD:** {ho_so['cccd']}")

                st.write(
                "**Thời gian tạo:**",
                ho_so["thoi_gian_tao"].strftime("%d/%m/%Y %H:%M")
                if ho_so["thoi_gian_tao"] else ""
            )

            with right:

                st.markdown(
                f"""
<div style="
background:{badge_color};
padding:10px;
border-radius:30px;
text-align:center;
color:white;
font-weight:bold;
margin-top:25px;
">
{status}
</div>
""",
                unsafe_allow_html=True
            )
        st.markdown("<br>", unsafe_allow_html=True)

        action_col, button_col = st.columns([5,1])

        with action_col:

            action = st.selectbox(
                "Chọn quyết định",
                [
                    "-- Chọn --",
                    "Duyệt",
                    "Từ chối",
                    "Lưu trữ"
                ],
                key=f"sel_{ho_so['reg_id']}"
            )

        with button_col:

            st.write("")
            st.write("")

            confirm = st.button(
                "Xác nhận",
                key=f"btn_{ho_so['reg_id']}",
                use_container_width=True
            )
        if confirm:

            if action == "-- Chọn --":

                st.warning("Vui lòng chọn quyết định.")

            elif (
                action == "Lưu trữ"
                and ho_so["trang_thai"] not in ["Da duyet", "Tu choi"]
            ):

                st.error(
                    "Chỉ được lưu trữ hồ sơ đã có kết quả."
                )

            else:

                try:

                    xd_bll.xu_ly_ho_so(
                        current_user,
                        ho_so["reg_id"],
                        ho_so["trang_thai"],
                        action
                    )

                    st.success(
                        f"Đã cập nhật hồ sơ {ho_so['reg_id']}."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(str(e))

        st.markdown("<br>", unsafe_allow_html=True)

