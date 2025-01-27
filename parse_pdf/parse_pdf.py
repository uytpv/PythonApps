import fitz
import mysql.connector
from models.map import Map

from mysql_database import MySQLDatabase


def writeFile(fileName, str):  # Hàm ghi file
    with open(fileName, "w", encoding="UTF-8") as file:
        file.write(str)


def xuLyXuongDong(text):
    lines = text.split('\n')  # Tách văn bản thành các dòng
    i = 0
    while i < len(lines) - 1:
        # Kiểm tra xem dòng hiện tại có "." ở cuối không và dòng tiếp theo có đủ dài không
        if not lines[i].endswith('.') and (len(lines[i + 1]) > 0 and not lines[i + 1][0].isdigit() and not lines[i + 1][0].isupper()):
            # Nếu không có "." ở cuối và dòng tiếp theo không bắt đầu bằng số hoặc ký tự viết hoa
            # Nối dòng tiếp theo vào dòng hiện tại
            lines[i] = lines[i] + ' ' + lines[i + 1]
            lines.pop(i + 1)  # Xoá dòng tiếp theo
        else:
            i += 1
    result = '\n'.join(lines)  # Nối lại thành văn bản mới
    return result


doc = fitz.open('example.pdf')  # or fitz.Document(filename)

page = doc.load_page(15)
pageContent = xuLyXuongDong(page.get_text('text'))

for line in pageContent:
    map = Map(
        life_path=22,
        balance=3,
        expression=1,
        lpe_bridge=3,
        heart_desire=9,
        birthday=8,
        personality=1,
        hdp_bridge=8,
        maturity=5,
        karmic_lessons=[4, 6],
        rational_thought=3,
        subconscious_confidence=7,
        hidden_passion=[5, 6],
        challenge=[0, 2, 2, 2],
        pinnacle=[7, 5, 3, 5],
        year=[2, 3, 4, 5, 6],
        month=[7, 6, 7]
    )


# Khởi tạo class Database
db = MySQLDatabase()
# Thử kết nối
db.connect()

# Viết câu truy vấn SELECT với điều kiện
query = "SELECT * FROM indicator_number WHERE indicator = %s AND number = %s"
data = ('life_path', 7)

# Thực hiện truy vấn SELECT
result = db.fetch_data(query, data)
# Đảm bảo rằng đã đọc hết kết quả trước
db.clear_results()
if result:
    print("Dữ liệu được tìm thấy:")
    for row in result:
        print(row)
else:
    print("Không tìm thấy dữ liệu thỏa mãn điều kiện.")

# Đóng kết nối với cơ sở dữ liệu
db.close()

writeFile('parse_pdf.txt', pageContent)
