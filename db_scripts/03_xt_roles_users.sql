ALTER SESSION SET CONTAINER = FREEPDB1;

BEGIN EXECUTE IMMEDIATE 'REVOKE EXECUTE ON PASSPORT_APP.PROC_TAO_HO_SO FROM PUBLIC'; EXCEPTION WHEN OTHERS THEN NULL; END;
/

GRANT SELECT ON PASSPORT_APP.APP_USERS TO APP_GUEST;
GRANT EXECUTE ON PASSPORT_APP.PROC_TAO_HO_SO TO ROLE_CD;

UPDATE PASSPORT_APP.APP_USERS
SET PASSWORD_HASH = STANDARD_HASH('123', 'SHA256')
WHERE PASSWORD_HASH = 'hashed_pw';

COMMIT;

-- VPD POLICY_CD_OWN_PASSPORT gioi han cong dan ROLE_CD chi SELECT cac dong PASSPORT_DATA co CCCD trung voi username cd_<cccd>.
-- Chay phan function, drop policy va add policy nay bang user SEC_MGR.
CREATE OR REPLACE FUNCTION SEC_MGR.FUNC_CD_OWN_PASSPORT (
    p_schema IN VARCHAR2,
    p_object IN VARCHAR2
)
RETURN VARCHAR2
AS
    v_user VARCHAR2(100);
    v_cccd VARCHAR2(12);
BEGIN
    v_user := LOWER(SYS_CONTEXT('USERENV', 'SESSION_USER'));
    v_cccd := SUBSTR(v_user, 4);

    IF SUBSTR(v_user, 1, 3) = 'cd_' AND REGEXP_LIKE(v_cccd, '^[0-9]{12}$') THEN
        RETURN 'CCCD = ''' || v_cccd || '''';
    END IF;

    RETURN '1=1';
END;
/

BEGIN
    DBMS_RLS.DROP_POLICY(
        object_schema => 'PASSPORT_APP',
        object_name   => 'PASSPORT_DATA',
        policy_name   => 'POLICY_CD_OWN_PASSPORT'
    );
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

BEGIN
    DBMS_RLS.ADD_POLICY(
        object_schema   => 'PASSPORT_APP',
        object_name     => 'PASSPORT_DATA',
        policy_name     => 'POLICY_CD_OWN_PASSPORT',
        function_schema => 'SEC_MGR',
        policy_function => 'FUNC_CD_OWN_PASSPORT',
        statement_types => 'SELECT',
        enable          => TRUE
    );
END;
/

-- VPD POLICY_CD_OWN_HISTORY gioi han cong dan ROLE_CD chi SELECT lich su cua cac ho so co CCCD trung voi username cd_<cccd>.
-- Chay phan function, drop policy va add policy nay bang user SEC_MGR.
CREATE OR REPLACE FUNCTION SEC_MGR.FUNC_CD_OWN_HISTORY (
    p_schema IN VARCHAR2,
    p_object IN VARCHAR2
)
RETURN VARCHAR2
AS
    v_user VARCHAR2(100);
    v_cccd VARCHAR2(12);
BEGIN
    v_user := LOWER(SYS_CONTEXT('USERENV', 'SESSION_USER'));
    v_cccd := SUBSTR(v_user, 4);

    IF SUBSTR(v_user, 1, 3) = 'cd_' AND REGEXP_LIKE(v_cccd, '^[0-9]{12}$') THEN
        RETURN 'REG_ID IN (
            SELECT REG_ID
            FROM PASSPORT_APP.PASSPORT_DATA
            WHERE CCCD = ''' || v_cccd || '''
        )';
    END IF;

    RETURN '1=1';
END;
/

BEGIN
    DBMS_RLS.DROP_POLICY(
        object_schema => 'PASSPORT_APP',
        object_name   => 'PASSPORT_REQUEST_HISTORY',
        policy_name   => 'POLICY_CD_OWN_HISTORY'
    );
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

BEGIN
    DBMS_RLS.ADD_POLICY(
        object_schema   => 'PASSPORT_APP',
        object_name     => 'PASSPORT_REQUEST_HISTORY',
        policy_name     => 'POLICY_CD_OWN_HISTORY',
        function_schema => 'SEC_MGR',
        policy_function => 'FUNC_CD_OWN_HISTORY',
        statement_types => 'SELECT',
        enable          => TRUE
    );
END;
/

COMMIT;

EXIT;
