# Hướng dẫn sử dụng:
# cú pháp run: python convert_mkv_to_mp4.py 'C:\\Users\\UY\\Downloads\\Three.Kingdoms.E25.2010.ViE.mHD.BluRay.DD5.1.x264-TRiM.mkv'

import os
import subprocess
import sys

def convert_mkv_to_mp4(input_file):
    # Trích xuất tên file (không bao gồm phần mở rộng)
    base_name = os.path.splitext(input_file)[0]
    output_file = base_name + '.mp4'  # Tạo tên file đầu ra với phần mở rộng là .mp4
    ffmpeg_cmd = [
        'ffmpeg',
        # Sử dụng phần cứng render (GPU) nếu có sẵn, nếu không tự động chuyển sang phần mềm render
        '-hwaccel', 'auto',
        '-hwaccel_device', 'auto',  # Chọn thiết bị phần cứng render tự động
        '-i', input_file,
        '-c:v', 'copy',
        '-c:a', 'copy',
        output_file
    ]
    subprocess.run(ffmpeg_cmd, capture_output=True, check=True)

# Lấy tham số từ câu lệnh
if len(sys.argv) != 2:
    print('Vui lòng cung cấp đúng một tham số: input_file')
else:
    input_file = sys.argv[1]
    convert_mkv_to_mp4(input_file)
