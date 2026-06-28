-- ============================================================================
-- FILE: 04_xd_vpd_policy.sql
-- Xét duyệt hồ sơ và thiết lập chính sách bảo mật chặn truy cập dữ liệu cư dân.
-- ============================================================================

---------------------------------------------------------------------------------
-- Thực hiện: SYS_ORACLEFREE
-- Cấp quyền DBA cho SEC_MGR để có thể gán Policy lên bảng của PASSPORT_APP
---------------------------------------------------------------------------------
ALTER SESSION SET CONTAINER = FREEPDB1;

GRANT DBA TO SEC_MGR;
GRANT EXECUTE ON DBMS_RLS TO SEC_MGR;

COMMIT;

---------------------------------------------------------------------------------
-- Thực hiện: SEC_MGR
-- Tạo hàm kiểm tra logic và kích hoạt chốt chặn bảo mật (VPD) lên bảng dữ liệu dân cư
---------------------------------------------------------------------------------
ALTER SESSION SET CONTAINER = FREEPDB1;

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
        RETURN '1=2';
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
COMMIT;

---------------------------------------------------------------------------------
-- TEST 
---------------------------------------------------------------------------------

-- Tài khoản xd_nv01 (Pass: 123, Service: FREEPDB1)
-- Đóng vai nhân viên Xét duyệt (Bị chặn) -> Trả về 0 rows (Bảng trống trơn).
ALTER SESSION SET CONTAINER = FREEPDB1;
SELECT * FROM PASSPORT_APP.RESIDENT_DATA;

-- Test truy cập dữ liệu Hồ sơ (Kiểm chứng OLS) -> Oracle chỉ trả về đúng dữ liệu có trạng thái là 'Da xac thuc', 'Tu choi', 'Da duyet'
SELECT REG_ID, CCCD, TRANG_THAI, MAC_LABEL FROM PASSPORT_APP.PASSPORT_DATA;

-- Tài khoản PASSPORT_APP (Pass: 123, Service: FREEPDB1)
-- Đóng vai chủ sở hữu bảng (Không bị chặn) -> Bảng hiển thị đầy đủ thông tin danh sách cư dân gốc.
ALTER SESSION SET CONTAINER = FREEPDB1;
SELECT * FROM PASSPORT_APP.RESIDENT_DATA;





