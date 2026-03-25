#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script để kiểm tra ứng dụng
Không cần chạy GUI, chỉ test logic tải video
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from downloader_core import DownloaderCore

def test_downloader():
    """Test downloader core"""
    
    print("\n" + "="*60)
    print("🧪 TEST DOWNLOADER CORE")
    print("="*60 + "\n")
    
    # Tạo downloader
    downloader = DownloaderCore(output_path='test_videos')
    
    # Test 1: Xác định URL type
    print("✅ Test 1: Xác định loại URL")
    test_urls = [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "youtube"),
        ("https://www.facebook.com/reel/123456", "facebook"),
        ("https://www.google.com", "unknown"),
    ]
    
    for url, expected in test_urls:
        result = downloader.detect_url_type(url)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {url} -> {result}")
    
    # Test 2: Làm sạch tên file
    print("\n✅ Test 2: Làm sạch tên file")
    test_filenames = [
        "Video Title 🎬 | 2025",
        "File<Name>With|Invalid?Characters",
        "",
        "   ",
    ]
    
    for filename in test_filenames:
        clean = downloader.clean_filename(filename)
        print(f"  '{filename}' -> '{clean}'")
    
    # Test 3: Thư mục output
    print("\n✅ Test 3: Thư mục output")
    print(f"  Output path: {downloader.output_path}")
    print(f"  Folder exists: {os.path.exists(downloader.output_path)}")
    
    print("\n" + "="*60)
    print("✨ Test hoàn tất!")
    print("="*60 + "\n")

if __name__ == '__main__':
    test_downloader()
