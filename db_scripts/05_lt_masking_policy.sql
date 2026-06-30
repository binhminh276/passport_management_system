--------------------------------------------------------------------------------
-- FILE: 05_lt_masking_policy.sql
-- Phu trach: ROLE_LT
-- THU TU CHAY: 01 -> 02 -> 07 -> 08 -> 05 
--
-- Pham vi nghiep vu:
--   - LT XEM ho so o trang thai 'Da luu tru' va 'Da hoan thanh'
--   - LT duoc phep 1 THAO TAC GHI DUY NHAT: chuyen 'Da luu tru' -> 'Da hoan thanh'
--   - Sau khi 'Da hoan thanh': ho so niem phong, KHONG ai con sua duoc nua
--   - LT chi xem duoc ho so thuoc dung TINH minh quan ly (MA_TINH_QUAN_LY)
--
-- Ky thuat ap dung:
--   (1) VPD Column Masking (DBMS_RLS + sec_relevant_cols) - che CCCD, HO_TEN
--   (2) VPD Row-Level (DBMS_RLS thuong)  - loc theo MA_TINH_THUONG_TRU = MA_TINH_QUAN_LY
--   (3) OLS (PASSPORT_MAC_POL) - loc theo trang thai qua MAC_LABEL
--   (4) Procedure co kiem soat 
--------------------------------------------------------------------------------


--==============================================================================
-- PHAN 1: VPD COLUMN MASKING - che CCCD, HO_TEN cho ROLE_LT
--==============================================================================

-- >>> CONN SEC_MGR / 123
ALTER SESSION SET CONTAINER = FREEPDB1;

CREATE OR REPLACE FUNCTION SEC_MGR.LT_MASKING_FUNC (
    p_schema IN VARCHAR2,
    p_object IN VARCHAR2
) RETURN VARCHAR2
AS
    v_user VARCHAR2(100);
    v_role_count NUMBER;
BEGIN
    v_user := SYS_CONTEXT('USERENV','SESSION_USER');

    SELECT COUNT(*) INTO v_role_count
    FROM PASSPORT_APP.APP_USERS
    WHERE UPPER(USERNAME) = v_user AND DB_ROLE = 'ROLE_LT';

    IF v_role_count > 0 THEN
        RETURN '1=0';   -- thuoc ROLE_LT -> che cot
    END IF;

    RETURN '1=1';
EXCEPTION
    WHEN OTHERS THEN RETURN '1=0';
END;
/

BEGIN
    DBMS_RLS.DROP_POLICY('PASSPORT_APP', 'PASSPORT_DATA', 'LT_MASKING_POLICY');
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    DBMS_RLS.ADD_POLICY(
        object_schema          => 'PASSPORT_APP',
        object_name            => 'PASSPORT_DATA',
        policy_name            => 'LT_MASKING_POLICY',
        function_schema        => 'SEC_MGR',
        policy_function        => 'LT_MASKING_FUNC',
        statement_types        => 'SELECT',
        sec_relevant_cols      => 'CCCD,HO_TEN',
        sec_relevant_cols_opt  => DBMS_RLS.ALL_ROWS,
        enable                 => TRUE
    );
END;
/

COMMIT;


--==============================================================================
-- PHAN 2: VPD ROW-LEVEL - loc theo MA_TINH_THUONG_TRU = MA_TINH_QUAN_LY cua LT
-- (Dung cot da co san trong APP_USERS tu file 02, khong tao them gi)
--==============================================================================

-- >>> CONN SEC_MGR / 123

CREATE OR REPLACE FUNCTION SEC_MGR.FUNC_LIMIT_PASSPORT_TINH_LT (
    p_schema IN VARCHAR2,
    p_object IN VARCHAR2
) RETURN VARCHAR2
AS
    v_user VARCHAR2(100);
    v_role_count NUMBER;
BEGIN
    v_user := SYS_CONTEXT('USERENV','SESSION_USER');

    SELECT COUNT(*) INTO v_role_count
    FROM PASSPORT_APP.APP_USERS
    WHERE UPPER(USERNAME) = v_user AND DB_ROLE = 'ROLE_LT';

    IF v_role_count > 0 THEN
        RETURN 'MA_TINH_THUONG_TRU = (SELECT MA_TINH_QUAN_LY FROM PASSPORT_APP.APP_USERS WHERE UPPER(USERNAME) = SYS_CONTEXT(''USERENV'',''SESSION_USER''))';
    END IF;

    RETURN '1=1';
EXCEPTION
    WHEN OTHERS THEN RETURN '1=2';
END;
/

BEGIN
    DBMS_RLS.DROP_POLICY('PASSPORT_APP', 'PASSPORT_DATA', 'POLICY_LT_PASSPORT_TINH');
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
    DBMS_RLS.ADD_POLICY(
        object_schema   => 'PASSPORT_APP',
        object_name     => 'PASSPORT_DATA',
        policy_name     => 'POLICY_LT_PASSPORT_TINH',
        function_schema => 'SEC_MGR',
        policy_function => 'FUNC_LIMIT_PASSPORT_TINH_LT',
        statement_types => 'SELECT',
        enable          => TRUE
    );
END;
/

COMMIT;


--==============================================================================
-- PHAN 3: VIEW DANH SACH HO SO (Da luu tru + Da hoan thanh)
--==============================================================================

-- >>> CONN PASSPORT_APP / 123
ALTER SESSION SET CONTAINER = FREEPDB1;

CREATE OR REPLACE VIEW PASSPORT_APP.VW_PASSPORT_LT AS
SELECT
    REG_ID,
    NOI_DUNG_DE_NGHI,
    CO_QUAN_TIEP_NHAN,
    MA_TINH_THUONG_TRU,
    TRANG_THAI,
    THOI_GIAN_TAO
FROM PASSPORT_APP.PASSPORT_DATA
WHERE TRANG_THAI IN ('Da luu tru', 'Da hoan thanh');

GRANT SELECT ON PASSPORT_APP.VW_PASSPORT_LT TO ROLE_LT;

COMMIT;


--==============================================================================
-- PHAN 4: PROCEDURE HOAN TAT LUU TRU (Da luu tru -> Da hoan thanh)
--==============================================================================

-- >>> CONN PASSPORT_APP / 123
ALTER SESSION SET CONTAINER = FREEPDB1;

CREATE OR REPLACE PROCEDURE PASSPORT_APP.PROC_HOAN_TAT_LUU_TRU (
    p_reg_id          IN PASSPORT_APP.PASSPORT_DATA.REG_ID%TYPE,
    p_nguoi_cap_nhat  IN VARCHAR2
) AS
    v_trang_thai_cu PASSPORT_APP.PASSPORT_DATA.TRANG_THAI%TYPE;
BEGIN
    SELECT TRANG_THAI INTO v_trang_thai_cu
    FROM PASSPORT_APP.PASSPORT_DATA
    WHERE REG_ID = p_reg_id;

    IF v_trang_thai_cu != 'Da luu tru' THEN
        RAISE_APPLICATION_ERROR(-20001, 'Chi duoc hoan tat ho so dang o trang thai Da luu tru');
    END IF;

    UPDATE PASSPORT_APP.PASSPORT_DATA
    SET TRANG_THAI = 'Da hoan thanh',
        MAC_LABEL  = CHAR_TO_LABEL('PASSPORT_MAC_POL', 'PUB:LT:TW')
    WHERE REG_ID = p_reg_id;

    INSERT INTO PASSPORT_APP.PASSPORT_REQUEST_HISTORY
        (REG_ID, TRANG_THAI_CU, TRANG_THAI_MOI, NGUOI_CAP_NHAT)
    VALUES
        (p_reg_id, v_trang_thai_cu, 'Da hoan thanh', p_nguoi_cap_nhat);

    COMMIT;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20002, 'Khong tim thay ho so nay');
END PROC_HOAN_TAT_LUU_TRU;
/

GRANT EXECUTE ON PASSPORT_APP.PROC_HOAN_TAT_LUU_TRU TO ROLE_LT;
GRANT SELECT ON PASSPORT_APP.APP_USERS TO ROLE_LT;
COMMIT;


--==============================================================================
-- PHAN 5: KIEM THU (TEST CASES)
-- User lt_nv01 (MA_TINH_QUAN_LY = '01') da duoc tao san tu file 07/08
--==============================================================================

-- >>> CONN lt_nv01 / 123

-- TEST 1: Xem danh sach qua view (Da luu tru + Da hoan thanh, dung tinh, OLS)
SELECT * FROM PASSPORT_APP.VW_PASSPORT_LT;

-- >>> CONN lt_nv02 / 123
SELECT * FROM PASSPORT_APP.VW_PASSPORT_LT;


-- TEST 2: Kiem chung Column Masking 
SELECT REG_ID, CCCD, HO_TEN FROM PASSPORT_APP.PASSPORT_DATA;
-- Ky vong: CCCD, HO_TEN deu RONG

-- TEST 3: Hoan tat thanh cong 1 ho so dang Da luu tru
-- (thay <REG_ID> bang ma ho so thuc te dang co trang thai Da luu tru, vi du 11)
EXEC PASSPORT_APP.PROC_HOAN_TAT_LUU_TRU(11, 'lt_nv01');
SELECT REG_ID, TRANG_THAI FROM PASSPORT_APP.VW_PASSPORT_LT WHERE REG_ID = 11;
-- Ky vong: TRANG_THAI = 'Da hoan thanh'

-- TEST 4: Goi lai lan 2 cho cung REG_ID -> phai bi chan
EXEC PASSPORT_APP.PROC_HOAN_TAT_LUU_TRU(11, 'lt_nv01');
-- Ky vong: ORA-20001: Chi duoc hoan tat ho so dang o trang thai Da luu tru

-- TEST 5: Goi tren ho so dang trang thai khac (vi du Da duyet, REG_ID=3) -> phai bi chan
EXEC PASSPORT_APP.PROC_HOAN_TAT_LUU_TRU(3, 'lt_nv01');
-- Ky vong: ORA-20001 (neu doc duoc) hoac ORA-20002/NO_DATA_FOUND (neu bi OLS/RowPolicy chan truoc)



