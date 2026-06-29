ALTER SESSION SET CONTAINER = FREEPDB1;

PROMPT Phan 1: Chay bang SYS AS SYSDBA hoac LBACSYS sau khi chay 07_mac_ols_policy.sql.
PROMPT Muc dich: cap quyen OLS de APP_GUEST goi procedure tao tai khoan khong bi ORA-12407.
GRANT PASSPORT_MAC_POL_DBA TO APP_GUEST;

PROMPT Phan 2: Chay bang SEC_MGR sau khi chay 08_proc_tao_tai_khoan.sql.
PROMPT Muc dich: chuan hoa username/role khi tao DB user va gan OLS label de tranh ORA-12406.
CREATE OR REPLACE PROCEDURE SEC_MGR.PROC_TAO_TAI_KHOAN (
    p_username IN VARCHAR2,
    p_raw_password IN VARCHAR2,
    p_password_hash IN VARCHAR2,
    p_db_role IN VARCHAR2
)
AUTHID DEFINER
AS
    v_label VARCHAR2(50);
    v_privs VARCHAR2(50);
    v_username VARCHAR2(50);
    v_db_role VARCHAR2(50);
BEGIN
    v_username := UPPER(TRIM(p_username));
    v_db_role := UPPER(TRIM(p_db_role));

    INSERT INTO PASSPORT_APP.APP_USERS (USERNAME, PASSWORD_HASH, DB_ROLE, IS_ACTIVE)
    VALUES (LOWER(TRIM(p_username)), p_password_hash, v_db_role, 1);

    EXECUTE IMMEDIATE 'CREATE USER ' || DBMS_ASSERT.SIMPLE_SQL_NAME(v_username) || ' IDENTIFIED BY "' || p_raw_password || '"';
    EXECUTE IMMEDIATE 'GRANT CONNECT TO ' || DBMS_ASSERT.SIMPLE_SQL_NAME(v_username);
    EXECUTE IMMEDIATE 'GRANT ' || DBMS_ASSERT.SIMPLE_SQL_NAME(v_db_role) || ' TO ' || DBMS_ASSERT.SIMPLE_SQL_NAME(v_username);

    IF v_db_role = 'ROLE_CD' THEN
        v_label := 'CONF:XT:TW';
    ELSIF v_db_role = 'ROLE_XT' THEN
        v_label := 'CONF:XT:TW';
        v_privs := 'WRITEUP';
    ELSIF v_db_role = 'ROLE_XD' THEN
        v_label := 'CONF:XD:TW';
        v_privs := 'WRITEDOWN';
    ELSIF v_db_role = 'ROLE_LT' THEN
        v_label := 'PUB:LT:TW';
    ELSIF v_db_role = 'ROLE_GS' THEN
        v_label := 'SEC:XT,XD,LT:TW';
    END IF;

    IF v_label IS NOT NULL THEN
        SA_USER_ADMIN.SET_USER_LABELS(
            policy_name     => 'PASSPORT_MAC_POL',
            user_name       => v_username,
            max_read_label  => v_label,
            max_write_label => v_label,
            def_label       => v_label,
            row_label       => v_label
        );
    END IF;

    IF v_privs IS NOT NULL THEN
        SA_USER_ADMIN.SET_USER_PRIVS(
            policy_name => 'PASSPORT_MAC_POL',
            user_name   => v_username,
            privileges  => v_privs
        );
    END IF;
END;
/

GRANT EXECUTE ON SEC_MGR.PROC_TAO_TAI_KHOAN TO APP_GUEST;
