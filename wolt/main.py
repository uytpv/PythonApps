import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np

# Đọc file xlsx
data = pd.read_excel('data.xlsx')

# Tạo DataFrame
df = pd.DataFrame(data)

# Tạo các biến độc lập và phụ thuộc
X = df[['Pick', 'Drop', 'Total']]
y = df['Fee']

# Chia dữ liệu thành tập huấn luyện và kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Khởi tạo và huấn luyện mô hình hồi quy tuyến tính
model = LinearRegression()
model.fit(X_train, y_train)

# Dự đoán kết quả trên tập kiểm tra
predictions = model.predict(X_test)

# Tính toán sai số
error = np.sqrt(np.mean((predictions - y_test) ** 2))

# In ra sai số
print("Root Mean Squared Error:", error)

# Lưu mô hình nếu cần
# pd.to_pickle(model, 'model.pkl')


# Giả sử df là DataFrame của bạn
# Sắp xếp DataFrame theo cột 'Fee' theo thứ tự giảm dần
sorted_df = df.sort_values(by='Fee', ascending=False)

# Tìm giá trị nhỏ nhất của 'Drop', 'Pick', và 'Total'
min_drop = sorted_df['Drop'].min()
min_pick = sorted_df['Pick'].min()
min_total = sorted_df['Total'].min()

# Lọc để tìm các dòng có giá trị 'Drop', 'Pick', hoặc 'Total' là nhỏ nhất nhưng có 'Fee' cao nhất
optimal_rows = sorted_df[(sorted_df['Drop'] == min_drop) | (sorted_df['Pick'] == min_pick) | (sorted_df['Total'] == min_total)]

# In kết quả
print("Các dòng tối ưu nhất:")
print(optimal_rows)