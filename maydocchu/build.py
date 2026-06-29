import PyInstaller.__main__
import os

def build_exe():
    # Tên file script chính
    main_script = "main.py"
    
    # Tên ứng dụng sau khi build
    app_name = "MayDocChu"
    
    # Các tham số cho PyInstaller
    params = [
        main_script,
        "--onefile",           # Đóng gói thành 1 file duy nhất
        "--windowed",          # Không hiện cửa sổ console khi chạy
        f"--name={app_name}",  # Tên file exe
        "--clean",             # Dọn dẹp cache trước khi build
        "--add-data=scripts.json;.", # Thêm scripts.json vào thư mục tạm của exe
        # Thêm các icon nếu có
        # "--icon=app_icon.ico" 
    ]
    
    print(f"Starting build {app_name}.exe...")
    PyInstaller.__main__.run(params)
    print("Build completed! Check 'dist' folder.")

if __name__ == "__main__":
    build_exe()
