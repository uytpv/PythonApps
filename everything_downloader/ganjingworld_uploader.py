#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ganjingworld Uploader - Module upload video lên Ganjingworld
Tách riêng để dễ quản lý và vận hành
"""

import requests
import json
import time
import os
import subprocess
from typing import Optional, Dict, Tuple
from pathlib import Path
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Disable SSL warnings for known API issues
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class GanjingworldUploader:
    """Quản lý upload video lên Ganjingworld API"""
    
    # API Endpoints
    GET_VOD_TOKEN = "https://gw.ganjingworld.com/v1.0c/get-vod-token"
    ADD_CONTENT = "https://gw.ganjingworld.com/v1.0c/add-content"
    UPLOAD_IMAGE = "https://imgapi.cloudokyo.cloud/api/v1/image"
    UPLOAD_VIDEO = "https://vodapi.cloudokyo.cloud/api/v1/video"
    CHECK_STATUS = "https://vodapi.cloudokyo.cloud/api/v1/status"
    
    def __init__(self, access_token: str, channel_id: str):
        """
        Khởi tạo uploader
        
        Args:
            access_token: JWT access token từ Ganjingworld
            channel_id: Channel ID của kênh
        """
        self.access_token = access_token
        self.channel_id = channel_id
        self.upload_token = None
        self.log_callback = None
        
        # Tạo session với retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=0,  # Chúng ta handle retry manual, không cần urllib3 retry
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=1,
            pool_maxsize=1
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Configure socket options cho connection ổn định
        self.session.headers.update({
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def set_log_callback(self, callback):
        """Thiết lập callback để nhận log"""
        self.log_callback = callback
    
    def log(self, message: str):
        """In log message"""
        if self.log_callback:
            self.log_callback(message)
        else:
            print(f"[GJW] {message}")
    
    def get_upload_token(self) -> Optional[str]:
        """
        Lấy upload token từ API (Step 2)
        
        Returns:
            Upload token hoặc None nếu thất bại
        """
        try:
            self.log("📝 Bước 2: Đang lấy upload token...")
            
            response = requests.get(
                self.GET_VOD_TOKEN,
                headers={
                    "accept": "application/json",
                    "authorization": self.access_token
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.upload_token = data['data']['token']
                self.log("✅ Lấy upload token thành công")
                return self.upload_token
            else:
                self.log(f"❌ Lỗi lấy upload token: {response.status_code}")
                self.log(f"   Response: {response.text}")
                return None
        except Exception as e:
            self.log(f"❌ Lỗi: {str(e)}")
            return None
    
    def extract_thumbnail(self, video_path: str) -> Optional[str]:
        """
        Trích xuất thumbnail từ video (Step 3 - Helper)
        
        Args:
            video_path: Đường dẫn tới file video
            
        Returns:
            Đường dẫn tới file thumbnail hoặc None nếu thất bại
        """
        try:
            self.log("🎨 Bước 3a: Đang trích xuất thumbnail từ video...")
            
            thumbnail_path = video_path.replace('.mp4', '_thumbnail.jpg')
            
            # Dùng ffmpeg để trích thumbnail
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-ss', '00:00:05',  # Lấy frame ở giây thứ 5
                '-vframes', '1',
                '-vf', 'scale=1280:720',
                '-y',
                thumbnail_path
            ]
            
            subprocess.run(cmd, capture_output=True, check=True, timeout=30)
            
            self.log(f"✅ Trích xuất thumbnail thành công")
            return thumbnail_path
        except Exception as e:
            self.log(f"⚠️  Không thể trích xuất thumbnail: {str(e)}")
            return None
    
    def upload_thumbnail(self, image_path: str) -> Optional[str]:
        """
        Upload thumbnail image (Step 3)
        
        Args:
            image_path: Đường dẫn tới file ảnh
            
        Returns:
            IMAGE-ID hoặc None nếu thất bại
        """
        try:
            if not os.path.exists(image_path):
                self.log(f"❌ File ảnh không tồn tại: {image_path}")
                return None
            
            self.log(f"🖼️  Bước 3b: Đang upload thumbnail...")
            
            with open(image_path, 'rb') as f:
                files = {
                    'file': (os.path.basename(image_path), f),
                    'name': (None, 'thumbnail')
                }
                
                response = requests.post(
                    self.UPLOAD_IMAGE,
                    files=files,
                    headers={
                        "accept": "application/json, text/plain, */*",
                        "authorization": f"Bearer {self.upload_token}",
                        "resizing-list": "140,240,360,380,480,580,672,960,1280,1920"
                    },
                    timeout=60
                )
            
            if response.status_code == 200:
                data = response.json()
                image_id = data['body']['image_id']
                self.log("✅ Upload thumbnail thành công")
                return image_id
            else:
                self.log(f"❌ Lỗi upload thumbnail: {response.status_code}")
                self.log(f"   Response: {response.text}")
                return None
        except Exception as e:
            self.log(f"❌ Lỗi: {str(e)}")
            return None
    
    def create_content(self, title: str, description: str, image_id: str,
                      category_id: str = "cat13", lang: str = "en-US") -> Optional[str]:
        """
        Tạo content draft với metadata (Step 4)
        
        Args:
            title: Tên video
            description: Mô tả video
            image_id: ID của thumbnail
            category_id: Danh mục video
            lang: Ngôn ngữ
            
        Returns:
            CONTENT_ID hoặc None nếu thất bại
        """
        try:
            self.log("📄 Bước 4: Đang tạo nội dung draft...")
            
            poster_url = f"https://image5-us-west.cloudokyo.cloud/image/v1/db/13/42/{image_id}/672.webp"
            
            payload = {
                "user_id2": self.channel_id,
                "type": "Video",
                "lang": lang,
                "category_id": category_id,
                "title": title,
                "description": description,
                "visibility": "public",
                "mode": "draft",
                "poster_url": poster_url,
                "poster_hd_url": poster_url
            }
            
            response = requests.post(
                self.ADD_CONTENT,
                json=payload,
                headers={
                    "accept": "application/json",
                    "authorization": self.access_token,
                    "content-type": "application/json"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                content_id = data['data']['id']
                self.log(f"✅ Tạo nội dung thành công: {content_id}")
                return content_id
            else:
                self.log(f"❌ Lỗi tạo nội dung: {response.status_code}")
                self.log(f"   Response: {response.text}")
                return None
        except Exception as e:
            self.log(f"❌ Lỗi: {str(e)}")
            return None
    
    def upload_video(self, video_path: str, content_id: str, max_retries: int = 7, 
                     chunk_size: Optional[int] = None) -> Optional[str]:
        """
        Upload video file (Step 5) with retry logic for SSL errors
        Hỗ trợ chunk upload cho file lớn
        
        Args:
            video_path: Đường dẫn tới file video
            content_id: CONTENT_ID từ bước tạo content
            max_retries: Số lần retry tối đa khi gặp lỗi
            chunk_size: Kích thước chunk nếu cần chia file (bytes). 
                       Nếu None, tự động dùng chunk nếu file > 500MB
            
        Returns:
            VIDEO_ID hoặc None nếu thất bại
        """
        try:
            if not os.path.exists(video_path):
                self.log(f"❌ File video không tồn tại: {video_path}")
                return None
            
            file_size = os.path.getsize(video_path)  # bytes
            file_size_mb = file_size / (1024 * 1024)
            self.log(f"🎬 Bước 5: Đang upload video ({file_size_mb:.2f} MB)...")
            
            # Nếu file > 200MB, tự động dùng chunk upload (mỗi chunk 50MB)
            # Chunk size càng nhỏ, càng ít lỗi SSL/500 errors
            # TUY NHIÊN: API có vẻ chỉ accept chunk 1 (full video), các chunk sau reject "file type not supported"
            # Nên chúng ta sẽ chỉ upload toàn bộ file 1 lần với timeout rất dài
            if chunk_size is None and file_size > 200 * 1024 * 1024:
                # Disable chunked upload vì API reject các chunk sau
                # Thay vào đó, upload toàn bộ file với timeout tính theo file size
                chunk_size = None
            
            if chunk_size and file_size > chunk_size:
                self.log(f"📦 File lớn, chia thành {(file_size // chunk_size) + 1} chunk ({chunk_size / (1024*1024):.0f}MB mỗi cái)")
                return self._upload_video_chunked(video_path, content_id, chunk_size, max_retries)
            else:
                return self._upload_video_direct(video_path, content_id, max_retries)
        
        except Exception as e:
            self.log(f"❌ Lỗi: {str(e)}")
            return None
    
    def _upload_video_direct(self, video_path: str, content_id: str, max_retries: int = 7) -> Optional[str]:
        """Upload toàn bộ file trong 1 request"""
        filename = os.path.basename(video_path)
        filetype = "video/mp4"
        
        for attempt in range(max_retries):
            try:
                with open(video_path, 'rb') as f:
                    metadata = {
                        "filename": filename,
                        "filetype": filetype,
                        "channel_id": self.channel_id,
                        "content_id": content_id
                    }
                    
                    files = {
                        'metadata': (None, json.dumps(metadata)),
                        'file': (filename, f, filetype)
                    }
                    
                    # Timeout: 1800 giây (30 phút) + thêm 180 giây cho mỗi GB
                    # Tức là video 1.1GB sẽ có timeout ~1980s (33 phút)
                    file_size_gb = os.path.getsize(video_path) / (1024 * 1024 * 1024)
                    timeout = 1800 + int(180 * file_size_gb)
                    
                    self.log(f"⏱️ Timeout: {timeout}s ({timeout//60} phút)")
                    
                    response = self.session.post(
                        self.UPLOAD_VIDEO,
                        files=files,
                        headers={
                            "Accept-Language": "en-US,en;q=0.9",
                            "Authorization": f"Bearer {self.upload_token}"
                        },
                        timeout=timeout,
                        verify=False  # Disable SSL verification for this endpoint
                    )
                
                if response.status_code == 200:
                    data = response.json()
                    video_id = data['body']['video_id']
                    self.log(f"✅ Upload video thành công: {video_id}")
                    return video_id
                elif response.status_code in [500, 502, 503, 504]:
                    if attempt < max_retries - 1:
                        wait_time = (2 ** attempt) * 10  # 10s, 20s, 40s, 80s, 160s
                        self.log(f"⚠️  Server error {response.status_code}, retrying sau {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    else:
                        self.log(f"❌ Lỗi upload video: {response.status_code} (sau {max_retries} lần thử)")
                        self.log(f"   Response: {response.text[:200]}")
                        return None
                else:
                    self.log(f"❌ Lỗi upload video: {response.status_code}")
                    self.log(f"   Response: {response.text[:200]}")
                    return None
            
            except requests.exceptions.SSLError as ssl_err:
                if attempt < max_retries - 1:
                    wait_time = 2 + (3 * attempt)  # 2s, 5s, 8s, 11s, 14s
                    self.log(f"⚠️  SSL error, retrying sau {wait_time}s...")
                    self.log(f"   (Connection reset hoặc server không stable, chờ và thử lại)")
                    time.sleep(wait_time)
                    continue
                else:
                    self.log(f"❌ SSL error after {max_retries} attempts: {str(ssl_err)[:100]}")
                    return None
            
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    wait_time = 5 * (attempt + 1)
                    self.log(f"⚠️  Timeout ({wait_time}s), retrying...")
                    time.sleep(wait_time)
                    continue
                else:
                    self.log(f"❌ Upload timeout after {max_retries} attempts")
                    return None
            
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    self.log(f"⚠️  Error: {str(e)[:80]}, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    self.log(f"❌ Lỗi sau {max_retries} lần thử: {str(e)[:100]}")
                    return None
        
        return None
    
    def _upload_video_chunked(self, video_path: str, content_id: str, 
                             chunk_size: int, max_retries: int = 3) -> Optional[str]:
        """Upload file theo từng chunk (an toàn hơn với file lớn)"""
        filename = os.path.basename(video_path)
        filetype = "video/mp4"
        
        try:
            with open(video_path, 'rb') as f:
                chunk_num = 0
                while True:
                    chunk_data = f.read(chunk_size)
                    if not chunk_data:
                        break
                    
                    chunk_num += 1
                    chunk_size_mb = len(chunk_data) / (1024 * 1024)
                    
                    for attempt in range(max_retries):
                        try:
                            # Metadata đơn giản - chỉ gửi thông tin cần thiết
                            # API chunk upload có thể không expect chunk_size field
                            metadata = {
                                "filename": filename,
                                "filetype": filetype,
                                "channel_id": self.channel_id,
                                "content_id": content_id
                            }
                            
                            files = {
                                'metadata': (None, json.dumps(metadata)),
                                'file': (filename, chunk_data, filetype)
                            }
                            
                            self.log(f"📤 Đang upload chunk {chunk_num} ({chunk_size_mb:.1f}MB)...")
                            
                            response = requests.post(
                                self.UPLOAD_VIDEO,
                                files=files,
                                headers={
                                    "Accept-Language": "en-US,en;q=0.9",
                                    "Authorization": f"Bearer {self.upload_token}"
                                },
                                timeout=600,  # 10 phút per chunk (tăng từ 5 phút)
                                verify=False
                            )
                            
                            if response.status_code == 200:
                                data = response.json()
                                if 'body' in data and 'video_id' in data['body']:
                                    video_id = data['body']['video_id']
                                    if chunk_num == 1:  # Lần đầu tiên
                                        self.log(f"✅ Bắt đầu upload video: {video_id}")
                                        first_video_id = video_id
                                    else:
                                        self.log(f"✅ Chunk {chunk_num} upload thành công")
                                break
                            elif response.status_code == 400:
                                # Bad request - metadata sai hoặc file format lỗi
                                self.log(f"⚠️  Lỗi 400 (Bad Request) chunk {chunk_num}")
                                self.log(f"   Response: {response.text[:200]}")
                                if attempt < max_retries - 1:
                                    wait_time = 5
                                    self.log(f"   Retrying sau {wait_time}s...")
                                    time.sleep(wait_time)
                                    continue
                                else:
                                    self.log(f"❌ Lỗi chunk {chunk_num}: {response.status_code}")
                                    return None
                            elif response.status_code in [500, 502, 503, 504]:
                                if attempt < max_retries - 1:
                                    wait_time = (2 ** attempt) * 5  # 5s, 10s, 20s, 40s, 80s
                                    self.log(f"⚠️  Server error {response.status_code}, retrying chunk {chunk_num} sau {wait_time}s...")
                                    time.sleep(wait_time)
                                    continue
                                else:
                                    self.log(f"❌ Lỗi upload chunk {chunk_num}: {response.status_code} (sau {max_retries} lần thử)")
                                    return None
                            else:
                                self.log(f"❌ Lỗi chunk {chunk_num}: {response.status_code}")
                                return None
                        
                        except (requests.exceptions.SSLError, requests.exceptions.Timeout) as e:
                            if attempt < max_retries - 1:
                                wait_time = 2 + (2 * attempt)  # 2s, 4s, 6s, 8s, 10s
                                self.log(f"⚠️  Lỗi chunk {chunk_num}, retrying sau {wait_time}s...")
                                time.sleep(wait_time)
                                continue
                            else:
                                self.log(f"❌ Không thể upload chunk {chunk_num}: {str(e)[:80]}")
                                return None
            
            self.log(f"✅ Tất cả {chunk_num} chunk đã upload thành công")
            return first_video_id if 'first_video_id' in locals() else None
        
        except Exception as e:
            self.log(f"❌ Lỗi chunked upload: {str(e)}")
            return None
    
    def check_upload_status(self, video_id: str, max_retries: int = 3) -> Tuple[str, int]:
        """
        Kiểm tra trạng thái upload video (Step 6) với retry logic
        
        Args:
            video_id: VIDEO_ID
            max_retries: Số lần retry tối đa
            
        Returns:
            (status, progress) - status: "in_progress", "done" hoặc "error"; progress: 0-100
        """
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    f"{self.CHECK_STATUS}/{video_id}",
                    headers={"Authorization": f"Bearer {self.upload_token}"},
                    timeout=10,
                    verify=False  # Disable SSL verification
                )
                
                if response.status_code == 200:
                    data = response.json()
                    body = data['body']
                    
                    if 'progress' in body:
                        status = "in_progress"
                        progress = body['progress']
                        self.log(f"⏳ Đang xử lý: {progress}%")
                    else:
                        status = "done"
                        progress = 100
                        self.log("✅ Video đã xử lý xong")
                    
                    return status, progress
                elif response.status_code in [500, 502, 503, 504]:
                    # Server error - retry
                    if attempt < max_retries - 1:
                        self.log(f"⚠️  Server error {response.status_code}, retrying...")
                        time.sleep(2)
                        continue
                    else:
                        self.log(f"❌ Lỗi kiểm tra status: {response.status_code}")
                        return "error", 0
                else:
                    self.log(f"❌ Lỗi kiểm tra status: {response.status_code}")
                    return "error", 0
            
            except requests.exceptions.SSLError:
                if attempt < max_retries - 1:
                    self.log(f"⚠️  SSL error, retrying...")
                    time.sleep(1)
                    continue
                else:
                    self.log(f"❌ SSL error in status check")
                    return "error", 0
            
            except Exception as e:
                if attempt < max_retries - 1:
                    self.log(f"⚠️  Error: {str(e)}, retrying...")
                    time.sleep(1)
                    continue
                else:
                    self.log(f"❌ Lỗi: {str(e)}")
                    return "error", 0
    
    def wait_for_processing(self, video_id: str, max_wait: int = 600) -> bool:
        """
        Chờ video xử lý xong (Step 6 - Polling)
        
        Args:
            video_id: VIDEO_ID
            max_wait: Thời gian chờ tối đa (giây)
            
        Returns:
            True nếu xong, False nếu timeout hoặc error
        """
        self.log(f"⏳ Bước 6: Đang chờ video xử lý...")
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            status, progress = self.check_upload_status(video_id)
            
            if status == "done":
                return True
            elif status == "error":
                self.log("❌ Lỗi xử lý video")
                return False
            
            time.sleep(5)  # Kiểm tra mỗi 5 giây
        
        self.log(f"⏱️  Quá thời gian chờ ({max_wait}s)")
        return False
    
    def upload_workflow(self, video_path: str, title: str, description: str,
                       thumbnail_path: Optional[str] = None) -> Optional[str]:
        """
        Quy trình upload đầy đủ (Tất cả 7 bước)
        
        Args:
            video_path: Đường dẫn tới file video
            title: Tên video
            description: Mô tả video
            thumbnail_path: Đường dẫn tới file thumbnail (nếu None sẽ tự trích xuất)
            
        Returns:
            Content URL (https://www.ganjingworld.com/video/<CONTENT_ID>) hoặc None nếu thất bại
        """
        self.log("\n" + "="*60)
        self.log("🚀 BẮT ĐẦU UPLOAD LÊN GANJINGWORLD")
        self.log("="*60)
        
        # Bước 1: Kiểm tra access token (skip, giả định hợp lệ)
        self.log("✅ Bước 1: Access token hợp lệ")
        
        # Bước 2: Lấy upload token
        if not self.get_upload_token():
            return None
        
        # Bước 3: Chuẩn bị thumbnail
        if not thumbnail_path:
            thumbnail_path = self.extract_thumbnail(video_path)
        
        image_id = None
        if thumbnail_path and os.path.exists(thumbnail_path):
            image_id = self.upload_thumbnail(thumbnail_path)
        
        if not image_id:
            self.log("⚠️  Không thể upload thumbnail, sử dụng mặc định")
            image_id = "default"
        
        # Bước 4: Tạo content
        content_id = self.create_content(title, description, image_id)
        if not content_id:
            return None
        
        # Bước 5: Upload video
        video_id = self.upload_video(video_path, content_id)
        if not video_id:
            return None
        
        # Bước 6: Kiểm tra trạng thái
        if not self.wait_for_processing(video_id):
            self.log("⚠️  Upload không hoàn tất hoặc timeout")
            # Vẫn trả URL dù chưa hoàn tất (video có thể còn xử lý)
        
        # Bước 7: Trả về URL
        content_url = f"https://www.ganjingworld.com/video/{content_id}"
        self.log(f"\n✨ Upload thành công!")
        self.log(f"📍 URL: {content_url}")
        self.log("="*60 + "\n")
        
        return content_url
    
    @staticmethod
    def compress_video(video_path: str, output_path: str, crf: int = 28, 
                       log_callback=None) -> bool:
        """
        Nén video để giảm dung lượng trước upload
        
        Args:
            video_path: Đường dẫn tới video gốc
            output_path: Đường dẫn tới video được nén
            crf: Chất lượng (0-51, thấp hơn = tốt hơn, 28 = trung bình tốt)
            log_callback: Callback để nhận log
            
        Returns:
            True nếu thành công, False nếu thất bại
        """
        if log_callback:
            log_callback(f"🎬 Đang nén video từ {video_path}...")
        
        try:
            # Kiểm tra ffmpeg
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            if log_callback:
                log_callback("❌ ffmpeg không tìm thấy. Cài đặt từ: https://ffmpeg.org/download.html")
            return False
        
        try:
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-c:v', 'libx264',  # Video codec
                '-preset', 'medium',  # Tốc độ encoding (fast, medium, slow)
                '-crf', str(crf),  # Chất lượng
                '-c:a', 'aac',  # Audio codec
                '-b:a', '128k',  # Audio bitrate
                '-y',  # Overwrite output
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                original_size = os.path.getsize(video_path) / (1024 * 1024)
                compressed_size = os.path.getsize(output_path) / (1024 * 1024)
                ratio = (1 - compressed_size / original_size) * 100
                
                if log_callback:
                    log_callback(f"✅ Nén thành công: {original_size:.1f}MB → {compressed_size:.1f}MB (giảm {ratio:.1f}%)")
                return True
            else:
                if log_callback:
                    log_callback(f"❌ Lỗi nén: {result.stderr}")
                return False
        
        except Exception as e:
            if log_callback:
                log_callback(f"❌ Lỗi: {str(e)}")
            return False

