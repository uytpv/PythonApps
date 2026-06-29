import sys
import os
import threading
import time
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QTextBrowser, QLabel, QLineEdit, QScrollArea, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QTimer, QThread
from PyQt6.QtGui import QFont, QColor, QTextCursor, QTextCharFormat
from datetime import datetime
from downloader_core import DownloaderCore
from ganjingworld_uploader import GanjingworldUploader

class LogSignal(QObject):
    """Signal để gửi log từ thread tải"""
    log_signal = pyqtSignal(str)

class SpinnerSignal(QObject):
    """Signal để cập nhật spinner từ thread"""
    spinner_signal = pyqtSignal(str)

class DownloaderGUI(QMainWindow):
    """Giao diện ứng dụng tải video"""
    
    def __init__(self):
        super().__init__()
        self.log_signal = LogSignal()
        self.log_signal.log_signal.connect(self.append_log)
        
        self.spinner_signal = SpinnerSignal()
        self.spinner_signal.spinner_signal.connect(self.update_spinner)
        
        # Khởi tạo downloader với callback
        self.downloader = DownloaderCore(
            output_path=self.get_videos_folder(),
            log_callback=self.emit_log
        )
        
        self.is_downloading = False
        self.last_downloaded_file = None  # Lưu lại file vừa tải
        self.spinner_running = False  # Flag để kiểm soát spinner
        
        # Loading animation
        self.spinner_frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.spinner_index = 0
        
        self.init_ui()
    
    def get_videos_folder(self):
        """Lấy thư mục videos cùng cấp với ứng dụng"""
        if getattr(sys, 'frozen', False):
            # Chạy từ exe
            app_dir = os.path.dirname(sys.executable)
        else:
            # Chạy từ script
            app_dir = os.path.dirname(os.path.abspath(__file__))
        
        videos_dir = os.path.join(app_dir, 'videos')
        return videos_dir
    
    def init_ui(self):
        """Khởi tạo giao diện"""
        self.setWindowTitle("📹 Everything Downloader - YouTube & Facebook")
        self.setGeometry(100, 100, 900, 850)
        
        # Widget chính
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout chính (vertical)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # ===== PHẦN 1: INPUT URL =====
        title_label = QLabel("📥 Nhập URL Video:")
        title_font = QFont()
        title_font.setPointSize(11)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # Input form với nút download
        input_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste URL YouTube hoặc Facebook tại đây...")
        self.url_input.setMinimumHeight(40)
        self.url_input.returnPressed.connect(self.on_download_click)
        self.url_input.focusEvent = self.on_url_input_focus  # Bắt sự kiện focus
        self.url_input.focusInEvent = self.on_url_input_focus
        input_layout.addWidget(self.url_input)
        
        self.download_btn = QPushButton("📥 Download")
        self.download_btn.setMinimumHeight(40)
        self.download_btn.setMinimumWidth(120)
        self.download_btn.clicked.connect(self.on_download_click)
        self.download_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        input_layout.addWidget(self.download_btn)
        main_layout.addLayout(input_layout)
        
        # Checkbox chỉ tải file audio
        self.audio_only_checkbox = QCheckBox("🎵 Chỉ tải file âm thanh (Audio Only)")
        self.audio_only_checkbox.setStyleSheet("font-size: 10pt; padding: 5px;")
        main_layout.addWidget(self.audio_only_checkbox)
        
        # ===== PHẦN 2: GANJINGWORLD UPLOAD CONTROLS =====
        gjw_label = QLabel("☁️ Ganjingworld Upload (Tùy chọn):")
        gjw_label.setFont(title_font)
        main_layout.addWidget(gjw_label)
        
        # Checkbox để bật/tắt upload
        self.gjw_checkbox = QCheckBox("🚀 Tự động upload lên Ganjingworld sau khi tải xong")
        self.gjw_checkbox.setStyleSheet("font-size: 10pt; padding: 5px;")
        self.gjw_checkbox.stateChanged.connect(self.on_gjw_checkbox_changed)
        main_layout.addWidget(self.gjw_checkbox)
        
        # Kết nối sự kiện checkbox chỉ tải audio
        self.audio_only_checkbox.stateChanged.connect(self.on_audio_only_changed)
        
        # Access Token input
        token_layout = QHBoxLayout()
        token_label = QLabel("🔑 Access Token:")
        token_label.setMinimumWidth(120)
        token_label.setVisible(False)
        token_layout.addWidget(token_label)
        
        self.gjw_token_input = QLineEdit()
        self.gjw_token_input.setPlaceholderText("Paste JWT Access Token từ Ganjingworld...")
        self.gjw_token_input.setMinimumHeight(35)
        self.gjw_token_input.setEchoMode(QLineEdit.EchoMode.Password)  # Ẩn token
        self.gjw_token_input.setVisible(False)
        self.gjw_token_input.setEnabled(False)
        token_layout.addWidget(self.gjw_token_input)
        main_layout.addLayout(token_layout)
        
        self.token_label = token_label  # Lưu ref để toggle visibility
        
        # Channel ID input
        channel_layout = QHBoxLayout()
        channel_label = QLabel("📺 Channel ID:")
        channel_label.setMinimumWidth(120)
        channel_label.setVisible(False)
        channel_layout.addWidget(channel_label)
        
        self.gjw_channel_input = QLineEdit()
        self.gjw_channel_input.setPlaceholderText("Paste Channel ID từ Ganjingworld...")
        self.gjw_channel_input.setMinimumHeight(35)
        self.gjw_channel_input.setVisible(False)
        self.gjw_channel_input.setEnabled(False)
        channel_layout.addWidget(self.gjw_channel_input)
        main_layout.addLayout(channel_layout)
        
        self.channel_label = channel_label  # Lưu ref để toggle visibility
        
        # ===== PHẦN 3: LOG DISPLAY =====
        log_label = QLabel("📋 Tiến Trình Tải:")
        log_label.setFont(title_font)
        main_layout.addWidget(log_label)
        
        # Log text area (sử dụng QTextBrowser để click được link)
        self.log_text = QTextBrowser()
        self.log_text.setReadOnly(True)
        self.log_text.setOpenLinks(False)
        self.log_text.anchorClicked.connect(self.on_link_clicked)
        self.log_text.setMinimumHeight(300)
        self.log_text.setFont(QFont("Courier", 14))
        self.log_text.setStyleSheet("""
            QTextBrowser {
                background-color: #1e1e1e;
                color: #00ff00;
                border: 1px solid #333333;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        main_layout.addWidget(self.log_text)
        
        # ===== PHẦN 4: THÔNG TIN =====
        info_layout = QHBoxLayout()
        
        self.status_label = QLabel("✅ Sẵn sàng")
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        info_layout.addWidget(self.status_label)
        
        # Nút mở thư mục
        self.open_folder_btn = QPushButton("📂 Mở thư mục")
        self.open_folder_btn.setMinimumHeight(30)
        self.open_folder_btn.clicked.connect(self.on_open_folder_click)
        self.open_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                border-radius: 4px;
                padding: 0 10px;
                font-size: 9pt;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            QPushButton:pressed {
                background-color: #0a6cbd;
            }
        """)
        info_layout.addWidget(self.open_folder_btn)
        
        info_layout.addStretch()
        
        videos_folder_label = QLabel(f"📁 Thư mục: {self.get_videos_folder()}")
        videos_folder_label.setStyleSheet("color: #666666; font-size: 9pt;")
        info_layout.addWidget(videos_folder_label)
        
        main_layout.addLayout(info_layout)
        
        # Set layout
        central_widget.setLayout(main_layout)
        
        # Log ban đầu
        self.append_log(f"{'='*60}")
        self.append_log(f"🎬 Everything Downloader - YouTube & Facebook Video Downloader")
        self.append_log(f"{'='*60}")
        self.append_log(f"📁 Thư mục lưu video: {self.get_videos_folder()}")
        self.append_log(f"{'='*60}\n")
    
    def emit_log(self, message: str):
        """Phát tín hiệu log từ thread khác"""
        self.log_signal.log_signal.emit(message)
    
    def append_log(self, message: str):
        """Thêm log vào text area"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        self.log_text.append(formatted_message)
        
        # Scroll xuống dưới cùng và reset định dạng để không bị dính link/format cũ
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.setCharFormat(QTextCharFormat())
        self.log_text.setTextCursor(cursor)
    
    def update_spinner(self, frame_text: str):
        """Cập nhật loading spinner (called from signal)"""
        self.status_label.setText(frame_text)
        
    def on_link_clicked(self, url):
        """Xử lý click vào link trong log"""
        if url.toString() == 'open_folder':
            self.on_open_folder_click()
            
    def on_open_folder_click(self):
        """Mở thư mục chứa file và chọn file đó"""
        folder = self.get_videos_folder()
        if self.last_downloaded_file and os.path.exists(self.last_downloaded_file):
            if sys.platform == 'win32':
                import subprocess
                subprocess.run(['explorer', '/select,', os.path.normpath(self.last_downloaded_file)])
            else:
                os.startfile(folder) if hasattr(os, 'startfile') else subprocess.run(['open', folder])
        else:
            if os.path.exists(folder):
                if sys.platform == 'win32':
                    os.startfile(folder)
                else:
                    import subprocess
                    subprocess.run(['open', folder])
            else:
                self.append_log("❌ Thư mục videos chưa được tạo")
    
    def run_spinner(self):
        """Chạy spinner animation trong thread riêng"""
        while self.spinner_running:
            try:
                spinner = self.spinner_frames[self.spinner_index]
                self.spinner_signal.spinner_signal.emit(f"{spinner} Đang tải...")
                self.spinner_index = (self.spinner_index + 1) % len(self.spinner_frames)
                time.sleep(0.1)  # Update mỗi 100ms
            except Exception:
                break
    
    def on_url_input_focus(self, event):
        """Reset trạng thái khi focus vào input"""
        self.status_label.setText("✅ Sẵn sàng")
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.spinner_running = False
        super(type(self.url_input), self.url_input).focusInEvent(event)
    
    def on_gjw_checkbox_changed(self, state):
        """Bật/tắt input khi checkbox thay đổi"""
        is_checked = self.gjw_checkbox.isChecked()
        
        # Toggle visibility và enabled
        self.token_label.setVisible(is_checked)
        self.gjw_token_input.setVisible(is_checked)
        self.gjw_token_input.setEnabled(is_checked)
        
        self.channel_label.setVisible(is_checked)
        self.gjw_channel_input.setVisible(is_checked)
        self.gjw_channel_input.setEnabled(is_checked)
        
        if is_checked:
            self.append_log("✅ Ganjingworld upload được kích hoạt")
        else:
            self.append_log("⏹️ Ganjingworld upload bị vô hiệu hóa")
            
    def on_audio_only_changed(self, state):
        """Xử lý khi checkbox chỉ tải audio thay đổi trạng thái"""
        is_audio = self.audio_only_checkbox.isChecked()
        if is_audio:
            self.gjw_checkbox.setChecked(False)
            self.gjw_checkbox.setEnabled(False)
            self.append_log("ℹ️ Đã vô hiệu hóa Ganjingworld Upload vì Ganjingworld chỉ hỗ trợ video")
        else:
            self.gjw_checkbox.setEnabled(True)
    
    def on_download_click(self):
        """Xử lý khi click nút Download"""
        url = self.url_input.text().strip()
        
        if not url:
            self.append_log("❌ Vui lòng nhập URL")
            return
        
        if self.is_downloading:
            self.append_log("⚠️ Đang tải video khác, vui lòng chờ...")
            return
        
        # Bắt đầu tải trong thread riêng
        self.is_downloading = True
        self.download_btn.setEnabled(False)
        self.url_input.setEnabled(False)
        self.audio_only_checkbox.setEnabled(False)
        
        # Bắt đầu loading spinner (sẽ chạy trong thread riêng)
        self.status_label.setText("⠋ Đang tải...")
        self.status_label.setStyleSheet("color: #ff9800; font-weight: bold;")
        self.spinner_index = 0
        self.spinner_running = True
        
        self.append_log(f"\n{'='*60}")
        self.append_log(f"🎬 Bắt đầu tải lúc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.append_log(f"{'='*60}\n")
        
        # Start spinner thread
        spinner_thread = threading.Thread(target=self.run_spinner)
        spinner_thread.daemon = True
        spinner_thread.start()
        
        audio_only = self.audio_only_checkbox.isChecked()
        download_thread = threading.Thread(target=self.download_video, args=(url, audio_only))
        download_thread.daemon = True
        download_thread.start()
    
    def download_video(self, url: str, audio_only: bool = False):
        """Tải video hoặc audio (chạy trong thread)"""
        try:
            success = self.downloader.download(url, audio_only=audio_only)
            
            if success:
                self.emit_log(f"✨ Tải hoàn tất!")
                
                # Lấy file vừa tải
                videos_folder = self.get_videos_folder()
                if os.path.exists(videos_folder):
                    files = sorted(
                        [f for f in os.listdir(videos_folder) if os.path.isfile(os.path.join(videos_folder, f)) and not f.endswith(('.part', '.ytdl', '.temp'))],
                        key=lambda x: os.path.getctime(os.path.join(videos_folder, x)),
                        reverse=True
                    )
                    if files:
                        self.last_downloaded_file = os.path.join(videos_folder, files[0])
                        self.emit_log(f"📂 Đã lưu tại: {files[0]}")
                
                # Hiển thị liên kết mở thư mục
                self.emit_log("<a href='open_folder' style='color: #2196F3; font-weight: bold;'>👉 Click vào đây để mở thư mục chứa file vừa tải</a>")
                
                # Kiểm tra nếu cần upload lên GJW
                if self.gjw_checkbox.isChecked() and not audio_only:
                    self.upload_to_ganjingworld()
                else:
                    if self.gjw_checkbox.isChecked() and audio_only:
                        self.emit_log("ℹ️ Bỏ qua tự động upload lên Ganjingworld vì đây là file âm thanh (Audio Only).")
                    
                    self.url_input.clear()
                    self.status_label.setText("✅ Tải thành công")
                    self.status_label.setStyleSheet("color: green; font-weight: bold;")
                    self.spinner_running = False
            else:
                self.status_label.setText("❌ Tải thất bại")
                self.status_label.setStyleSheet("color: red; font-weight: bold;")
                self.spinner_running = False
        
        except Exception as e:
            self.emit_log(f"❌ Lỗi không xác định: {str(e)}")
            self.status_label.setText("❌ Tải thất bại")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            self.spinner_running = False
        
        finally:
            self.is_downloading = False
            self.download_btn.setEnabled(True)
            self.url_input.setEnabled(True)
            self.audio_only_checkbox.setEnabled(True)
    
    def upload_to_ganjingworld(self):
        """Upload video lên Ganjingworld"""
        self.append_log(f"\n{'='*60}")
        self.append_log("☁️ Bắt đầu upload lên Ganjingworld...")
        self.append_log(f"{'='*60}\n")
        
        # Kiểm tra credentials
        access_token = self.gjw_token_input.text().strip()
        channel_id = self.gjw_channel_input.text().strip()
        
        if not access_token:
            self.append_log("❌ Vui lòng nhập Access Token")
            self.status_label.setText("❌ Upload thất bại")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            self.spinner_running = False
            return
        
        if not channel_id:
            self.append_log("❌ Vui lòng nhập Channel ID")
            self.status_label.setText("❌ Upload thất bại")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            self.spinner_running = False
            return
        
        if not self.last_downloaded_file or not os.path.exists(self.last_downloaded_file):
            self.append_log("❌ Không tìm thấy file video vừa tải")
            self.status_label.setText("❌ Upload thất bại")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            self.spinner_running = False
            return
        
        # Lấy tên video làm title
        video_filename = os.path.basename(self.last_downloaded_file)
        video_title = os.path.splitext(video_filename)[0]
        
        self.append_log(f"📁 File video: {video_filename}")
        self.append_log(f"📝 Title: {video_title}\n")
        
        # Upload trong thread riêng
        upload_thread = threading.Thread(
            target=self.perform_upload,
            args=(self.last_downloaded_file, video_title, access_token, channel_id)
        )
        upload_thread.daemon = True
        upload_thread.start()
    
    def perform_upload(self, video_path: str, title: str, access_token: str, channel_id: str):
        """Thực hiện upload (chạy trong thread)"""
        try:
            uploader = GanjingworldUploader(access_token, channel_id)
            uploader.set_log_callback(self.emit_log)
            
            # Gọi workflow upload đầy đủ
            content_url = uploader.upload_workflow(
                video_path=video_path,
                title=title,
                description=f"Tải lên bởi Everything Downloader"
            )
            
            if content_url:
                self.append_log(f"\n✨ Upload hoàn tất!")
                self.append_log(f"🔗 URL: {content_url}\n")
                self.url_input.clear()
                self.status_label.setText("✅ Upload thành công")
                self.status_label.setStyleSheet("color: green; font-weight: bold;")
            else:
                self.append_log(f"\n❌ Upload thất bại")
                self.status_label.setText("❌ Upload thất bại")
                self.status_label.setStyleSheet("color: red; font-weight: bold;")
        
        except Exception as e:
            self.append_log(f"❌ Lỗi upload: {str(e)}")
            self.status_label.setText("❌ Upload thất bại")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
        
        finally:
            self.spinner_running = False
            self.is_downloading = False
            self.download_btn.setEnabled(True)
            self.url_input.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    window = DownloaderGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
