import streamlit as st
from bll import xd_bll

def render_xd_page():
    # Khởi tạo state để lưu hồ sơ đang được chọn xem chi tiết
    if 'selected_hs' not in st.session_state:
        st.session_state.selected_hs = None

    # =========================================================================
    # 1. CSS CHUẨN HOÁ: ÉP CHỮ NỔI 100% VÀ TẠO KHỐI CARD TỪ CONTAINER NATIVE
    # =========================================================================
    st.markdown("""
        <style>
        /* Ép nền tối toàn trang */
        .stApp { background-color: #0B0F19; color: #E2E8F0 !important; }
        .block-container { padding-top: 2rem; max-width: 95%; }

        /* BAN LỆNH: Ép tất cả chữ của Streamlit (Headers, Labels, P) phải thành màu sáng */
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, 
        .stApp p, .stApp label, .stApp span, div[data-testid="stMarkdownContainer"] p {
            color: #E2E8F0 !important;
        }
        
        /* Biến đổi st.container(border=True) thành Card Đen */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #131B2B !important;
            border: 1px solid #1E293B !important;
            border-radius: 12px !important;
            padding: 20px !important;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4) !important;
        }

        /* Khối Banner Header đầu trang */
        .custom-banner { 
            background: linear-gradient(90deg, #1E3A8A 0%, #2563EB 100%);
            padding: 20px 30px; border-radius: 12px; margin-bottom: 20px; 
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        .custom-banner h1 { color: #FFFFFF !important; font-size: 28px; margin-bottom: 5px; font-weight: bold; }
        .custom-banner p { color: #93C5FD !important; font-size: 15px; margin: 0; }
        
        /* Item danh sách hồ sơ bên trái */
        .list-item-box {
            background-color: #172133; border: 1px solid #283548;
            border-radius: 8px; padding: 12px; margin-bottom: 12px;
        }
        .hs-title { color: #60A5FA !important; font-weight: bold; font-size: 16px; margin-bottom: 3px; }
        .hs-sub { color: #94A3B8 !important; font-size: 13px; }
        
        /* Badges trạng thái */
        .badge { padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: bold; display: inline-block; }
        .b-xacthuc { background-color: rgba(245, 158, 11, 0.15); color: #F59E0B !important; border: 1px solid #F59E0B; }
        .b-duyet { background-color: rgba(16, 185, 129, 0.15); color: #10B981 !important; border: 1px solid #10B981; }
        .b-tuchoi { background-color: rgba(239, 68, 68, 0.15); color: #EF4444 !important; border: 1px solid #EF4444; }

        /* Bảng lịch sử thao tác HTML Table tự chế để không bị lỗi dòng */
        .hist-table { width: 100%; text-align: left; border-collapse: collapse; font-size: 13px; margin-top: 10px;}
        .hist-table th { color: #94A3B8 !important; padding: 12px 10px; border-bottom: 2px solid #1E293B; text-transform: uppercase; font-size: 11px; font-weight: 600;}
        .hist-table td { padding: 12px 10px; border-bottom: 1px solid #1E293B; color: #E2E8F0 !important; }
        </style>
    """, unsafe_allow_html=True)

    # Chốt chặn phân quyền
    if st.session_state.get("user_role") != "ROLE_XD":
        st.error("Truy cập bị từ chối.")
        return
    current_user = st.session_state.get("username", "xd_nv01")

    # Gọi dữ liệu tầng BLL
    try:
        danh_sach = xd_bll.get_danh_sach_ho_so(current_user)
        quy_dinh = xd_bll.get_danh_sach_quy_dinh(current_user)
        ten_tinh_ql = xd_bll.get_ten_tinh_quan_ly(current_user)
        lich_su_log = xd_bll.get_lich_su_thao_tac(current_user)
    except Exception as e:
        st.error(f"Lỗi hệ thống: {str(e)}")
        return

    # =========================================================================
    # 2. BANNER & THÔNG SỐ TRÊN CÙNG
    # =========================================================================
    st.markdown("""
        <div class="custom-banner">
            <h1>CỤC QUẢN LÝ XUẤT NHẬP CẢNH</h1>
            <h3>Hệ thống Dịch vụ công Quốc gia</h3>
            <p>Phân hệ kiểm duyệt hồ sơ hộ chiếu điện tử</p>
        </div>
    """, unsafe_allow_html=True)

    hs_cho = len([hs for hs in danh_sach if hs['trang_thai'] not in ['Da duyet', 'Tu choi']])
    hs_xong = len([hs for hs in danh_sach if hs['trang_thai'] in ['Da duyet', 'Tu choi']])

    m1, m2, m3, m4 = st.columns(4)
    CARD_BG = "#161F32" # Xanh xám nhạt 
    BORDER_DEFAULT = "#243256"

    with m1:
        with st.container(border=False): 
            st.markdown(
            f"""
            <div style='background-color: {CARD_BG}; border: 1px solid #10B981; padding: 16px; rounded-top: 12px; border-radius: 12px;'>
                <p style='font-size:12px; color:#94A3B8; margin:0; font-weight:600;'>TÌNH TRẠNG</p>
                <h4 style='margin:4px 0 0 0; color:#10B981 !important; display:flex; align-items:center; gap:6px;'>
                    <span style='color:#10B981;'>●</span> Đang hoạt động
                </h4>
            </div>
            """, 
            unsafe_allow_html=True
        )

    with m2:
        with st.container(border=False):
            st.markdown(
            f"""
            <div style='background-color: {CARD_BG}; border: 1px solid {BORDER_DEFAULT}; padding: 16px; border-radius: 12px;'>
                <p style='font-size:12px; color:#94A3B8; margin:0; font-weight:600;'>CÁN BỘ ĐANG TRỰC</p>
                <h4 style='margin:4px 0 0 0; color:#F8FAFC;'>{current_user.upper()} ({ten_tinh_ql})</h4>
            </div>
            """, 
            unsafe_allow_html=True
        )

    with m3:
        with st.container(border=False):
            st.markdown(
            f"""
            <div style='background-color: {CARD_BG}; border: 1px solid #F59E0B; padding: 16px; border-radius: 12px; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.05);'>
                <p style='font-size:12px; color:#94A3B8; margin:0; font-weight:600;'>HỒ SƠ CHỜ XÉT DUYỆT</p>
                <h4 style='margin:4px 0 0 0; color:#F59E0B !important; font-weight:700;'>{hs_cho} Đơn</h4>
            </div>
            """, 
            unsafe_allow_html=True
        )

    with m4:
        with st.container(border=False):
            st.markdown(
            f"""
            <div style='background-color: {CARD_BG}; border: 1px solid #A855F7; padding: 16px; border-radius: 12px;'>
                <p style='font-size:12px; color:#94A3B8; margin:0; font-weight:600;'>HỒ SƠ ĐÃ XỬ LÝ</p>
                <h4 style='margin:4px 0 0 0; color:#A855F7 !important;'>{hs_xong} Đơn</h4>
            </div>
            """, 
            unsafe_allow_html=True
        )
    st.write("") 

    # =========================================================================
    # 3. THÂN TRANG: CHIA ĐÔI MASTER - DETAIL LAYOUT (CHỈ CHỈNH MÀU SẮC)
    # =========================================================================
    col_list, col_detail = st.columns([1, 2.2])

    # Định nghĩa màu nâng tầng để card nổi lên khỏi nền tối
    CARD_BG = "#161F32"          # Nền của Khối to (Sáng hơn nền hệ thống)
    ITEM_BG = "#1E293B"          # Nền của từng item hồ sơ chưa chọn
    ITEM_ACTIVE_BG = "#1E1B4B"   # Nền của hồ sơ đang được chọn (Tím xanh nổi bật)
    BORDER_COLOR = "#243256"     # Màu viền phân tách khối

    # ------------------ CỘT TRÁI: DANH SÁCH ------------------
    with col_list:
        # Thay đổi màu nền container danh sách để nổi bật khỏi nền tổng
        with st.container(border=False):
            st.markdown(f"""
                <div style='background-color: {CARD_BG}; border: 1px solid {BORDER_COLOR}; padding: 15px; border-radius: 12px; margin-bottom: 10px;'>
                    <h4 style='margin-top:0; margin-bottom:15px; font-weight:bold; color: #F8FAFC;'> DANH SÁCH HỒ SƠ</h4>
                </div>
            """, unsafe_allow_html=True)
            
            search = st.text_input("Tìm kiếm", placeholder="Mã HS hoặc CCCD...", label_visibility="collapsed")
            st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
            
            if not danh_sach:
                st.info("Danh sách trống.")
            else:
                for hs in danh_sach:
                    if search and search.lower() not in hs['ho_ten'].lower() and search not in str(hs['cccd']):
                        continue
                    
                    stt = hs['trang_thai']
                    if stt == 'Da duyet': cls, txt = "b-duyet", "Đã duyệt"
                    elif stt == 'Tu choi': cls, txt = "b-tuchoi", "Từ chối"
                    else: cls, txt = "b-xacthuc", "Chờ duyệt"

                    ho_ten = hs['ho_ten'] if hs['ho_ten'] else "Chưa cập nhật"
                    tg = hs['thoi_gian_tao'].strftime("%d/%m/%Y %H:%M") if hs['thoi_gian_tao'] else ""

                    # Xác định trạng thái đang chọn để đổi màu nền item
                    is_selected = (st.session_state.selected_hs == hs['reg_id'])
                    current_item_bg = ITEM_ACTIVE_BG if is_selected else ITEM_BG
                    current_item_border = "#6366f1" if is_selected else BORDER_COLOR

                    # Giữ nguyên cấu trúc HTML cũ, chỉnh sửa màu nền, viền và chữ để tăng độ tương phản
                    st.markdown(f"""
                        <div class="list-item-box" style="background-color: {current_item_bg}; border: 1px solid {current_item_border}; padding: 12px; border-radius: 8px; margin-bottom: 10px;">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
                                <div class="hs-title" style="color: #60A5FA; font-weight: bold;">HS-{hs['reg_id']:04d}</div>
                                <div class="badge {cls}">{txt}</div>
                            </div>
                            <div style="font-weight:bold; font-size:15px; margin-bottom:3px; color: #F1F5F9;">{ho_ten}</div>
                            <div class="hs-sub" style="color: #94A3B8;">CCCD: {hs['cccd']}</div>
                            <div class="hs-sub" style="color: #64748B;"> {tg}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Xem chi tiết HS-{hs['reg_id']:04d}", key=f"select_{hs['reg_id']}", use_container_width=True):
                        st.session_state.selected_hs = hs['reg_id']
                        st.rerun()

    # ------------------ CỘT PHẢI: CHI TIẾT HỒ SƠ & THAO TÁC ------------------
    with col_detail:
        # Thay đổi màu nền container chi tiết để nổi bật khỏi nền tổng
        with st.container(border=False):
            if st.session_state.selected_hs is None:
                st.markdown(f"<div style='text-align:center; padding-top:180px; color:#94A3B8; background-color: {CARD_BG}; border: 1px dashed {BORDER_COLOR}; border-radius: 12px; min-height: 500px;'> Hãy chọn một hồ sơ bên trái để tiến hành thẩm định nghiệp vụ.</div>", unsafe_allow_html=True)
            else:
                hs_ct = xd_bll.get_chi_tiet_ho_so(current_user, st.session_state.selected_hs)
                
                if hs_ct:
                    c_info, c_btn1, c_btn2 = st.columns([2, 1, 1])
                    with c_info:
                        st.markdown(f"""
                            <h2 style='margin:0; font-weight:bold; color:#F8FAFC;'>{hs_ct['ho_ten']}</h2>
                            <span class='hs-sub' style='color: #94A3B8;'>Mã số: </span><span style='color:#60A5FA; font-weight:bold;'>HS-{hs_ct['reg_id']:04d}</span>
                            <span class='hs-sub' style='color: #94A3B8;'>&nbsp;&nbsp;•&nbsp;&nbsp;Số CCCD: {hs_ct['cccd']}</span>
                        """, unsafe_allow_html=True)
                    
                    with c_btn1:
                        st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
                        if st.button(" TỪ CHỐI", key="btn_reject", use_container_width=True):
                            xd_bll.xu_ly_ho_so(current_user, hs_ct['reg_id'], hs_ct['trang_thai'], "Từ chối")
                            st.session_state.selected_hs = None
                            st.success("Đã từ chối hồ sơ.")
                            st.rerun()
                    with c_btn2:
                        st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
                        if st.button(" PHÊ DUYỆT", key="btn_approve", type="primary", use_container_width=True):
                            xd_bll.xu_ly_ho_so(current_user, hs_ct['reg_id'], hs_ct['trang_thai'], "Duyệt")
                            st.session_state.selected_hs = None
                            st.success("Đã phê duyệt hồ sơ.")
                            st.rerun()

                    st.markdown("<hr style='border-color:#1E293B; margin: 15px 0;'>", unsafe_allow_html=True)

                    ct_left, ct_right = st.columns([1.1, 1.1])
                    with ct_left:
                        st.markdown(f"""<div style='background:#172133; padding:15px; border-radius:8px; border: 1px solid #283548;'>
<h5 style='color:#94A3B8 !important; margin-top:0; font-weight:bold;'>THÔNG TIN CÁ NHÂN ĐỐI CHIẾU</h5>
<div style='display:flex; justify-content:space-between; margin-top:12px; font-size:14px;'>
    <span style='color:#94A3B8;'>Ngày sinh:</span>
    <span style='font-weight:bold;'>{hs_ct['ngay_sinh']}</span>
</div>
<div style='display:flex; justify-content:space-between; margin-top:8px; font-size:14px;'>
    <span style='color:#94A3B8;'>Giới tính:</span>
    <span style='font-weight:bold;'>{hs_ct['gioi_tinh']}</span>
</div>
<div style='display:flex; justify-content:space-between; margin-top:8px; font-size:14px;'>
    <span style='color:#94A3B8;'>Số điện thoại:</span>
    <span style='font-weight:bold;'>{hs_ct['sdt']}</span>
</div>
<div style='display:flex; justify-content:space-between; margin-top:8px; font-size:14px;'>
    <span style='color:#94A3B8;'>Email:</span>
    <span style='color:#60A5FA; font-weight:bold;'>{hs_ct['email']}</span>
</div>
<hr style='border-color:#283548; margin: 15px 0;'>
<h5 style='color:#94A3B8 !important; margin-top:0; font-weight:bold;'>HỒ SƠ & TÀI LIỆU ĐÍNH KÈM</h5>
<div style='display:flex; justify-content:space-between; margin-top:12px; font-size:14px;'>
    <span style='color:#94A3B8;'>Loại thủ tục:</span>
    <span style='color:#F59E0B; font-weight:bold;'>{hs_ct['loai_yeu_cau']}</span>
</div>
<div style='display:flex; justify-content:space-between; margin-top:8px; font-size:14px;'>
    <span style='color:#94A3B8;'>Ảnh thẻ 4x6:</span>
    <span style='color:#10B981; font-weight:bold;'>{ 'Đã tải lên ✓' if hs_ct['anh_chan_dung'] else 'Chưa có ' }</span>
</div>
<div style='display:flex; justify-content:space-between; margin-top:8px; font-size:14px;'>
    <span style='color:#94A3B8;'>Giấy tờ bổ sung:</span>
    <span style='color:#10B981; font-weight:bold;'>{ 'Có tệp đính kèm ✓' if hs_ct['giay_to_dinh_kem'] else 'Không có ❌' }</span>
</div>
<hr style='border-color:#283548; margin: 15px 0;'>
<h5 style='color:#94A3B8 !important; margin-top:0; font-weight:bold;'>HỆ THỐNG CSDL DÂN CƯ</h5>
<p style='color:#10B981 !important; font-weight:bold; font-size:13px; margin:0;'>● Hồ sơ hợp lệ (Xác thực qua Token VPD)</p>
</div>""", unsafe_allow_html=True)
                    
                    with ct_right:
                        # Tinh chỉnh lại màu chữ tiêu đề quy định bắt buộc cho sắc nét và tương phản tốt hơn
                        st.markdown("<h5 style='color:#F59E0B !important; margin-top:0; font-weight:bold; margin-left:5px;'> QUY ĐỊNH KIỂM DUYỆT BẮT BUỘC</h5>", unsafe_allow_html=True)
                        if quy_dinh:
                            for qd in quy_dinh:
                                st.checkbox(f"Điều {qd['quy_dinh_id']}: {qd['noi_dung']}", value=True, key=f"qd_{hs_ct['reg_id']}_{qd['quy_dinh_id']}")

    st.write("")

    # =========================================================================
    # 4. NHẬT KÝ THAO TÁC CÁ NHÂN (HOÀN TOÀN TỰ CHỨA HTML TABLE KHÔNG SỢ LỖI)
    # =========================================================================
    with st.container(border=True):
        st.markdown("""
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; color:#60A5FA; font-weight:bold;"> NHẬT KÝ THAO TÁC NGHIỆP VỤ CA TRỰC CÁ NHÂN</h4>
                <span style="font-size: 12px; color: #94A3B8;">Bảo mật phân vùng dữ liệu bằng Oracle VPD</span>
            </div>
        """, unsafe_allow_html=True)

        if not lich_su_log:
            st.info("Phiên làm việc này chưa ghi nhận thao tác xét duyệt nào.")
        else:
            # Tự động loại bỏ thụt lề để tránh Streamlit hiểu nhầm là khối code (Code block)
            table_html = "<table class='hist-table'>"
            table_html += "<tr><th>Log ID</th><th>Mã Hồ Sơ</th><th>Trạng thái cũ</th><th>Trạng thái mới</th><th>Cán bộ xử lý</th><th>Thời gian hệ thống</th></tr>"
            
            for log in lich_su_log:
                st_moi = log['trang_thai_moi']
                if st_moi == 'Da duyet': cls_m = "b-duyet"
                elif st_moi == 'Tu choi': cls_m = "b-tuchoi"
                else: cls_m = "b-xacthuc"

                tg_log = log['thoi_gian_cap_nhat'].strftime("%d/%m/%Y %H:%M:%S") if log['thoi_gian_cap_nhat'] else ""
                
                # Viết nối chuỗi liền mạch trên 1 dòng để tuyệt đối không phát sinh dấu cách đầu dòng
                table_html += f"<tr><td style='color:#94A3B8;'>LOG-{log['history_id']:03d}</td><td style='color:#60A5FA; font-weight:bold;'>HS-{log['reg_id']:04d}</td><td>{log['trang_thai_cu']}</td><td><span class='badge {cls_m}'>{st_moi}</span></td><td>{current_user.upper()}</td><td style='color:#94A3B8;'>{tg_log}</td></tr>"
                
            table_html += "</table>"
            st.markdown(table_html, unsafe_allow_html=True)
