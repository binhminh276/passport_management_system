-- Xét duyệt hồ sơ và thiết lập chính sách bảo mật chặn truy cập dữ liệu cư dân.
-- Thực hiện: SEC_MGR

ALTER SESSION SET CONTAINER = FREEPDB1;

-- 1. Hàm kiểm tra quyền động qua bảng APP_USERS
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

-- 2. Áp dụng VPD lên bảng RESIDENT_DATA
BEGIN
    DBMS_RLS.DROP_POLICY('PASSPORT_APP', 'RESIDENT_DATA', 'POLICY_BLOCK_XD_RESIDENT');
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    DBMS_RLS.ADD_POLICY(
        object_schema   => 'PASSPORT_APP',
        object_name     => 'RESIDENT_DATA',
        policy_name     => 'POLICY_BLOCK_XD_RESIDENT',
        function_schema => 'SEC_MGR',
        policy_function => 'FUNC_BLOCK_RESIDENT_XD',
        statement_types => 'SELECT',
        sec_relevant_cols => NULL,
        enable          => TRUE
    );
END;
/
COMMIT;










