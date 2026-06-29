#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import PyInstaller.__main__
import os
import sys
import shutil

def build_exe():
    """Đóng gói ứng dụng thành file EXE"""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_file = os.path.join(script_dir, 'everything_downloader.py')
    
    # Xóa build cũ
    build_dir = os.path.join(script_dir, 'build')
    dist_dir = os.path.join(script_dir, 'dist')
    
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
        print(f"🗑️ Đã xóa thư mục build cũ")
    
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
        print(f"🗑️ Đã xóa thư mục dist cũ")
    
    PyInstaller.__main__.run([
        main_file,
        '--name=everything_downloader',
        '--onefile',
        '--windowed',
        '--splash=' + os.path.join(script_dir, 'splash.png'),
        '--add-data=' + os.path.join(script_dir, 'downloader_core.py') + ';.',
        '--add-data=' + os.path.join(script_dir, 'gui.py') + ';.',
        '--add-data=' + os.path.join(script_dir, 'bin') + ';bin',
        '--collect-all=PyQt6',
        '--collect-all=yt_dlp',
        '--noconfirm',
        f'--distpath={dist_dir}',
        f'--workpath={build_dir}',
        f'--specpath={build_dir}',
    ])
    
    exe_path = os.path.join(dist_dir, 'everything_downloader.exe')
    
    if os.path.exists(exe_path):
        print("\n" + "="*70)
        print("✅ ĐÓNG GÓI HOÀN TẤT!")
        print("="*70)
        print(f"📁 File EXE nằm tại: {exe_path}")
        print(f"📦 Dung lượng: {os.path.getsize(exe_path) / (1024*1024):.2f} MB")
        print("\n💡 HƯỚNG DẪN SỬ DỤNG:")
        print("1. Copy file everything_downloader.exe đến một thư mục riêng")
        print("2. Chạy file exe")
        print("3. Video sẽ được lưu trong thư mục 'videos' cùng cấp với exe")
        print("="*70 + "\n")
    else:
        print("\n❌ Lỗi: Không thể tạo file EXE")

if __name__ == '__main__':
    print("\n🔨 BẮT ĐẦU ĐÓNG GÓI ỨNG DỤNG...")
    print("="*70)
    print("⏳ Quá trình này có thể mất vài phút...\n")
    build_exe()
