import os
import ctypes

# Đường dẫn đến thư mục cần quét
folder_path = r'C:\TaiVe'

# Đường dẫn file kết quả
output_file = os.path.join(folder_path, 'filelist.txt')

# Hàm kiểm tra xem file có bị ẩn không (Windows only)
def is_hidden(filepath):
    try:
        attrs = ctypes.windll.kernel32.GetFileAttributesW(str(filepath))
        return attrs != -1 and (attrs & 2)  # FILE_ATTRIBUTE_HIDDEN = 2
    except Exception as e:
        print(f"Lỗi khi kiểm tra thuộc tính ẩn: {e}")
        return False

# Lấy danh sách file trong thư mục
file_names = []
for filename in os.listdir(folder_path):
    full_path = os.path.join(folder_path, filename)
    if os.path.isfile(full_path):
        if is_hidden(full_path):
            file_names.append(f"_{filename}")
        else:
            file_names.append(filename)

# Ghi danh sách file vào filelist.txt
with open(output_file, 'w', encoding='utf-8') as f:
    for name in file_names:
        f.write(name + '\n')

print(f"Đã tạo danh sách file tại: {output_file}")
