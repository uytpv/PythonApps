from bs4 import BeautifulSoup
import re

def extract_tiktok_urls(html_file, output_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    tiktok_url_pattern = re.compile(r'https://www.tiktok.com/@\w+/video/\d+')
    unique_urls = set()

    for link in soup.find_all('a', href=True):
        href = link['href']
        if tiktok_url_pattern.match(href):
            unique_urls.add(href)

    with open(output_file, 'w', encoding='utf-8') as out_file:
        for url in unique_urls:
            out_file.write(url + '\n')

# Đường dẫn tới file HTML của bạn
html_file_path = 'nguyenphonglaws_20240117.html'

# File đầu ra chứa các URL
output_file_path = 'urls.txt'

extract_tiktok_urls(html_file_path, output_file_path)
