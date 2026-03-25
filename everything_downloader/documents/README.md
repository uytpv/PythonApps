# 📹 Everything Downloader - YouTube & Facebook Video Downloader

Ứng dụng desktop đơn giản để tải video từ YouTube và Facebook.

## 🎯 Tính năng

- ✅ Tải video từ YouTube
- ✅ Tải video từ Facebook (Reels, Posts, Videos trong Groups)
- ✅ Giao diện GUI đơn giản, dễ sử dụng
- ✅ Hiển thị tiến trình tải real-time
- ✅ Tự động lưu video vào thư mục `videos` cùng cấp với chương trình

## 📦 Yêu cầu

### Để chạy từ script:

- Python 3.8+
- PyQt6
- yt-dlp
- requests

### Để chạy file EXE:

- Windows (bất kỳ phiên bản)
- Không cần cài đặt Python

## 🚀 Cách sử dụng

### Tùy chọn 1: Chạy từ script

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Chạy ứng dụng
python everything_downloader.py
```

### Tùy chọn 2: Chạy file EXE

1. **Đóng gói thành EXE:**

   ```bash
   pip install PyInstaller
   python build_exe.py
   ```

2. **Chạy file EXE:**
   - Tìm file `everything_downloader.exe` trong thư mục `dist/`
   - Chạy file exe
   - Video sẽ được lưu trong thư mục `videos/` cùng cấp với exe

## 📖 Hướng dẫn sử dụng

1. Mở ứng dụng
2. Copy URL video từ YouTube hoặc Facebook vào ô input
3. Click nút "📥 Download" hoặc nhấn Enter
4. Chương trình tự động tải video
5. Video sẽ được lưu vào thư mục `videos/`

## 📝 Các link được hỗ trợ

### YouTube:

- https://www.youtube.com/watch?v=...
- https://youtu.be/...

### Facebook:

- https://www.facebook.com/reel/...
- https://www.facebook.com/share/v/...
- https://www.facebook.com/groups/.../permalink/...

## 🔧 Cấu trúc thư mục

```
everything_downloader/
├── everything_downloader.py      # File main
├── downloader_core.py             # Module tải video
├── gui.py                         # Giao diện PyQt6
├── build_exe.py                   # Script đóng gói
├── requirements.txt               # Dependencies
├── README.md                      # Hướng dẫn
├── dist/                          # Thư mục chứa file EXE (sau khi build)
│   └── everything_downloader.exe  # File EXE
└── videos/                        # Thư mục lưu video
    └── [video files here]
```

## ⚙️ Cài đặt (nếu cần)

Nếu gặp lỗi liên quan đến ffmpeg, bạn có thể cần cài ffmpeg:

### Windows:

1. Download từ: https://ffmpeg.org/download.html
2. Hoặc sử dụng package manager:
   ```bash
   choco install ffmpeg
   ```

## 🐛 Xử lý sự cố

### Lỗi: "No module named 'PyQt6'"

```bash
pip install PyQt6
```

### Lỗi: "Unable to open file"

Đảm bảo thư mục `videos/` tồn tại hoặc sẽ được tạo tự động.

### Lỗi: "Signature extraction failed"

Đây là lỗi YouTube có thể gặp. Thử lại sau hoặc update yt-dlp:

```bash
pip install --upgrade yt-dlp
```

## 📄 License

MIT License

## 👨‍💻 Tác giả

UY - 2025

---

**Chúc bạn sử dụng vui vẻ! 🎉**
