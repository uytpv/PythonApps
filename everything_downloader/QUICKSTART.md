## Quick Start Guide - Ganjingworld Upload Feature

### ⚡ 5-Minute Setup

#### Step 1: Get Your Credentials (2 min)
1. Log in to your Ganjingworld account
2. Go to Account Settings → API Access (or equivalent)
3. Copy your **Access Token** (long JWT string, ~200+ characters)
4. Copy your **Channel ID** (starts with "1frk", e.g., `1frk2ne41b04vrB9rtsk4yYgK1mo0c`)

#### Step 2: Launch Application (1 min)
```bash
python everything_downloader.py
```
Or run the compiled EXE: `EverythingDownloader_v0.3.exe`

#### Step 3: Enable Upload Feature (1 min)
1. In the GUI, look for section: **☁️ Ganjingworld Upload (Tùy chọn)**
2. Check the box: **🚀 Tự động upload lên Ganjingworld sau khi tải xong**
3. Two new input fields appear:
   - **🔑 Access Token** (paste your token here)
   - **📺 Channel ID** (paste your channel ID here)

#### Step 4: Download + Auto-Upload (1 min)
1. Paste a YouTube or Facebook URL
2. Click **📥 Download**
3. Video downloads normally
4. Upload automatically starts!
5. Watch progress in the log
6. Done! Video now on Ganjingworld

---

### 🎬 Example Workflow

```
User Action                          App Action                   Result
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Check upload checkbox              Inputs become visible
   ✅ "Tự động upload..."             Ready for credentials

2. Paste Access Token                 Field shows ••••••••••••••   Token stored
3. Paste Channel ID                   Field shows: 1frk2ne41b04... ID stored

4. Paste YouTube URL                  Field ready for input
   e.g., youtube.com/watch?v=xyz

5. Click "📥 Download"                ⠋ Downloading...            Video saved
                                      ✅ Tải hoàn tất!

6. (Auto-triggered)                   ⠙ Upload starting...
   Upload to Ganjingworld             ✅ Step 2: Token obtained
                                      ✅ Step 3: Thumbnail uploaded
                                      ✅ Step 4: Content created
                                      ✅ Step 5: Video uploading...
                                      ✅ Step 6: Processing...
                                      ✅ Upload hoàn tất!

7. View result in log                 📍 URL: ganjingworld.com/...  Success!
                                      URL in clipboard (can copy)
```

---

### 🔑 Credentials Format

**Access Token**
- Format: JWT token
- Looks like: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiJ...`
- Length: 200+ characters
- Display: Password field (hidden with dots)
- Expires: ~10 days (get new one if fails)

**Channel ID**
- Format: Text identifier
- Looks like: `1frk2ne41b04vrB9rtsk4yYgK1mo0c`
- Length: 20-30 characters
- Display: Normal text field
- No expiry (permanent)

---

### ⏱️ Processing Times

| Operation | Time |
|-----------|------|
| Download | 5-30 sec (depends on video length) |
| Extract Thumbnail | 1-2 sec |
| Upload Thumbnail | 1-3 sec |
| Create Content | 1 sec |
| Upload Video | 30-300 sec (depends on file size) |
| Process on Server | 30-180 sec |
| **Total** | **1-10 minutes** |

Larger videos = longer upload time

---

### ✅ Success Indicators

When upload is complete, you'll see:
```
✨ Upload thành công!
📍 URL: https://www.ganjingworld.com/video/content_id_xxx
```

The URL is clickable and takes you directly to your video on Ganjingworld.

---

### ❌ Common Issues & Fixes

| Problem | Solution |
|---------|----------|
| "Vui lòng nhập Access Token" | Make sure checkbox is checked and token pasted |
| "Vui lòng nhập Channel ID" | Make sure checkbox is checked and ID pasted |
| "Lỗi lấy upload token: 401" | Token expired - get new one from Ganjingworld |
| "Lỗi lấy upload token: 403" | Channel ID doesn't match token - verify both |
| Upload freezes | Check internet connection, very large file? |
| "Không tìm thấy file video" | Download may have failed - try again |
| FFmpeg error | Make sure FFmpeg is installed and in PATH |

---

### 🎓 Tips & Tricks

**Tip 1: Security**
- Never share your Access Token
- Re-enter credentials each session (not saved)
- Token is shown as password field for safety

**Tip 2: Large Files**
- Large videos take longer to upload
- App stays responsive (doesn't freeze)
- Watch the log for progress

**Tip 3: Multiple Videos**
- You can download multiple videos
- Enable upload only for ones you want uploaded
- Each upload gets new content URL

**Tip 4: Video Titles**
- Title auto-set to filename (minus extension)
- Description: "Tải lên bởi Everything Downloader"
- Future: Manual title/description input

**Tip 5: Thumbnails**
- Auto-extracted from 5-second mark
- Future: Custom thumbnail upload

---

### 📱 UI Layout

```
┌─────────────────────────────────────────────────────────┐
│ 📹 Everything Downloader - YouTube & Facebook          │ ← Title
├─────────────────────────────────────────────────────────┤
│ 📥 Nhập URL Video:                                      │
│ ┌──────────────────────────────────┐ ┌──────────────┐  │
│ │ Paste URL...                     │ │ 📥 Download  │  │
│ └──────────────────────────────────┘ └──────────────┘  │
├─────────────────────────────────────────────────────────┤
│ ☁️ Ganjingworld Upload (Tùy chọn):                      │ ← NEW
│ ☑️ 🚀 Tự động upload lên Ganjingworld sau khi tải xong │ ← NEW
│                                                         │
│ 🔑 Access Token:  ┌────────────────────────────────┐   │ ← NEW
│                   │ ••••••••••••••••••••••••••••   │   │
│                   └────────────────────────────────┘   │
│                                                         │
│ 📺 Channel ID:    ┌────────────────────────────────┐   │ ← NEW
│                   │ 1frk2ne41b04vrB9rtsk4yYgK1... │   │
│                   └────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│ 📋 Tiến Trình Tải:                                      │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ [22:40:15] ✅ Ready                                 │ │
│ │ [22:40:20] ✨ Download complete!                   │ │
│ │ [22:40:22] ⠙ Uploading to Ganjingworld...          │ │
│ │ [22:41:15] ✅ Upload successful!                   │ │
│ │ [22:41:15] 📍 URL: ganjingworld.com/video/xxx      │ │
│ └─────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│ ✅ Tải thành công  📁 Thư mục: .../videos             │
└─────────────────────────────────────────────────────────┘
```

**Areas marked "← NEW" are the new Ganjingworld features.**

---

### 🔄 Disable Upload

To disable Ganjingworld upload:
1. Uncheck: **🚀 Tự động upload lên Ganjingworld sau khi tải xong**
2. Input fields disappear and are disabled
3. App works normally (just download, no upload)
4. To re-enable: Check box again and enter credentials

---

### 📊 What Happens Behind Scenes

When you click Download with upload enabled:

```
1. Download Module
   ├─ Fetches video from YouTube/Facebook
   ├─ Converts to MP4 if needed
   └─ Saves to /videos folder

2. File Tracking
   ├─ Remembers file location
   └─ Passes to upload module

3. Upload Module
   ├─ Validates credentials
   ├─ Gets upload token from GJW
   ├─ Extracts thumbnail via FFmpeg
   ├─ Uploads thumbnail
   ├─ Creates content metadata
   ├─ Uploads video file
   ├─ Waits for server processing
   └─ Returns content URL

4. GUI Update
   ├─ Shows progress in log
   ├─ Updates status label
   └─ Final URL displayed
```

All in separate threads so GUI never freezes! 🎯

---

### 🚀 Ready to Go!

You're all set! Follow these steps:
1. ✅ Get credentials from Ganjingworld
2. ✅ Launch Everything Downloader
3. ✅ Check upload checkbox
4. ✅ Enter credentials
5. ✅ Download a video
6. ✅ Watch it upload automatically!

---

### 📞 Need Help?

Refer to:
- **GANJINGWORLD_FEATURE.md** - Full feature documentation
- **IMPLEMENTATION_SUMMARY.md** - Technical details
- Log output - Shows what's happening at each step

### ⚡ Performance

- App startup: ~2 seconds
- Video download: 5-30 seconds (varies)
- Video upload: 30-300 seconds (file size dependent)
- Typical end-to-end: **1-10 minutes**

**Everything is non-blocking - app stays responsive!** 💪

---

**Enjoy automated video downloads + uploads to Ganjingworld!** 🎉
