import mysql.connector
import configparser
from mysql.connector import Error


class MySQLDatabase:
    def __init__(self):
        # Đọc cấu hình từ file
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        # Lấy thông tin kết nối từ file cấu hình
        self.host = self.config['mysql']['host']
        self.port = self.config['mysql']['port']
        self.database = self.config['mysql']['database']
        self.user = self.config['mysql']['user']
        self.password = self.config['mysql']['password']

    def connect(self):
        try:
            # Thực hiện kết nối đến CSDL
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print(
                    f"Kết nối thành công đến CSDL: {self.connection.get_server_info()}")
                # Khởi tạo một cursor
                self.cursor = self.connection.cursor(buffered=True)

        except Error as e:
            print(f"Lỗi kết nối CSDL: {e}")

    def execute_query(self, query, data=None):
        # Thực hiện truy vấn SQL
        try:
            if data:
                self.cursor.execute(query, data)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return self.cursor
        except Exception as e:
            print("Lỗi:", str(e))
            self.connection.rollback()
            return None

    def fetch_data(self, query, data=None):
        # Lấy dữ liệu từ truy vấn SQL
        cursor = self.execute_query(query, data)
        if cursor:
            return cursor.fetchall()
        else:
            return []

    def insert_data(self, query, data):
        # Chèn dữ liệu vào cơ sở dữ liệu
        return self.execute_query(query, data)

    def update_data(self, query, data):
        # Cập nhật dữ liệu trong cơ sở dữ liệu
        return self.execute_query(query, data)

    def delete_data(self, query, data):
        # Xóa dữ liệu từ cơ sở dữ liệu
        return self.execute_query(query, data)

    def close(self):
        # Đóng kết nối
        self.cursor.close()
        self.connection.close()

    def clear_results(self):
        if self.cursor:
            self.cursor.fetchall()  # Đọc hết kết quả còn lại
