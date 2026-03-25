# 🎬 Hướng Dẫn Chi Tiết: Tạo Video từ Hình Ảnh (Image-to-Video)

## 📋 Tổng Quan

Bài hướng dẫn này sẽ giúp bạn **tạo video động từ một hình ảnh tĩnh** (chẳng hạn như `character.png`) bằng mô hình **I2V-A14B (Image-to-Video)** của Wan2.2.

---

## 🎯 Bước 1: Chuẩn Bị Hình Ảnh

### 1.1 Yêu Cầu về Hình Ảnh
- **Định dạng:** JPG, PNG, JPEG (khuyến nghị JPG để tối ưu)
- **Độ phân giải:** 720x720 đến 1280x1280 pixel
- **Kích thước tệp:** < 10MB
- **Nội dung:** Nhân vật rõ ràng, có độ tương phản tốt

### 1.2 Tổ Chức Thư Mục
```
Wan2.2/
├── character.png          ← Hình ảnh của bạn (đặt ở đây)
├── examples/
│   └── i2v_input.JPG      ← Hoặc đặt ở đây
├── generate.py
├── requirements.txt
└── Wan2.2-I2V-A14B/       ← Thư mục model
    ├── config.json
    ├── model.safetensors
    └── ...
```

### 1.3 Chuyển Đổi Hình Ảnh (Nếu Cần)
Nếu hình ảnh có nền xanh hoặc cần xử lý, bạn có thể sử dụng Python:

```python
from PIL import Image

# Mở hình ảnh
img = Image.open('character.png')

# Chuyển đổi sang RGB nếu là RGBA
if img.mode == 'RGBA':
    # Tạo nền trắng
    background = Image.new('RGB', img.size, 'white')
    background.paste(img, mask=img.split()[3])  # 3 là alpha channel
    background.save('character.jpg', 'JPEG', quality=95)
else:
    img.save('character.jpg', 'JPEG', quality=95)

print("✓ Đã chuyển đổi thành công!")
```

---

## 🔧 Bước 2: Kiểm Tra Môi Trường

### 2.1 Kiểm Tra Python Version
```bash
python --version
# Kết quả mong muốn: Python 3.8 hoặc cao hơn
```

### 2.2 Kiểm Tra PyTorch và CUDA
```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}')"
```

**Kết quả mong muốn:**
```
PyTorch: 2.4.0 hoặc cao hơn
CUDA Available: True
GPU: [Tên GPU của bạn]
```

### 2.3 Kiểm Tra Mô Hình
```bash
# Đảm bảo thư mục Wan2.2-I2V-A14B tồn tại
ls -la Wan2.2-I2V-A14B/
# Hoặc trên Windows:
dir Wan2.2-I2V-A14B\
```

---

## 🎬 Bước 3: Tạo Video từ Hình Ảnh (Image-to-Video)

### 3.1 Lệnh Cơ Bản (480P - Nhanh hơn)

Nếu bạn muốn tạo video **nhanh** với độ phân giải thấp hơn:

```bash
python generate.py \
    --task i2v-A14B \
    --size 640*480 \
    --ckpt_dir ./Wan2.2-I2V-A14B \
    --offload_model True \
    --convert_model_dtype \
    --image character.png \
    --prompt "A character standing in a bright studio, looking at the camera with a subtle smile"
```

### 3.2 Lệnh Chất Lượng Cao (720P - Khuyến Nghị)

Để tạo video **chất lượng cao** với độ phân giải 720P:

```bash
python generate.py \
    --task i2v-A14B \
    --size 1280*720 \
    --ckpt_dir ./Wan2.2-I2V-A14B \
    --offload_model True \
    --convert_model_dtype \
    --image character.png \
    --prompt "A character standing in a bright studio, looking at the camera with a subtle smile"
```

### 3.3 Lệnh Tối Ưu Nhất (720P, CPU T5)

Sử dụng CPU để xử lý T5 (tiết kiệm VRAM GPU):

```bash
python generate.py \
    --task i2v-A14B \
    --size 1280*720 \
    --ckpt_dir ./Wan2.2-I2V-A14B \
    --offload_model True \
    --convert_model_dtype \
    --t5_cpu \
    --image character.png \
    --prompt "A character standing in a bright studio, looking at the camera with a subtle smile"
```

---

## 🔤 Bước 4: Viết Prompt (Mô Tả) Tốt

Prompt (mô tả) rất quan trọng để quyết định chuyển động và bối cảnh của video.

### 4.1 Các Ví Dụ Prompt Tốt

**Ví Dụ 1: Chuyển động cơ bản**
```
A character slowly turning their head and smiling at the camera
```
(Tạm dịch: Một nhân vật từ từ quay đầu và cười nhìn vào camera)

**Ví Dụ 2: Chuyển động năng động**
```
A character dancing with energetic movements in a brightly lit room
```
(Tạm dịch: Một nhân vật nhảy múa với những chuyển động năng lượng trong một phòng sáng)

**Ví Dụ 3: Chuyển động nói chuyện**
```
A character talking to the camera, gesturing with hands while speaking
```
(Tạm dịch: Một nhân vật nói chuyện với camera, vẫy tay khi nói)

**Ví Dụ 4: Chuyển động tình cảm**
```
A character with gentle expressions, looking thoughtfully out the window with a peaceful expression
```
(Tạm dịch: Một nhân vật với những biểu cảm nhẹ nhàng, nhìn ra cửa sổ một cách suy tư với biểu cảm yên bình)

**Ví Dụ 5: Chuyển động phức tạp**
```
A character walking around the room, occasionally looking at the camera, with natural and smooth movements
```
(Tạm dịch: Một nhân vật đi bộ quanh phòng, thỉnh thoảng nhìn vào camera, với những chuyển động tự nhiên và mượt mà)

### 4.2 Mẹo Viết Prompt Hiệu Quả

✅ **NÊN:**
- Mô tả chuyển động rõ ràng (walking, dancing, talking, smiling)
- Thêm bối cảnh (in a room, on a stage, outdoors)
- Thêm cảm xúc (happy, sad, thoughtful, excited)
- Sử dụng tính từ (slowly, smoothly, energetically)

❌ **KHÔNG NÊN:**
- Quá ngắn hoặc quá chung chung ("character video")
- Yêu cầu thay đổi ngoại hình quá lớn
- Mô tả quá chi tiết kỹ thuật (làm AI bối rối)
- Nhập các ký tự không phải tiếng Anh

---

## ⚙️ Bước 5: Tham Số Quan Trọng Giải Thích

| Tham Số | Ý Nghĩa | Ví Dụ |
|---------|---------|-------|
| `--task` | Loại mô hình sử dụng | `i2v-A14B` (Image-to-Video) |
| `--size` | Độ phân giải (chiều rộng * chiều cao) | `1280*720` (HD), `640*480` (nhỏ) |
| `--ckpt_dir` | Thư mục chứa model | `./Wan2.2-I2V-A14B` |
| `--image` | Đường dẫn hình ảnh đầu vào | `character.png` hoặc `./path/to/image.jpg` |
| `--prompt` | Mô tả mong muốn video | `"A character dancing"` |
| `--offload_model` | Tải/gỡ mô hình linh hoạt (tiết kiệm VRAM) | `True` hoặc `False` |
| `--convert_model_dtype` | Chuyển đổi kiểu dữ liệu (tiết kiệm bộ nhớ) | Không cần giá trị |
| `--t5_cpu` | Sử dụng CPU cho T5 encoder | Không cần giá trị |
| `--seed` | Seed ngẫu nhiên (tái tạo kết quả) | `42`, `123` |

### Kết Hợp Tham Số Tối Ưu

**Cho GPU 8GB:**
```bash
python generate.py \
    --task i2v-A14B \
    --size 640*480 \
    --ckpt_dir ./Wan2.2-I2V-A14B \
    --offload_model True \
    --convert_model_dtype \
    --t5_cpu \
    --image character.png \
    --prompt "Your prompt here"
```

**Cho GPU 16GB:**
```bash
python generate.py \
    --task i2v-A14B \
    --size 1280*720 \
    --ckpt_dir ./Wan2.2-I2V-A14B \
    --offload_model True \
    --convert_model_dtype \
    --image character.png \
    --prompt "Your prompt here"
```

**Cho GPU 24GB+:**
```bash
python generate.py \
    --task i2v-A14B \
    --size 1280*720 \
    --ckpt_dir ./Wan2.2-I2V-A14B \
    --image character.png \
    --prompt "Your prompt here"
```

---

## 🎥 Bước 6: Chạy Lệnh và Giám Sát Tiến Độ

### 6.1 Chạy Lệnh (Ví Dụ Đầy Đủ)

```bash
python generate.py \
    --task i2v-A14B \
    --size 1280*720 \
    --ckpt_dir ./Wan2.2-I2V-A14B \
    --offload_model True \
    --convert_model_dtype \
    --image character.png \
    --prompt "A character standing in a bright studio, smiling gently at the camera"
```

### 6.2 Giám Sát Quá Trình

Bạn sẽ thấy các thông báo như:
```
Loading model...
Processing image...
Generating video...
[████████░░░░░░░░░░] 50% - Estimated time: 2 minutes
Video saved to: output/video_0.mp4
```

**Thời gian xử lý dự kiến:**
- 480P: 3-5 phút (GPU 8GB)
- 720P: 5-10 phút (GPU 8GB)
- 720P: 3-5 phút (GPU 16GB+)

---

## 📁 Bước 7: Tìm Kiếm Video Đầu Ra

### 7.1 Vị Trí Lưu File

Video sẽ được lưu trong thư mục output (tên thường như):
```
output/
├── video_0.mp4
├── video_1.mp4
├── ...
└── latest.mp4
```

### 7.2 Kiểm Tra Video

**Trên Windows:**
```bash
# Mở thư mục output
start output
# Hoặc xem file mới nhất
dir output /O-D
```

**Trên macOS/Linux:**
```bash
# Liệt kê các file
ls -lah output/

# Phát video
ffplay output/video_0.mp4
```

---

## 🐛 Bước 8: Khắc Phục Sự Cố

### Lỗi 1: "CUDA out of memory"

**Nguyên nhân:** GPU không đủ bộ nhớ  
**Giải pháp:**
```bash
# Giảm độ phân giải
--size 640*480

# Hoặc sử dụng offload_model
--offload_model True --t5_cpu
```

### Lỗi 2: "Model not found"

**Nguyên nhân:** Thư mục mô hình không tồn tại  
**Giải pháp:**
```bash
# Kiểm tra thư mục
ls Wan2.2-I2V-A14B/

# Tải xuống mô hình nếu chưa có
huggingface-cli download Wan-AI/Wan2.2-I2V-A14B --local-dir ./Wan2.2-I2V-A14B
```

### Lỗi 3: "Image not found"

**Nguyên nhân:** Đường dẫn hình ảnh sai  
**Giải pháp:**
```bash
# Sử dụng đường dẫn tuyệt đối
--image /full/path/to/character.png

# Hoặc kiểm tra file tồn tại
ls -la character.png
```

### Lỗi 4: "OutOfMemoryError"

**Nguyên nhân:** RAM hệ thống không đủ  
**Giải pháp:**
```bash
# Đóng các ứng dụng khác
# Hoặc thêm swap space (Linux)
```

### Lỗi 5: Video chất lượng thấp

**Nguyên nhân:** Hình ảnh đầu vào không tốt hoặc prompt không rõ  
**Giải pháp:**
- Sử dụng hình ảnh độ phân giải cao (720p+)
- Viết prompt chi tiết hơn
- Điều chỉnh seed: `--seed 42`

---

## 📝 Bước 9: Ví Dụ Hoàn Chỉnh

### Ví Dụ: Tạo Video Nhân Vật Nhảy Múa

```bash
# 1. Chuẩn bị
# - Đặt character.png vào thư mục Wan2.2
# - Tải model I2V-A14B (nếu chưa có)

# 2. Chạy lệnh tạo video
python generate.py \
    --task i2v-A14B \
    --size 1280*720 \
    --ckpt_dir ./Wan2.2-I2V-A14B \
    --offload_model True \
    --convert_model_dtype \
    --image character.png \
    --prompt "A character dancing with energetic movements, showing happiness and joy, with smooth transitions"

# 3. Chờ xử lý (5-10 phút)

# 4. Tìm video trong thư mục output
# output/video_0.mp4
```

---

## 💡 Lưu Ý Quan Trọng

1. **Thời gian chạy:** Lần đầu tiên sẽ lâu hơn do phải load model
2. **Kết quả ngẫu nhiên:** Mỗi lần chạy có thể khác, sử dụng `--seed` để cố định
3. **VRAM:** Nếu thiếu VRAM, hãy sử dụng `--offload_model True`
4. **Prompt tiếng Anh:** Mô tả bằng tiếng Anh sẽ cho kết quả tốt hơn
5. **Hình ảnh chất lượng:** Hình ảnh rõ ràng, sáng sẽ tạo video tốt hơn

---

## 🎓 Tiếp Theo

Sau khi tạo video thành công, bạn có thể:

1. **Chỉnh sửa video:** Sử dụng các công cụ như FFmpeg, Adobe Premiere, v.v.
2. **Thêm âm thanh:** 
   ```bash
   ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac output.mp4
   ```
3. **Chuyển đổi định dạng:**
   ```bash
   ffmpeg -i video.mp4 -c:v h264 -crf 23 output.mp4
   ```
4. **Thử các mô hình khác:** T2V-A14B (từ văn bản), S2V-14B (từ giọng nói), v.v.

---

## 📞 Liên Hệ & Hỗ Trợ

- **GitHub:** https://github.com/Wan-Video/Wan2.2
- **Website:** https://wanimate.net/
- **Documentation:** https://wanimate.net/installation

---

**Chúc bạn tạo video thành công! 🎉**

