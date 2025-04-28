import os
from bs4 import BeautifulSoup
import requests

# Đường dẫn tới tệp HTML
html_file = 'parse_link.html'

# Thư mục tải xuống
download_dir = r'C:\TaiVe'
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# File lưu danh sách các file đã tải
filelist_path = os.path.join(download_dir, 'filelist.txt')

# Đọc danh sách file đã tải nếu tồn tại
downloaded_files = set()
if os.path.exists(filelist_path):
    with open(filelist_path, 'r', encoding='utf-8') as f:
        downloaded_files = set(line.strip() for line in f if line.strip())

# Đảm bảo HTML tồn tại
if os.path.exists(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Lấy các link 'Xem báo cáo'
    urls = [link.get('href') for link in soup.find_all('a', text='Xem báo cáo')]

    # Duyệt ngược
    for url in reversed(urls):
        filename = os.path.basename(url) + '.pdf'

        if filename in downloaded_files:
            print(f'Đã có trong filelist.txt: {filename}, bỏ qua.')
            continue

        try:
            response = requests.get(url)
            response.raise_for_status()
            file_path = os.path.join(download_dir, filename)

            with open(file_path, 'wb') as f:
                f.write(response.content)

            # Ghi thêm tên file vào filelist.txt
            with open(filelist_path, 'a', encoding='utf-8') as f:
                f.write(filename + '\n')

            print(f'Đã tải xuống: {filename}')

        except Exception as e:
            print(f'Lỗi khi tải {url}: {e}')

    print('✅ Hoàn tất quá trình tải file.')
else:
    print('❌ Không tìm thấy file HTML đầu vào.')
