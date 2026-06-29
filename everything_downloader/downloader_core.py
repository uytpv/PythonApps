import yt_dlp
import os
import re
from datetime import datetime
from typing import Callable, Optional

class DownloaderCore:
    """Module tải video từ YouTube và Facebook"""
    
    def __init__(self, output_path: str = 'videos', log_callback: Optional[Callable] = None):
        """
        Khởi tạo downloader
        
        Args:
            output_path: Thư mục lưu video
            log_callback: Hàm callback để hiển thị log
        """
        self.output_path = output_path
        self.log_callback = log_callback
        
        # Tạo thư mục nếu không tồn tại
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
    
    def log(self, message: str):
        """Ghi log"""
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)
    
    def detect_url_type(self, url: str) -> str:
        """
        Xác định loại URL (youtube, facebook, hoặc unknown)
        
        Returns:
            'youtube', 'facebook', hoặc 'unknown'
        """
        url = url.lower()
        if 'youtube.com' in url or 'youtu.be' in url:
            return 'youtube'
        elif 'facebook.com' in url or 'fb.watch' in url:
            return 'facebook'
        else:
            return 'unknown'
    
    def clean_filename(self, filename: str) -> str:
        """Làm sạch tên file"""
        # Loại bỏ ký tự kiểm soát và emoji
        filename = ''.join(c if ord(c) >= 32 else '' for c in filename)
        
        # Loại bỏ emoji (ký tự Unicode cao)
        filename = ''.join(c if ord(c) < 0x1F300 else '' for c in filename)
        
        # Loại bỏ ký tự không hợp lệ trên Windows
        invalid_chars = '<>:"/\\|?*\n\t'
        filename = ''.join(c if c not in invalid_chars else '' for c in filename)
        
        # Loại bỏ khoảng trắng liên tiếp
        filename = ' '.join(filename.split())
        
        # Cắt tên file nếu quá dài
        filename = filename[:100].strip()
        
        # Nếu tên file rỗng, dùng tên mặc định
        if not filename or filename.isspace():
            filename = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return filename
    
    def find_existing_video(self, video_title: str, video_id: str, audio_only: bool = False) -> Optional[str]:
        """
        Kiểm tra xem video hoặc audio đã được tải trước đó chưa
        
        Args:
            video_title: Tên video/audio
            video_id: ID video/audio
            audio_only: Chỉ kiểm tra định dạng audio
            
        Returns:
            Đường dẫn file nếu tìm thấy, None nếu chưa tải
        """
        safe_filename = self.clean_filename(video_title)
        
        # Kiểm tra các định dạng phổ biến
        extensions = ['mp3', 'm4a', 'webm', 'ogg', 'wav'] if audio_only else ['mp4', 'mkv', 'webm', 'flv', 'avi']
        for ext in extensions:
            # Kiểm tra theo tên đã làm sạch
            final_file = os.path.join(self.output_path, f"{safe_filename}.{ext}")
            if os.path.exists(final_file):
                return final_file
            
            # Kiểm tra theo ID video
            id_file = os.path.join(self.output_path, f"{video_id}.{ext}")
            if os.path.exists(id_file):
                return id_file
        
        return None
    
    def download(self, url: str, audio_only: bool = False) -> bool:
        """
        Tải video hoặc audio từ URL
        
        Args:
            url: URL video
            audio_only: Chỉ tải âm thanh
            
        Returns:
            True nếu tải thành công, False nếu lỗi
        """
        try:
            url = url.strip()
            if not url:
                self.log("❌ URL không được để trống")
                return False
            
            # Xác định loại URL
            url_type = self.detect_url_type(url)
            self.log(f"🔍 Loại URL: {url_type.upper()}")
            
            if url_type == 'unknown':
                self.log("❌ URL không được hỗ trợ. Vui lòng sử dụng YouTube hoặc Facebook")
                return False
            
            # Lấy thông tin video trước khi download để kiểm tra xem đã tồn tại chưa
            try:
                with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    video_id = info.get('id', 'unknown')
                    video_title = info.get('title', 'unknown_title')
                    
                    # Kiểm tra xem file đã tồn tại chưa
                    existing_file = self.find_existing_video(video_title, video_id, audio_only)
                    if existing_file:
                        self.log(f"✅ Video/Audio đã tồn tại, bỏ qua download: {existing_file}")
                        return True
            except Exception as e:
                self.log(f"⚠️ Không thể lấy thông tin video, tiếp tục download...")
            
            # Kiểm tra xem ffmpeg có tồn tại không
            import shutil
            ffmpeg_path = shutil.which('ffmpeg')
            
            # Kiểm tra thêm trong thư mục local 'bin' nếu không tìm thấy trong PATH
            if not ffmpeg_path:
                local_bin = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bin', 'ffmpeg.exe')
                if os.path.exists(local_bin):
                    ffmpeg_path = local_bin
                    self.log(f"✅ Tìm thấy ffmpeg tại: {ffmpeg_path}")

            # Cấu hình yt-dlp
            ydl_opts = {
                'outtmpl': os.path.join(self.output_path, '%(id)s.%(ext)s'),
                'quiet': False,
                'no_warnings': True,
                'socket_timeout': 30,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                },
                'logger': self._yt_dlp_logger(),
            }

            if ffmpeg_path and os.path.isabs(ffmpeg_path):
                ydl_opts['ffmpeg_location'] = ffmpeg_path

            if audio_only:
                ydl_opts['format'] = 'bestaudio/best'
                if ffmpeg_path:
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                else:
                    self.log("⚠️ Không tìm thấy ffmpeg. Âm thanh sẽ được tải ở định dạng gốc (m4a/webm).")
            else:
                if ffmpeg_path:
                    # Ưu tiên 1080p > 720p > 480p có merge
                    ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/bestvideo[height<=720]+bestaudio/best[height<=720]/best'
                    ydl_opts['merge_output_format'] = 'mp4'
                else:
                    self.log("⚠️ Không tìm thấy ffmpeg. Chất lượng video sẽ bị giới hạn (tối đa 720p) vì không thể trộn video và âm thanh.")
                    self.log("💡 Bạn có thể bỏ 'ffmpeg.exe' vào thư mục 'bin' trong thư mục dự án để tăng chất lượng lên 1080p+.")
                    # Nếu không có ffmpeg, chỉ tải file đã có sẵn video+audio (thường tối đa 720p cho mp4)
                    ydl_opts['format'] = 'best[ext=mp4]/best'
            
            self.log(f"🔄 Đang tải: {url}")
            
            # Khởi động tải xuống
            download_success = False
            info = None
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    download_success = True
            except yt_dlp.utils.DownloadError as e:
                error_msg = str(e)
                if 'HTTP Error 403' in error_msg:
                    self.log(f"⚠️ 403 Forbidden detected. Retrying with browser cookies (Chrome)...")
                    cookie_opts = ydl_opts.copy()
                    cookie_opts['cookiesfrombrowser'] = ('chrome', )
                    try:
                        with yt_dlp.YoutubeDL(cookie_opts) as ydl:
                            info = ydl.extract_info(url, download=True)
                            download_success = True
                    except Exception as cookie_e:
                        self.log(f"❌ Failed even with cookies: {str(cookie_e)[:100]}")
                        return False
                else:
                    if 'This video is not available' in error_msg:
                        self.log(f"⚠️ Video không khả dụng hoặc bị xóa")
                    elif 'Signature extraction failed' in error_msg:
                        self.log(f"⚠️ Lỗi xác thực")
                    else:
                        self.log(f"❌ Lỗi tải video: {error_msg[:100]}")
                    return False
            
            if download_success and info:
                video_id = info.get('id', 'unknown')
                video_ext = info.get('ext', 'mp4')
                video_title = info.get('title', 'unknown_title')
                
                # Làm sạch tên file
                safe_filename = self.clean_filename(video_title)
                
                # Tìm tệp thực tế được tải xuống (đề phòng postprocessor đổi ext sang mp3)
                actual_ext = video_ext
                temp_file = os.path.join(self.output_path, f"{video_id}.{video_ext}")
                for ext in ['mp3', 'm4a', 'webm', 'ogg', 'wav', 'mp4', video_ext]:
                    check_path = os.path.join(self.output_path, f"{video_id}.{ext}")
                    if os.path.exists(check_path):
                        temp_file = check_path
                        actual_ext = ext
                        break
                
                # Tên file cuối cùng
                final_file = os.path.join(self.output_path, f"{safe_filename}.{actual_ext}")
                
                # Đổi tên file
                if os.path.exists(temp_file):
                    if os.path.exists(final_file):
                        final_file = os.path.join(
                            self.output_path, 
                            f"{safe_filename}_{datetime.now().strftime('%H%M%S')}.{actual_ext}"
                        )
                    os.rename(temp_file, final_file)
                
                self.log(f"✅ Tải thành công: {final_file}")
                return True
            
            return False
        except Exception as e:
            self.log(f"⚠️ Lỗi không xác định: {str(e)[:100]}")
            return False
    
    def _yt_dlp_logger(self):
        """Tạo logger cho yt-dlp"""
        class YtdlpLogger:
            def __init__(self, callback):
                self.callback = callback
            
            def debug(self, msg):
                if 'Downloading' in msg or 'Merging' in msg:
                    self.callback(f"ℹ️ {msg[:80]}")
            
            def info(self, msg):
                if 'Downloading' in msg or 'Downloaded' in msg:
                    self.callback(f"ℹ️ {msg[:80]}")
            
            def warning(self, msg):
                self.callback(f"⚠️ {msg[:80]}")
            
            def error(self, msg):
                self.callback(f"❌ {msg[:80]}")
        
        return YtdlpLogger(self.log)
