import re

# Đọc nội dung tệp
with open('page_source.html', 'r', encoding='utf-8') as file:
    content = file.read()

# Tìm tất cả các ID dạng tt1234567
ids = re.findall(r'tt\d{7}', content)

# In kết quả
if ids:
    print("Các ID tìm thấy:", ids)
else:
    print("Không tìm thấy ID nào.")