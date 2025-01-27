import os
import yt_dlp

# Đường dẫn đến file chứa danh sách URL
url_list_file = 'urls.txt'
# Đường dẫn đến file để ghi những URL đã tải xuống
downloaded_list_file = 'downloaded.txt'
# Thư mục để lưu video
download_path = 'videos'

def download_video(url):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(download_path, '%(id)s.%(ext)s'),
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_id = info_dict.get('id', None)
            if video_id:
                ydl.download([url])
                return True, video_id
            else:
                return False, None
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False, None

def process_url_list():
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    with open(url_list_file, 'r') as file:
        urls = file.readlines()

    remaining_urls = []
    downloaded_urls = []

    for url in urls:
        url = url.strip()
        if url:
            success, video_id = download_video(url)
            if success:
                print(f"Downloaded video {video_id} from {url}")
                downloaded_urls.append(url)
            else:
                remaining_urls.append(url)

    with open(url_list_file, 'w') as file:
        for url in remaining_urls:
            file.write(url + '\n')

    with open(downloaded_list_file, 'a') as file:
        for url in downloaded_urls:
            file.write(url + '\n')

if __name__ == "__main__":
    process_url_list()
