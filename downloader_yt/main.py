import yt_dlp  # Sử dụng yt-dlp thay cho pytube
import os
import requests


# Đường dẫn đến file chứa danh sách URL
url_list_file = 'urls.txt'
# Đường dẫn đến file để ghi những URL đã tải xuống
downloaded_list_file = 'downloaded.txt'
# Thư mục để lưu video và metadata
download_path = 'videos'

def clean_filename(filename):
    invalid_chars = '<>:"/\\|?*\n'
    return ''.join(c for c in filename if c not in invalid_chars)

def download_youtube_video(video_url, output_path='videos', sound=False):
    try:
        # Cấu hình yt-dlp để tải video hoặc chỉ âm thanh dựa trên tham số đầu vào
        if sound:
            ydl_opts = {
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'format': 'bestaudio/best',  # Tải âm thanh chất lượng cao nhất
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            ydl_opts = {
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'format': 'bestvideo+bestaudio/best',  # Tải video chất lượng cao nhất
            }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(video_url, download=True)
            video_title = result.get('title')
            safe_filename = clean_filename(video_title)
            
            # Xác định tên file đầu ra dựa trên định dạng tải xuống
            output_file_ext = '.mp3' if sound else '.mp4'
            output_file_path = os.path.join(output_path, safe_filename + output_file_ext)

        # Tải thumbnail
        thumbnail_url = result.get('thumbnail')
        if thumbnail_url:
            thumbnail_content = requests.get(thumbnail_url).content
            with open(os.path.join(output_path, safe_filename + '.jpg'), 'wb') as thumb_file:
                thumb_file.write(thumbnail_content)

        # Lưu Title và Description vào file .txt
        description = result.get('description', 'No description available.')
        with open(os.path.join(output_path, safe_filename + '.txt'), 'w', encoding='utf-8') as info_file:
            info_file.write(f"Title: {video_title}\n")
            info_file.write(f"Description: {description}\n")

        file_type = "Âm thanh" if sound else "Video"
        print(f"{file_type} đã được tải về: {output_file_path}")
        return True
    except Exception as e:
        print(f"Lỗi: {str(e)}")
        return False

def process_url_list(sound=False):
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    with open(url_list_file, 'r') as file:
        urls = file.readlines()

    remaining_urls = []

    for url in urls:
        url = url.strip()
        
        if url and download_youtube_video(url, sound=sound):
            with open(downloaded_list_file, 'a') as file_downloaded:
                file_downloaded.write(url + '\n')
        else:
            remaining_urls.append(url)

    with open(url_list_file, 'w') as file:
        file.writelines(remaining_urls)

# Chạy quá trình tải, có thể truyền đối số `sound=True` để chỉ tải âm thanh
process_url_list(sound=False)
