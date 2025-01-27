import os
from bs4 import BeautifulSoup
import requests

# Đường dẫn tới tệp HTML của bạn
html_file = 'parse_link.html'

# Đảm bảo rằng tệp tồn tại
if os.path.exists(html_file):

    # Mở tệp HTML và chuyển đổi nó thành đối tượng BeautifulSoup
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')

    # Lấy tất cả các thẻ 'a' trong HTML và lưu trữ chúng trong một danh sách
    urls = []
    for link in soup.find_all('a', text='Xem file'):
        urls.append(link.get('href'))

    # Thư mục để lưu trữ các tệp đã tải xuống
    download_dir = 'C:\\TaiVe'

    # Đảm bảo rằng thư mục tồn tại
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Tạo một danh sách trung gian để lưu trữ các liên kết còn lại
    remaining_urls = list(urls)

    # Lặp qua các đường dẫn và tải xuống tệp
    for url in urls:
        # Trích xuất tên tệp từ liên kết
        filename = os.path.basename(url)

        # Gửi yêu cầu tải xuống và lưu phản hồi vào tệp trong thư mục download_dir
        response = requests.get(url)
        with open(os.path.join(download_dir, filename), 'wb') as f:
            f.write(response.content)

        print(f'Tải xuống tệp {filename} thành công.')

        # Loại bỏ liên kết đã tải xuống khỏi danh sách
        remaining_urls.remove(url)

    print('Đã tải xuống tất cả các tệp.')
else:
    print('File not found.')
