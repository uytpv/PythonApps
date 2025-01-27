import os
import subprocess

# Đường dẫn đến thư mục chứa các tệp HTML
input_folder = r'C:\Users\UY\Downloads\KinhVan'

# Đường dẫn đến thư mục đầu ra cho các tệp EPUB
output_folder = r'C:\Users\UY\Downloads\KinhVanEPUB'

# Đường dẫn đến thư viện Calibre
calibre_path = r'C:\Program Files\Calibre2\ebook-convert.exe'  # Lưu ý thay đổi đường dẫn

# Thông tin tác giả (author)
author = 'Lý Hồng Chí'

# Tạo thư mục đầu ra nếu nó chưa tồn tại
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Lấy danh sách tất cả các tệp HTML trong thư mục đầu vào
html_files = [f for f in os.listdir(input_folder) if f.endswith('.html')]

# Tạo danh sách các tệp EPUB đã chuyển đổi
converted_epubs = []

# Chuyển đổi từng tệp HTML thành tệp EPUB nếu chưa được chuyển đổi
for html_file in html_files:
    epub_file = html_file.replace('.html', '.epub')
    
    if epub_file not in converted_epubs:
        html_path = os.path.join(input_folder, html_file)
        title = os.path.splitext(html_file)[0]  # Sử dụng tên tệp (không bao gồm phần mở rộng) làm tiêu đề
        epub_path = os.path.join(output_folder, epub_file)
        
        # Sử dụng Calibre để chuyển đổi, thêm thông tin tác giả và tiêu đề
        command = [
            calibre_path,
            html_path,
            epub_path,
            '--authors', author,
            '--title', title
        ]
        
        try:
            subprocess.run(command, check=True)
            print(f'Đã chuyển đổi {html_file} thành {epub_file}')
        except subprocess.CalledProcessError as e:
            print(f'Lỗi khi chuyển đổi {html_file}: {e}')
    else:
        print(f'{html_file} đã được chuyển đổi trước đó.')

print('Hoàn thành chuyển đổi.')
