# passport_management_system

passport_management_system/
|-- db_scripts/
|   |-- 01_init_tables.sql
|   |-- 02_insert_data_and_proc.sql
|   |-- 03_xt_roles_users.sql
|   |-- 04_xd_vpd_policy.sql
|   |-- 05_lt_masking_policy.sql
|   |-- 06_gs_audit_policy.sql
|-- app/
|   |-- main.py
|   |-- config.py
|   |-- dal/
|   |   |-- db_connection.py
|   |   |-- user_dal.py
|   |   |-- xt_dal.py
|   |   |-- xd_dal.py
|   |   |-- lt_dal.py
|   |   |-- gs_dal.py
|   |-- bll/
|   |   |-- auth_bll.py
|   |   |-- xt_bll.py
|   |   |-- xd_bll.py
|   |   |-- lt_bll.py
|   |   |-- gs_bll.py
|   |-- ui/
|   |   |-- login_view.py
|   |   |-- register_view.py
|   |   |-- xt_view.py
|   |   |-- xd_view.py
|   |   |-- lt_view.py
|   |   |-- gs_view.py
|-- file_storage/
|-- docker-compose.yml