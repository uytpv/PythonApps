from PIL import Image
import requests
from io import BytesIO

# Đường dẫn URL của ảnh
image_url = "https://scontent-hel3-1.xx.fbcdn.net/v/t39.30808-6/345654085_1245585829431026_2221827497398178742_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=730e14&_nc_ohc=7o2y4uhexE8AX8si5tL&_nc_ht=scontent-hel3-1.xx&oh=00_AfDCPWlZm9SsRJ27zpY9trwQPVIYidGVyODbZkan6x4yTQ&oe=646515A8"

# Tải ảnh từ URL
response = requests.get(image_url)
image = Image.open(BytesIO(response.content))

# Kiểm tra xem ảnh có chứa thông tin EXIF hay không
if hasattr(image, "exif"):
    # Lấy thông tin EXIF
    exif_data = image._getexif()
    
    if exif_data is not None:
        # In thông tin EXIF
        for tag, value in exif_data.items():
            tag_name = Image.TAGS.get(tag, tag)
            print(f"{tag_name}: {value}")
else:
    print("Ảnh không chứa thông tin EXIF.")
