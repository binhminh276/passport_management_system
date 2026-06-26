--------------------------------------------------------------------------------
-- FILE: 05_lt_masking_policy.sql
-- Script nay gom toan bo cau lenh lien quan ROLE_LT.
-- CAN CHAY TUNG PHAN BANG DUNG USER TUONG UNG (xem ghi chu moi phan).
-- Neu dung SQL Developer: mo connection tab dung user, copy dung phan vao chay.
--------------------------------------------------------------------------------

--==============================================================================
-- PHAN 1: COLUMN MASKING (DBMS_REDACT)
-- >>> CONN SEC_MGR / 123
--==============================================================================
BEGIN
  DBMS_REDACT.ADD_POLICY(
    object_schema       => 'PASSPORT_APP',
    object_name         => 'PASSPORT_DATA',
    column_name         => 'CCCD',
    policy_name         => 'REDACT_LT_POLICY',
    function_type       => DBMS_REDACT.FULL,
    expression          => 'SYS_CONTEXT(''USERENV'',''SESSION_USER'') = ''USER_LT''',
    policy_description  => 'Che cot CCCD cho USER_LT khi truy van truc tiep bang goc'
  );
END;
/

BEGIN
  DBMS_REDACT.ALTER_POLICY(
    object_schema => 'PASSPORT_APP', object_name => 'PASSPORT_DATA',
    policy_name => 'REDACT_LT_POLICY', action => DBMS_REDACT.ADD_COLUMN,
    column_name => 'HO_TEN', function_type => DBMS_REDACT.FULL
  );
END;
/

BEGIN
  DBMS_REDACT.ALTER_POLICY(
    object_schema => 'PASSPORT_APP', object_name => 'PASSPORT_DATA',
    policy_name => 'REDACT_LT_POLICY', action => DBMS_REDACT.ADD_COLUMN,
    column_name => 'SDT', function_type => DBMS_REDACT.FULL
  );
END;
/

BEGIN
  DBMS_REDACT.ALTER_POLICY(
    object_schema => 'PASSPORT_APP', object_name => 'PASSPORT_DATA',
    policy_name => 'REDACT_LT_POLICY', action => DBMS_REDACT.ADD_COLUMN,
    column_name => 'EMAIL', function_type => DBMS_REDACT.FULL
  );
END;
/

COMMIT;


--==============================================================================
-- PHAN 2: SECURITY VIEW + PROCEDURE
-- >>> CONN PASSPORT_APP / 123
--==============================================================================
CREATE OR REPLACE VIEW PASSPORT_APP.VW_PASSPORT_LT AS
SELECT REG_ID, NOI_DUNG_DE_NGHI, CO_QUAN_TIEP_NHAN, TRANG_THAI, THOI_GIAN_TAO
FROM PASSPORT_APP.PASSPORT_DATA
WHERE TRANG_THAI = 'Da duyet';

CREATE OR REPLACE PROCEDURE PASSPORT_APP.PROC_LUU_TRU_HO_SO (
    p_reg_id          IN PASSPORT_APP.PASSPORT_DATA.REG_ID%TYPE,
    p_nguoi_cap_nhat  IN VARCHAR2 DEFAULT 'USER_LT'
) AS
    v_trang_thai_cu PASSPORT_APP.PASSPORT_DATA.TRANG_THAI%TYPE;
BEGIN
    SELECT TRANG_THAI INTO v_trang_thai_cu
    FROM PASSPORT_APP.PASSPORT_DATA WHERE REG_ID = p_reg_id;

    IF v_trang_thai_cu <> 'Da duyet' THEN
        RAISE_APPLICATION_ERROR(-20001, 'Chi duoc luu tru ho so co trang thai Da duyet');
    END IF;

    UPDATE PASSPORT_APP.PASSPORT_DATA
    SET TRANG_THAI = 'Da luu tru' WHERE REG_ID = p_reg_id;

    INSERT INTO PASSPORT_APP.PASSPORT_REQUEST_HISTORY
        (REG_ID, TRANG_THAI_CU, TRANG_THAI_MOI, NGUOI_CAP_NHAT)
    VALUES (p_reg_id, v_trang_thai_cu, 'Da luu tru', p_nguoi_cap_nhat);

    COMMIT;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20002, 'Khong tim thay REG_ID nay');
END PROC_LUU_TRU_HO_SO;
/

GRANT SELECT ON PASSPORT_APP.VW_PASSPORT_LT TO ROLE_LT;
GRANT EXECUTE ON PASSPORT_APP.PROC_LUU_TRU_HO_SO TO ROLE_LT;

COMMIT;


--==============================================================================
-- PHAN 3: TAO DATABASE USER CHO NHAN VIEN LT
-- >>> CONN SYS / SYS 
--==============================================================================
CREATE USER USER_LT IDENTIFIED BY 123;
GRANT CONNECT TO USER_LT;
GRANT ROLE_LT TO USER_LT;

COMMIT;


--==============================================================================
-- PHAN 4: KIEM THU (TEST)
-- CONN USER_LT / 123
--==============================================================================
-- 4.1. Phai BI TU CHOI
SELECT * FROM PASSPORT_APP.PASSPORT_DATA;

-- 4.2. Phai XEM DUOC, khong co cot nhay cam
SELECT * FROM PASSPORT_APP.VW_PASSPORT_LT;

-- 4.3. Phai CHAY DUOC
EXEC PASSPORT_APP.PROC_LUU_TRU_HO_SO(3);

-- 4.4. Goi lai -> PHAI BAO LOI ORA-20001 (dung thiet ke)
EXEC PASSPORT_APP.PROC_LUU_TRU_HO_SO(3);

-- 4.5. Xem lai view -> REG_ID vua xu ly phai bien mat
SELECT * FROM PASSPORT_APP.VW_PASSPORT_LT;