import requests

# Đường dẫn URL của ảnh trên Facebook
photo_url = "https://scontent-hel3-1.xx.fbcdn.net/v/t39.30808-6/345654085_1245585829431026_2221827497398178742_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=730e14&_nc_ohc=7o2y4uhexE8AX8si5tL&_nc_ht=scontent-hel3-1.xx&oh=00_AfDCPWlZm9SsRJ27zpY9trwQPVIYidGVyODbZkan6x4yTQ&oe=646515A8"

# Tách ID của ảnh từ URL
photo_id = photo_url.split("/")[-2]

# Gửi yêu cầu API để lấy thông tin của ảnh
api_url = f"https://graph.facebook.com/{photo_id}"
params = {"fields": "place", "access_token": "YOUR_ACCESS_TOKEN"}
response = requests.get(api_url, params=params)

# Kiểm tra và in thông tin vị trí
data = response.json()
print(data)
if "place" in data:
    location = data["place"]["location"]
    print("Vị trí: {}, {}".format(location["latitude"], location["longitude"]))
else:
    print("Không tìm thấy thông tin vị trí cho ảnh này.")
