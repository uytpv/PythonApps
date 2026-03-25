# 🎨 GUI PREVIEW - Giao Diện Ứng Dụng

## 📺 Bố Cục Ứng Dụng

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  📹 Everything Downloader - YouTube & Facebook          [_][□][X]           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  📥 Nhập URL Video:                                                         ║
║  ┌──────────────────────────────────────────────────────────────┬──────────┐ ║
║  │ Paste URL YouTube hoặc Facebook tại đây...                  │ Download │ ║
║  └──────────────────────────────────────────────────────────────┴──────────┘ ║
║                                                                              ║
║  📋 Tiến Trình Tải:                                                         ║
║  ┌──────────────────────────────────────────────────────────────────────────┐ ║
║  │ [17:44:49] ============================================================ │ ║
║  │ [17:44:49] 🎬 Everything Downloader - YouTube & Facebook Video...       │ ║
║  │ [17:44:49] ============================================================ │ ║
║  │ [17:44:49] 📁 Thư mục lưu video: c:\...\videos                         │ ║
║  │ [17:44:49] ============================================================ │ ║
║  │ [17:44:50]                                                             │ ║
║  │ [17:44:51] [1/1] 🔄 Đang tải: https://www.youtube.com/watch?v=...      │ ║
║  │ [17:44:51] 🔍 Loại URL: YOUTUBE                                        │ ║
║  │ [17:44:51] ℹ️ Downloading format 251 from ...                          │ ║
║  │ [17:44:54] ℹ️ Downloaded 45%.                                          │ ║
║  │ [17:44:57] ℹ️ Downloaded 89%.                                          │ ║
║  │ [17:44:59] ✅ Tải thành công: c:\...\videos\Video_Title.mp4            │ ║
║  │ [17:45:00] ✨ Tải hoàn tất!                                            │ ║
║  │ [17:45:00] ============================================================ │ ║
║  └──────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  ✅ Tải thành công          📁 Thư mục: c:\Users\...\videos                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## 🎯 Các Thành Phần

### 1️⃣ **Input Section**

```
📥 Nhập URL Video:
┌─────────────────────────────────────────────────────────────┬──────────┐
│ Paste URL YouTube hoặc Facebook tại đây...                  │ Download │
└─────────────────────────────────────────────────────────────┴──────────┘
```

- **Input Field**: Nhập hoặc paste URL
- **Download Button**: Màu xanh, kích thước lớn
- **Shortcut**: Nhấn Enter để tải

### 2️⃣ **Log Display Section**

```
📋 Tiến Trình Tải:
┌──────────────────────────────────────────────────────────────────────────┐
│ [HH:MM:SS] Log message here...                                           │
│ [HH:MM:SS] 🔄 Status update...                                           │
│ [HH:MM:SS] ✅ Success message...                                         │
└──────────────────────────────────────────────────────────────────────────┘
```

- **Timestamp**: [HH:MM:SS] cho mỗi dòng
- **Emoji**: Biểu thị loại message
- **Auto-scroll**: Cuộn xuống dưới cùng tự động
- **Dark theme**: Nền đen, chữ xanh (như terminal)

### 3️⃣ **Status Section**

```
✅ Tải thành công          📁 Thư mục: c:\Users\...\videos
```

- **Status Label**:
  - 🟢 ✅ Sẵn sàng (Xanh)
  - 🟡 ⏳ Đang tải (Vàng)
  - 🔴 ❌ Lỗi (Đỏ)
- **Folder Info**: Hiển thị đường dẫn thư mục videos

## 📊 Kích Thước Cửa Sổ

- **Width**: 900px
- **Height**: 700px
- **Responsive**: Tự động điều chỉnh

## 🎨 Màu Sắc & Style

### **Button**

```
Normal: #4CAF50 (Green)
Hover: #45a049 (Dark Green)
Pressed: #3d8b40 (Very Dark Green)
Disabled: #cccccc (Gray)
Text: White, Bold
```

### **Log Display**

```
Background: #1e1e1e (Very Dark Gray)
Text: #00ff00 (Green - Terminal style)
Border: #333333 (Dark Gray)
```

### **Input Field**

```
Background: White
Border: Light Gray
Placeholder: Gray
```

### **Labels**

```
Title: Bold, 11pt
Info: 9pt, Light Gray
Status: Bold, Color-coded
```

## 🔄 Interaction Flow

### **Scenario 1: Tải YouTube Video**

```
1. User opens app
   ↓
2. User pastes: https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ↓
3. User clicks "Download"
   ↓
4. GUI detects URL type: YOUTUBE
   ↓
5. yt-dlp starts downloading in separate thread
   ↓
6. Real-time log updates
   ↓
7. Video saves to: videos/[Title].mp4
   ↓
8. Status shows: ✅ Tải thành công
```

### **Scenario 2: Tải Facebook Reel**

```
1. User pastes: https://www.facebook.com/reel/4258812534390478
   ↓
2. User clicks "Download"
   ↓
3. GUI detects URL type: FACEBOOK
   ↓
4. yt-dlp downloads video
   ↓
5. Filename is cleaned (removes emoji, special chars)
   ↓
6. Video saves to: videos/[Cleaned_Title].mp4
   ↓
7. Status shows: ✅ Tải thành công
```

### **Scenario 3: Error Handling**

```
1. User enters invalid URL
   ↓
2. User clicks "Download"
   ↓
3. GUI shows: ❌ URL không được hỗ trợ
   ↓
4. Status shows: ❌ Tải thất bại
   ↓
5. Log displays error message
   ↓
6. User can try again with valid URL
```

## 📱 Responsive Behavior

### **Min Window Size**

```
Width: 600px
Height: 500px
```

### **Max Window Size**

```
Width: 1400px
Height: 1000px
```

### **Elements Scale**

- Input field: Flexible width
- Buttons: Fixed width (120px)
- Log area: Expandable height
- Text: Readable at any size

## ⌨️ Keyboard Shortcuts

| Shortcut | Action              |
| -------- | ------------------- |
| Enter    | Start download      |
| Ctrl+A   | Select all in input |
| Ctrl+V   | Paste URL           |
| Ctrl+C   | Copy from log       |

## 🖱️ Mouse Actions

| Action             | Result               |
| ------------------ | -------------------- |
| Click Input        | Focus input          |
| Click Download     | Start download       |
| Hover Button       | Button changes color |
| Scroll Log         | Manual scroll        |
| Double-click Input | Select all           |

## 🎯 UX Best Practices

✓ **Clear Visual Hierarchy**

- Input at top (most important)
- Log in middle (feedback)
- Status at bottom (summary)

✓ **Immediate Feedback**

- Button color changes on hover
- Log updates in real-time
- Status changes reflect process

✓ **Error Prevention**

- Validate URL before download
- Check folder permissions
- Handle network errors gracefully

✓ **User Guidance**

- Placeholder text in input
- Status messages with emoji
- Log shows detailed process

✓ **Accessibility**

- Large, readable fonts
- High contrast colors
- Clear button labels
- Keyboard navigation support

---

**Design Philosophy**: Simple, Clean, Functional
**Target Users**: Non-technical users
**Learning Curve**: 30 seconds
**Time to Download**: 1 minute (including copy-paste)

🎨 **Desain yang berfokus pada UX!**
