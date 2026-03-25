# 💾 INSTALLATION GUIDE - Hướng Dẫn Cài Đặt

## 📋 Mục Lục

1. [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
2. [Cài Đặt Python](#cài-đặt-python)
3. [Cài Đặt Dependencies](#cài-đặt-dependencies)
4. [Chạy Từ Script](#chạy-từ-script)
5. [Đóng Gói Thành EXE](#đóng-gói-thành-exe)
6. [Cài FFmpeg (Nếu Cần)](#cài-ffmpeg-nếu-cần)
7. [Xử Lý Sự Cố](#xử-lý-sự-cố)

---

## ⚙️ Yêu Cầu Hệ Thống

### **Minimum Requirements**

- **OS**: Windows 10, 11, hoặc mới hơn
- **RAM**: 2 GB (2 GB)
- **Disk**: 500 MB (cho dependencies + video)
- **Internet**: Connection cần thiết để tải video

### **Recommended Requirements**

- **OS**: Windows 11
- **RAM**: 4 GB hoặc hơn
- **Disk**: 1 GB + dung lượng cho video
- **Internet**: Tốc độ cao (4G, Fiber)

---

## 🐍 Cài Đặt Python

### **Bước 1: Download Python**

1. Truy cập https://www.python.org/downloads/
2. Click "Download Python 3.11.x" (phiên bản mới nhất)
3. Chọn Windows installer (64-bit)

### **Bước 2: Cài Đặt**

1. Chạy file `python-3.11.x-amd64.exe`
2. **QUAN TRỌNG**: Tick "Add Python to PATH"
3. Click "Install Now"
4. Chờ cài đặt hoàn tất

### **Bước 3: Kiểm Tra**

Mở Command Prompt (cmd) và gõ:

```bash
python --version
```

Output:

```
Python 3.11.x
```

---

## 📦 Cài Đặt Dependencies

### **Cách 1: Tự động (Recommended)**

```bash
# Mở cmd/PowerShell tại thư mục everything_downloader

cd c:\Users\UY\works\_PythonApps\everything_downloader

# Cài tất cả dependencies
pip install -r requirements.txt
```

### **Cách 2: Thủ công**

```bash
# Cài từng package

pip install PyQt6==6.10.0
pip install yt-dlp==2024.11.18
pip install requests==2.31.0
```

### **Cách 3: Upgrade pip (Nếu Có Lỗi)**

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Sau đó cài lại dependencies
pip install -r requirements.txt
```

---

## 🎬 Chạy Từ Script

### **Bước 1: Mở Terminal**

```bash
# Tại Windows:
# - Nhấn Win + R
# - Gõ: cmd
# - Nhấn Enter

# Hoặc PowerShell:
# - Nhấn Win + X
# - Chọn "Windows PowerShell"
```

### **Bước 2: Navigate đến Thư Mục**

```bash
cd c:\Users\UY\works\_PythonApps\everything_downloader
```

### **Bước 3: Chạy Ứng Dụng**

```bash
python everything_downloader.py
```

### **Kết Quả**

- Cửa sổ GUI xuất hiện
- Ứng dụng sẵn sàng sử dụng

---

## 📦 Đóng Gói Thành EXE

### **Bước 1: Cài PyInstaller**

```bash
pip install PyInstaller
```

### **Bước 2: Đóng Gói**

```bash
cd c:\Users\UY\works\_PythonApps\everything_downloader
python build_exe.py
```

**Thời gian chờ**: 3-5 phút (lần đầu sẽ dài hơn)

### **Bước 3: Tìm File EXE**

```
c:\Users\UY\works\_PythonApps\everything_downloader\dist\everything_downloader.exe
```

### **Bước 4: Copy & Chạy**

1. Copy file `everything_downloader.exe` đến thư mục riêng
2. Double-click để chạy
3. Ứng dụng tự động tạo thư mục `videos/`

---

## 🔧 Cài FFmpeg (Nếu Cần)

FFmpeg là công cụ xử lý video. Thường yt-dlp sẽ tự động tải.

### **Cách 1: Tự động (Easy)**

```bash
# yt-dlp sẽ tự động download FFmpeg
# Không cần làm gì
```

### **Cách 2: Cài thủ công**

Windows (sử dụng Chocolatey):

```bash
# Cài Chocolatey (nếu chưa có)
# Làm theo: https://chocolatey.org/install

# Cài FFmpeg
choco install ffmpeg
```

Windows (không có Chocolatey):

1. Download từ: https://ffmpeg.org/download.html
2. Giải nén
3. Thêm vào PATH (Environment Variables)

---

## 🧪 Kiểm Tra Cài Đặt

### **Test 1: Kiểm Tra Python**

```bash
python --version
# Output: Python 3.11.x
```

### **Test 2: Kiểm Tra Dependencies**

```bash
pip list | findstr PyQt6
pip list | findstr yt-dlp
pip list | findstr requests
```

### **Test 3: Chạy Test Script**

```bash
cd c:\Users\UY\works\_PythonApps\everything_downloader
python test.py
# Output: ✨ Test hoàn tất!
```

### **Test 4: Chạy Ứng Dụng**

```bash
python everything_downloader.py
# Output: GUI xuất hiện
```

---

## 🐛 Xử Lý Sự Cố

### **Lỗi 1: Python không tìm được**

```
'python' is not recognized as an internal or external command
```

**Giải pháp:**

1. Cài lại Python
2. **Nhớ tick "Add Python to PATH"**
3. Restart Windows

### **Lỗi 2: Module không tìm được**

```
ModuleNotFoundError: No module named 'PyQt6'
```

**Giải pháp:**

```bash
pip install PyQt6
```

### **Lỗi 3: Permission denied**

```
PermissionError: [Errno 13] Permission denied
```

**Giải pháp:**

1. Chạy cmd/PowerShell với quyền Admin
2. Hoặc chọn thư mục có quyền ghi

### **Lỗi 4: EXE không chạy**

```
Application failed to start
```

**Giải pháp:**

1. Kiểm tra Windows version
2. Cập nhật Windows
3. Cài .NET Framework 4.7+

### **Lỗi 5: Video không tải**

```
[youtube] ERROR: unable to extract video data
```

**Giải pháp:**

1. Update yt-dlp: `pip install --upgrade yt-dlp`
2. Kiểm tra URL có đúng
3. Thử lại sau vài phút

### **Lỗi 6: Không có dung lượng**

```
[download] Insufficient disk space
```

**Giải pháp:**

1. Xóa video cũ hoặc file không cần
2. Dọn dẹp Windows
3. Sử dụng ổ khác nếu có

---

## 📊 Dung Lượng Dependencies

| Package     | Dung Lượng  |
| ----------- | ----------- |
| PyQt6       | ~100 MB     |
| yt-dlp      | ~10 MB      |
| requests    | ~2 MB       |
| PyInstaller | ~50 MB      |
| **Tổng**    | ~**160 MB** |

**Lưu ý**: EXE đóng gói sẽ có dung lượng ~300-400 MB

---

## 💻 Tập Lệnh Cài Đặt Nhanh

### **Windows (Batch Script)**

Tạo file `install.bat`:

```batch
@echo off
echo Installing Everything Downloader...
pip install --upgrade pip
pip install -r requirements.txt
echo Installation complete!
pause
```

Chạy: Double-click `install.bat`

### **Windows (PowerShell Script)**

Tạo file `install.ps1`:

```powershell
Write-Host "Installing Everything Downloader..."
pip install --upgrade pip
pip install -r requirements.txt
Write-Host "Installation complete!"
```

Chạy: `powershell -ExecutionPolicy Bypass -File install.ps1`

---

## 🎯 Checklist Cài Đặt

- [ ] Python 3.8+ đã cài
- [ ] Python đã thêm vào PATH
- [ ] pip list cho thấy PyQt6, yt-dlp, requests
- [ ] Test script chạy thành công
- [ ] Ứng dụng GUI mở được
- [ ] Tải video thành công
- [ ] Video lưu vào thư mục videos/

---

## 📞 Cần Giúp?

### **Bước Troubleshooting:**

1. Kiểm tra Python version: `python --version`
2. Kiểm tra pip: `pip --version`
3. Chạy test: `python test.py`
4. Kiểm tra log lỗi
5. Tìm giải pháp trên Google

### **Các Tài Nguyên**

- Python Docs: https://docs.python.org/
- PyQt6 Docs: https://doc.qt.io/qtforpython-6/
- yt-dlp GitHub: https://github.com/yt-dlp/yt-dlp
- Windows Troubleshooting: https://support.microsoft.com

---

## ✅ Cài Đặt Hoàn Tất!

Nếu tất cả các bước trên đều thành công:

```bash
python everything_downloader.py
```

**Chúc bạn sử dụng vui vẻ! 🎉**

---

**Phiên Bản**: 1.0.0
**Cập Nhập**: 2025-11-29
