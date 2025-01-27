from bs4 import BeautifulSoup
import re

def extract_youtube_urls(html_file, output_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    youtube_url_pattern = re.compile(r'/watch\?v=([\w-]+)')
    # youtube_url_pattern = re.compile(r'/shorts/([\w-]+)')

    unique_urls = set()

    for link in soup.find_all('a', href=True):
        href = link['href']
        match = youtube_url_pattern.match(href)
        if match:
            video_id = match.group(1)
            youtube_url = f'https://www.youtube.com/watch?v={video_id}'
            # youtube_url = f'https://www.youtube.com/short/{video_id}'
            unique_urls.add(youtube_url)

    with open(output_file, 'w', encoding='utf-8') as out_file:
        for url in unique_urls:
            out_file.write(url + '\n')

# Đường dẫn tới file HTML của bạn
html_file_path = 'uy_nhac.html'

# File đầu ra chứa các URL
output_file_path = 'urls.txt'

extract_youtube_urls(html_file_path, output_file_path)