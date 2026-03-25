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
    """Làm sạch tên file để tránh lỗi khi lưu."""
    invalid_chars = '<>:"/\\|?*\n'
    return ''.join(c for c in filename if c not in invalid_chars).strip()

def download_youtube_video(video_url, output_path='videos', sound=False):
    """Tải video hoặc âm thanh từ YouTube bằng yt-dlp."""
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Cấu hình yt-dlp
        if sound:
            ydl_opts = {
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            output_file_ext = '.mp3'
        else:
            ydl_opts = {
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'noplaylist': True,
            }
            output_file_ext = '.mp4'

        # Show yt-dlp version
        try:
            ytdlp_version = getattr(yt_dlp, '__version__', None)
            if ytdlp_version:
                print(f"yt-dlp version: {ytdlp_version}")
        except Exception:
            pass

        # Tải video - try primary options, then retry with a simpler format if not available
        result = None
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(video_url, download=True)


        except yt_dlp.utils.DownloadError as e:
            errmsg = str(e)
            # If we hit a 403 Forbidden, try using cookies from browser
            if 'HTTP Error 403' in errmsg:
                print('⚠️ 403 Forbidden detected. Retrying with browser cookies (Chrome)...')
                cookie_opts = ydl_opts.copy()
                cookie_opts['cookiesfrombrowser'] = ('chrome', )
                try:
                    with yt_dlp.YoutubeDL(cookie_opts) as ydl:
                        result = ydl.extract_info(video_url, download=True)
                except Exception as cookie_e:
                    print(f"❌ Failed even with cookies: {str(cookie_e)}")
                    raise e # Re-raise original error if cookie attempt fails
            elif 'Requested format is not available' in errmsg or 'Signature extraction failed' in errmsg or 'has no valid formats' in errmsg:
                 print('⚠️ Primary format failed, retrying with a more permissive format...')
                 fallback_opts = ydl_opts.copy()
                 fallback_opts['format'] = 'bestvideo+bestaudio/best'
                 with yt_dlp.YoutubeDL(fallback_opts) as ydl:
                     result = ydl.extract_info(video_url, download=True)
            else:
                raise

        # Lấy thông tin video sau khi download thành công
        video_title = result.get('title', 'unknown_title')
        safe_filename = clean_filename(video_title)
        output_file_path = os.path.join(output_path, safe_filename + output_file_ext)

        # Kiểm tra nếu tệp đã tồn tại
        if os.path.exists(output_file_path):
            print(f"📂 Tệp đã tồn tại: {output_file_path}")
            return True

        # Tải ảnh thumbnail
        thumbnail_url = result.get('thumbnail')
        if thumbnail_url:
            try:
                thumbnail_content = requests.get(thumbnail_url).content
                with open(os.path.join(output_path, safe_filename + '.jpg'), 'wb') as thumb_file:
                    thumb_file.write(thumbnail_content)
            except requests.RequestException as e:
                print(f"⚠️ Lỗi tải thumbnail: {str(e)}")

        # Lưu thông tin metadata (tiêu đề, mô tả)
        description = result.get('description', 'Không có mô tả.')
        with open(os.path.join(output_path, safe_filename + '.txt'), 'w', encoding='utf-8') as info_file:
            info_file.write(f"🎬 Title: {video_title}\n")
            info_file.write(f"📄 Description: {description}\n")

        file_type = "🎵 Âm thanh" if sound else "📹 Video"
        print(f"✅ {file_type} đã được tải về: {output_file_path}")
        return True

    except yt_dlp.utils.DownloadError as e:
        print(f"❌ Lỗi tải video: {str(e)}")
    except Exception as e:
        print(f"⚠️ Lỗi không xác định: {str(e)}")
    return False

#xóa url đã download ra khỏi danh sách chờ download urls.txt
def xoa_url(filename, string):
    try:
        with open(filename, "r") as f:
            lines = f.readlines()

        with open(filename, "w") as f:
            for line in lines:
                if string not in line:
                    f.write(line)
    except FileNotFoundError:
        print(f"File '{filename}' không tồn tại.")
    except Exception as e:
        print(f"Lỗi khi xử lý file: {e}")

#ghi url đã download thành công vào file downloaded.txt
def ghi_ulr(filename, string):
    with open(filename, "a") as f:
        f.write(string + '\n')

#kiểm tra nếu url đã có trong downloaded.txt thì không download nữa
def exist(filename, string):
    try:
        with open(filename, "r") as f:
            for line in f:
                if string in line:
                    print(f"url '{string}' đã download rồi")
                    return True
            return False
    except FileNotFoundError:
        print(f"File '{filename}' không tồn tại.")
        return False
    except Exception as e:  # Bắt thêm lỗi chung
        print(f"Lỗi khi kiểm tra file: {e}")
        return False

def process_url_list(sound):
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    try:  # Bọc toàn bộ quá trình xử lý file để bắt lỗi
        with open(url_list_file, 'r') as file:
            urls = file.readlines()

        for url in urls:
            url = url.strip()
            if not exist(downloaded_list_file, url):
                if url and download_youtube_video(url, sound=sound):
                    ghi_ulr(downloaded_list_file, url)
                    xoa_url(url_list_file, url)
            else:
                xoa_url(url_list_file, url)

    except FileNotFoundError:
        print(f"File '{url_list_file}' không tồn tại.")
    except Exception as e:  # Bắt lỗi chung cho toàn bộ quá trình
        print(f"Lỗi trong quá trình xử lý danh sách URL: {e}")

if __name__ == "__main__":
    # Chạy quá trình tải, có thể truyền đối số `sound=True` để chỉ tải âm thanh
    process_url_list(sound=False)