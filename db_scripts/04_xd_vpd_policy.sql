-- ============================================================================
-- FILE: 04_xd_vpd_policy.sql
-- Xét duyệt hồ sơ và thiết lập các chính sách bảo mật VPD (Row-Level Security)
-- ============================================================================

---------------------------------------------------------------------------------
-- PHẦN 1: THỰC HIỆN BỞI SYS_ORACLEFREE
-- Mục đích: Cấp quyền DBA cho SEC_MGR để có thể gán Policy lên bảng của PASSPORT_APP
---------------------------------------------------------------------------------
ALTER SESSION SET CONTAINER = FREEPDB1;

GRANT CREATE PROCEDURE TO SEC_MGR;
GRANT EXECUTE ON DBMS_RLS TO SEC_MGR;

COMMIT;
-- XONG PHẦN 1, BẮT BUỘC PHẢI DISCONNECT VÀ CONNECT LẠI TÀI KHOẢN SEC_MGR


---------------------------------------------------------------------------------
-- PHẦN 2: THỰC HIỆN BỞI SEC_MGR
-- Mục đích: Khởi tạo các hàm kiểm tra logic và kích hoạt chốt chặn bảo mật (VPD)
---------------------------------------------------------------------------------
ALTER SESSION SET CONTAINER = FREEPDB1;

-- =====================================================================
-- CHÍNH SÁCH 1: NGĂN CHẶN XÉT DUYỆT XEM DỮ LIỆU CƯ DÂN GỐC
-- =====================================================================

-- 1. Hàm kiểm tra quyền (BLOCK ROLE_XD)
CREATE OR REPLACE FUNCTION SEC_MGR.FUNC_BLOCK_RESIDENT_XD (
    p_schema IN VARCHAR2,
    p_object IN VARCHAR2
) 
RETURN VARCHAR2 
AS
    v_user VARCHAR2(100);
    v_role_count NUMBER;
BEGIN
    v_user := SYS_CONTEXT('USERENV', 'SESSION_USER');
    
    -- Kiểm tra xem user hiện tại có mang DB_ROLE là ROLE_XD không
    SELECT COUNT(*) INTO v_role_count 
    FROM PASSPORT_APP.APP_USERS 
    WHERE UPPER(USERNAME) = v_user AND DB_ROLE = 'ROLE_XD';
    
    IF v_role_count > 0 THEN
        RETURN '1=2'; -- Chặn tuyệt đối
    END IF;
    
    RETURN '1=1';
EXCEPTION
    WHEN OTHERS THEN
        RETURN '1=2'; 
END;
/

-- Dọn dẹp policy cũ tránh lỗi
BEGIN
    DBMS_RLS.DROP_POLICY(
        object_schema => 'PASSPORT_APP', 
        object_name   => 'RESIDENT_DATA', 
        policy_name   => 'POLICY_BLOCK_XD_RESIDENT'
    );
EXCEPTION 
    WHEN OTHERS THEN NULL;
END;
/    
    
-- 2. Áp dụng chính sách VPD lên bảng RESIDENT_DATA
BEGIN
    DBMS_RLS.ADD_POLICY(
        object_schema   => 'PASSPORT_APP',
        object_name     => 'RESIDENT_DATA',
        policy_name     => 'POLICY_BLOCK_XD_RESIDENT',
        function_schema => 'SEC_MGR',
        policy_function => 'FUNC_BLOCK_RESIDENT_XD',
        statement_types => 'SELECT', -- Chỉ chặn khi cố tình xem dữ liệu
        sec_relevant_cols => NULL,
        enable          => TRUE
    );
END;
/

-- =====================================================================
-- CHÍNH SÁCH 2: NHÂN VIÊN CHỈ ĐƯỢC XEM LỊCH SỬ THAO TÁC CỦA CHÍNH MÌNH
-- =====================================================================

-- 1. Hàm kiểm tra (Lọc lịch sử theo tên người dùng)
CREATE OR REPLACE FUNCTION SEC_MGR.FUNC_LIMIT_HISTORY_XD (
    p_schema IN VARCHAR2,
    p_object IN VARCHAR2
) 
RETURN VARCHAR2 
AS
    v_user VARCHAR2(100);
    v_role_count NUMBER;
BEGIN
    v_user := SYS_CONTEXT('USERENV', 'SESSION_USER');
    
    SELECT COUNT(*) INTO v_role_count 
    FROM PASSPORT_APP.APP_USERS 
    WHERE UPPER(USERNAME) = v_user AND DB_ROLE = 'ROLE_XD';
    
    IF v_role_count > 0 THEN
        -- Chỉ trả về các dòng lịch sử do chính tài khoản này thực hiện
        RETURN 'UPPER(NGUOI_CAP_NHAT) = ''' || v_user || '''';
    END IF;
    
    RETURN '1=1';
EXCEPTION
    WHEN OTHERS THEN
        RETURN '1=2'; 
END;
/

-- 2. Dọn dẹp policy cũ
BEGIN
    DBMS_RLS.DROP_POLICY('PASSPORT_APP', 'PASSPORT_REQUEST_HISTORY', 'POLICY_XD_HISTORY_OWNER');
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

-- 3. Gắn Policy vào bảng lịch sử PASSPORT_REQUEST_HISTORY
BEGIN
    DBMS_RLS.ADD_POLICY(
        object_schema   => 'PASSPORT_APP',
        object_name     => 'PASSPORT_REQUEST_HISTORY',
        policy_name     => 'POLICY_XD_HISTORY_OWNER',
        function_schema => 'SEC_MGR',
        policy_function => 'FUNC_LIMIT_HISTORY_XD',
        statement_types => 'SELECT',
        sec_relevant_cols => NULL,
        enable          => TRUE
    );
END;
/

COMMIT;

-- =====================================================================
-- CHÍNH SÁCH 3 : XÉT DUYỆT TỈNH NÀO CHỈ ĐƯỢC XEM HỒ SƠ TỈNH ĐÓ
-- =====================================================================
-- 1. Hàm kiểm tra 
CREATE OR REPLACE FUNCTION SEC_MGR.FUNC_LIMIT_PASSPORT_TINH (
    p_schema IN VARCHAR2,
    p_object IN VARCHAR2
) 
RETURN VARCHAR2 
AS
    v_user VARCHAR2(100);
    v_role_count NUMBER;
BEGIN
    v_user := SYS_CONTEXT('USERENV', 'SESSION_USER');
    
    -- Kiểm tra xem user đăng nhập có phải bộ phận Xét duyệt không
    SELECT COUNT(*) INTO v_role_count 
    FROM PASSPORT_APP.APP_USERS 
    WHERE UPPER(USERNAME) = v_user AND DB_ROLE = 'ROLE_XD';
    
    IF v_role_count > 0 THEN
        -- Ép điều kiện: Mã tỉnh thường trú của hồ sơ phải trùng với mã tỉnh quản lý của cán bộ đang đăng nhập
        RETURN 'MA_TINH_THUONG_TRU = (SELECT MA_TINH_QUAN_LY FROM PASSPORT_APP.APP_USERS WHERE UPPER(USERNAME) = SYS_CONTEXT(''USERENV'', ''SESSION_USER''))';
    END IF;
    
    RETURN '1=1';
EXCEPTION
    WHEN OTHERS THEN RETURN '1=2'; 
END;
/

-- 2. Dọn dẹp policy cũ
BEGIN
    DBMS_RLS.DROP_POLICY('PASSPORT_APP', 'PASSPORT_DATA', 'POLICY_XD_PASSPORT_TINH');
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

    -- 3. Gắn Policy vào bảng PASSPORT_DATA
BEGIN
    DBMS_RLS.ADD_POLICY(
        object_schema   => 'PASSPORT_APP',
        object_name     => 'PASSPORT_DATA',
        policy_name     => 'POLICY_XD_PASSPORT_TINH',
        function_schema => 'SEC_MGR',
        policy_function => 'FUNC_LIMIT_PASSPORT_TINH',
        statement_types => 'SELECT',
        enable          => TRUE
    );
END;
/

COMMIT;

---------------------------------------------------------------------------------
-- PHẦN 3: KỊCH BẢN TEST NGHIỆM THU
---------------------------------------------------------------------------------

/* ==========================================================
   TEST TRÊN TÀI KHOẢN: xd_nv01 (Pass: 123, Service: FREEPDB1)
   ========================================================== */
ALTER SESSION SET CONTAINER = FREEPDB1;

-- Test 1 (Chính sách 1): Xem bảng RESIDENT_DATA 
-- => Kết quả mong đợi: Bảng trống trơn (0 rows) do bị chặn bởi VPD.
SELECT * FROM PASSPORT_APP.RESIDENT_DATA;

-- Test 2 (OLS): Xem bảng Hồ sơ 
-- => Kết quả mong đợi: Chỉ thấy các hồ sơ trạng thái 'Da xac thuc', 'Tu choi', 'Da duyet'.
SELECT REG_ID, CCCD, TRANG_THAI, MAC_LABEL FROM PASSPORT_APP.PASSPORT_DATA;

-- Test 3 (Chính sách 2): Xem bảng Lịch sử
-- => Kết quả mong đợi: Chỉ thấy các dòng có cột NGUOI_CAP_NHAT là 'XD_NV01' (nếu có). 
-- Không thấy lịch sử của XD_NV02 hoặc XT_NV01.
SELECT * FROM PASSPORT_APP.PASSPORT_REQUEST_HISTORY;

-- Test 4 (Chính sách 3): Xem bảng PASSPORT_DATA trên xd_nv01 (Cán bộ tỉnh '02')
-- => Kết quả mong đợi: Do có OLS + VPD, xd_nv01 chỉ thấy các hồ sơ ở trạng thái xét duyệt 
-- VÀ ĐỒNG THỜI hồ sơ đó phải thuộc tỉnh '02' (Mã tỉnh thường trú). Các tỉnh khác bị giấu hoàn toàn.
SELECT REG_ID, CCCD, MA_TINH_THUONG_TRU, TRANG_THAI FROM PASSPORT_APP.PASSPORT_DATA;

/* ==========================================================
   TEST TRÊN TÀI KHOẢN: xd_nv02 (Cán bộ tỉnh '01')
   ========================================================== */
-- => Kết quả mong đợi: Chỉ thấy các hồ sơ thuộc tỉnh '01'. Không thể can thiệp chéo sang tỉnh '02' của xd_nv01.
SELECT REG_ID, CCCD, MA_TINH_THUONG_TRU, TRANG_THAI FROM PASSPORT_APP.PASSPORT_DATA;

/* ==========================================================
   TEST TRÊN TÀI KHOẢN: PASSPORT_APP (Pass: 123, Service: FREEPDB1)
   ========================================================== */
ALTER SESSION SET CONTAINER = FREEPDB1;

-- Đóng vai chủ sở hữu bảng (Không bị chặn bởi VPD)
-- => Kết quả mong đợi: Bảng hiển thị đầy đủ danh sách cư dân gốc.
SELECT * FROM PASSPORT_APP.RESIDENT_DATA;

-- Đóng vai chủ sở hữu bảng xem lịch sử
-- => Kết quả mong đợi: Xem được toàn bộ lịch sử thao tác của tất cả nhân viên.
SELECT * FROM PASSPORT_APP.PASSPORT_REQUEST_HISTORY;
