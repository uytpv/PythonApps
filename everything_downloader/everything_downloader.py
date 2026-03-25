#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# Thêm thư mục hiện tại vào path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QFont
from gui import DownloaderGUI

class SplashCloseSignal(QObject):
    """Signal để đóng splash screen"""
    close_signal = pyqtSignal()

class SplashScreen(QWidget):
    """Splash screen hiển thị ngay lập tức"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.start_spinner()
    
    def setup_ui(self):
        """Cấu hình giao diện"""
        self.setWindowTitle("Everything Downloader")
        self.setGeometry(0, 0, 500, 300)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        
        # Center on screen
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - 500) // 2
        y = (screen.height() - 300) // 2
        self.move(x, y)
        
        # Styling
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #1e1e1e, stop:1 #2d2d2d);
                border: 2px solid #4CAF50;
                border-radius: 10px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Logo/Title
        title = QLabel("📹 Everything Downloader")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #4CAF50;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("YouTube & Facebook Video Downloader")
        subtitle_font = QFont()
        subtitle_font.setPointSize(10)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #00ff00;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # Loading spinner
        self.spinner_frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.loading_label = QLabel(self.spinner_frames[0])
        loading_font = QFont()
        loading_font.setPointSize(14)
        self.loading_label.setFont(loading_font)
        self.loading_label.setStyleSheet("color: #00ff00;")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.loading_label)
        
        # Status text
        self.status_label = QLabel("Đang khởi động...")
        status_font = QFont()
        status_font.setPointSize(9)
        self.status_label.setFont(status_font)
        self.status_label.setStyleSheet("color: #666666;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        self.setLayout(layout)
    
    def start_spinner(self):
        """Bắt đầu animation spinner"""
        self.spinner_index = 0
        self.spinner_timer = QTimer()
        self.spinner_timer.timeout.connect(self.update_spinner)
        self.spinner_timer.start(100)  # Update mỗi 100ms
    
    def update_spinner(self):
        """Cập nhật spinner frame"""
        self.loading_label.setText(self.spinner_frames[self.spinner_index])
        self.spinner_index = (self.spinner_index + 1) % len(self.spinner_frames)
    
    def stop_spinner(self):
        """Dừng spinner"""
        self.spinner_timer.stop()

def main():
    """Hàm main"""
    app = QApplication(sys.argv)
    
    # Tạo splash screen và hiển thị
    splash = SplashScreen()
    splash.show()
    
    # Tạo main window nhưng chưa hiển thị
    main_window = DownloaderGUI()
    
    # Timer để đóng splash screen và hiển thị main window sau 1 giây
    def show_main():
        splash.stop_spinner()
        splash.close()
        main_window.show()
    
    timer = QTimer()
    timer.timeout.connect(show_main)
    timer.setSingleShot(True)  # Chỉ chạy một lần
    timer.start(1500)  # 1.5 giây sau
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
