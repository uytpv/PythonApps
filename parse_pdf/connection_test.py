import mysql.connector
from mysql.connector import Error
import configparser

# Đọc thông tin kết nối từ file config.ini
config = configparser.ConfigParser()
config.read('config.ini')

host = config['mysql']['host']
port = config['mysql']['port']
database = config['mysql']['database']
user = config['mysql']['user']
password = config['mysql']['password']

try:
    # Thực hiện kết nối đến CSDL
    connection = mysql.connector.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    if connection.is_connected():
        print(f"Kết nối thành công đến CSDL: {connection.get_server_info()}")

except Error as e:
    print(f"Lỗi kết nối CSDL: {e}")

finally:
    if 'connection' in locals():
        connection.close()
        print("Đóng kết nối CSDL.")
