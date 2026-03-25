# 🎬 Hướng Dẫn Cài Đặt Wan Animate (Wan2.2)

## Tổng Quan

Wan Animate là một framework tập trung vào **hoạt hình nhân vật** và **thay thế nhân vật** trong video. Nó cho phép bạn tạo video hoạt hình chất lượng cao bằng cách sao chép chính xác các biểu cảm khuôn mặt và chuyển động cơ thể từ video tham chiếu.

**Nguồn:** https://wanimate.net/#installation

---

## 📋 Yêu Cầu Hệ Thống

| Yêu Cầu    | Thông Tin               |
| ---------- | ----------------------- |
| **GPU**    | 8GB+ VRAM (khuyến nghị) |
| **Python** | 3.8 trở lên             |
| **CUDA**   | 11.8 hoặc tương thích   |
| **RAM**    | 16GB+ (khuyến nghị)     |

---

## 🚀 Các Bước Cài Đặt

### **Bước 1: Clone Repository**

Sao chép mã nguồn từ GitHub:

```bash
git clone https://github.com/Wan-Video/Wan2.2.git
cd Wan2.2
```

### **Bước 2: Cài Đặt Dependencies (Các Thư Viện Phụ Thuộc)**

#### 2.1 Cài Đặt Các Gói Cơ Bản

```bash
# Đảm bảo torch >= 2.4.0
pip install torch>=2.4.0

# Cài đặt các gói từ requirements.txt
pip install -r requirements.txt

# Nếu cài đặt flash_attn bị lỗi, hãy cài đặt các gói khác trước,
# sau đó cài đặt flash_attn cuối cùng
pip install flash_attn
```

#### 2.2 Cài Đặt Dependencies cho Speech-to-Video (Tùy Chọn)

Nếu bạn muốn sử dụng CosyVoice để tạo video từ giọng nói:

```bash
pip install -r requirements_s2v.txt
```

### **Bước 3: Tải Xuống Model Weights (Trọng Số Mô Hình)**

Các mô hình có sẵn:

| Mô Hình         | Loại                | Độ Phân Giải | Mô Tả                           |
| --------------- | ------------------- | ------------ | ------------------------------- |
| **T2V-A14B**    | Text-to-Video       | 480P & 720P  | Tạo video từ văn bản mô tả      |
| **I2V-A14B**    | Image-to-Video      | 480P & 720P  | Tạo video từ hình ảnh           |
| **TI2V-5B**     | Text+Image-to-Video | 720P         | Tạo video từ văn bản + hình ảnh |
| **S2V-14B**     | Speech-to-Video     | 480P & 720P  | Tạo video từ giọng nói          |
| **Animate-14B** | Character Animation | Variable     | Hoạt hình và thay thế nhân vật  |

#### 3.1 Tải Xuống Sử Dụng HuggingFace

```bash
# Cài đặt huggingface-cli
pip install "huggingface_hub[cli]"

# Tải xuống mô hình T2V (Text-to-Video)
huggingface-cli download Wan-AI/Wan2.2-T2V-A14B --local-dir ./Wan2.2-T2V-A14B

# Tải xuống mô hình I2V (Image-to-Video)
huggingface-cli download Wan-AI/Wan2.2-I2V-A14B --local-dir ./Wan2.2-I2V-A14B

# Tải xuống mô hình TI2V
huggingface-cli download Wan-AI/Wan2.2-TI2V-5B --local-dir ./Wan2.2-TI2V-5B

# Tải xuống mô hình S2V (Speech-to-Video)
huggingface-cli download Wan-AI/Wan2.2-S2V-14B --local-dir ./Wan2.2-S2V-14B

# Tải xuống mô hình Animate (Character Animation)
huggingface-cli download Wan-AI/Wan2.2-Animate-14B --local-dir ./Wan2.2-Animate-14B
```

#### 3.2 Tải Xuống Sử Dụng ModelScope (Dành cho Khu Vực Trung Quốc)

Nếu bạn ở Trung Quốc hoặc không thể truy cập HuggingFace, hãy sử dụng ModelScope:

```bash
# Cài đặt modelscope
pip install modelscope

# Tải xuống mô hình
modelscope download Wan-AI/Wan2.2-T2V-A14B --local_dir ./Wan2.2-T2V-A14B
```

### **Bước 4: Chạy Demo (Tùy Chọn)**

```bash
python demo.py --character_image path/to/character.jpg \
               --reference_video path/to/reference.mp4
```

---

## 💻 Các Lệnh Chạy Nhanh

### **1. Text-to-Video (T2V-A14B) - Tạo Video từ Văn Bản**

```bash
python generate.py \
    --task t2v-A14B \
    --size 1280*720 \
    --ckpt_dir ./Wan2.2-T2V-A14B \
    --offload_model True \
    --convert_model_dtype \
    --prompt "Hai chú mèo nhân hóa mặc quần áo đấm bốc sáng bóng, chúng đánh nhau dữ dội trên sân khấu được chiếu sáng."
```

### **2. Image-to-Video (I2V-A14B) - Tạo Video từ Hình Ảnh**

```bash
python generate.py \
    --task i2v-A14B \
    --size 1280*720 \
    --ckpt_dir ./Wan2.2-I2V-A14B \
    --offload_model True \
    --convert_model_dtype \
    --image examples/i2v_input.JPG \
    --prompt "Phong cách kỳ nghỉ hè ở bãi biển, một chú mèo trắng mặc kính mát ngồi trên ván lướt."
```

### **3. Text+Image-to-Video (TI2V-5B) - Kết Hợp Văn Bản và Hình Ảnh**

```bash
python generate.py \
    --task ti2v-5B \
    --size 1280*704 \
    --ckpt_dir ./Wan2.2-TI2V-5B \
    --offload_model True \
    --convert_model_dtype \
    --t5_cpu \
    --prompt "Hai chú mèo nhân hóa mặc quần áo đấm bốc sáng bóng, chúng đánh nhau dữ dội trên sân khấu được chiếu sáng."
```

### **4. Speech-to-Video (S2V-14B) - Tạo Video từ Giọng Nói**

```bash
python generate.py \
    --task s2v-14B \
    --size 1024*704 \
    --ckpt_dir ./Wan2.2-S2V-14B/ \
    --offload_model True \
    --convert_model_dtype \
    --prompt "Phong cách kỳ nghỉ hè ở bãi biển, một chú mèo trắng mặc kính mát ngồi trên ván lướt." \
    --audio examples/talk.wav
```

### **5. Character Animation - Hoạt Hình Nhân Vật**

#### 5.1 Bước Tiền Xử Lý (Preprocessing) - Chế Độ Hoạt Hình

```bash
python ./wan/modules/animate/preprocess/preprocess_data.py \
    --ckpt_path ./Wan2.2-Animate-14B/process_checkpoint \
    --video_path ./examples/wan_animate/animate/video.mp4 \
    --refer_path ./examples/wan_animate/animate/image.jpeg \
    --save_path ./examples/wan_animate/animate/process_results \
    --resolution_area 1280 720 \
    --retarget_flag \
    --use_flux
```

#### 5.2 Chạy Hoạt Hình

```bash
python generate.py \
    --task animate-14B \
    --ckpt_dir ./Wan2.2-Animate-14B/ \
    --src_root_path ./examples/wan_animate/animate/process_results/ \
    --refert_num 1
```

### **6. Character Replacement - Thay Thế Nhân Vật**

#### 6.1 Bước Tiền Xử Lý (Preprocessing) - Chế Độ Thay Thế

```bash
python ./wan/modules/animate/preprocess/preprocess_data.py \
    --ckpt_path ./Wan2.2-Animate-14B/process_checkpoint \
    --video_path ./examples/wan_animate/replace/video.mp4 \
    --refer_path ./examples/wan_animate/replace/image.jpeg \
    --save_path ./examples/wan_animate/replace/process_results \
    --resolution_area 1280 720 \
    --iterations 3 \
    --k 7 \
    --w_len 1 \
    --h_len 1 \
    --replace_flag
```

#### 6.2 Chạy Thay Thế

```bash
python generate.py \
    --task animate-14B \
    --ckpt_dir ./Wan2.2-Animate-14B/ \
    --src_root_path ./examples/wan_animate/replace/process_results/ \
    --refert_num 1 \
    --replace_flag \
    --use_relighting_lora
```

---

## 🎯 Các Trường Hợp Sử Dụng (Use Cases)

### 🎬 **Phim và Giải Trí**

Tạo hoạt hình nhân vật chân thực cho phim, chương trình TV, và nội dung kỹ thuật số.

### 🎮 **Ngành Trò Chơi**

Tạo hoạt hình nhân vật động cho trò chơi video, từ cinematic đến các tương tác trong trò chơi.

### 📚 **Nội Dung Giáo Dục**

Tạo video giáo dục với các nhân vật hoạt hình có thể giải thích các khái niệm phức tạp.

### 🎨 **Nghệ Thuật và Hoạt Hình Kỹ Thuật Số**

Các nghệ sĩ có thể nhanh chóng tạo bản mẫu hoạt hình nhân vật.

### 💼 **Đào Tạo Doanh Nghiệp**

Phát triển tài liệu đào tạo với các nhân vật hoạt hình.

### 🔬 **Nghiên Cứu và Phát Triển**

Nghiên cứu các mẫu chuyển động con người, biểu cảm khuôn mặt, và mô hình hành vi.

---

## ❓ Câu Hỏi Thường Gặp (FAQ)

### **Q1: Wan Animate là gì?**

**Trả lời:** Wan Animate là một framework thống nhất cho hoạt hình nhân vật và thay thế nhân vật. Nó có thể hoạt hình bất kỳ nhân vật nào dựa trên video của người diễn viên, sao chép chính xác các biểu cảm khuôn mặt và chuyển động của người diễn viên.

### **Q2: Thay thế nhân vật hoạt động như thế nào?**

**Trả lời:** Wan Animate có thể thay thế các nhân vật trong video bằng các nhân vật hoạt hình, bảo tồn biểu cảm và chuyển động của họ đồng thời sao chép cách chiếu sáng và tông màu môi trường gốc để tích hợp liền mạch.

### **Q3: Yêu cầu hệ thống là gì?**

**Trả lời:** Wan Animate yêu cầu GPU hiện đại có đủ VRAM để xử lý video. GPU có ít nhất 8GB VRAM được khuyến nghị để hoạt động tối ưu.

### **Q4: Có phải là mã nguồn mở không?**

**Trả lời:** Có, mô hình và mã nguồn là mã nguồn mở trên GitHub: https://github.com/Wan-Video/Wan2.2.git

### **Q5: Có thể sử dụng cho mục đích thương mại không?**

**Trả lời:** Vui lòng kiểm tra thỏa thuận giấy phép. Các mô hình thường được cấp phép theo Apache 2.0.

---

## 🛠️ Sử Dụng Script Tự Động

Nếu bạn muốn tự động hóa quy trình cài đặt, hãy sử dụng script `wan_animate_setup.py`:

### **Cài Đặt Đầy Đủ (Mặc Định)**

```bash
python wan_animate_setup.py
```

### **Chỉ Clone Repository**

```bash
python wan_animate_setup.py --clone-only
```

### **Tải Xuống Mô Hình Cụ Thể**

```bash
python wan_animate_setup.py --models t2v i2v animate
```

### **Sử Dụng ModelScope (Trung Quốc)**

```bash
python wan_animate_setup.py --models t2v --use-modelscope
```

### **Liệt Kê Tất Cả Mô Hình Có Sẵn**

```bash
python wan_animate_setup.py --list-models
```

### **Cài Đặt Dependencies cho Speech-to-Video**

```bash
python wan_animate_setup.py --install-s2v
```

---

## ⚠️ Ghi Chú Quan Trọng

1. **Flash_attn là tùy chọn** - Nếu cài đặt thất bại, bạn vẫn có thể sử dụng Wan2.2 (sẽ chậm hơn)
2. **Tải xuống mô hình mất thời gian** - Model lớn có thể mất vài giờ để tải
3. **Yêu cầu GPU mạnh** - Để có kết quả tốt, bạn cần GPU có VRAM đủ
4. **CUDA tương thích** - Đảm bảo CUDA 11.8 hoặc tương thích với PyTorch

---

## 📞 Hỗ Trợ

- **Tài Liệu:** https://wanimate.net/
- **GitHub:** https://github.com/Wan-Video/Wan2.2
- **Liên Hệ:** https://wanimate.net/contact

---

## 📝 Ghi Chú Bản Quyền

© 2025 Wan Animate. Được xây dựng với kiến trúc mô hình Wan cho hoạt hình và thay thế nhân vật.
