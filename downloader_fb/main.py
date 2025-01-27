import yt_dlp  # Sử dụng yt-dlp để tải video từ Facebook
import os
import requests

# Đường dẫn đến file chứa danh sách URL
url_list_file = 'fb_urls.txt'
# Đường dẫn đến file để ghi những URL đã tải xuống
downloaded_list_file = 'fb_downloaded.txt'
# Thư mục để lưu video và metadata
download_path = 'fb_videos'

def clean_filename(filename):
    invalid_chars = '<>:"/\\|?*\n'
    return ''.join(c for c in filename if c not in invalid_chars)

def download_facebook_video(video_url, output_path='fb_videos'):
    try:
        # Cấu hình yt-dlp để tải video từ Facebook
        ydl_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'format': 'bestvideo+bestaudio/best',
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"Downloaded: {video_url}")
    except Exception as e:
        print(f"Error downloading {video_url}: {e}")

def main():
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    if not os.path.exists(url_list_file):
        print(f"URL list file not found: {url_list_file}")
        return

    with open(url_list_file, 'r') as f:
        urls = f.readlines()

    downloaded_urls = set()
    if os.path.exists(downloaded_list_file):
        with open(downloaded_list_file, 'r') as f:
            downloaded_urls = set(f.read().splitlines())

    for url in urls:
        url = url.strip()
        if url and url not in downloaded_urls:
            download_facebook_video(url)
            with open(downloaded_list_file, 'a') as f:
                f.write(url + '\n')

if __name__ == "__main__":
    main()