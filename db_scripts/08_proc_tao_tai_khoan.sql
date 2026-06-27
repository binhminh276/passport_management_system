/* Thu tuc tao tai khoan tu dong co ho tro cap dac quyen OLS */
ALTER SESSION SET CONTAINER = FREEPDB1;

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
BEGIN
    INSERT INTO PASSPORT_APP.APP_USERS (USERNAME, PASSWORD_HASH, DB_ROLE, IS_ACTIVE)
    VALUES (p_username, p_password_hash, p_db_role, 1);

    EXECUTE IMMEDIATE 'CREATE USER ' || DBMS_ASSERT.ENQUOTE_NAME(p_username, FALSE) || ' IDENTIFIED BY "' || p_raw_password || '"';
    EXECUTE IMMEDIATE 'GRANT CONNECT TO ' || DBMS_ASSERT.ENQUOTE_NAME(p_username, FALSE);
    EXECUTE IMMEDIATE 'GRANT ' || DBMS_ASSERT.ENQUOTE_NAME(p_db_role, FALSE) || ' TO ' || DBMS_ASSERT.ENQUOTE_NAME(p_username, FALSE);

    IF p_db_role = 'ROLE_CD' THEN
        v_label := 'CONF:XT:TW';
    ELSIF p_db_role = 'ROLE_XT' THEN
        v_label := 'CONF:XT:TW';
        v_privs := 'WRITEUP';
    ELSIF p_db_role = 'ROLE_XD' THEN
        v_label := 'CONF:XD:TW';
        v_privs := 'WRITEDOWN';
    ELSIF p_db_role = 'ROLE_LT' THEN
        v_label := 'PUB:LT:TW';
    ELSIF p_db_role = 'ROLE_GS' THEN
        v_label := 'SEC:XT,XD,LT:TW';
    END IF;

    IF v_label IS NOT NULL THEN
        SA_USER_ADMIN.SET_USER_LABELS(
            policy_name     => 'PASSPORT_MAC_POL',
            user_name       => p_username,
            max_read_label  => v_label,
            max_write_label => v_label,
            def_label       => v_label,
            row_label       => v_label
        );
    END IF;
    
    IF v_privs IS NOT NULL THEN
        SA_USER_ADMIN.SET_USER_PRIVS(
            policy_name => 'PASSPORT_MAC_POL',
            user_name   => UPPER(p_username),
            privileges  => v_privs
        );
    END IF;
END;
/

GRANT EXECUTE ON SEC_MGR.PROC_TAO_TAI_KHOAN TO APP_GUEST;