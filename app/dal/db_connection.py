import oracledb
import config

# Thiết lập kết nối đến Oracle Database theo chế độ Thin mode.
def get_db_connection(username, password):
    dsn_str = f"{config.DB_HOST}:{config.DB_PORT}/{config.DB_SERVICE}"
    
    try:
        connection = oracledb.connect(
            user=username,
            password=password,
            dsn=dsn_str
        )
        return connection
    except oracledb.DatabaseError as e:
        raise Exception(f"Lỗi kết nối CSDL: {str(e)}")