#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Build Release Package - Tạo folder phân phối sạch cho người dùng
Chỉ chứa: everything_downloader.exe + README.txt + videos/
Quản lý version tự động
"""

import PyInstaller.__main__
import os
import sys
import shutil
import json

def get_version():
    """Lấy version hiện tại và cập nhật"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    version_file = os.path.join(script_dir, 'version.json')
    
    # Nếu chưa có version file, tạo mới
    if not os.path.exists(version_file):
        version_data = {'major': 0, 'minor': 1, 'build': 0}
        with open(version_file, 'w') as f:
            json.dump(version_data, f, indent=2)
        return '0.1'
    
    # Đọc version hiện tại
    with open(version_file, 'r') as f:
        version_data = json.load(f)
    
    major = version_data['major']
    minor = version_data['minor']
    
    # Tạo version string
    version_str = f"{major}.{minor}"
    
    return version_str, version_data, version_file

def increment_version(version_data, version_file):
    """Tăng version (0.1 -> 0.2 -> ... -> 0.9 -> 1.0)"""
    minor = version_data['minor']
    major = version_data['major']
    
    minor += 1
    
    # Khi minor = 10, đổi thành major 1.0
    if minor >= 10:
        major += 1
        minor = 0
    
    version_data['major'] = major
    version_data['minor'] = minor
    
    # Lưu version mới
    with open(version_file, 'w') as f:
        json.dump(version_data, f, indent=2)
    
    return f"{major}.{minor}"
import json

def build_exe():
    """Đóng gói thành EXE"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_file = os.path.join(script_dir, 'everything_downloader.py')
    
    # Xóa build cũ
    build_dir = os.path.join(script_dir, 'build')
    dist_dir = os.path.join(script_dir, 'dist')
    
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    
    print("🔨 Đang đóng gói EXE...")
    
    PyInstaller.__main__.run([
        main_file,
        '--name=everything_downloader',
        '--onefile',
        '--windowed',
        '--splash=' + os.path.join(script_dir, 'splash.png'),
        '--collect-all=PyQt6',
        '--collect-all=yt_dlp',
        '--noconfirm',
        f'--distpath={dist_dir}',
        f'--workpath={build_dir}',
        f'--specpath={build_dir}',
    ])
    
    return dist_dir

def create_clean_release(dist_dir, version):
    """Tạo folder phân phối sạch"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exe_path = os.path.join(dist_dir, 'everything_downloader.exe')
    release_dir = os.path.join(script_dir, f'EverythingDownloader_v{version}')
    
    # Xóa release cũ
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    
    os.makedirs(release_dir)
    
    # Copy EXE
    if os.path.exists(exe_path):
        shutil.copy(exe_path, os.path.join(release_dir, 'everything_downloader.exe'))
        print(f"✅ Đã copy EXE vào release folder")
    else:
        print(f"❌ Không tìm thấy EXE")
        return False
    
    # Tạo thư mục videos
    videos_dir = os.path.join(release_dir, 'videos')
    os.makedirs(videos_dir, exist_ok=True)
    
    # Tạo file README.txt
    readme_content = f"""╔════════════════════════════════════════════════════════════════╗
║       📹 EVERYTHING DOWNLOADER v{version}                        ║
║       YouTube & Facebook Video Downloader                    ║
╚════════════════════════════════════════════════════════════════╝

🚀 CÁCH SỬ DỤNG:

1. Double-click file: everything_downloader.exe
2. Copy-paste URL từ YouTube hoặc Facebook
3. Click "Download" hoặc nhấn Enter
4. Video sẽ được lưu vào thư mục "videos/"

─────────────────────────────────────────────────────────────

✅ HỖTRỢ CÁC URL:

YouTube:
  • https://www.youtube.com/watch?v=...
  • https://youtu.be/...

Facebook:
  • https://www.facebook.com/reel/...
  • https://www.facebook.com/share/v/...

─────────────────────────────────────────────────────────────

❓ CÂU HỎI THƯỜNG GẶP:

Q: Video lưu ở đâu?
A: Thư mục "videos/" cùng cấp với file .exe

Q: Có fee không?
A: Hoàn toàn miễn phí!

Q: An toàn không?
A: 100% an toàn, không cần đăng nhập, không lưu dữ liệu

Q: Có thể tải video nào?
A: YouTube & Facebook (Reels, Posts, Group videos)

─────────────────────────────────────────────────────────────

⚠️ LƯU Ý:

• Chỉ chạy được trên Windows 10/11
• Cần kết nối Internet
• Tốc độ tải phụ thuộc vào chất lượng Internet

─────────────────────────────────────────────────────────────

🎉 Chúc bạn sử dụng vui vẻ!

Phiên bản: {version}
Ngày: 2025-11-29
"""
    
    with open(os.path.join(release_dir, 'README.txt'), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ Đã tạo README.txt")
    
    return True

def create_zip_package(release_dir, version):
    """Nén folder thành ZIP"""
    script_dir = os.path.dirname(release_dir)
    zip_path = os.path.join(script_dir, f'EverythingDownloader_v{version}')
    
    print("\n📦 Đang nén thành file ZIP...")
    shutil.make_archive(zip_path, 'zip', script_dir, f'EverythingDownloader_v{version}')
    
    zip_size = os.path.getsize(zip_path + '.zip') / (1024*1024)
    print(f"✅ Đã tạo: EverythingDownloader_v{version}.zip ({zip_size:.2f} MB)")
    
    return zip_path + '.zip'

def main():
    print("\n" + "="*70)
    print("📦 BUILD RELEASE PACKAGE - TẠO FOLDER PHÂN PHỐI")
    print("="*70)
    
    # Lấy version hiện tại
    result = get_version()
    if isinstance(result, str):
        # Lần đầu tiên, chỉ có version string
        version = result
        version_data, version_file = None, None
    else:
        version, version_data, version_file = result
    
    print(f"\n📌 Version hiện tại: v{version}")
    
    # Build EXE
    dist_dir = build_exe()
    
    # Tạo clean release
    print("\n📦 Đang tạo folder phân phối sạch...")
    if create_clean_release(dist_dir, version):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        release_dir = os.path.join(script_dir, f'EverythingDownloader_v{version}')
        exe_size = os.path.getsize(os.path.join(release_dir, 'everything_downloader.exe')) / (1024*1024)
        
        # Nén thành ZIP
        zip_path = create_zip_package(release_dir, version)
        
        # Tăng version cho lần build tiếp theo
        if version_data and version_file:
            next_version = increment_version(version_data, version_file)
            print(f"\n✅ Version tiếp theo sẽ là: v{next_version}")
        
        print("\n" + "="*70)
        print("✅ HOÀN TẤT TẠO FOLDER PHÁT HÀNH!")
        print("="*70)
        print(f"📁 Folder phân phối: {release_dir}")
        print(f"📦 File ZIP: {zip_path}")
        print(f"📹 File EXE: everything_downloader.exe ({exe_size:.2f} MB)")
        print(f"📄 Hướng dẫn: README.txt")
        print(f"📁 Thư mục video: videos/")
        print("\n💡 PHÂN PHỐI CÁCH DÙNG:")
        print(f"1. Gửi file: EverythingDownloader_v{version}.zip cho người dùng")
        print("2. Người dùng giải nén → chạy: everything_downloader.exe")
        print("3. Không cần cài đặt gì khác")
        print("="*70 + "\n")
    else:
        print("\n❌ Lỗi: Không thể tạo release package")

if __name__ == '__main__':
    main()
