#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test Application - Kiểm tra ứng dụng trước khi build
Không cần PyQt6 GUI, chỉ test logic
"""

import sys
import os
import subprocess

# Thêm thư mục hiện tại vào path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from downloader_core import DownloaderCore

def print_header(text):
    """In tiêu đề"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}")

def print_success(text):
    """In thành công"""
    print(f"  ✅ {text}")

def print_error(text):
    """In lỗi"""
    print(f"  ❌ {text}")

def print_info(text):
    """In thông tin"""
    print(f"  ℹ️  {text}")

def test_dependencies():
    """Kiểm tra dependencies"""
    print_header("1️⃣  KIỂM TRA DEPENDENCIES")
    
    dependencies = [
        ('PyQt6', 'PyQt6'),
        ('yt-dlp', 'yt_dlp'),
        ('requests', 'requests'),
    ]
    
    all_ok = True
    for name, module in dependencies:
        try:
            __import__(module)
            print_success(f"{name} được cài đặt")
        except ImportError:
            print_error(f"{name} chưa được cài đặt")
            all_ok = False
    
    return all_ok

def test_files():
    """Kiểm tra file cần thiết"""
    print_header("2️⃣  KIỂM TRA FILE CẦN THIẾT")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    required_files = [
        'everything_downloader.py',
        'gui.py',
        'downloader_core.py',
    ]
    
    all_ok = True
    for filename in required_files:
        filepath = os.path.join(script_dir, filename)
        if os.path.exists(filepath):
            print_success(f"{filename} tồn tại")
        else:
            print_error(f"{filename} không tồn tại")
            all_ok = False
    
    return all_ok

def test_downloader_core():
    """Kiểm tra DownloaderCore"""
    print_header("3️⃣  KIỂM TRA DOWNLOADER CORE")
    
    try:
        # Kiểm tra URL detection
        downloader = DownloaderCore(
            output_path=os.path.join(os.path.dirname(__file__), 'test_videos'),
            log_callback=lambda x: None
        )
        
        test_urls = [
            ('https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'youtube'),
            ('https://youtu.be/dQw4w9WgXcQ', 'youtube'),
            ('https://www.facebook.com/reel/123456789/', 'facebook'),
            ('https://www.facebook.com/share/v/123456789/', 'facebook'),
            ('https://example.com/video', 'unknown'),
        ]
        
        all_ok = True
        for url, expected_type in test_urls:
            detected_type = downloader.detect_url_type(url)
            if detected_type == expected_type:
                print_success(f"URL detection: {url[:50]}... → {detected_type}")
            else:
                print_error(f"URL detection: {url[:50]}... → {detected_type} (expected {expected_type})")
                all_ok = False
        
        return all_ok
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_filename_cleaning():
    """Kiểm tra làm sạch tên file"""
    print_header("4️⃣  KIỂM TRA LÀM SẠCH TÊN FILE")
    
    try:
        downloader = DownloaderCore(
            output_path=os.path.join(os.path.dirname(__file__), 'test_videos'),
            log_callback=lambda x: None
        )
        
        test_filenames = [
            ('Normal Video Name.mp4', 'Normal Video Name.mp4'),
            ('Video with 😀 emoji.mp4', 'Video with emoji.mp4'),
            ('Video with spécial çhars.mp4', 'Video with special chars.mp4'),
            ('A' * 150 + '.mp4', 'A' * 100 + '.mp4'),  # Truncate
        ]
        
        all_ok = True
        for filename, expected_pattern in test_filenames:
            cleaned = downloader.clean_filename(filename)
            if len(cleaned) <= 100 and '😀' not in cleaned:
                print_success(f"Clean: {filename[:40]}... → {cleaned[:40]}...")
            else:
                print_error(f"Clean failed: {filename[:40]}...")
                all_ok = False
        
        return all_ok
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_video_directory():
    """Kiểm tra tạo thư mục video"""
    print_header("5️⃣  KIỂM TRA THƯ MỤC VIDEO")
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        test_videos_dir = os.path.join(script_dir, 'test_videos')
        
        downloader = DownloaderCore(
            output_path=test_videos_dir,
            log_callback=lambda x: None
        )
        
        if os.path.exists(test_videos_dir):
            print_success(f"Thư mục {test_videos_dir} tồn tại")
            
            # Clean up
            import shutil
            if os.path.exists(test_videos_dir) and os.listdir(test_videos_dir) == []:
                shutil.rmtree(test_videos_dir)
                print_info("Đã xóa thư mục test tạm")
            
            return True
        else:
            print_error(f"Không thể tạo thư mục {test_videos_dir}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_pyinstaller():
    """Kiểm tra PyInstaller"""
    print_header("6️⃣  KIỂM TRA PYINSTALLER")
    
    try:
        result = subprocess.run(['pyinstaller', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print_success(f"PyInstaller: {version}")
            return True
        else:
            print_error("PyInstaller không được cài đặt")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_version_file():
    """Kiểm tra version file"""
    print_header("7️⃣  KIỂM TRA VERSION FILE")
    
    try:
        import json
        script_dir = os.path.dirname(os.path.abspath(__file__))
        version_file = os.path.join(script_dir, 'version.json')
        
        if os.path.exists(version_file):
            with open(version_file, 'r') as f:
                version_data = json.load(f)
            
            version_str = f"{version_data['major']}.{version_data['minor']}"
            print_success(f"Version file tồn tại: v{version_str}")
            return True
        else:
            print_info("Version file chưa tồn tại (sẽ tạo mới khi build)")
            return True
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_gui():
    """Kiểm tra giao diện GUI"""
    print_header("8️⃣  KIỂM TRA GIAO DIỆN GUI")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from gui import DownloaderGUI
        
        # Kiểm tra DownloaderGUI class
        if hasattr(DownloaderGUI, '__init__'):
            print_success("DownloaderGUI class tồn tại")
        else:
            print_error("DownloaderGUI class không tồn tại")
            return False
        
        # Kiểm tra các method cần thiết
        required_methods = ['init_ui', 'on_download_click', 'download_video', 'append_log']
        for method in required_methods:
            if hasattr(DownloaderGUI, method):
                print_success(f"Method {method} tồn tại")
            else:
                print_error(f"Method {method} không tồn tại")
                return False
        
        return True
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_splash_screen():
    """Kiểm tra splash screen"""
    print_header("9️⃣  KIỂM TRA SPLASH SCREEN")
    
    try:
        from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
        from PyQt6.QtCore import QTimer
        
        # Kiểm tra everything_downloader.py có splash screen
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_file = os.path.join(script_dir, 'everything_downloader.py')
        
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_components = [
            ('create_splash_screen', 'Hàm tạo splash screen'),
            ('QTimer', 'Timer cho animation'),
            ('spinner_frames', 'Loading spinner'),
            ('Đang khởi động', 'Status text'),
        ]
        
        all_ok = True
        for component, description in required_components:
            if component in content:
                print_success(f"{description} ({component}) được tìm thấy")
            else:
                print_error(f"{description} ({component}) không được tìm thấy")
                all_ok = False
        
        if all_ok:
            print_info("Splash screen sẵn sàng - sẽ hiển thị khi chạy exe")
        
        return all_ok
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def main():
    """Chạy toàn bộ test"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  🧪 EVERYTHING DOWNLOADER - TEST APPLICATION".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    results = []
    
    # Chạy các test
    results.append(("Dependencies", test_dependencies()))
    results.append(("Files", test_files()))
    results.append(("Downloader Core", test_downloader_core()))
    results.append(("Filename Cleaning", test_filename_cleaning()))
    results.append(("Video Directory", test_video_directory()))
    results.append(("PyInstaller", test_pyinstaller()))
    results.append(("Version File", test_version_file()))
    results.append(("GUI", test_gui()))
    results.append(("Splash Screen", test_splash_screen()))
    
    # Tóm tắt kết quả
    print_header("📊 TÓM TẮT KẾT QUẢ TEST")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")
    
    print(f"\n  {passed}/{total} test thành công\n")
    
    if passed == total:
        print_header("✅ SẴN SÀNG BUILD!")
        print("  Chạy lệnh: python build_release.py\n")
        return 0
    else:
        print_header("❌ CÓ LỖI CẦN SỬA!")
        print("  Vui lòng sửa các lỗi trên rồi chạy lại test\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
