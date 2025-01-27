from bs4 import BeautifulSoup
import os

def extract_custom_urls(html_file, output_file):
    # Lấy đường dẫn tuyệt đối đến file HTML
    html_file_path = os.path.join(os.path.dirname(__file__), html_file)

    with open(html_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    urls_and_titles = []

    for link in soup.find_all('a', href=True, class_='cursor-pointer'):
        href = link['href']
        if '/video/' in href:
            youtube_url = f'https://www.ganjingworld.com{href}'
            title_tag = link.find('h3', class_='postTitle')
            
            # Kiểm tra xem thẻ <h3> có tồn tại không
            if title_tag:
                title = title_tag.text.strip()
            else:
                title = "N/A"  # Nếu không tìm thấy, gán giá trị mặc định

            channel_tag = link.find('a', class_='channelName')

            # Kiểm tra xem thẻ <a> có tồn tại không
            if channel_tag:
                channel_name = channel_tag.text.strip()
            else:
                channel_name = "N/A"  # Nếu không tìm thấy, gán giá trị mặc định

            # Kiểm tra xem thẻ <span> có tồn tại không
            views_tag = link.find('span', class_='metaItem dotAfter')
            if views_tag:
                views = views_tag.text.strip().split()[0]
            else:
                views = "N/A"  # Nếu không tìm thấy, gán giá trị mặc định

            # Kiểm tra xem thẻ <span> có tồn tại không
            time_ago_tag = link.find('span', class_='metaItem')
            if time_ago_tag:
                time_ago = time_ago_tag.text.strip()
            else:
                time_ago = "N/A"  # Nếu không tìm thấy, gán giá trị mặc định

            # Tạo một tuple chứa thông tin
            info_tuple = (youtube_url, title, channel_name, views, time_ago)

            # Thêm tuple vào mảng
            urls_and_titles.append(info_tuple)

    # Lưu thông tin vào file
    with open(output_file, 'w', encoding='utf-8') as out_file:
        for url_info in urls_and_titles:
            out_file.write('\t'.join(url_info) + '\n')

# Đường dẫn tới file HTML của bạn
html_file_name = 'uy_nhac.html'

# File đầu ra chứa các URL
output_file_name = 'urls.txt'

extract_custom_urls(html_file_name, output_file_name)
