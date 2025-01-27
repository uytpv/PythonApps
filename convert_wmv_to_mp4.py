import os
import subprocess
import sys

def convert_wmv_to_mp4(input_file):
    base_name = os.path.splitext(input_file)[0]
    output_file = base_name + '.mp4'
    subtitle_file = base_name + '.srt'  # Đường dẫn tệp phụ đề cùng tên với tệp video

    ffmpeg_cmd = [
        'ffmpeg',
        '-hwaccel', 'auto',
        '-hwaccel_device', 'auto',
        '-i', input_file,
        '-i', subtitle_file,  # Đường dẫn tệp phụ đề
        '-c:v', 'libx264',
        '-c:a', 'copy',
        '-c:s', 'mov_text',  # Chọn codec phụ đề MOV_TEXT
        '-scodec', 'mov_text',  # Chọn codec phụ đề MOV_TEXT
        '-metadata:s:s:0', 'language=vie',  # Thêm thông tin ngôn ngữ cho phụ đề
        output_file
    ]

    subprocess.run(ffmpeg_cmd, capture_output=True, check=True)

if len(sys.argv) != 2:
    print('Vui lòng cung cấp đúng một tham số: input_file')
else:
    input_file = sys.argv[1]
    convert_wmv_to_mp4(input_file)
