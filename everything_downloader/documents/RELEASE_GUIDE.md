# 📦 RELEASE GUIDE - Hướng Dẫn Phát Hành

**Cách tạo và phân phối ứng dụng cho người dùng cuối**

---

## 🎯 Mục Đích

Tạo một **release package sạch** cho người dùng:

- ✅ Chỉ chứa `.exe` (không có source code)
- ✅ README.txt với hướng dẫn
- ✅ Folder `videos/` để lưu video
- ✅ Người dùng chỉ cần chạy `.exe`

---

## 🚀 Cách Tạo Release Package

### **Bước 1: Chạy Build Script**

```bash
cd c:\Users\UY\works\_PythonApps\everything_downloader
python build_release.py
```

**Kết quả:**

- ✅ Tạo file `everything_downloader.exe`
- ✅ Tạo thư mục `release/`
- ✅ Chứa: `.exe` + `README.txt` + `videos/`

### **Bước 2: Kiểm Tra Release Folder**

```
release/
├── everything_downloader.exe    ← File chạy duy nhất
├── README.txt                  ← Hướng dẫn sử dụng
└── videos/                     ← Thư mục lưu video
```

### **Bước 3: Phân Phối**

Copy toàn bộ folder `release/` cho người dùng:

```
Gửi folder: c:\...\everything_downloader\release\
```

---

## 👤 Cho Người Dùng

### **Hướng Dẫn Sử Dụng:**

1. **Tải folder từ bạn**

   - Nhận folder `release/` từ bạn
   - Giải nén (nếu là `.zip`)

2. **Chạy ứng dụng**

   - Double-click `everything_downloader.exe`
   - GUI xuất hiện

3. **Tải video**

   - Paste URL từ YouTube/Facebook
   - Click "Download"

4. **Tìm video**
   - Mở thư mục `videos/`
   - Video ở đây!

**Đơn giản như vậy! 🎉**

---

## 📁 Cấu Trúc Release

```
release/
│
├── 🎯 EXECUTABLE
│   └── everything_downloader.exe    (350-400 MB)
│
├── 📖 DOCUMENTATION
│   └── README.txt                  (Hướng dẫn)
│
└── 📁 DATA
    └── videos/                     (Thư mục output)
```

---

## 🔒 Che Giấu Source Code

**Lợi Ích:**
✅ Người dùng không thấy code
✅ Người dùng không thể sửa code
✅ Ứng dụng trông chuyên nghiệp
✅ Dễ dàng phân phối

**Trong Release Package:**

- ❌ Không có `.py` files
- ❌ Không có `downloader_core.py`
- ❌ Không có `gui.py`
- ❌ Không có `documents/`
- ❌ Không có `build/`, `dist/`, `__pycache__/`

**Chỉ có:**

- ✅ `everything_downloader.exe` (chứa tất cả)
- ✅ `README.txt` (hướng dẫn)
- ✅ `videos/` (thư mục output)

---

## 📦 File Build Scripts

### **build_exe.py** (Cũ)

- Chỉ tạo file `.exe` trong thư mục `dist/`
- Cần setup thêm

### **build_release.py** (Mới) ⭐

- Tạo `.exe`
- Tạo folder `release/` sạch
- Thêm `README.txt`
- Tạo thư mục `videos/`
- **Người dùng chỉ cần folder `release/`**

---

## 💡 So Sánh

### **Trước (Dev Folder):**

```
everything_downloader/
├── *.py files (source code)
├── documents/
├── requirements.txt
├── build/
├── dist/
└── ... (rối rắm)
```

❌ Người dùng nhìn thấy tất cả

### **Sau (Release Folder):**

```
release/
├── everything_downloader.exe
├── README.txt
└── videos/
```

✅ Sạch, chuyên nghiệp, dễ dùng

---

## 🎯 Qui Trình Phát Hành

```
1. Chạy build_release.py
         ↓
2. Kiểm tra folder release/
         ↓
3. Compress thành .zip (optional)
         ↓
4. Gửi cho người dùng
         ↓
5. Người dùng extract & chạy
         ↓
6. Tải video ✅
```

---

## 🗜️ Optional: Compress thành ZIP

### **Nếu muốn gửi file nhỏ hơn:**

```python
import shutil

# Compress release folder
shutil.make_archive(
    'everything_downloader_v1.0.0',
    'zip',
    'release'
)
```

**Kết quả:**

- `everything_downloader_v1.0.0.zip` (~150 MB)
- Người dùng extract → Chạy

---

## 📊 Release Package Size

| Item            | Size            |
| --------------- | --------------- |
| .exe            | 350-400 MB      |
| README.txt      | <1 KB           |
| videos/ (empty) | 0 KB            |
| **Total**       | **~350-400 MB** |

---

## ✅ Checklist Phát Hành

- [ ] Chạy `python build_release.py` thành công
- [ ] Folder `release/` tồn tại
- [ ] Có file `.exe`
- [ ] Có file `README.txt`
- [ ] Có thư mục `videos/`
- [ ] Test chạy `.exe` (double-click)
- [ ] Tải được video
- [ ] Compress (nếu muốn)
- [ ] Gửi cho người dùng

---

## 🚀 Quick Commands

```bash
# Build release package
python build_release.py

# Copy cho người dùng
xcopy release "D:\Share\everything_downloader" /E

# Compress
python -c "import shutil; shutil.make_archive('release', 'zip', 'release')"
```

---

## 📞 Troubleshooting

### **Q: EXE không chạy?**

A: Cập nhật yt-dlp: `pip install --upgrade yt-dlp` → Build lại

### **Q: File quá to?**

A: Đó là bình thường (PyQt6, yt-dlp, FFmpeg = ~350 MB)

### **Q: Người dùng yêu cầu code?**

A: Giải thích là compiled binary, không thể cung cấp source

### **Q: Muốn thêm logo?**

A: Edit `build_release.py`, thêm icon

---

## 🎓 Để Lần Sau

Nếu muốn tạo installer (.msi):

```bash
pip install pyinstaller-hooks-contrib
# ... cấu hình advanced
```

---

## ✨ Kết Luận

**Quy Trình Đơn Giản:**

1. `python build_release.py`
2. Gửi folder `release/`
3. Người dùng chạy `.exe`
4. Done! ✅

**Người dùng không cần biết về:**

- ❌ Python
- ❌ Terminal
- ❌ Dependencies
- ❌ Source code

**Chỉ cần:**

- ✅ Double-click `.exe`
- ✅ Sử dụng ứng dụng

---

**Version**: 1.0.0
**Date**: 2025-11-29

👉 [Back to INDEX.md](INDEX.md)
