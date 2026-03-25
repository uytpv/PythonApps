## Ganjingworld Upload Integration

### Overview

Everything Downloader now supports automatic video upload to Ganjingworld after downloading from YouTube or Facebook. This feature allows users to seamlessly download videos and push them to their Ganjingworld channel in one workflow.

### Architecture

#### New Files

**`ganjingworld_uploader.py`** - Core upload module
- Implements full Ganjingworld API integration
- Handles 7-step upload workflow
- Uses FFmpeg for thumbnail extraction
- Logging support via callbacks

#### Modified Files

**`gui.py`** - Enhanced with upload UI
- Added QCheckBox to enable/disable upload
- Added Access Token input field
- Added Channel ID input field
- Integrated upload workflow into download process
- Thread-safe GUI updates

### Features

#### 1. Upload Toggle Checkbox
- Located in UI under "Ganjingworld Upload (Tùy chọn)"
- When checked: Shows/enables Access Token and Channel ID inputs
- When unchecked: Hides/disables inputs

#### 2. Credentials Management
- **Access Token**: JWT token from Ganjingworld (64+ characters)
  - Displayed as password field for security
  - Required when upload is enabled
  
- **Channel ID**: Your Ganjingworld channel identifier
  - Typically starts with "1frk"
  - Required when upload is enabled

#### 3. Upload Workflow
When user clicks Download with upload enabled:
1. Video downloads normally
2. After download completes, upload starts automatically
3. 7-step process:
   - Get upload token from Ganjingworld API
   - Extract thumbnail from video (5-second mark)
   - Upload thumbnail image
   - Create content draft with metadata
   - Upload video file
   - Poll for processing completion
   - Return content URL

### Usage

#### Step 1: Get Credentials
1. Visit Ganjingworld account settings
2. Generate/copy Access Token (JWT format)
3. Get your Channel ID

#### Step 2: Enable Upload in GUI
1. Check the checkbox: "Tự động upload lên Ganjingworld sau khi tải xong"
2. Input fields appear: Access Token and Channel ID
3. Paste your credentials into respective fields

#### Step 3: Download and Upload
1. Paste YouTube/Facebook URL
2. Click "📥 Download" button
3. App downloads video
4. Upload starts automatically if enabled
5. Watch progress in log display
6. Final URL appears in log when complete

### Technical Details

#### API Endpoints Used
- `https://gw.ganjingworld.com/v1.0c/get-vod-token` - Get upload token
- `https://imgapi.cloudokyo.cloud/api/v1/image` - Upload thumbnail
- `https://gw.ganjingworld.com/v1.0c/add-content` - Create content
- `https://vodapi.cloudokyo.cloud/api/v1/video` - Upload video
- `https://vodapi.cloudokyo.cloud/api/v1/status` - Check status

#### Dependencies
- `requests` - HTTP API calls
- `subprocess` - FFmpeg integration
- `PyQt6` - GUI (already used)

#### Threading Model
- Download runs in thread (existing)
- Upload runs in separate thread
- UI updates via Qt signals (thread-safe)
- All blocking operations don't freeze GUI

#### Error Handling
- Validates credentials before upload
- Checks file existence
- Handles API errors gracefully
- Timeout handling (600s for video upload)
- Logs all errors for debugging

### Log Output Examples

#### Successful Upload
```
============================================================
☁️ Bắt đầu upload lên Ganjingworld...
============================================================

📝 Bước 2: Đang lấy upload token...
✅ Lấy upload token thành công
🎨 Bước 3a: Đang trích xuất thumbnail từ video...
✅ Trích xuất thumbnail thành công
🖼️  Bước 3b: Đang upload thumbnail...
✅ Upload thumbnail thành công
📄 Bước 4: Đang tạo nội dung draft...
✅ Tạo nội dung thành công: video_id_xxx
🎬 Bước 5: Đang upload video (150.75 MB)...
✅ Upload video thành công: vid_id_yyy
⏳ Bước 6: Đang chờ video xử lý...
✅ Video đã xử lý xong

✨ Upload thàng công!
📍 URL: https://www.ganjingworld.com/video/video_id_xxx
```

#### Error Handling
```
❌ Vui lòng nhập Access Token
❌ Vui lòng nhập Channel ID
❌ File video không tồn tại
⚠️  Không thể trích xuất thumbnail: [error details]
```

### Testing

Run the integration test:
```bash
python test_integration.py
```

Expected output:
```
Total: 4/4 tests passed
- Imports: PASS
- Uploader Class: PASS
- GUI Attributes: PASS
- Credentials Handling: PASS
```

### Configuration

#### Video Processing
- Thumbnail extracted from: 5-second mark
- Thumbnail resolution: 1280x720 (HD)
- Video upload timeout: 600 seconds (10 minutes)
- Status check interval: 5 seconds
- Max wait for processing: 600 seconds

#### UI Settings
- Access Token field: Password mode (hidden)
- Channel ID field: Normal text input
- Auto-focus on download completion: No (respects user interaction)

### Security Notes

1. **Access Tokens**: Never share your JWT token
   - Tokens shown as password field (masked)
   - Not saved to config by default
   - Re-enter per session for security

2. **Credentials**: Channel ID is public, Access Token is private
   - Keep Access Token secure
   - Don't share in screenshots/logs

3. **File Handling**: 
   - Auto-finds most recently downloaded video
   - Validates file before upload
   - Temporary thumbnail deleted after upload

### Future Enhancements

Potential features for future versions:
- Save credentials securely (encrypted config file)
- Batch upload multiple videos
- Custom title/description per upload
- Video category selection
- Thumbnail customization
- Upload schedule/cron support
- Analytics tracking

### Troubleshooting

#### "❌ Vui lòng nhập Access Token"
- Make sure checkbox is checked
- Copy full JWT token (should be 200+ characters)
- Verify token hasn't expired

#### "❌ Vui lòng nhập Channel ID"
- Make sure checkbox is checked
- Channel ID typically starts with "1frk"
- Verify no extra spaces

#### "❌ Lỗi lấy upload token: 401"
- Access token may be expired
- Try regenerating token from Ganjingworld
- Verify Channel ID matches token

#### "⚠️  Không thể trích xuất thumbnail"
- FFmpeg may not be in PATH
- Video file may be corrupted
- Try re-downloading video
- Check FFmpeg installation

#### Upload times out
- Large files need more time
- 600-second limit may be insufficient
- Check internet connection
- Try smaller video file

### File Structure
```
everything_downloader/
├── gui.py                      # Main GUI (updated)
├── ganjingworld_uploader.py    # NEW: Upload module
├── downloader_core.py          # Download logic (unchanged)
├── everything_downloader.py    # Entry point (unchanged)
├── test_integration.py         # NEW: Integration tests
└── ...
```

### Version Info
- Feature added: v0.3
- Module: ganjingworld_uploader.py
- Requires: Python 3.11+, PyQt6, requests, FFmpeg
