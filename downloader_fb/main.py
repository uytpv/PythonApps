import yt_dlp
import os
import requests
from datetime import datetime

# Đường dẫn đến file chứa danh sách URL
url_list_file = 'fb_urls.txt'
# Đường dẫn đến file để ghi những URL đã tải xuống
downloaded_list_file = 'fb_downloaded.txt'
# Thư mục để lưu video và metadata
download_path = 'fb_videos'

def clean_filename(filename):
    """Làm sạch tên file để tránh lỗi khi lưu."""
    # Loại bỏ emoji và ký tự đặc biệt
    import unicodedata
    
    # Loại bỏ ký tự kiểm soát và emoji
    filename = ''.join(c if ord(c) >= 32 else '' for c in filename)
    
    # Loại bỏ emoji (ký tự Unicode cao)
    filename = ''.join(c if ord(c) < 0x1F300 else '' for c in filename)
    
    # Loại bỏ ký tự không hợp lệ trên Windows
    invalid_chars = '<>:"/\\|?*\n\t'
    filename = ''.join(c if c not in invalid_chars else '' for c in filename)
    
    # Loại bỏ khoảng trắng liên tiếp
    filename = ' '.join(filename.split())
    
    # Cắt tên file nếu quá dài (giới hạn 100 ký tự)
    filename = filename[:100].strip()
    
    # Nếu tên file rỗng, dùng tên mặc định với ngày tháng năm và giờ phút giây
    if not filename or filename.isspace():
        filename = f"facebook_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    return filename

def download_facebook_video(video_url, output_path='fb_videos'):
    """Tải video từ Facebook bằng yt-dlp (hỗ trợ Reels, Posts, Groups)."""
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Cấu hình yt-dlp để tải video từ Facebook
        # Sử dụng ID làm tên file tạm để tránh lỗi ký tự không hợp lệ
        ydl_opts = {
            'outtmpl': os.path.join(output_path, '%(id)s.%(ext)s'),
            'format': 'best',  # Lấy định dạng tốt nhất có sẵn
            'quiet': False,
            'no_warnings': False,
            'socket_timeout': 30,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"🔄 Đang tải: {video_url}")
            info = ydl.extract_info(video_url, download=True)
            
            # Lấy thông tin video
            video_id = info.get('id', 'unknown')
            video_ext = info.get('ext', 'mp4')
            video_title = info.get('title', 'unknown_title')
            
            # Làm sạch tên file
            safe_filename = clean_filename(video_title)
            
            # Tệp tạm được tải xuống với tên ID
            temp_file = os.path.join(output_path, f"{video_id}.{video_ext}")
            
            # Tên file cuối cùng
            final_file = os.path.join(output_path, f"{safe_filename}.{video_ext}")
            
            # Đổi tên file từ ID sang tên được làm sạch
            if os.path.exists(temp_file):
                if os.path.exists(final_file):
                    # Nếu file đã tồn tại, thêm timestamp
                    final_file = os.path.join(output_path, f"{safe_filename}_{datetime.now().strftime('%H%M%S')}.{video_ext}")
                os.rename(temp_file, final_file)
            
            output_file = final_file

        print(f"✅ Tải thành công: {output_file}")
        return True

    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        # Xử lý một số lỗi phổ biến
        if 'This video is not available' in error_msg:
            print(f"⚠️ Video không khả dụng hoặc bị xóa: {video_url}")
        elif 'Signature extraction failed' in error_msg:
            print(f"⚠️ Lỗi xác thực Facebook: {video_url}")
        else:
            print(f"❌ Lỗi tải video: {error_msg}")
        return False
    except Exception as e:
        print(f"⚠️ Lỗi không xác định: {str(e)}")
        return False

def xoa_url(filename, string):
    """Xóa URL đã tải khỏi danh sách chờ."""
    try:
        with open(filename, "r", encoding='utf-8') as f:
            lines = f.readlines()

        with open(filename, "w", encoding='utf-8') as f:
            for line in lines:
                if string not in line:
                    f.write(line)
    except FileNotFoundError:
        print(f"File '{filename}' không tồn tại.")
    except Exception as e:
        print(f"Lỗi khi xử lý file: {e}")

def ghi_url(filename, string):
    """Ghi URL đã tải vào danh sách đã tải."""
    try:
        with open(filename, "a", encoding='utf-8') as f:
            f.write(string + '\n')
    except Exception as e:
        print(f"Lỗi khi ghi file: {e}")

def exist(filename, string):
    """Kiểm tra nếu URL đã tải rồi."""
    try:
        with open(filename, "r", encoding='utf-8') as f:
            for line in f:
                if string in line:
                    print(f"ℹ️ URL '{string}' đã tải rồi")
                    return True
        return False
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"Lỗi khi kiểm tra file: {e}")
        return False

def process_url_list():
    """Xử lý danh sách URL từ file."""
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    try:
        if not os.path.exists(url_list_file):
            print(f"⚠️ File '{url_list_file}' không tồn tại. Tạo file mới...")
            with open(url_list_file, 'w', encoding='utf-8') as f:
                f.write("")
            print(f"Vui lòng thêm URL vào file '{url_list_file}' và chạy lại.")
            return

        with open(url_list_file, 'r', encoding='utf-8') as file:
            urls = file.readlines()

        if not urls:
            print(f"⚠️ File '{url_list_file}' trống. Vui lòng thêm URL vào.")
            return

        print(f"📋 Tổng số URL: {len(urls)}")
        print(f"⏰ Bắt đầu tải lúc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        downloaded_count = 0
        for idx, url in enumerate(urls, 1):
            url = url.strip()
            if not url:
                continue

            print(f"[{idx}/{len(urls)}] ", end="")
            if not exist(downloaded_list_file, url):
                if download_facebook_video(url, download_path):
                    ghi_url(downloaded_list_file, url)
                    xoa_url(url_list_file, url)
                    downloaded_count += 1
            else:
                xoa_url(url_list_file, url)

        print(f"\n✨ Hoàn thành! Đã tải {downloaded_count} video.")
        print(f"⏰ Kết thúc lúc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    except Exception as e:
        print(f"❌ Lỗi trong quá trình xử lý danh sách URL: {e}")

if __name__ == "__main__":
    process_url_list()