# ⚡ QUICK START - Hướng Dẫn Nhanh

## 🎯 Bắt Đầu Nhanh Nhất

### **Cách 1: Chạy từ Script (2 bước)**

```bash
# Bước 1: Cài dependencies
python -m pip install -r requirements.txt

# Bước 2: Chạy ứng dụng
python everything_downloader.py
```

### **Cách 2: Đóng Gói EXE (3 bước)**

```bash
# Bước 1: Cài PyInstaller
python -m pip install PyInstaller

# Bước 2: Đóng gói
python build_exe.py

# Bước 3: Chạy file EXE
dist/everything_downloader.exe
```

---

## 📝 Cách Sử Dụng Ứng Dụng

1. **Mở ứng dụng**

   - Chạy script: `python everything_downloader.py`
   - Hoặc chạy EXE: `everything_downloader.exe`

2. **Paste URL**

   - Copy link video từ YouTube hoặc Facebook
   - Paste vào ô input

3. **Click Download**

   - Click nút "📥 Download" hoặc nhấn Enter

4. **Xem tiến trình**

   - Theo dõi log real-time
   - Đợi cho đến khi hiển thị "✅ Tải thành công"

5. **Tìm video**
   - Mở thư mục `videos/` cùng cấp với chương trình
   - Video đã được lưu ở đó

---

## 🔗 Các URL được hỗ trợ

### YouTube

- `https://www.youtube.com/watch?v=...`
- `https://youtu.be/...`

### Facebook

- `https://www.facebook.com/reel/...`
- `https://www.facebook.com/share/v/...`
- `https://www.facebook.com/groups/.../permalink/...`

---

## ⚙️ Cài Đặt Dependencies (Nếu Cần)

```bash
# Cài tất cả
python -m pip install -r requirements.txt

# Hoặc cài riêng lẻ
python -m pip install PyQt6
python -m pip install yt-dlp
python -m pip install requests
```

---

## 🐛 Xử Lý Sự Cố Nhanh

| Lỗi                        | Giải Pháp                                |
| -------------------------- | ---------------------------------------- |
| `No module named 'PyQt6'`  | `pip install PyQt6`                      |
| `No module named 'yt_dlp'` | `pip install yt-dlp`                     |
| `Permission denied`        | Chạy terminal với quyền admin            |
| Video không tải            | Kiểm tra URL có đúng không, thử URL khác |

---

## 💾 Thư Mục Video

- **Script**: `everything_downloader/videos/`
- **EXE**: `videos/` (cùng cấp với exe)

---

## ✅ Kiểm Tra Cài Đặt

```bash
python test.py
```

Nếu thấy "✨ Test hoàn tất!" = ✓ Mọi thứ hoạt động!

---

**Chúc bạn tải video vui vẻ! 🎉**
